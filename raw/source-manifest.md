# Source Manifest

This manifest lists source material used to initialize Hermes.

Note: inherited local source references may contain upstream harness-forge paths that do not exist inside this Hermes artifact.

Each source should identify:

- Source URL or local path.
- Collection or review date.
- Wiki pages that depend on it.

## External Sources

1. Hermes Agent guide
   - URL: `https://wikidocs.net/book/19414`
   - Role: Hermes architecture, memory, skills, MCP, cron, gateway, and security model.
   - Reviewed: 2026-05-01
   - Used by: `wiki/pages/hermes-operating-model.md`, `wiki/pages/hermes-rejected-options.md`

2. Boris Cherny / Claude Code workflow interpretation
   - URL: `https://wikidocs.net/blog/@jaehong/8587/`
   - Role: short living instructions, plan-first work, permission boundary, verification loop, context reset.
   - Reviewed: 2026-05-01
   - Used by: `wiki/pages/hermes-operating-model.md`, `wiki/pages/hermes-rejected-options.md`

3. CLAUDE.md anti-pattern article
   - URL: `https://siosio3103.medium.com/당신의-claude-md는-아마-잘못되었을-겁니다-boris-cherny가-절대-하지-않는-7가지-실수-f2201efd098b`
   - Role: context rot, living documents, verification, permission safety, format drift.
   - Reviewed: 2026-05-01
   - Used by: `wiki/pages/hermes-operating-model.md`, `wiki/pages/hermes-rejected-options.md`

4. Karpathy LLM Wiki
   - URL: `https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f`
   - Role: raw/source/wiki/schema separation, ingest/query/lint, index/log, provenance.
   - Reviewed: 2026-05-01
   - Used by: `wiki/pages/hermes-operating-model.md`, `wiki/pages/hermes-rejected-options.md`

## Local Sources

1. `philosophy.md`
   - Role: harness-forge load-bearing invariants.
   - Reviewed: 2026-05-01
   - Used by: `SOUL.md`, `wiki/pages/hermes-operating-model.md`, `wiki/pages/hermes-rejected-options.md`

2. `automation-boundary.md`
   - Role: auto-apply, human-gate, and block boundaries.
   - Reviewed: 2026-05-01
   - Used by: `policy/automation.md`, `wiki/pages/hermes-operating-model.md`, `wiki/pages/hermes-rejected-options.md`

3. `raw/kamill-forge/v0.1-notes.md`
   - Role: user-approved naming, scope, v0.1 defaults, and workflow-role clarification for the Kamill Forge governance layer.
   - Collected: 2026-05-13
   - Used by: `policy/kamill-forge.md`, `wiki/pages/kamill-forge-overview.md`, `wiki/pages/kamill-forge-staged-proposal-format.md`, `wiki/pages/kamill-forge-discord-anchoring.md`, `wiki/pages/kamill-forge-script-only-watchdog.md`
