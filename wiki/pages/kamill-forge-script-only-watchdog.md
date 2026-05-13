# Kamill Forge Script-Only Watchdog Plan

Status: Phase 0 design description. Not implemented.

## Purpose

This page describes the intended shape of a future script-only quiet-day check for Kamill Forge. It gives a later Phase 1 implementation a bounded reference while keeping Phase 0 free of executable artifacts.

The watchdog concept exists to avoid unnecessary LLM calls and avoid false positives. On quiet days, it should do nothing visible.

## Source Provenance

- `raw/kamill-forge/v0.1-notes.md` — user-approved v0.1 defaults: threshold-primary design, script-only watchdog for quiet-day checks, no LLM calls on quiet days, avoid false positives.
- `policy/kamill-forge.md` — active Quiet-Day Rule, Mutation Boundary, and Phase Boundaries.
- `policy/automation.md` — automation classification and acceptance question.
- `wiki/pages/kamill-forge-discord-anchoring.md` — anchor state used to avoid false-positive project targeting.
- `wiki/pages/kamill-forge-staged-proposal-format.md` — proposal packet used when a candidate needs user review.

## Intended Behavior

A future script-only watchdog should:

- run as a local script only after explicit scoped Phase 1 approval;
- read only approved threshold inputs and candidate counts;
- classify whether any candidate crosses a configured threshold;
- exit quietly when no candidate crosses threshold and the user has not explicitly requested a Kamill Forge cycle;
- avoid LLM calls on quiet days;
- avoid network calls, Discord API calls, memory writes, skill writes, Core mutations, project mutations, cron changes, hooks, and curator changes;
- surface above-threshold candidates for staged review instead of applying them.

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

Exact threshold values are not chosen in Phase 0. A later Phase 1 proposal should define them explicitly before any script artifact exists.

Potential inputs include:

- repeated-observation count for Experience Distillation candidates;
- explicit user-intent signal for Kamill Improvement candidates;
- source type and source reliability;
- anchor state for Discord candidates;
- proposed mutation target and risk class;
- false-positive cost.

Unanchored Discord candidates may cross threshold only as global/unanchored candidates unless the user retargets them or a clear confirmed anchor exists.

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

## Phase 0 Boundary

This page is a design plan only. No `scripts/`, `skills/`, hook, cron job, watchdog script artifact, or curator change is added in Phase 0.

Phase 1 implementation of any watchdog requires an explicit scoped approval under `policy/kamill-forge.md` Phase Boundaries. A Phase 0 wiki page does not authorize the corresponding executable artifact.

## Verification Expectation for Phase 1

When Phase 1 is explicitly approved, the implementation should demonstrate:

- quiet-day exit with zero LLM calls and zero mutations;
- below-threshold candidate behavior with no staged proposal;
- above-threshold candidate behavior that surfaces a staged proposal candidate but does not auto-apply it;
- unanchored Discord behavior that remains global/unanchored;
- deterministic tests or dry-run fixtures for empty, below-threshold, above-threshold, malformed, anchored, and unanchored inputs;
- run trace recorded in `logs/log.md` for any non-quiet exit.
