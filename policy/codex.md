# Hermes Codex Operating Policy

Status: Local active policy for Codex sessions operating on this Hermes Core artifact.

This policy forward-propagates existing Hermes Core rules into Codex operation. It does not create a new Core rule for downstream projects.

## Source Provenance

- `policy/automation.md`.
- `policy/promotion.md`.
- `policy/harness-review.md`.
- `policy/claude-cli.md`.
- `logs/log.md` entries on 2026-05-03 and 2026-05-04 for peer review, Claude CLI invocation, and downstream propagation.
- User approval on 2026-05-04 to run Codex through Hermes with intentionally strong early review gates.

## Scope

This applies when Codex works on this Hermes Core directory or uses this directory as its operating layer.

It does not automatically apply to downstream project Hermes layers. Downstream projects adopt, defer, or opt out under `policy/promotion.md`.

## Adopted Core Rules

Codex must use:

- `policy/automation.md` to classify changes before applying them.
- `policy/promotion.md` before proposing reverse propagation or forward propagation.
- `policy/harness-review.md` for Hermes operating-layer changes.
- `policy/claude-cli.md` when invoking Claude from Codex Desktop or another GUI-launched session.

## Codex Operating Defaults

- Treat Codex-Hermes setup, policy, skills, memory-boundary, execution-flow, and handoff changes as human-gated.
- Prefer strong peer review while Hermes is still early. This is intentional operating conservatism, not an error to optimize away.
- Do not turn DiveBase's stricter workflow into a mandatory Core default merely because it is useful. Use `policy/workflow-profiles.md` for recommended opt-in project profiles.
- If Claude review is requested but unavailable, hanging, or inconclusive, record the failed layer and the fallback decision in `logs/log.md` before treating the Codex review as complete.

## Review Boundary

For Hermes operating-layer changes:

- Human approval is required before changing active behavior.
- Claude review should be requested when available.
- Codex must review the actual diff, scope, policy fit, verification, and log updates.
- The decision trace must state whether Claude review accepted the change, was skipped, or failed at command, auth, workspace-access, timeout, or no-output layer.

## Verification

A Codex-Hermes change is complete only when:

- The affected files are listed.
- The policy classification is recorded.
- Peer-review status is recorded.
- A local consistency check is performed where practical.
