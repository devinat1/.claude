# Lab creator example syntax

Use this as the shape reference for labs created by the lab-creator skill. A generated lab has one target concept, visible tests, a learner-owned answer file, and a hidden solution file.

## Generated directory layout

```text
~/.claude/process-exercises/<repo>/YYYY-MM-DD-<concept-slug>/
  EXAMPLE.md
  answer.<ext>        # or answer.md for conceptual labs
  test_answer.<ext>   # or tests.md for conceptual labs
  SOLUTION.<ext>      # never shown before grading
```

`EXAMPLE.md` is public. It teaches the syntax of the lab files and how to read the tests. It must not contain the answer, hidden grading notes, or hints that make the exercise trivial.

## Code lab shape

`answer.<ext>` contains only the learner-facing starter code.

```python
def normalize_topic(raw: str) -> str:
    """Return a filesystem-safe slug for a topic name."""
    raise NotImplementedError("Write your solution here")
```

`test_answer.<ext>` contains runnable tests. Use clear case names and normal assertions.

```python
from answer import normalize_topic


def test_lowercases_and_replaces_spaces():
    assert normalize_topic("Signal Handling") == "signal-handling"


def test_strips_extra_separators():
    assert normalize_topic("  nats / jetstream  ") == "nats-jetstream"
```

`SOLUTION.<ext>` contains a complete passing implementation. Do not print, open, or summarize it before grading.

## Conceptual lab shape

`answer.md` gives the learner a place to respond.

```markdown
# Answer

## Scenario 1

Write your answer here.

## Scenario 2

Write your answer here.
```

`tests.md` contains numbered scenarios. Each one has a checkable `Expected` block.

```markdown
# Tests

## Scenario 1: Worker receives SIGTERM during an activity

Explain what should happen to in-flight work and shutdown timing.

Expected:
- Mentions graceful shutdown before process exit.
- Distinguishes activity cancellation from immediate process death.
- Names the consequence of exceeding the shutdown grace period.

## Scenario 2: Client sends duplicate signals

Explain how the workflow should keep state consistent.

Expected:
- Mentions idempotency or deduplication.
- Explains where the durable state lives.
- Avoids relying on process-local memory.
```

`SOLUTION.md` contains the model answer and scoring notes. Keep it hidden until the grader finishes the real grade and calibration check.

## Case count and naming

- Use 2-4 cases for most labs.
- Name each case after the behavior it checks.
- Prefer one concept per case.
- Include edge cases only when they teach the target concept.

## Good Expected blocks

Good `Expected` blocks are observable:

```markdown
Expected:
- Identifies the operation that must be idempotent.
- Explains why retry can run the operation more than once.
- Gives one concrete deduplication key.
```

Weak `Expected` blocks are vague:

```markdown
Expected:
- Understands retries.
- Gives a good answer.
```

## Anti-patterns

- Do not create multiple labs in one directory.
- Do not include the solution in public files.
- Do not grade inside the lab-creator skill.
- Do not write uncheckable expectations like "has a deep understanding".
- Do not ask for a predicted score. The grader skill handles calibration.
