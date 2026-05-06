# Hermes Workflow Profiles

Status: Recommended, opt-in per project.

Hermes Core may recommend workflow profiles, but it does not force them onto downstream projects. A project adopts, defers, or opts out under `policy/promotion.md`.

## Source Provenance

- `/Users/mero/Dev/13.claude/workouts/divebase/.hermes/policy/workflow.md`.
- `/Users/mero/Dev/13.claude/workouts/divebase/.hermes/logs/log.md`.
- `/Users/mero/Dev/13.claude/workouts/honbabseoul/.hermes/archive/legacy-harness-2026-05-03/.claude/commands/plan.md`.
- `/Users/mero/Dev/13.claude/workouts/honbabseoul/.hermes/archive/legacy-harness-2026-05-03/.claude/commands/develop.md`.
- `/Users/mero/Dev/13.claude/workouts/honbabseoul/.hermes/archive/legacy-harness-2026-05-03/.claude/commands/review.md`.
- User-approved Core propagation decision on 2026-05-05.

## Stricter Claude-First Profile

This profile is recommended for projects where planning quality, final judgment, and traceability matter more than minimizing model cost or workflow weight.

Model preferences:

- `plan`: Claude Opus.
- `develop`: Claude Sonnet.
- `closeoff`: Claude Opus final review, followed by Codex final review.

Role split:

- Claude writes the plan.
- Codex reviews the plan against source, scope, policy, and verification.
- Claude performs development after the plan is accepted.
- Codex reviews the diff and verification evidence.
- Closeoff is not a single-model step. It combines Claude Opus final review, Codex final judgment, verification evidence, PR or merge handling where applicable, and handoff updates.

## Adoption Boundary

Adoption is project-local.

Before applying this profile to a project, confirm:

- The project benefits from a heavier planning and review gate.
- The project has enough task complexity or release risk to justify Opus usage for planning and final review.
- The project has no conflicting local workflow policy.
- The adoption, deferral, or opt-out reason can be recorded in the project log.

Projects with lighter Hermes layers may defer this profile to avoid unnecessary process and model-cost overhead.
