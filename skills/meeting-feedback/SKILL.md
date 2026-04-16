---
name: meeting-feedback
description: Use when the user wants to evaluate their communication performance in a meeting. Fetches notes from Granola MCP, evaluates across 12 dimensions with dual-lens critique (layperson + expert), and saves a scorecard. Trigger on /meeting-feedback or when user asks for meeting feedback or review.
---

# Meeting Feedback

Evaluate communication performance in meetings using notes and transcripts from Granola. Deliver brutal, honest feedback across 12 dimensions from two perspectives: a confused non-technical stakeholder and a ruthless domain expert. No softening. No excuses.

## Step 1: Fetch Meeting Data

Use the Granola MCP tools to fetch meeting data.

- **No argument provided:** Fetch the most recent meeting's notes and transcript.
- **Argument provided:** Search for a meeting matching the argument (title or keyword) and fetch its notes and transcript.

You need both the **transcript** (what was actually said) and the **summary/notes** (structured takeaways). The transcript is the primary source for evaluation — it contains the raw evidence. The summary helps you understand what the meeting was about.

If the transcript is not available (e.g., free plan limitation), evaluate based on the notes/summary alone but note at the top of the scorecard: "Evaluated from summary only — transcript unavailable. Scores for Expressiveness and Conciseness may be less precise."

## Step 2: Infer Meeting Context

From the meeting data, infer:

- **Meeting type:** standup, demo, architecture review, strategy/planning, 1:1, customer call, sprint review, retrospective, brainstorm, or other
- **User's role:** presenting, facilitating, participating, or defending a decision
- **Topic familiarity:** home turf, comfortable, stretching, or unfamiliar — inferred from the user's speech patterns (confidence, depth of explanation, hedging frequency, use of qualifiers)

This context is displayed in the scorecard header. It does NOT reduce evaluation intensity. Both lenses are always at full weight.

## Step 3: Evaluate All 12 Dimensions

Evaluate the user's communication across all 12 dimensions below. For EVERY dimension:

1. Assign a score: red, yellow, or green
2. Write a one-liner critique — brutal, specific, no hedging
3. Pull a transcript excerpt as evidence — quote the user's actual words with timestamp if available

**Scoring definitions:**
- **Red** — You failed at this. A non-technical stakeholder was lost, or an expert would have called you out. Needs immediate work.
- **Yellow** — You were passable but left meat on the bone. You got by, but a stronger communicator would have done it better.
- **Green** — You nailed it. Nothing to critique here for this meeting.

**Be harsh. Default to yellow unless the evidence clearly supports green. Green means genuinely excellent, not "fine." Red means a real problem, not a nitpick. When in doubt between two colors, pick the harsher one.**

### Category 1: Communication Craft

How you say it, regardless of audience.

**Expressiveness — Word Choice**
Did you use precise, vivid vocabulary or fall back on vague filler ("kind of", "basically", "stuff", "like", "sort of")? The brutal question: "Did you use the *right* word, or the *easy* word?"

**Expressiveness — Conviction**
Did you own your position or hedge? Look for: "I think maybe", "probably", "I'm not sure but", "we could potentially", "it might be". Confidence without arrogance vs. uncertainty disguised as humility. The brutal question: "Did you sound like someone who knows, or someone who hopes they're right?"

**Expressiveness — Narrative**
Did your points have structure — setup, tension, resolution — or were they a flat list of facts? Did you build to a conclusion or just stop? The brutal question: "If someone tuned in mid-sentence, could they tell where you were going?"

**Conciseness**
Signal-to-noise ratio. Did you make your point in the fewest words needed? Look for: circular reasoning, restating the same point, verbal run-on sentences, unnecessary preamble. The brutal question: "How many of your words could be deleted without losing meaning?"

### Category 2: Layperson Lens

Could a non-technical stakeholder follow this?

**Jargon Accessibility**
Did you use technical terms without explaining them? Did you assume shared vocabulary that doesn't exist? Look for: acronyms without expansion, technical concepts dropped without context, domain-specific shorthand. The brutal question: "Would your VP of Sales know what you just said?"

**Analogy & Metaphor Quality**
When you translated technical concepts, was the metaphor accurate and illuminating — or misleading, oversimplified, or patronizing? Did you even attempt to translate, or did you just barrel through in technical language? The brutal question: "Did your analogy make them smarter, or just make them nod?"

**So-What Clarity**
Did you connect technical detail to business impact? Does the listener know *why they should care*? Or did you present implementation details without ever saying what it means for the product, the customer, or the timeline? The brutal question: "If they forgot everything else, would they still know what matters and why?"

