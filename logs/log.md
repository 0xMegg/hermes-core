# Hermes Log

Append important decisions, verification results, and run notes here.

## 2026-05-01

### Decision: Initialize Hermes as a small operating system

Decision:

- Use short `AGENTS.md` as trigger/invariant router.
- Keep identity in `SOUL.md`.
- Keep user preferences in `USER.md`.
- Keep operational memory in `MEMORY.md`.
- Keep source material in `raw/`.
- Keep synthesized knowledge in `wiki/`.
- Keep repeatable procedures in `skills/`.
- Keep automation boundaries in `policy/automation.md`.
- Keep decision and verification traces in `logs/log.md`.

Reason:

- Avoid context rot from a large instruction file.
- Preserve provenance for durable knowledge.
- Keep automation bounded by reversibility, impact, and measurement.
- Prevent harness-forge mechanics from becoming meta-heavy Hermes ceremony.

Verification:

- Initial structure created with separate files for rules, identity, user preferences, memory, wiki, raw sources, policy, and logs.

### Decision: Record rejected Hermes design paths in the wiki

Decision:

- Added `wiki/pages/hermes-rejected-options.md`.
- Updated `wiki/index.md`.
- Updated `wiki/log.md`.

Reason:

- The operating model records the final structure, but later sessions also need to know which alternatives were already considered and why they were not chosen.
- Rejected options are durable design knowledge, not operational memory, so they belong in `wiki/`.

Verification:

- The rejected-options page includes provenance, rejection reasons, defaults, and revisit conditions.

### Decision: Clarify MVP entrypoint and ambiguity boundaries

Decision:

- Added `README.md` as the directory entrypoint.
- Added read order, precedence, and log boundary notes to `AGENTS.md`.
- Clarified the `USER.md` and `MEMORY.md` boundary.
- Clarified that `policy/automation.md` applies to Hermes itself.
- Added glossary, log boundary, and self-application sections to `wiki/pages/hermes-operating-model.md`.
- Marked `philosophy.md` and `automation-boundary.md` as source documents rather than active policy.

Reason:

- Claude review found that a fresh agent could otherwise misread duplicate source files as active policy, confuse `logs/log.md` with `wiki/log.md`, or infer missing definitions for verification, blast radius, measurable, and meta work box.

Verification:

- Updated files now define entrypoint, precedence, source status, glossary terms, log separation, and self-application.

### Decision: Keep verification/lint artifacts observation-driven

Decision:

- Kept `AGENTS.md` as the canonical read-order source and simplified `README.md` to point there.
- Strengthened the inherited-source labels in `philosophy.md` and `automation-boundary.md`.
- Did not add `skills/wiki-lint.md`, `policy/wiki-lint.md`, or `skills/candidates.md` yet.
- Did not split `USER.md` yet.

Reason:

- A later review correctly identified drift risk from duplicated read order and possible confusion around inherited source files.
- Claude review judged those two issues as low-cost immediate fixes.
- Claude review judged lint/checklist skills, candidates tracking, USER splitting, and external-memory precedence as premature until repeated incidents or distribution needs are observed.

Verification:

- `README.md` now delegates read order to `AGENTS.md`.
- Root source documents now explicitly say they are inherited source documents and not active policy.

### Decision: Mark instance files before template reuse

Decision:

- Marked `USER.md` as an instance file that must be replaced per user/project.
- Added a Template Reuse section to `README.md`.
- Added inherited upstream path disclaimers to `raw/source-manifest.md` and `wiki/pages/hermes-operating-model.md`.
- Continued to defer `USER.template.md`, `skills/candidates.md`, and verification/lint checklist artifacts.

Reason:

- A later review identified that `USER.md` currently contains original-user Korean response preferences and trigger phrases, which could leak into reused templates.
- The same review identified that inherited source documents reference upstream harness-forge paths that do not exist in this artifact.
- Claude review judged the marker, reuse guide, and upstream-path disclaimer as low-cost immediate fixes, while separate template files and new skill/checklist artifacts remain premature until reuse or repetition is observed.

Verification:

- `USER.md` now starts with an instance-file warning.
- `README.md` identifies reusable scaffolding and instance files.
- Source provenance docs now warn that upstream paths may not exist locally.

## 2026-05-03

### Decision: Define Core promotion and propagation policy

Decision:

