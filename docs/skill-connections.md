# Skill connections

This file is the source of truth for completion-time skill suggestions and
runtime skill-usage disclosures.

## Completion suggestions

When a source skill below reaches an intentional final result, append:

```markdown
**Suggested next:**
- `/target` — [one short reason tied to the result that just completed]
```

An intentional final result includes a valid no-op and a user-requested early
result, such as an interview scorecard. An error, blocked run, abandoned flow,
or request for missing input is incomplete and gets no suggestions.

Include every target configured for the source. Generate each reason from the
completed result rather than using a fixed description. Suggestions are manual:
the user decides whether to invoke one. If the source actually invoked a target
during the same run, omit that target from the suggestions.

Only the top-level skill that owns the user's current workflow emits completion
suggestions. When a source skill runs as a child inside another skill, keep its
standalone suggestion block internal; the parent owns the visible completion
output and its own suggestions. Borrowing selected instructions without invoking
the full child workflow does not trigger the child's suggestions either.

**Router handoff:** `/learn` transfers workflow ownership to the selected
learning modality. That modality emits its configured completion suggestions;
`/learn` emits none and does not duplicate them.

| Source | Suggest |
| --- | --- |
| `clarify` | `coherent`, `unscramble`, `pragmatic`, `mentor` |
| `socratic-teacher` | `dunning-krueger` |
| `illustrate` | `coherent`, `socratic-teacher`, `lab`, `exam`, `dunning-krueger` |
| `lab` | `dunning-krueger` |
| `exam` | `dunning-krueger` |
| `unscramble` | `confounder`, `ramble` |
| `scope-creep` | `confounder`, `coherent` |
| `blog` | `post`, `youtube` |
| `todo-triage` | `focus` |
| `apset` | `research-gap`, `research-advisor` |
| `research-advisor` | `dunning-krueger` |
| `momtest` | `ramble`, `linear` |
| `pragmatic` | `linear` |

### Conditional suggestions

When `dunning-krueger` stops because the supplied context has insufficient
user-authored evidence, suggest `clarify`, `coherent`, and `learn`. A completed
assessment does not add this block.

## Runtime disclosures

When a parent skill actually invokes another skill or starts borrowing another
skill's instructions, say so at that moment in one short, natural sentence. Name
the relationship and why it is being used, for example:

> Using `/clarify`'s interview style here to structure the APSET questions.

Disclose only relationships used in the current run. Mere references,
recommendations, installed tools, shared plain documents, and configured but
unused dependencies are not disclosures. Do not repeat disclosures in the
completion suggestion block.
