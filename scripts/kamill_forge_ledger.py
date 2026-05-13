#!/usr/bin/env python3
"""Manual Kamill Forge Phase 1-C candidate ledger dry-run tool.

Reads an explicit candidate JSON file and either prints normalized inert ledger
records to stdout or appends them to an explicitly requested dry-run JSONL
ledger. This script never scans, never calls networks/LLMs, and never applies
memory, skill, Core, or project mutations.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DRY_RUN_ROOT = REPO_ROOT / "logs" / "kamill-forge" / "dry-runs"
RULE_ID = "repeated_observation_count"
REQUIRED_CANDIDATE_FIELDS = {
    "lane",
    "anchor_status",
    "source_type",
    "source_ref",
}


class LedgerInputError(ValueError):
    """Raised when an input cannot be safely normalized."""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize Kamill Forge candidates for a manual dry-run ledger."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Explicit JSON file containing a Phase 1-B candidate or payload.",
    )
    parser.add_argument(
        "--ledger-out",
        help=(
            "Optional append-only JSONL output path. Must be under "
            "logs/kamill-forge/dry-runs/ unless using a system temp path for tests."
        ),
    )
    return parser.parse_args(argv)


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except OSError as exc:
        raise LedgerInputError(f"could not read input: {path}") from exc
    except json.JSONDecodeError as exc:
        raise LedgerInputError("invalid input JSON") from exc
    if not isinstance(data, dict):
        raise LedgerInputError("input root must be an object")
    return data


def _candidate_from_ledger_entry(data: dict[str, Any]) -> dict[str, Any] | None:
    candidate = data.get("candidate")
    if isinstance(candidate, dict):
        return candidate
    return None


def extract_candidates(data: dict[str, Any]) -> tuple[str | None, list[dict[str, Any]]]:
    ledger_candidate = _candidate_from_ledger_entry(data)
    if ledger_candidate is not None:
        return data.get("run_id"), [ledger_candidate]

    candidates = data.get("candidates")
    if isinstance(candidates, list):
        normalized = []
        for index, candidate in enumerate(candidates):
            if not isinstance(candidate, dict):
                raise LedgerInputError(f"invalid candidate {index}: must be an object")
            normalized.append(candidate)
        return data.get("run_id"), normalized

    if any(field in data for field in REQUIRED_CANDIDATE_FIELDS):
        return data.get("run_id"), [data]

    raise LedgerInputError("input must contain a candidate object or candidates list")


def stable_candidate_id(candidate: dict[str, Any]) -> str:
    existing_id = candidate.get("id")
    if isinstance(existing_id, str) and existing_id:
        return existing_id
    material = {
        "anchor_status": candidate.get("anchor_status"),
        "lane": candidate.get("lane"),
        "rule_id": candidate.get("rule_id", RULE_ID),
        "source_ref": candidate.get("source_ref"),
        "source_type": candidate.get("source_type"),
        "suggested_target": candidate.get(
            "suggested_target", candidate.get("proposed_mutation_class")
        ),
    }
    digest = hashlib.sha256(
        json.dumps(material, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:16]
    return f"kf-{digest}"


def normalize_candidate(candidate: dict[str, Any], run_id: str | None, index: int) -> dict[str, Any]:
    missing = sorted(field for field in REQUIRED_CANDIDATE_FIELDS if not candidate.get(field))
    if missing:
        raise LedgerInputError(
            f"invalid candidate {index}: missing required fields: {', '.join(missing)}"
        )
    if candidate["anchor_status"] not in {"anchored", "global-unanchored"}:
        raise LedgerInputError(f"invalid candidate {index}: unsupported anchor_status")

    repo_path = candidate.get("repo_path")
    if candidate["anchor_status"] == "global-unanchored":
        repo_path = None
    elif not isinstance(repo_path, str) or not repo_path:
        raise LedgerInputError(f"invalid candidate {index}: anchored candidates require repo_path")

    return {
        "id": stable_candidate_id(candidate),
        "run_id": candidate.get("run_id", run_id),
        "lane": candidate["lane"],
        "anchor_status": candidate["anchor_status"],
        "repo_path": repo_path,
        "source_type": candidate["source_type"],
        "source_ref": candidate["source_ref"],
        "rule_id": candidate.get("rule_id", RULE_ID),
        "evidence_summary": candidate.get(
            "evidence_summary", candidate.get("summary", "")
        ),
        "proposed_mutation_class": candidate.get(
            "proposed_mutation_class", candidate.get("suggested_target", "")
        ),
        "risk_class": candidate.get("risk_class", "human_gate_required"),
        "requires_user_approval": True,
        "auto_apply": False,
    }


def ledger_entry(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_schema": "kamill-forge.phase-1c.candidate-ledger.v1",
        "appended_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source": "manual-dry-run",
        "candidate": candidate,
        "draft_status": "none",
    }


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def assert_allowed_output_path(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    dry_root = DRY_RUN_ROOT.resolve()
    temp_root = Path(tempfile.gettempdir()).resolve()
    if _is_relative_to(resolved, dry_root) or _is_relative_to(resolved, temp_root):
        return resolved
    raise LedgerInputError(
        "ledger output must be under logs/kamill-forge/dry-runs/ "
        "or a system temp path used by tests"
    )


def append_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    allowed = assert_allowed_output_path(path)
    allowed.parent.mkdir(parents=True, exist_ok=True)
    with allowed.open("a", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        run_id, candidates = extract_candidates(load_json(Path(args.input)))
        records = [
            ledger_entry(normalize_candidate(candidate, run_id, index))
            for index, candidate in enumerate(candidates)
        ]
        if args.ledger_out:
            append_jsonl(Path(args.ledger_out), records)
        print(json.dumps({"status": "dry_run", "records": records}, sort_keys=True))
    except LedgerInputError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
