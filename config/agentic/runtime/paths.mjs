import { mkdirSync } from "node:fs";
import { homedir } from "node:os";
import { join, resolve, relative, isAbsolute } from "node:path";
import { randomUUID } from "node:crypto";

export function agenticRunFile(skill, filename) {
  const root = process.env.AGENTIC_HOME || join(homedir(), ".agentic");
  const runs = resolve(root, "state", "runs", skill);
  const directory = process.env.AGENTIC_RUN_DIR || join(runs, randomUUID());
  const within = relative(runs, resolve(directory));
  if (within.startsWith("..") || isAbsolute(within)) {
    throw new Error("AGENTIC_RUN_DIR must be inside " + runs);
  }
  mkdirSync(directory, { recursive: true });
  return join(directory, filename);
}
