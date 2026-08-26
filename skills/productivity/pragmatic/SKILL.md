---
name: pragmatic
description: >
  Use when a non-trivial build needs a two-person reality check before
  implementation: limited bandwidth, rough deadline, scope check, technical
  risk, business value, MVP sizing, or pragmatic build brief.
---

# Pragmatic

## Consequential advice

Before offering a cut, phase, or course of action, follow the `Advice gate` in
`dissenter`. Do not select a winner; wait for the user's choice.
When the gate applies, first say that you are using `/dissenter` and why.

Clarify a build until it is realistic for two people with limited bandwidth:
`clarify`, constrained by scarce founder time.

Before the interview begins, say that you are using `/clarify`'s interview
discipline with a founder-bandwidth constraint.

<HARD-GATE>
Do NOT change files, scaffold, commit, or produce an implementation plan. Stop
after build brief and implementation prompt.
</HARD-GATE>

## Checklist

1. **Explore context** - read docs, files, and recent commits when they answer
   feasibility.
2. **Scope check** - if the request spans independent subsystems, flag it and
   help the user pick one slice.
3. **Deadline check** - accept rough deadlines like "two weeks from now"; ask
   for founder-hours only if the mismatch is unclear.
4. **Interview one question at a time** - clarify scope, risk, value, non-goals,
   and "useful enough."
5. **Reality check** - if the idea is too large or risky, state the mismatch and
   let the user choose whether to cut, phase, or proceed.
6. **Deliver artifacts** - brief first, copy-paste prompt second.

## Question Focus

| Axis | Ask until clear |
|---|---|
| **Scope discipline** | What can be cut without killing the value? What is the smallest useful slice? |
| **Technical risk** | What unknowns, integrations, data, deploy, or maintenance dominate? |
| **Business value** | Why is this worth scarce founder time now? What assumption must be true for the work to matter? |
| **Deadline realism** | What date or event constrains the work? What remains useful if the full idea misses it? |

## Question Discipline

- Ask one question per message.
- Prefer multiple choice when it speeds the answer.
- Explore the repo instead of asking when the answer is in files.
- Use rough time boxes unless precision changes the recommendation.
- When the user is stuck, offer a short recommended cut, then continue asking.
- Do not issue a hard "do not build" verdict unless the user asks for one.

## Final Artifact

Return:

````md
## Pragmatic Build Brief

**Build:** [the agreed slice]

**Why now:** [business value and urgency]

**Deadline:** [rough deadline or time box]

**Smallest useful slice:** [the first valuable version]

**Scope cuts:** [what is deliberately not being built]

**Technical risks:** [unknowns, integrations, data, deploy, maintenance]

**Value assumption:** [what must be true for this to be worth doing]

**Reality check:** [fit/mismatch for two people with limited bandwidth]

**First milestone:** [smallest checkpoint that proves progress]

```text
[Self-contained implementation prompt with what to build, why, constraints,
success criteria, non-goals, risks, and unresolved questions.]
```
````

Stop after the brief and prompt unless the user explicitly asks to implement.
Then append the `pragmatic` completion suggestions from
[skill connections](../../../docs/skill-connections.md).

## Common Mistakes

- Treating the idea as approved: re-test scope, risk, and value.
- Asking generic questions: ask what changes cuts, risk, or deadline fit.
- Forcing exact hours: rough deadlines are enough unless capacity changes the
  decision.
- Silently shrinking the idea: name the mismatch and let the user choose.
