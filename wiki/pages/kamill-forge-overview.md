# Kamill Forge Overview

## Purpose

Kamill Forge is the named governance layer for the Hermes Experience Distillation Loop. It governs how Hermes turns repeated experience, user-originated improvement ideas, and operating-layer observations into staged proposals for memory, skills, policy, or project changes.

Kamill Forge does not replace Hermes Core. `hermes-core` remains the operating-layer template and reference project. Kamill Forge names a layer inside that operating model.

## Source Provenance

- `raw/kamill-forge/v0.1-notes.md` — user-approved naming, scope, and v0.1 defaults collected on 2026-05-13.
- `policy/automation.md` — existing Core automation boundary.
- `policy/promotion.md` — existing Core/project propagation boundary.
- `policy/codex.md` — local Codex operation and peer-review boundary for this Hermes Core artifact.
- `policy/claude-cli.md` — Claude invocation boundary used for review and judgment.

## Relationship to Existing Hermes Mechanisms

Kamill Forge is not a parallel automatic learning system. It governs the existing Hermes mechanisms:

- `memory` for compact durable facts.
- `skills` for reusable procedures.
- `session_search` for cross-session recall.
- `curator` for skill lifecycle maintenance.

The layer decides when an observed improvement candidate is safe to propose, how it should be reviewed, and where it should stop before user approval.

## v0.1 Operating Shape

Kamill Forge v0.1 is threshold-primary and conservative:

1. A candidate appears through repeated experience, a user-originated idea, or an explicit operating-layer observation.
2. Quiet-day checks are script-only and make no LLM calls when no candidate crosses threshold.
3. Unanchored Discord candidates remain global/unanchored until the user retargets them to a specific repository or project.
4. Codex proposes a narrow staged change.
5. Claude judges the proposal when available.
6. Kamill/Hermes synthesizes the result for the user in Korean.
7. The user decides.
8. No memory, skill, Core, or project mutation happens before explicit approval.

## Kamill Improvement Lane

User-originated Kamill or Hermes improvement ideas use the same governance flow, but they are tracked as a distinct Kamill Improvement Lane. This keeps direct improvement requests visible without allowing them to bypass the same staged proposal, review, and approval gates.

## Quiet-Day Behavior

A quiet day is a day with no candidate above threshold and no explicit user request to run a Kamill Forge improvement cycle. In that case, v0.1 should perform only script-level checks and exit without calling an LLM or mutating Hermes state.

## Phase 0 Boundary

Phase 0 introduces the design and policy boundary only. It does not add watchdog scripts, cron jobs, skills, hooks, curator changes, or automatic mutation paths.

## Naming Boundary

`hermes-core` should remain the repository and template name during Phase 0. Kamill Forge should be used for the governance layer. A repository or project rename would be a separate high-blast-radius decision because it could break historical references, downstream template usage, fresh-agent read order, and provenance trails.
