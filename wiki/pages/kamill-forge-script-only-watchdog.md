# Kamill Forge Script-Only Watchdog Plan

Status: Phase 1-B minimal manual classifier implemented.

## Purpose

This page describes the implemented Phase 1-B minimal manual classifier for Kamill Forge. It remains a bounded script-only check: it reads one explicit JSON input file, emits inert candidate JSON only for above-threshold repeated observations, and keeps quiet-day runs silent.

The watchdog concept exists to avoid unnecessary LLM calls and avoid false positives. On quiet days, it does nothing visible and writes no files.

## Source Provenance

- `raw/kamill-forge/v0.1-notes.md` — user-approved v0.1 defaults: threshold-primary design, script-only watchdog for quiet-day checks, no LLM calls on quiet days, avoid false positives.
- `policy/kamill-forge.md` — active Quiet-Day Rule, Mutation Boundary, and Phase Boundaries.
- `policy/automation.md` — automation classification and acceptance question.
- `wiki/pages/kamill-forge-discord-anchoring.md` — anchor state used to avoid false-positive project targeting.
- `wiki/pages/kamill-forge-staged-proposal-format.md` — proposal packet used when a candidate needs user review.

## Intended Behavior

A Phase 1-B script-only watchdog:

- runs as a local script only after explicit scoped Phase 1 approval;
- reads only the explicit JSON file passed with `--input`;
- classifies whether any candidate crosses the runtime `--min-observations` test threshold;
- exits quietly when no candidate crosses threshold;
- avoids LLM calls, network calls, Discord API calls, memory writes, skill writes, Core mutations, project mutations, cron changes, hooks, and curator changes;
- surfaces above-threshold candidates as inert stdout JSON instead of applying them.

## Quiet-Day Rule

A quiet day is a check where:

- no candidate crosses the configured threshold; and
- the user has not explicitly requested a Kamill Forge cycle.

On a quiet day, the check should:

- print nothing or only machine-silent status expected by the scheduler;
- make zero LLM calls;
- make zero file mutations;
- make zero memory or skill mutations;
- open no staged proposal;
- exit successfully.

## Planned Threshold Inputs

Exact policy threshold values are not chosen in Phase 1-B. `--min-observations` is a runtime/test parameter for the manual classifier, not a durable policy threshold or downstream behavior rule.

Potential inputs include:

- repeated-observation count for Experience Distillation candidates;
- explicit user-intent signal for Kamill Improvement candidates;
- source type and source reliability;
- anchor state for Discord candidates;
- proposed mutation target and risk class;
- false-positive cost.

Unanchored Discord candidates may cross threshold only as global/unanchored candidates unless the user retargets them or a clear confirmed anchor exists.

## Phase 1-B Implemented Surface

The current implementation is limited to:

- `scripts/kamill_forge_watchdog.py` — manual `--input <json file>` classifier.
- `tests/test_kamill_forge_watchdog.py` — behavior tests for quiet-day, above-threshold, malformed, deterministic-id, and no network/LLM import checks.
- `tests/fixtures/kamill_forge_watchdog/` — explicit JSON fixtures only.

The script emits no output on quiet days. Above-threshold candidates are written only to stdout as inert JSON with `requires_user_approval: true` and `auto_apply: false`.

Phase 1-B accepts only the `experience-distillation` lane. This is an implementation boundary for the manual classifier, not a general Kamill Forge lane policy.

The emitted `rule_id` value is an internal classifier label. It is not a durable rule registry, policy threshold, ledger schema, or downstream contract.

## Non-Goals

The script-only watchdog plan does not authorize:

- LLM invocation on quiet days;
- automatic staged proposal generation;
- automatic memory, skill, Core, or project mutation;
- cron scheduling;
- hook installation;
- curator configuration or behavior changes;
- Discord ingestion or anchoring heuristics;
- downstream project propagation.

## Phase Boundary

Phase 1-B is a minimal manual script implementation only. It does not authorize cron scheduling, hook installation, skill or curator integration, automatic staged proposal generation, automatic memory/skill/Core/project mutation, candidate ledger schema, durable threshold values, or downstream project propagation.

Any Phase 1-C/Phase 2 consumer, ledger, scheduler, hook, skill, curator, or downstream behavior requires a new explicit scoped approval under `policy/kamill-forge.md` Phase Boundaries.

## Phase 1-C Implemented Surface

Phase 1-C adds manual dry-run tooling for candidate review only:

- `scripts/kamill_forge_ledger.py` — normalizes an explicit candidate JSON or Phase 1-B payload, prints dry-run ledger records by default, and appends JSONL only when `--ledger-out` is explicitly provided.
- `scripts/kamill_forge_proposal_draft.py` — renders a staged proposal draft from one explicit candidate JSON, prints markdown by default, and writes a draft file only when `--out` is explicitly provided.
- `tests/test_kamill_forge_ledger.py` and `tests/test_kamill_forge_proposal_draft.py` — verify stdout-only defaults, explicit dry-run file output, malformed-input fail-closed behavior, unanchored Discord `repo_path: null`, output path restrictions, and absence of network/LLM import terms.

The runtime write boundary is limited to explicit dry-run output paths under `logs/kamill-forge/dry-runs/` and test temp paths. The scripts do not schedule themselves, install hooks, call networks or LLMs, write memory or skills, update Core policy/wiki/log files at runtime, mutate projects, or promote staged drafts into approved changes.

## Verification Expectation for Phase 1

When Phase 1 is explicitly approved, the implementation should demonstrate:

- quiet-day exit with zero LLM calls and zero mutations;
- below-threshold candidate behavior with no staged proposal;
- above-threshold candidate behavior that surfaces a staged proposal candidate but does not auto-apply it;
- unanchored Discord behavior that remains global/unanchored;
- deterministic tests or dry-run fixtures for empty, below-threshold, above-threshold, malformed, anchored, and unanchored inputs;
- run trace recorded in `logs/log.md` for any non-quiet exit.
