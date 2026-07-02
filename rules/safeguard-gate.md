# Safeguard gate

Before any **non-trivial feature, build, or refactor**, invoke the
`safeguard` skill via the **Skill tool** as your **first action**. Do not
Read the skill file — use the Skill tool.

**Do not** write code, scaffold, edit files, or produce implementation plans
until safeguard completes (Build Brief delivered) or the user opts out.

**Skip safeguard** when the user says **skip safeguard**, already provided a
detailed plan/issue, or is addressing bounded PR review comments.

**Route to `clarify`** for clear bug fixes with obvious scope.

**When in doubt:** prefer `clarify` for bugs; prefer `safeguard` when the
change adds behavior, crosses services/repos, or reshapes architecture.

Project repos may also define `.claude/rules/safeguard-gate.md`,
`.cursor/rules/safeguard-gate.mdc`, or `AGENTS.md` § Before building — follow
those in addition to this user rule.