**Actionability**
Did you leave them knowing what happens next, what you need from them, or what the decision is? Or did you just... stop talking? The brutal question: "Did you end with a clear ask, or just... stop talking?"

### Category 3: Expert Lens

Would a domain expert respect this?

**Technical Accuracy**
Are the facts, numbers, and claims correct? Did you oversimplify to the point of being wrong? Did you make claims you can't back up? The brutal question: "Would an expert in the room wince at anything you said?"

**Depth vs. Hand-Waving**
Did you demonstrate genuine understanding or pattern-match the right buzzwords without substance? Could you go one level deeper if challenged? The brutal question: "If someone asked 'why?' one more time, would you have an answer?"

**Rigor of Reasoning**
Is your logic sound? Did you skip steps, make leaps, or present correlation as causation? Did you draw conclusions your evidence doesn't support? The brutal question: "Could someone poke a hole in your argument in under 10 seconds?"

**Nuance & Edge-Case Awareness**
Did you acknowledge complexity, tradeoffs, and limitations — or did you present everything as clean and simple? Did you show awareness of where your solution breaks? The brutal question: "Did you show you know where this breaks, or did you pretend it doesn't?"

## Step 4: Render the Scorecard

Output the scorecard in this exact format. Use the emoji indicators for color: 🟢 (green), 🟡 (yellow), 🔴 (red).

```
Meeting: [title]
Type: [inferred meeting type]
Your Role: [presenting / facilitating / participating / defending]
Topic Familiarity: [home turf / comfortable / stretching / unfamiliar]

── Communication Craft ──────────────────────
Expressiveness — Word Choice:    [emoji]  "[one-liner critique]"
                                           📎 "[transcript excerpt]"
Expressiveness — Conviction:     [emoji]  "[one-liner critique]"
                                           📎 "[transcript excerpt]"
Expressiveness — Narrative:      [emoji]  "[one-liner critique]"
                                           📎 "[transcript excerpt]"
Conciseness:                     [emoji]  "[one-liner critique]"
                                           📎 "[transcript excerpt]"

── Layperson Lens ───────────────────────────
Jargon Accessibility:            [emoji]  "[one-liner critique]"
                                           📎 "[transcript excerpt]"
Analogy & Metaphor Quality:      [emoji]  "[one-liner critique]"
                                           📎 "[transcript excerpt]"
So-What Clarity:                 [emoji]  "[one-liner critique]"
                                           📎 "[transcript excerpt]"
Actionability:                   [emoji]  "[one-liner critique]"
                                           📎 "[transcript excerpt]"

── Expert Lens ──────────────────────────────
Technical Accuracy:              [emoji]  "[one-liner critique]"
                                           📎 "[transcript excerpt]"
Depth vs. Hand-Waving:           [emoji]  "[one-liner critique]"
                                           📎 "[transcript excerpt]"
Rigor of Reasoning:              [emoji]  "[one-liner critique]"
                                           📎 "[transcript excerpt]"
Nuance & Edge-Case Awareness:    [emoji]  "[one-liner critique]"
                                           📎 "[transcript excerpt]"

── Summary ──────────────────────────────────
Biggest strength: [one sentence]
Most urgent fix:  [one sentence]
```

## Step 5: Save the Scorecard

Save the scorecard to `feedback-history/` in the current working directory:

- Filename: `feedback-history/YYYY-MM-DD-<meeting-title-slug>.md`
- Slugify the meeting title: lowercase, replace spaces with hyphens, remove special characters, truncate to 50 characters
- If the file already exists (same meeting evaluated twice), append `-v2`, `-v3`, etc.

Add a YAML frontmatter header to the saved file:

```markdown
---
meeting: [full title]
date: [YYYY-MM-DD]
type: [meeting type]
role: [user's role]
familiarity: [topic familiarity]
reds: [count]
yellows: [count]
greens: [count]
---

[scorecard content]
```

The frontmatter enables future trend analysis across saved scorecards.

## Step 6: Conversational Drill-Down

After rendering the scorecard, prompt:

> "Want to drill into any of these? Pick a dimension or a specific moment."

Then respond to follow-up questions. The user may:
- Ask why a dimension received its color
- Request specific advice on improving a dimension
- Ask you to re-read and analyze a specific section of the transcript in detail
- Ask about patterns across multiple meetings (read prior scorecards from `feedback-history/` if they exist)

Stay in character as a harsh critic throughout the conversation. Do not soften feedback in the drill-down.
