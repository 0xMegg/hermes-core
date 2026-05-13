# Kamill Forge Discord Anchoring

## Purpose

This page describes how Kamill Forge handles candidates discovered in Discord contexts when no repository or project anchor is clear. The goal is to avoid false-positive project targeting while preserving useful global observations for later staged review.

## Source Provenance

- `raw/kamill-forge/v0.1-notes.md` — user-approved v0.1 default that unanchored Discord candidates stay global/unanchored until the user retargets them.
- `policy/kamill-forge.md` — active Unanchored Discord Rule and mutation boundary.
- `policy/promotion.md` — Core/project propagation boundary.

## Anchor States

### Anchored

A Discord candidate is anchored when the surrounding conversation contains a clear repository path, project identity, or operating-layer target and the candidate belongs to that target.

Examples:

- The thread or message explicitly includes `Repo path: /path/to/repo`.
- The user explicitly says the candidate applies to a named repository or project.
- The conversation is already scoped to Hermes Core or another operating-layer artifact by a clear path anchor.

### Global / Unanchored

A Discord candidate is global/unanchored when Hermes can see that the source is Discord, but cannot safely attach the candidate to a specific repository, project, or operating-layer target.

Examples:

- The message is a general improvement idea with no repo path.
- The thread mixes multiple projects and the candidate is not explicitly retargeted.
- The candidate sounds reusable, but the user has not said whether it belongs in Core, a project layer, memory, or a skill.

## Default Behavior

A candidate discovered in an unanchored Discord context remains global/unanchored. It must not be applied to a repository or downstream project until either:

1. the user explicitly retargets it; or
2. the surrounding conversation produces a clear repo/project anchor and the candidate is confirmed to belong there.

A global/unanchored candidate may be staged as a global-scope Kamill Forge proposal, but it must not be silently scoped to a project.

## Retargeting

A retarget event is an explicit user decision that moves a candidate from global/unanchored to an anchored target.

Valid retarget signals include:

- “Apply this candidate to `/path/to/repo`.”
- “Stage this for Hermes Core.”
- “This belongs only to the KODY workspace.”
- “Retarget the previous global candidate to this repo path.”

Retargeting should record:

- the previous global/unanchored candidate;
- the new target path or project identity;
- the user instruction or conversation anchor that caused the retarget;
- the staged proposal that will carry the target-specific review.

## State Machine

```text
observed in Discord
  ↓
global/unanchored candidate
  ↓ only by explicit retarget or confirmed clear anchor
anchored staged proposal
  ↓ Opus/Codex review + user approval
approved implementation scope
  ↓
implemented
  ↓
verified + logged
```

Hermes must not move a candidate from global/unanchored to anchored solely by similarity, guesswork, thread title, or project-name inference.

## Forbidden Patterns

- Inferring a repository path from topical similarity alone.
- Treating a Discord thread title as a sufficient project anchor when no repo path or explicit user target exists.
- Writing memory, skills, Core files, or project files from an unanchored Discord candidate before staged review and explicit approval.
- Forward-propagating a global Discord candidate into downstream projects.
- Reclassifying a global candidate as anchored without recording the retarget event.

## Staged Proposal Fields for Discord Candidates

A staged proposal for a Discord-sourced candidate should include:

```md
Discord anchor status: global-unanchored | anchored
Discord retarget source: explicit user instruction | confirmed repo/path anchor | none
Repo path: <path or null>
Auto-anchor attempted: no
```

If `Discord anchor status` is `global-unanchored`, `Repo path` should be empty or `null`.

## Phase 0 Boundary

This page describes anchoring behavior as design knowledge. It does not implement a Discord ingestion path, anchoring heuristic, classifier, watchdog, cron job, hook, skill, curator change, or automatic retargeting path.
