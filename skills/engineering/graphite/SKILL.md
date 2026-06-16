---
name: graphite
description: Split branch work into a logical Graphite PR stack. Use when the user invokes /graphite.
disable-model-invocation: true
---

Split the work in /branch into a logical stack of PRs using the Graphite CLI. Order the stack so that lower PRs contain the changes least likely to need revision, minimizing merge conflicts when I make edits to PRs higher in the stack.