- Added `policy/promotion.md` for project-to-Core reverse propagation and Core-to-project forward propagation.
- Updated `AGENTS.md` read order and precedence so fresh agents load the promotion boundary.
- Updated `README.md`, `wiki/pages/hermes-operating-model.md`, `wiki/index.md`, and `wiki/log.md` to reflect the new active policy.

Reason:

- DiveBase produced multiple operating-layer rules that appear reusable: workflow phases, Claude-first/Codex-reviewed flow, task close gate, and harness change review.
- Honbabseoul adopted a lighter Hermes layer, showing that Core needs an explicit gate for reusable harness rules instead of informal cross-project copying.
- Claude review recommended pull-only forward propagation, failure-mode-first rule definitions, and a small MVP policy rather than automatic sync or a large rule registry.

Verification:

- `policy/promotion.md` exists and is referenced from `AGENTS.md`, `README.md`, `wiki/pages/hermes-operating-model.md`, and `wiki/index.md`.
- `AGENTS.md` remains short at 31 lines after adding the promotion policy to read order.
- Trailing-whitespace check returned no matches across changed Markdown files.
- `git diff --check` was not available because this template directory is not a git repository.

### Decision: Reverse-propagate DiveBase harness review rule as incubating Core policy

Decision:

- Added `policy/harness-review.md` as the first project-to-Core reverse propagation from DiveBase.
- Set status to Incubating, not Recommended.
- Kept `policy/promotion.md` as governance only and did not add incubating rule content there.
- Did not add the incubating policy to `AGENTS.md` read order; downstream adoption remains opt-in.

Reason:

- DiveBase proved the need for peer-agent review on Hermes operating-layer changes through the task close gate and harness change review decisions.
- Claude and Codex agreed that the reusable invariant is narrower than the full DiveBase workflow: harness or operating-layer changes should receive available peer-agent review after the human gate and before taking effect.
- Claude challenged the initial Codex proposal to mark the rule Recommended; Codex accepted that Incubating better follows `policy/promotion.md` because broader downstream adoption is not yet proven.
- Claude also challenged embedding the rule inside `policy/promotion.md`; Codex accepted that a separate single-purpose policy keeps promotion governance separate from promoted rule content.

Verification:

- `policy/harness-review.md` records status, provenance, scope, exclusions, review standard, and logging requirement.
- The policy uses "available peer-agent review" and identifies Claude/Codex as the current reviewer set, avoiding hard-coding them as the invariant.
- The policy excludes typo-only docs/wiki edits unless they affect authority, procedure, or active operating guidance.
- Claude final review accepted the implemented policy with no blocking issues.

## 2026-05-04

### Decision: Add and forward-propagate Claude CLI invocation policy

Decision:

- Added `policy/claude-cli.md` as a Recommended Core operating policy.
- Added it to `AGENTS.md` read order and reusable scaffolding in `README.md`.
- Forward propagation target projects: DiveBase and Honbabseoul.
- Recommended status is based on explicit human-gated approval to propagate the rule plus immediate downstream adoption in both target projects.

Reason:

- Codex Desktop repeatedly failed to invoke Claude reliably because two separate layers were being conflated: GUI launcher PATH omitted the Claude executable path, and Claude `-p` workspace access did not include sibling project directories unless the working directory or `--add-dir` was set correctly.
- Claude review accepted the root cause split and recommended absolute executable invocation plus scoped per-call workspace access instead of broad permanent read grants.
- Claude final review of the implemented Core and downstream propagation found one blocking log-date issue, which was corrected here; remaining notes were non-blocking.
- Codex review accepted the implemented policy and propagation as scoped, additive, reversible, and consistent with `policy/promotion.md` and `policy/harness-review.md`.
- The rule prevents a repeated operating failure and is additive, reversible, and measurable.

Verification:

- `claude --version` failed in Codex Desktop with `command not found`.
- `/opt/homebrew/bin/claude --version`, `auth status`, and a short `-p` prompt succeeded.
- Cross-project file read failed without `--add-dir` and succeeded with `--add-dir`.
- Claude final review verified read-order consistency, project isolation, and downstream adoption records after running with explicit `--add-dir` for DiveBase and Honbabseoul.

### Decision: Forward-propagate Core policy into Codex-Hermes operation

Decision:

- Added `policy/codex.md` as a local active policy for Codex sessions operating on this Hermes Core artifact.
- Added it to `AGENTS.md` read order.
- Indexed it in `wiki/index.md`.
- Documented in `README.md` that this is local operator policy to review before template reuse.

Reason:

