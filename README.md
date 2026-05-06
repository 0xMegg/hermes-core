# Hermes Core

This directory is the MVP operating artifact for Hermes.

It is not a transcript archive and not a prompt dump. It contains the minimum structure needed for a fresh agent to understand how Hermes should operate without re-deriving the design decisions.

## Read Order

`AGENTS.md` is the canonical read-order and precedence source. Start there.

Reference as needed:

- `raw/source-manifest.md` — source provenance.
- `wiki/index.md` — durable knowledge catalog.
- `logs/log.md` — decision and verification trace.

## Source Documents

The root files `philosophy.md` and `automation-boundary.md` are inherited source documents. They are not active operating policy. Active rules live in `AGENTS.md`, `SOUL.md`, and `policy/automation.md`.

## Codex Operation

Codex sessions that operate on this Hermes Core artifact also read `policy/codex.md`.
That file is local operating policy for Codex-Hermes use, not a downstream project default.

## Template Reuse

Reusable scaffolding:

- `AGENTS.md`
- `SOUL.md`
- `policy/automation.md`
- `policy/promotion.md`
- `policy/workflow-profiles.md`
- `policy/claude-cli.md`
- `wiki/pages/hermes-operating-model.md`
- `wiki/pages/hermes-rejected-options.md`
- `raw/source-manifest.md`
- `skills/README.md`

Instance files to replace or reset per user/project:

- `USER.md`
- `MEMORY.md`
- `logs/log.md`
- `wiki/log.md`

Local operator policy to review before reuse:

- `policy/codex.md`

Do not copy instance preferences into a new user or project without review.
