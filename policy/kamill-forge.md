# Kamill Forge Policy

Status: Phase 0 active governance boundary for Kamill Forge v0.1.

Kamill Forge is the governance layer for Hermes experience distillation. It governs proposals that may affect Hermes memory, skills, session recall, curator behavior, Core operating artifacts, or downstream project operating layers.

## Source Provenance

- `raw/kamill-forge/v0.1-notes.md`.
- `policy/automation.md`.
- `policy/promotion.md`.
- `policy/codex.md`.
- `policy/harness-review.md`.
- `policy/claude-cli.md`.

## Scope

This policy applies when a Kamill Forge cycle proposes or evaluates changes to:

- Hermes memory or user profile entries.
- Hermes skills.
- Core operating-layer files.
- Project operating-layer files.
- Curator behavior or skill lifecycle rules.
- Governance around session_search-derived lessons.
- User-originated Kamill/Hermes improvement ideas.

This policy does not rename Hermes Core, replace `policy/automation.md`, or create a parallel automatic learning system.

## v0.1 Defaults

- Threshold-primary design.
- Script-only quiet-day checks.
- No LLM calls on quiet days.
- Avoid false positives.
- Unanchored Discord candidates remain global/unanchored until the user retargets them.
- Opus plans first.
- Codex checks the plan and discusses it with Opus.
- Opus leads implementation when implementation is approved.
- Codex owns development review, verification review, and closeout.
- Kamill/Hermes synthesizes in Korean.
- User decides.
- Staged proposal only before explicit commit approval.
- No automatic memory, skill, Core, or project modifications without explicit approval.

## Candidate Lanes

### Experience Distillation Lane

Use this lane for repeated observations from real Hermes work that may justify a memory, skill, policy, wiki, or project-operating-layer proposal.

### Kamill Improvement Lane

Use this lane for user-originated Kamill or Hermes improvement ideas. These ideas may start with stronger user intent, but they still require staged proposal, review, and explicit approval before mutation.

## Quiet-Day Rule

If no candidate crosses the configured threshold and the user has not explicitly requested a Kamill Forge cycle, the check must stay script-only and exit quietly. It must not call an LLM, write memory, create or edit skills, modify Core, modify projects, or open a staged proposal.

## Unanchored Discord Rule

A candidate discovered in an unanchored Discord context remains global/unanchored. It must not be applied to a repository or downstream project until the user explicitly retargets it or the conversation has a clear repo path anchor.

## Mutation Boundary

Before explicit user approval, Kamill Forge may only produce a staged proposal. It must not automatically modify:

- Memory or user profile entries.
- Skills.
- Core policy, wiki, raw source, logs, or read order.
- Project files.
- Curator configuration or behavior.
- Cron jobs, hooks, watchdog scripts, or execution modes.

After user approval, the approved scope controls the maximum allowed mutation. A narrow approval does not authorize broader renaming, policy rewrites, downstream propagation, or automation scaffolding.

## Review Boundary

For Core operating-layer changes, follow the existing review posture:

1. Human gate before active policy, read-order, behavior, ownership, permission, or execution-flow changes.
2. Opus drafts the initial plan.
3. Codex checks the plan against scope, policy, provenance, and verification, then discusses the plan with Opus where needed.
4. Kamill/Hermes synthesizes the planning result in Korean for the user.
5. If implementation is explicitly approved, Opus leads implementation within the approved scope.
6. Codex owns development review, verification review, and closeout before the change is treated as complete.
7. Kamill/Hermes synthesizes the final decision and verification result in Korean.
8. Record important decisions and verification in `logs/log.md`.

If Opus or Codex review is unavailable, times out, or returns no usable output, record the failed review layer under the existing Claude CLI or Codex operating policy instead of silently treating the review as successful.

## Phase Boundaries

### Phase 0

Phase 0 is documentation and paper-run only. It may add this policy, raw source notes, wiki pages describing the design, index entries, read-order routing, and log entries.

Phase 0 must not produce a watchdog script artifact, cron job, skill, hook, curator change, or any automatic mutation path. Wiki descriptions of a future watchdog are design documents, not executable specifications.

### Phase 1 and Later

No Phase 1 work begins until the user explicitly approves a scoped Phase 1 plan. The approved scope controls the maximum allowed change. A Phase 0 wiki description does not authorize the corresponding Phase 1 artifact, and a narrow Phase 1 approval does not authorize broader scaffolding, automation, or downstream propagation.

## Acceptance Question

Before accepting a Kamill Forge proposal, ask:

"Does this reduce repeated judgment without letting Hermes modify memory, skills, Core, or projects before the user has approved the exact staged change?"

If the answer is unclear, keep the candidate staged and ask for a narrower human decision.