- User approved running Codex through Hermes and explicitly confirmed that intentionally strong early review gates are desired.
- Current analysis found no immediate reverse propagation into Core.
- Current analysis found that Codex operation should forward-propagate existing Core policy: `automation`, `promotion`, `harness-review`, and `claude-cli`.
- DiveBase's stricter `plan/develop/closeoff`, task close gate, and Claude-first/Codex-reviewed workflow remain useful local candidates but should not be promoted into Core yet because Honbabseoul uses a lighter Hermes layer and the workflow could impose project-fit costs.

Review:

- Claude review was requested twice through `/opt/homebrew/bin/claude -p`, including a shorter `sonnet` prompt, but both calls produced no output within the wait window and were killed.
- After the files were changed, Claude review was requested again with `/opt/homebrew/bin/claude --model sonnet -p`; it produced no output within 30 seconds and was killed.
- A later retry with `/opt/homebrew/bin/claude --model sonnet -p` completed successfully and returned `NO REQUIRED FIXES` for the Codex-Hermes propagation change.
- `/opt/homebrew/bin/claude --version` returned `2.1.126 (Claude Code)`.
- `/opt/homebrew/bin/claude auth status` returned logged-in status.
- Under `policy/claude-cli.md`, the earlier failures are recorded as Claude non-interactive review no-output/timeout issues, not command-entry or auth failures.
- Codex final review accepted the scope as local Codex-Hermes forward propagation, not Core reverse propagation.

Verification:

- This change is limited to Hermes operating documentation and policy.
- It does not modify downstream project Hermes layers.
- It does not reverse-propagate DiveBase workflow rules into Core.

## 2026-05-05

### Decision: Add opt-in workflow model profile

Decision:

- Added `policy/workflow-profiles.md` as a Recommended, opt-in Core workflow profile.
- Added it to `AGENTS.md` read order, `README.md` reusable scaffolding, and `wiki/index.md`.
- Updated `policy/codex.md` so it blocks mandatory Core-default promotion while allowing the new opt-in profile.

Reason:

- DiveBase logs and `.hermes/policy/workflow.md` show repeated value from a stricter Claude-first, Codex-reviewed flow.
- Honbabseoul legacy harness command frontmatter records the model mapping: `plan` uses Opus, `develop` uses Sonnet, and `review` uses Opus.
- The prior Core decision against mandatory promotion still stands because lighter Hermes projects may not benefit from the added process and Opus cost.
- User approved recording and propagating the profile as recommended opt-in guidance on 2026-05-05.

Review:

- Human gate: approved in-session by the user.
- Claude review: requested with `/opt/homebrew/bin/claude --model sonnet -p` plus scoped `--add-dir` access to DiveBase and Honbabseoul; it produced no stdout for more than 60 seconds and was terminated. Under `policy/claude-cli.md`, this is recorded as a Claude non-interactive no-output/timeout issue, not command-entry, auth, or workspace-access failure.
- Codex review: accepted the scope as additive, reversible policy guidance rather than a mandatory execution-flow change.

Verification:

- Local source search confirmed no prior role-model mapping existed in Hermes Core.
- Source search confirmed Honbabseoul legacy command frontmatter maps `plan` to Opus, `develop` to Sonnet, and `review` to Opus.
- Source search confirmed DiveBase active workflow uses Claude for plan/develop and Claude Opus plus Codex final review at close gate.

## 2026-05-11 — Harness Review Policy Discoverability Cleanup

Decision:

- Added `policy/harness-review.md` to the Core `AGENTS.md` fresh-agent read order as an incubating operating-layer peer review boundary.
- Added `policy/harness-review.md` to `wiki/index.md` Active Policy.
- Kept `philosophy.md` as inherited source/provenance rather than adding it to read order or Active Policy.

Reason:

- `policy/harness-review.md` already existed and was referenced by Core policy, but fresh agents could miss it when editing operating-layer files.
- `philosophy.md` explicitly declares itself inherited source, not active operating policy; its active invariants are already extracted into `AGENTS.md`, `SOUL.md`, and `wiki/pages/hermes-operating-model.md`.
- The cleanup preserves the philosophy boundary: concrete policy is discoverable, long philosophy is not turned into working instructions.

Verification:

- Human gate approved in-session on 2026-05-11.
- Claude CLI review checked the philosophy/essence boundary and recommended excluding `philosophy.md` from read order while indexing `harness-review.md`.
- `AGENTS.md` remains 35 lines after the read-order addition.
