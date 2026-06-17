# Focus — Todoist configuration

Edit project IDs here if your Todoist structure changes.

## Session lengths (Focusmate)

| Length | Use |
|--------|-----|
| **50 min** | Default for deep / focus work on the specified task |
| **25 min** | Low-energy / admin tasks |
| **75 min** | Rare — only when user asks |

User books Focusmates themselves. Assistant tells **how many** to book and **what goes in each**.

## Sizing constants

- **Underestimation buffer:** estimated session count × **1.5, round up**
- **Soft cap per parent task:** prefer ≤ **2** × 50min sessions; warn at 3–4 and suggest splitting into multiple parent tasks

## Low-energy allowlist (honest trade candidates)

| Project | ID |
|---------|-----|
| 💤 Back Burner | `6Crf57h3Hp9FpfC6` |
| Life | `6Crf57h3GFfHPPv2` |
| Health | `6HMvP93JgM4X33HQ` |
| homelab | `6gPfWrFM9fVhC9W5` |
| claude | `6gPfJp49HfxgrJW8` |

Ask once per session if the user wants to add another project beyond this list.

## Eisenhower matrix (Important + Urgent labels)

Todoist label names are **`Important`** and **`Urgent`** (capitalized). Classify every task from its `labels` array:

| Quadrant | Labels | Focus skill stance |
|----------|--------|-------------------|
| Q1 | `Urgent` + `Important` | Protect in today's plan; hardest to defer |
| Q2 | `Important` only | Schedule deep work; defer only after Q3/Q4 |
| Q3 | `Urgent` only | Fit in 25 min slots or batch; good defer candidates when overcommitted |
| Q4 | **neither** `Important` nor `Urgent` | Valid everyday work — routines, low-energy trades, nice-to-haves. First cut when overcommitted; not shameful when user names it |

**Classification rule:** No `Important` and no `Urgent` = **Q4**. Untagged tasks are Q4 by default — most backlog volume lives here. Low-energy allowlist work often stays Q4 by design.

**Combined ranking:** Quadrant first (Q1 → Q2 → Q3 → Q4), then Todoist priority within quadrant (`p1` > `p2` > `p3` > `p4`). A Q1 `p4` outranks a Q2 `p1`. A Q4 `p1` outranks other Q4 tasks but still ranks below Q1–Q3.

**Layering:** `blocked`, `cognitive`, and `timesink` apply on top of quadrant (e.g. `blocked` + Q1 = don't push through; `timesink` + Q3 = rabbit-hole risk).

## Labels (read-only reference)

| Label | Use |
|-------|-----|
| `Important` | Q2/Q1 — strategic work; factor into deferral and diagnosis |
| `Urgent` | Q1/Q3 — time pressure; pair with `Important` to detect firefighting |
| `blocked` | External dependency — don't push through |
| `cognitive` | High mental load — factor into energy matching |
| `timesink` | Warn if user is drifting here instead of stated focus |

## Todoist MCP cheat sheet

| Action | Tool | Notes |
|--------|------|-------|
| Today's + overdue tasks | `find-tasks-by-date` | `startDate: "today"` — returns `labels` and `priority` for quadrant classification |
| Find task by name/project | `find-tasks` | Match user-specified task or project |
| Q1 today | `find-tasks` | `filter: "(today | overdue) & (@Important & @Urgent)"` — or `labels: ["Important","Urgent"], labelsOperator: "and"` plus date pull |
| Q1/Q2 strategic today | `find-tasks` | `filter: "(today | overdue) & @Important"` — optional when user asks what fits without naming a task |
| Add session subtask | `add-tasks` | Set `parentId` to parent task ID |
| Change priority, labels, description | `update-tasks` | Priorities: `p1`–`p4` strings only; add/remove `Important`/`Urgent` when user agrees |
| Move due date | `reschedule-tasks` | Always for date moves; preserves recurrence |
| Session note on task | `add-comments` | Record trade rationale or agreed step |

**Never** use `update-tasks` with `dueString` to reschedule — it breaks recurring tasks.

## Micro-step reframe examples

- "Write methods section" → Open doc, write one subsection heading + 3 bullet points — no polish, one session.
- "File taxes" → Gather receipts into one folder — don't categorize yet, 25 min.
- "Review PR feedback" → Read comments on files 1–2 only — respond or note questions, 50 min.
- "Prepare for meeting" → List 3 questions you need answered — don't build slides, 25 min.
