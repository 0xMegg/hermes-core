#!/usr/bin/env python3
"""Manual Kamill Forge Phase 1-C staged proposal draft generator.

Renders a dry-run staged proposal draft from an explicit candidate JSON file.
By default the draft is printed to stdout. File output requires --out and is
restricted to the dry-run staged-proposals directory or a system temp path used
by tests.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DRY_RUN_PROPOSAL_ROOT = REPO_ROOT / "logs" / "kamill-forge" / "dry-runs" / "staged-proposals"
REQUIRED_CANDIDATE_FIELDS = {
    "lane",
    "anchor_status",
    "source_type",
    "source_ref",
}
RULE_ID = "repeated_observation_count"


class DraftInputError(ValueError):
    """Raised when a proposal draft cannot be generated safely."""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a manual dry-run Kamill Forge staged proposal draft."
    )
    parser.add_argument("--input", required=True, help="Explicit candidate JSON input file.")
    parser.add_argument(
        "--out",
        help=(
            "Optional markdown output path. Must be under "
            "logs/kamill-forge/dry-runs/staged-proposals/ unless using a "
            "system temp path for tests."
        ),
    )
    return parser.parse_args(argv)


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except OSError as exc:
        raise DraftInputError(f"could not read input: {path}") from exc
    except json.JSONDecodeError as exc:
        raise DraftInputError("invalid input JSON") from exc
    if not isinstance(data, dict):
        raise DraftInputError("input root must be an object")
    return data


def extract_candidate(data: dict[str, Any]) -> tuple[str | None, dict[str, Any]]:
    if isinstance(data.get("candidate"), dict):
        return data.get("run_id"), data["candidate"]
    candidates = data.get("candidates")
    if isinstance(candidates, list):
        if len(candidates) != 1:
            raise DraftInputError("proposal draft input must contain exactly one candidate")
        if not isinstance(candidates[0], dict):
            raise DraftInputError("candidate must be an object")
        return data.get("run_id"), candidates[0]
    if any(field in data for field in REQUIRED_CANDIDATE_FIELDS):
        return data.get("run_id"), data
    raise DraftInputError("input must contain one candidate object")


def normalize_candidate(candidate: dict[str, Any], run_id: str | None) -> dict[str, Any]:
    missing = sorted(field for field in REQUIRED_CANDIDATE_FIELDS if not candidate.get(field))
    if missing:
        raise DraftInputError(f"invalid candidate: missing required fields: {', '.join(missing)}")
    if candidate["anchor_status"] not in {"anchored", "global-unanchored"}:
        raise DraftInputError("invalid candidate: unsupported anchor_status")
    repo_path = candidate.get("repo_path")
    if candidate["anchor_status"] == "global-unanchored":
        repo_path = None
    elif not isinstance(repo_path, str) or not repo_path:
        raise DraftInputError("invalid candidate: anchored candidates require repo_path")

    return {
        "id": candidate.get("id", "pending-ledger-id"),
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


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug[:60] or "kamill-forge-candidate"


def render_draft(candidate: dict[str, Any]) -> str:
    date = datetime.now(timezone.utc).date().isoformat()
    title = slugify(candidate.get("evidence_summary") or candidate["source_ref"])
    repo_path = candidate["repo_path"] if candidate["repo_path"] is not None else "null"
    acceptance_answer = (
        "Conditionally yes: this draft reduces repeated judgment only if it remains "
        "a dry-run staged proposal and no memory, skill, Core, or project mutation "
        "occurs before explicit user approval."
    )
    return f"""# Kamill Forge Staged Proposal: {title}

Status: staged-draft
Date: {date}
Lane: {candidate['lane']}
Anchor status: {candidate['anchor_status']}
Target repo/path: {repo_path}
Proposed mutation class: {candidate['proposed_mutation_class']}

> Dry-run warning: This is a staged proposal draft only. It does not approve,
> implement, or apply any memory, skill, Core, or project mutation. Explicit
> user approval is required before any change.

## 1. Source Provenance

- Source type: {candidate['source_type']}
- Source location: {candidate['source_ref']}
- Run ID: {candidate.get('run_id') or 'null'}
- Candidate ID: {candidate['id']}
- Rule ID: {candidate['rule_id']}
- Raw evidence summary: {candidate['evidence_summary']}
- Discord anchor status and retarget source: {candidate['anchor_status']}; retarget source pending user decision.

## 2. Candidate Summary

{candidate['evidence_summary']}

## 3. Threshold / Trigger

- Trigger type: {candidate['rule_id']}
- Observation count: captured in the Phase 1-B source candidate when available.
- Why this crossed threshold: pending human review of the source evidence.
- False-positive risk: {candidate['risk_class']}

## 4. Proposed Scope

Exact proposed target files or state:

- Create: pending user-approved scope
- Modify: pending user-approved scope
- Do not touch: memory, skills, Core policy/wiki/raw/log files, project files, cron, hooks, curator behavior, or downstream operating layers before explicit approval.

## 5. Policy Classification

Under `policy/automation.md`:

- Auto-apply candidate: no
- Human gate required: yes
- Blocked by default: yes, until the user approves an exact staged change

Reason: the candidate may affect Hermes memory, skills, Core artifacts, project operating layers, or workflow behavior and therefore requires explicit human judgment.

## 6. Kamill Forge Acceptance Question

Question:

> Does this reduce repeated judgment without letting Hermes modify memory, skills, Core, or projects before the user has approved the exact staged change?

Answer: {acceptance_answer}

## 7. Review Plan

- Opus plan: pending
- Codex check/discussion: pending
- Kamill/Hermes Korean synthesis: pending
- User decision: pending
- If approved, Opus implementation: pending explicit scope
- Codex development review: pending
- Codex verification review: pending
- Closeout/log: pending

## 8. Verification Plan

Commands/checks:

- Define after the user approves the exact mutation target.
- Verify no automatic memory, skill, Core, or project mutation occurs before approval.

Expected result:

- Proposal remains staged until explicit approval.

## 9. User Decision

Decision: pending

Approved scope, if any: none

## 10. Closeout

Implemented: no
Verified: no
Log updated: no
Notes: Generated by the manual dry-run Phase 1-C staged proposal draft generator.
"""


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def assert_allowed_output_path(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    dry_root = DRY_RUN_PROPOSAL_ROOT.resolve()
    temp_root = Path(tempfile.gettempdir()).resolve()
    if _is_relative_to(resolved, dry_root) or _is_relative_to(resolved, temp_root):
        return resolved
    raise DraftInputError(
        "proposal output must be under logs/kamill-forge/dry-runs/staged-proposals/ "
        "or a system temp path used by tests"
    )


def write_draft(path: Path, draft: str) -> Path:
    allowed = assert_allowed_output_path(path)
    allowed.parent.mkdir(parents=True, exist_ok=True)
    allowed.write_text(draft, encoding="utf-8")
    return allowed


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        run_id, raw_candidate = extract_candidate(load_json(Path(args.input)))
        candidate = normalize_candidate(raw_candidate, run_id)
        draft = render_draft(candidate)
        if args.out:
            output_path = write_draft(Path(args.out), draft)
            print(str(output_path))
        else:
            print(draft)
    except DraftInputError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
