#!/usr/bin/env bash
set -euo pipefail

# Links owned skills in this repository to ~/.claude/skills for Claude Code.
# Only scans category buckets — does not touch third-party symlinks at skills/<name>.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/.claude/skills"
BUCKETS=(learning engineering interview productivity writing setup)

if [ -L "$DEST" ]; then
  resolved="$(readlink -f "$DEST")"
  case "$resolved" in
    "$REPO"|"$REPO"/*)
      echo "error: $DEST is a symlink into this repo ($resolved)." >&2
      echo "Remove it (rm \"$DEST\") and re-run; the script will recreate it as a real dir." >&2
      exit 1
      ;;
  esac
fi

mkdir -p "$DEST"

for bucket in "${BUCKETS[@]}"; do
  bucket_dir="$REPO/skills/$bucket"
  [ -d "$bucket_dir" ] || continue

  find "$bucket_dir" -name SKILL.md -print0 |
  while IFS= read -r -d '' skill_md; do
    src="$(dirname "$skill_md")"
    name="$(basename "$src")"
    target="$DEST/$name"

    if [ -e "$target" ] && [ ! -L "$target" ]; then
      rm -rf "$target"
    fi

    ln -sfn "$src" "$target"
    echo "linked $name -> $src"
  done
done
