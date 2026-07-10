---
name: pre-pr-review
description: |
  Use after a feature is complete and before opening a PR in any sibling.
  Repo-specific lint only — then runs ponytail-review, then loops
  thermo-nuclear-code-quality-review (via the loop skill) until the
  maintainability audit comes back clean.
  Triggers: feature complete, user says "open a PR", "pre-PR check",
  "review my changes", or before invoking gh pr create.
---

# Pre-PR review (repo-specific)

You are doing a final pre-PR check on changes about to be opened as a
pull request. The checklist part of this skill covers **repo-specific
invariants only**. Generic code-quality review (clarity, naming,
duplication, error handling, etc.) is the job of the
`thermo-nuclear-code-quality-review` skill. Complexity-only review is the
job of the `ponytail-review` skill. After this checklist report is
complete, **immediately run** `ponytail-review` on the same branch changes,
then **immediately drive** the `thermo-nuclear-code-quality-review` skill
on those changes **in a loop until it comes back clean** — see § Run the
complexity review and § Loop the maintainability audit. After the
thermo-nuclear output, always finish with the `Human attention map` section
— see § Human attention map. Do not stop after the pre-PR report unless
pre-PR findings are blocking (FAIL on repo-wide invariants or
verification); even then, still print the final `Human attention map`
section after noting that the ponytail-review pass and thermo-nuclear loop
were skipped.

**Behavior:** report findings, do not auto-fix. List violations with
file:line citations.

## Repo-wide invariants

These apply to any PR in any Syndeo-AI repo. Source of truth: top-level
`AGENTS.md` § Hard rules.

- No direct push to `main` in any repo. Branch + PR.
- Linear history required (rebase, no merge commits).
- A schema change is a backend-only PR; the frontend consumer PR lands
  separately, after.

## Per-sibling lint

Determine which siblings the PR touches (`git diff --name-only <base>`
and inspect the path prefixes). Run the relevant sub-checklists:

### backend/

- `errs.*` constructors only outside `internal/errs/` and tests. No
  direct `fmt.Errorf` or `errors.New` at call sites. Source:
  `backend/AGENTS.md` § Error handling.
- All tests use the table-driven pattern with `name`/`args`/`want`.
  Canonical shape: `internal/logger/logger_test.go`. Source:
  `backend/AGENTS.md` § Tests.
- `internal/logger` is the only sanctioned logger. No `fmt.Print*` or
  stdlib `log` for logging.
- Any new file under `backend/migrations/` passes
  `npx squawk-cli -c .squawk.toml migrations/<file>.sql`. CI enforces
  this; a clean local run avoids surprises.

### frontend/

- JSX uses only `<div>` and `<span>`. No semantic HTML (`<p>`, `<h1>`,
  etc.). Source: `frontend/AGENTS.md` § JSX.
- Conditionals use ternary, not `&&`.
- Tailwind only — no inline styles or style objects.
- `const` only, never `let`. No mutations.
- Named params, not positional.
- `try/catch` over `.then/.catch`.
- `Item[]` not `Array<Item>`. `arr.length === 0` not `!arr`.
- No non-null assertions (`x!`); use `x as NonNullable<typeof x>`.
- No `../` relative imports — use `@resyndeo/web/*` or
  `@resyndeo/types/...`. Same-dir `./foo` ok.
- Don't fetch inside components — use a helper.
- Release-please config intact: `"component": "web"` and
  `"include-component-in-tag": true` in `release-please-config.json`.
  Changing either silently switches the tag pattern and orphans every
  prior release PR. Source: `frontend/AGENTS.md` § Releases.
- `bunx tsc --noEmit` is clean.
- `bun run quality:fallow` passes — the Fallow gate (dead-code, health,
  dupes, security). CI enforces this (`.github/workflows/fallow.yml`); a
  clean local run avoids surprises. An unavoidable hit is suppressed
  inline with `// fallow-ignore-next-line <rule>`, not by loosening the
  command.

### gitops/

- No real secrets in the repo. The in-repo `values.yaml` files contain
  non-secret config only; secrets layer in via the gitignored
  `~/.config/resyndeo-gitops/values.secret.yaml`. Source: `gitops/AGENTS.md`
  § Hard rules.
- `helm-eso-common` includes use `{{ include` (not `{{- include`) —
  PR #184 footgun. Source: `gitops/AGENTS.md` § Secret flow.
- No direct push to `main`, `dev`, or `prod` (branch protection
  enforces, but call it out in review). Source: `gitops/AGENTS.md`
  § Hard rules.
- Self-managed `helm-argocd/` changes have been tested locally with
  `helm template` before commit.

### infra/, terminal-ui/

