#!/usr/bin/env python3
"""Safely replace the generated section of the LeetCode weekly plan."""

import argparse
import re
import shutil
import subprocess
import sys


START_MARKER = "<!-- leetcode-readiness:start -->"
END_MARKER = "<!-- leetcode-readiness:end -->"
DEFAULT_PATH = "Notes/CP/LeetCode Weekly Plan.md"
CLI_NOISE = (
    re.compile(r"^\d{4}-\d{2}-\d{2} .* Loading updated app package "),
    re.compile(r"^Your Obsidian installer is out of date\."),
)


def merge_generated_section(existing: str, generated: str) -> str:
    generated = generated.strip()
    if not generated:
        raise ValueError("generated section is empty")
    if START_MARKER in generated or END_MARKER in generated:
        raise ValueError("generated content must not contain section markers")

    block = f"{START_MARKER}\n{generated}\n{END_MARKER}"
    starts = existing.count(START_MARKER)
    ends = existing.count(END_MARKER)

    if starts == ends == 0:
        prefix = existing.rstrip()
        if not prefix:
            prefix = "# LeetCode Weekly Plan"
        return f"{prefix}\n\n{block}\n"

    if starts != 1 or ends != 1:
        raise ValueError("weekly plan has malformed or duplicate generated markers")

    start = existing.index(START_MARKER)
    end = existing.index(END_MARKER)
    if start > end:
        raise ValueError("weekly plan end marker appears before start marker")

    end += len(END_MARKER)
    return existing[:start] + block + existing[end:]


def clean_cli_output(output: str) -> str:
    return "\n".join(
        line for line in output.splitlines() if not any(pattern.match(line) for pattern in CLI_NOISE)
    )


def run_obsidian(executable: str, *args: str) -> str:
    result = subprocess.run(
        [executable, *args],
        capture_output=True,
        text=True,
        check=False,
    )
    stdout = clean_cli_output(result.stdout)
    stderr = clean_cli_output(result.stderr)
    error = "\n".join(part for part in (stdout, stderr) if part).strip()

    if result.returncode != 0 or stdout.startswith("Error:") or stderr.startswith("Error:"):
        raise RuntimeError(error or f"obsidian exited with status {result.returncode}")
    return stdout


def read_note(executable: str, vault: str, path: str) -> str:
    try:
        return run_obsidian(executable, "read", f"vault={vault}", f"path={path}")
    except RuntimeError as error:
        if "not found" in str(error).lower():
            return ""
        raise


def encode_content(content: str) -> str:
    return content.replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t")


def update_note(executable: str, vault: str, path: str, generated: str) -> None:
    updated = merge_generated_section(read_note(executable, vault, path), generated)
    run_obsidian(
        executable,
        "create",
        f"vault={vault}",
        f"path={path}",
        f"content={encode_content(updated)}",
        "overwrite",
    )

    saved = read_note(executable, vault, path)
    if saved.rstrip("\n") != updated.rstrip("\n"):
        raise RuntimeError("Obsidian verification failed; saved note does not match requested update")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", default="State")
    parser.add_argument("--path", default=DEFAULT_PATH)
    args = parser.parse_args()

    executable = shutil.which("obsidian")
    if not executable:
        parser.error("obsidian CLI is not installed or not on PATH")

    try:
        update_note(executable, args.vault, args.path, sys.stdin.read())
    except (RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"updated {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
