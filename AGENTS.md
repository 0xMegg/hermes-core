# Hermes Operating Rules

These rules are the short operating contract. Keep this file to one screen.

Read order for fresh agents:

1. `AGENTS.md` — operating rules and precedence.
2. `SOUL.md` — judgment posture.
3. `USER.md` — user preferences.
4. `MEMORY.md` — operational memory boundary.
5. `policy/automation.md` — change classification.
6. `policy/promotion.md` — Core/project rule propagation.
7. `policy/workflow-profiles.md` — opt-in workflow profiles.
8. `policy/codex.md` — Codex operation on this Hermes artifact.
9. `policy/claude-cli.md` — Claude CLI invocation boundary.
10. `wiki/pages/hermes-operating-model.md` — full model.
11. `wiki/pages/hermes-rejected-options.md` — decisions not to re-derive.

Precedence: `AGENTS.md` > `policy/` > `SOUL.md` > `USER.md` > `MEMORY.md` > `wiki/`.

1. Verification is the completion condition. An unverified result is not done.
2. Auto-apply only additive, reversible, measurable changes.
3. Behavior, ownership, permission, execution-flow, or project-judgment changes require a human gate.
4. Destructive or hard-to-reverse actions are blocked unless the user explicitly approves a scoped plan.
5. Decision trace is part of the artifact. Record important decisions in `logs/log.md`.
6. Keep boundaries clean: source in `raw/`, knowledge in `wiki/`, procedures in `skills/`, policy in `policy/`, operational memory in `MEMORY.md`.
7. Wiki pages require raw provenance. Do not create durable knowledge without a source.
8. Meta work needs a box. Do not let Hermes improvement displace product work unless it blocks execution.

For rationale, see `wiki/pages/hermes-operating-model.md`.
For automation boundaries, see `policy/automation.md`.
For Core/project rule propagation, see `policy/promotion.md`.

Log boundary: `logs/log.md` records decisions, execution traces, and verification results. `wiki/log.md` records wiki page changes only.