Defer to that sibling's `AGENTS.md` (now auto-loaded once `CLAUDE.md`
is in place per the AGENTS.md context-loading framework spec).

## Cross-cutting verification

Before reporting clean:

- `make test` from the super-repo root passes.
- If the PR touches frontend, `cd frontend && bunx tsc --noEmit` and
  `cd frontend && bun run quality:fallow` are both clean.

## Run the complexity review

Once the pre-PR checklist passes, invoke `ponytail-review` on the same
branch diff and print its normal output unchanged. This pass is report-only:
do not auto-fix its findings here, and do not block the
`thermo-nuclear-code-quality-review` loop on them.

If the pre-PR report has blocking FAILs on repo-wide invariants or
verification steps, skip both `ponytail-review` and the thermo-nuclear
loop, then still print the final `Human attention map`.

## Loop the maintainability audit until clean

`thermo-nuclear-code-quality-review` is not a one-shot. Once the pre-PR
checklist and `ponytail-review` pass have run, drive the audit with the
`loop` skill in self-paced mode (`/loop` with no interval) so that each
iteration:

1. Re-runs `thermo-nuclear-code-quality-review` on the current branch
   changes.
2. Addresses **every** finding it surfaces — fix the code, or, for a
   finding you are deliberately waiving, record the explicit
   justification the audit's approval bar demands.
3. Repeats.

End the loop only when a full thermo-nuclear pass reports **zero**
remaining code-quality issues. Do not open the PR while any thermo-nuclear
finding is still unresolved — keep looping until the audit comes back
clean.

Regardless of the thermo-nuclear result, the next and final output must be
the `Human attention map`. If the audit has unresolved findings because
the loop could not complete cleanly, print the human attention map anyway;
it is a separate risk signal, not a code-quality gate.

## Human attention map

At the very end of `pre-pr-review`, after the thermo-nuclear review output
when that step can run, invoke an explore agent to inspect the PR changes
and produce a required Markdown section titled exactly:

```markdown
## Human attention map
```

Purpose: help the PR author and GitHub reviewer distinguish ordinary
AI-generated edits from changed code sections that require careful human
review because mistakes could cause production outages, data loss or
corruption, security/auth regressions, billing or financial mistakes,
irreversible infrastructure changes, or similarly severe failures.

This report is required output only. It does not block PR creation or
merge by itself.

### Explore-agent scope

Give the explore agent a narrow brief:

- Review the branch diff against the PR base.
- Focus on changed files and enough nearby surrounding code to understand
  the changed section.
- Include enclosing function/component/resource context when useful.
- Do not broaden to the whole repo by default.
- Let the LLM make the final judgment about whether a changed section is
  critical.
- Flag only sections judged to be truly critical. Avoid "possible risk"
  or low-confidence noise.

### Report format

Always print the section.

If critical sections are found, use pasteable Markdown:

```markdown
## Human attention map

- `<file>` — `<function/component/resource/area>`, changed lines `<lines>`
  - Nearby context: `<short surrounding code snippet or enclosing context
    summary>`
  - Why this is critical: `<specific severe consequence>`
  - Human review focus: `<what the reviewer should inspect carefully>`
```

If no critical sections are identified:

```markdown
## Human attention map

No critical sections identified.
```

If the explore agent cannot inspect everything it needs to review, fail
closed without fake precision:

```markdown
## Human attention map

Incomplete: the explore agent could not inspect enough changed files and
nearby context to classify the critical sections confidently. The diff is
too large or insufficiently inspectable for this pass, so a human should
review the changed areas directly.
```

Do not mark every changed file as critical by default when exploration is
incomplete. State the incompleteness plainly.

## Output

Produce a checklist-style report:

```
## Pre-PR review

### Repo-wide invariants
- [PASS|FAIL] <invariant> — <evidence or finding>
...

### Per-sibling: backend/
...

### Verification
- [PASS|FAIL] make test — <evidence>
...

### Next step (automatic)
Running `ponytail-review`, then looping `thermo-nuclear-code-quality-review`
(via the `loop` skill) until the maintainability audit comes back clean.

## Human attention map
<critical sections, "No critical sections identified.", or incomplete notice>
```

Do not modify any files during the pre-PR checklist itself. If a violation
is fixable in one line, suggest the fix inline; do not apply it. Then,
unless this report has blocking FAILs on repo-wide invariants or
verification steps, run `ponytail-review` (§ Run the complexity review),
then hand off to the looped maintainability audit (§ Loop the
maintainability audit) without waiting for user confirmation — keep looping
`thermo-nuclear-code-quality-review` until it comes back clean. After the
thermo-nuclear output, or after noting why later review steps were skipped,
print the final `Human attention map`.
