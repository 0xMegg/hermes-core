# Kamill Forge Staged Proposal Format

## Purpose

A Kamill Forge staged proposal is the review packet created before any memory, skill, Core, or project mutation. It turns a candidate into a scoped user decision without applying the change.

A staged proposal is not an approval, implementation, automation hook, script, cron job, commit, or downstream propagation. It only makes the proposed change explicit enough for Opus planning, Codex checking, Kamill/Hermes Korean synthesis, and user decision.

## Source Provenance

- `raw/kamill-forge/v0.1-notes.md` — user-approved Kamill Forge v0.1 defaults and workflow-role clarification.
- `policy/kamill-forge.md` — active Kamill Forge governance boundary.
- `policy/automation.md` — auto-apply, human-gate, and blocked-by-default classification.
- `policy/promotion.md` — Core/project propagation boundary.

## Required Fields

Every staged proposal should include:

- **Title and date** — a short unique title and proposal date.
- **Candidate lane** — Experience Distillation or Kamill Improvement.
- **Origin** — repeated observation, user-originated idea, or explicit operating-layer note.
- **Source provenance** — where the candidate came from and what evidence supports it.
- **Anchor status** — repository path, project identity, or global/unanchored.
- **Proposed target** — exact memory entry, skill, policy file, wiki page, Core artifact, project operating-layer file, or no-mutation target.
- **Exact change shape** — one scoped change, not a bundle of unrelated changes.
- **Automation classification** — auto-apply candidate, human gate required, or blocked by default under `policy/automation.md`.
- **Acceptance question answer** — an explicit answer to the Kamill Forge acceptance question in `policy/kamill-forge.md`.
- **Verification or adoption check** — how the proposal will be checked after approval and implementation.
- **Review state** — Opus plan, Codex check/discussion, Kamill/Hermes Korean synthesis, user decision, implementation status, Codex review, and closeout.

## Template

```md
# Kamill Forge Staged Proposal: <short title>

Status: staged
Date: YYYY-MM-DD
Lane: experience-distillation | kamill-improvement
Anchor status: anchored | global-unanchored
Target repo/path: <repo path or null>
Proposed mutation class: memory | skill | policy | wiki | raw | log | core-template | project-layer | script | cron | hook | curator | none

## 1. Source Provenance

- Source type:
- Source location:
- Observed at:
- Raw evidence summary:
- If Discord: anchor status and retarget source:

## 2. Candidate Summary

One-paragraph summary of the repeated judgment cost or user-originated improvement idea.

## 3. Threshold / Trigger

- Trigger type:
- Observation count:
- Why this crossed threshold:
- False-positive risk:

## 4. Proposed Scope

Exact proposed target files or state:

- Create:
- Modify:
- Do not touch:

## 5. Policy Classification

Under `policy/automation.md`:

- Auto-apply candidate: yes/no
- Human gate required: yes/no
- Blocked by default: yes/no

Reason:

## 6. Kamill Forge Acceptance Question

Question:

> Does this reduce repeated judgment without letting Hermes modify memory, skills, Core, or projects before the user has approved the exact staged change?

Answer:

## 7. Review Plan

- Opus plan:
- Codex check/discussion:
- Kamill/Hermes Korean synthesis:
- User decision:
- If approved, Opus implementation:
- Codex development review:
- Codex verification review:
- Closeout/log:

## 8. Verification Plan

Commands/checks:

Expected result:

## 9. User Decision

Decision: pending | approved-scope | rejected | retired

Approved scope, if any:

## 10. Closeout

Implemented: yes/no
Verified: yes/no
Log updated: yes/no
Notes:
```

## Must Not Contain

A staged proposal must not contain:

- Applied edits.
- Memory or user-profile writes.
- Skill creation or editing.
- Core or project file mutation.
- Implicit downstream propagation.
- Cron, hook, watchdog, curator, or script side effects.
- Broad rename, broad sync, or multi-target bundling.
- Language that treats a proposal as already approved.

## Lifecycle

1. A candidate is observed through repeated Hermes work, a user-originated Kamill/Hermes improvement idea, or an explicit operating-layer observation.
2. If it crosses threshold or the user explicitly asks for a Kamill Forge cycle, Opus drafts the initial plan.
3. Codex checks the plan against scope, policy, provenance, and verification, then discusses it with Opus where needed.
4. Kamill/Hermes synthesizes the planning result in Korean for the user.
5. The user approves a scope, rejects the proposal, retires it, or asks for a narrower proposal.
6. If implementation is explicitly approved, Opus leads implementation within the approved scope.
7. Codex owns development review, verification review, and closeout.
8. Kamill/Hermes synthesizes the final result in Korean.
9. Important decisions and verification are recorded in `logs/log.md`.

## Phase 0 Boundary

This page describes the staged proposal format. It does not implement a proposal generator, template renderer, watchdog script, cron job, hook, skill, curator change, or any automatic mutation path.
