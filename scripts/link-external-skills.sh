#!/usr/bin/env bash
set -euo pipefail
# Catalogs are now one directory. This legacy entrypoint only checks it.
exec python3 "${AGENTIC_HOME:-$HOME/.agentic}/repos/skills/scripts/agentic" doctor
