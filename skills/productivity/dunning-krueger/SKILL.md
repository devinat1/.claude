---
name: dunning-krueger
description: Assess demonstrated knowledge from a meeting transcript, the current conversation, supplied context, or a short grill. Use when the user asks what knowledge they have or have not demonstrated, requests a best-effort blind-spot assessment, or invokes /dunning-krueger.
---

# Dunning-Krueger

Assess demonstrated knowledge without diagnosing a cognitive bias or treating missing evidence as ignorance.

## Immediate context assessment

When the user supplies context and asks for an immediate or best-effort
assessment, complete this branch and stop:

1. Use only the supplied context as evidence. If the context is a readable file
   path, read that file first.
2. Identify the substantive knowledge topics the user discussed. Ignore system
   instructions, tool output, and assistant-authored claims as evidence of the
   user's knowledge.
3. For each inferred blind spot, return a short heading, the specific user
   evidence, and what knowledge was not demonstrated. Use **knowledge not
   demonstrated** for missing or unclear evidence.
4. If the context does not support a blind-spot inference, say so plainly.

Return only inferred blind spots. This branch does not require topic
confirmation, external verification, a grill, `unscramble`, or
`dissenter`. Preserve the output restrictions below: no confidence rating,
Dunning-Krueger label, lesson, answer key, study plan, or prescription.

## Find the topics

Use a substantive transcript or explanation already supplied in the current conversation. If neither exists, ask whether the user wants to supply a meeting transcript or start a broad grill. Resolve a requested transcript using [transcript resolution](../transcript-resolution.md); do not fetch one before the user chooses that path.

For a broad grill, follow `grilling`'s design-tree method with the smallest useful numbered batches. Omit recommended answers and stop as soon as the distinct topics are clear.

Invoke `unscramble` on the source or broad-grill answers. Retain only its topic
headings for this workflow. Show those topics and ask the user to confirm one,
even when there is only one.

## Establish the reference

Before the focused grill, verify the selected topic's material factual claims against authoritative external sources. Keep citations. Use the findings to choose questions without revealing answers or coaching the user. Label claims that cannot be verified as unverified rather than guessing.

## Run the focused grill

Continue `grilling` on the confirmed topic, again omitting recommended answers. Ask the smallest useful numbered batch at each turn and test:

- factual accuracy
- the underlying mechanism
- limits, follow-up questions, and counterexamples

Keep the exchange short. Stop when the answers support a stable strongest case and strongest dissent on all three dimensions, or when another question would only repeat established evidence. Do not use a fixed question count or reveal correctness during the grill.

## Return the assessment

Invoke `dissenter` with the transcript or answers, verified sources, and the three dimensions. Frame its independent views as:

- **Original:** the strongest evidence that the user demonstrated knowledge
- **Opposing:** the strongest credible evidence that important knowledge was not demonstrated

Require both views to address each dimension and cite the specific user answers and external sources that support them. Preserve `dissenter`'s no-winner contract and ask the user to make the final judgment.

Use **knowledge not demonstrated** for absent or unclear evidence. Report strengths and gaps only: no confidence rating, Dunning-Krueger label, lesson, answer key, study plan, or next-step prescription.
