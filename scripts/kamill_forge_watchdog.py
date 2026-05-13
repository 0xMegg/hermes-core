#!/usr/bin/env python3
"""Manual Kamill Forge candidate classifier.

Phase 1-B scope: read one explicit JSON input file, emit inert candidate JSON
for above-threshold observations, and stay silent on quiet days.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

RULE_ID = "repeated_observation_count"
REQUIRED_FIELDS = {
    "source_type",
    "source_ref",
    "anchor_status",
    "lane",
    "observation_count",
    "summary",
    "suggested_target",
    "risk_class",
}


class WatchdogInputError(ValueError):
    """Raised when the input file cannot be classified safely."""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classify explicit Kamill Forge fixture/input candidates."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the explicit JSON input file to classify.",
    )
    parser.add_argument(
        "--min-observations",
        type=int,
        default=3,
        help="Runtime test threshold for repeated-observation candidates.",
    )
    return parser.parse_args(argv)


def load_input(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except OSError as exc:
        raise WatchdogInputError(f"could not read input: {path}") from exc
    except json.JSONDecodeError as exc:
        raise WatchdogInputError("invalid input JSON") from exc

    if not isinstance(data, dict):
        raise WatchdogInputError("input root must be an object")
    if not isinstance(data.get("run_id"), str) or not data["run_id"]:
        raise WatchdogInputError("input run_id must be a non-empty string")
    candidates = data.get("candidates")
    if not isinstance(candidates, list):
        raise WatchdogInputError("input candidates must be a list")
    return data


def validate_candidate(candidate: Any, index: int) -> dict[str, Any]:
    if not isinstance(candidate, dict):
        raise WatchdogInputError(f"invalid candidate {index}: must be an object")

    missing = sorted(field for field in REQUIRED_FIELDS if field not in candidate)
    if missing:
        raise WatchdogInputError(
            f"invalid candidate {index}: missing required fields: {', '.join(missing)}"
        )

    if candidate["lane"] != "experience-distillation":
        raise WatchdogInputError(
            f"invalid candidate {index}: unsupported lane {candidate['lane']!r}"
        )
    if candidate["anchor_status"] not in {"anchored", "global-unanchored"}:
        raise WatchdogInputError(
            f"invalid candidate {index}: unsupported anchor_status"
        )
    if not isinstance(candidate["observation_count"], int):
        raise WatchdogInputError(
            f"invalid candidate {index}: observation_count must be an integer"
        )
    for field in REQUIRED_FIELDS - {"observation_count"}:
        if not isinstance(candidate[field], str) or not candidate[field]:
            raise WatchdogInputError(
                f"invalid candidate {index}: {field} must be a non-empty string"
            )
    repo_path = candidate.get("repo_path")
    if candidate["anchor_status"] == "anchored" and (
        not isinstance(repo_path, str) or not repo_path
    ):
        raise WatchdogInputError(
            f"invalid candidate {index}: anchored candidates require repo_path"
        )
    return candidate


def candidate_id(candidate: dict[str, Any]) -> str:
    material = {
        "anchor_status": candidate["anchor_status"],
        "lane": candidate["lane"],
        "rule_id": RULE_ID,
        "source_ref": candidate["source_ref"],
        "source_type": candidate["source_type"],
        "suggested_target": candidate["suggested_target"],
    }
    digest = hashlib.sha256(
        json.dumps(material, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:16]
    return f"kf-{digest}"


def emit_candidate(run_id: str, candidate: dict[str, Any]) -> dict[str, Any]:
    repo_path = candidate.get("repo_path")
    if candidate["anchor_status"] == "global-unanchored":
        repo_path = None

    return {
        "id": candidate_id(candidate),
        "run_id": run_id,
        "lane": candidate["lane"],
        "anchor_status": candidate["anchor_status"],
        "repo_path": repo_path,
        "source_type": candidate["source_type"],
        "source_ref": candidate["source_ref"],
        "rule_id": RULE_ID,
        "evidence_summary": candidate["summary"],
        "proposed_mutation_class": candidate["suggested_target"],
        "requires_user_approval": True,
        "auto_apply": False,
    }


def classify(data: dict[str, Any], min_observations: int) -> dict[str, Any] | None:
    run_id = data["run_id"]
    emitted = []
    for index, raw_candidate in enumerate(data["candidates"]):
        candidate = validate_candidate(raw_candidate, index)
        if candidate["observation_count"] >= min_observations:
            emitted.append(emit_candidate(run_id, candidate))

    if not emitted:
        return None
    return {
        "status": "candidate_detected",
        "run_id": run_id,
        "candidates": emitted,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        data = load_input(Path(args.input))
        result = classify(data, args.min_observations)
    except WatchdogInputError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if result is None:
        return 0
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
