#!/usr/bin/env bash
set -euo pipefail

# Symlinks third-party skills from ~/.agents/skills into ~/.claude/skills for Claude Code.
# Run after: npx skills@latest add mattpocock/skills (and other external sources).

REPO="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS_SKILLS="$HOME/.agents/skills"
CLAUDE_SKILLS="$HOME/.claude/skills"

EXTERNAL_SKILLS=(
  caveman
  design-an-interface
  diagnose
  find-skills
  grill-me
  grill-with-docs
  handoff
  improve-codebase-architecture
  postiz
  prototype
  setup-matt-pocock-skills
  tdd
  teach
  to-issues
  to-prd
  triage
  write-a-skill
  zoom-out
)

mkdir -p "$CLAUDE_SKILLS" "$REPO/skills"

for name in "${EXTERNAL_SKILLS[@]}"; do
  src="$AGENTS_SKILLS/$name"
  if [ ! -f "$src/SKILL.md" ]; then
    echo "skip $name (not installed in $AGENTS_SKILLS)"
    continue
  fi

  repo_link="$REPO/skills/$name"
  claude_link="$CLAUDE_SKILLS/$name"

  ln -sfn "$src" "$repo_link"
  ln -sfn "$src" "$claude_link"
  echo "linked $name -> $src"
done

echo ""
echo "Install missing skills with:"
echo "  npx skills@latest add mattpocock/skills"
