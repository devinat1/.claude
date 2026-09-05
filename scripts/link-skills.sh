#!/usr/bin/env bash
set -euo pipefail

# Refreshes generated skill metadata, then links owned skills in this repository
# to Claude and Codex. Only scans category buckets and owned skill names.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DESTS=("$HOME/.claude/skills" "$HOME/.codex/skills")
BUCKETS=(learning productivity writing setup)
MOVED_OR_REMOVED=(break-it lab-creator update-blog-on-leetcode)

"$REPO/scripts/generate-skill-metadata.py"

for dest in "${DESTS[@]}"; do
  if [ -L "$dest" ]; then
    resolved="$(readlink -f "$dest")"
    case "$resolved" in
      "$REPO"|"$REPO"/*)
        echo "error: $dest is a symlink into this repo ($resolved)." >&2
        exit 1
        ;;
    esac
  fi
  mkdir -p "$dest"
done

# Remove only stale links previously created from this repository. Links to
# the engineering repository remain intact.
for dest in "${DESTS[@]}"; do
  for name in "${MOVED_OR_REMOVED[@]}"; do
    target="$dest/$name"
    if [ -L "$target" ]; then
      source="$(readlink "$target")"
      case "$source" in
        "$REPO/skills/"*)
          unlink "$target"
          echo "unlinked stale $target"
          ;;
      esac
    fi
  done
done

# Refuse to replace real directories or files; they may be third-party installs.
for bucket in "${BUCKETS[@]}"; do
  for skill_md in "$REPO/skills/$bucket"/*/SKILL.md; do
    name="$(basename "$(dirname "$skill_md")")"
    for dest in "${DESTS[@]}"; do
      target="$dest/$name"
      if [ -e "$target" ] && [ ! -L "$target" ]; then
        echo "error: refusing to replace $target; move it and re-run." >&2
        exit 1
      fi
    done
  done
done

for bucket in "${BUCKETS[@]}"; do
  bucket_dir="$REPO/skills/$bucket"
  [ -d "$bucket_dir" ] || continue

  find "$bucket_dir" -name SKILL.md -print0 |
  while IFS= read -r -d '' skill_md; do
    src="$(dirname "$skill_md")"
    name="$(basename "$src")"
    for dest in "${DESTS[@]}"; do
      target="$dest/$name"
      ln -sfn "$src" "$target"
      echo "linked $target -> $src"
    done
  done
done
