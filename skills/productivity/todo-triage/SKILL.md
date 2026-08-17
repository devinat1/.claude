---
name: todo-triage
description: Review Todoist tasks due today or overdue plus the triage backlog, group them by topic, choose focus tasks, and triage the rest. Use for a morning Todoist review, daily focus selection, or when the user invokes /todo-triage.
---

# Todo Triage

Turn today's dated commitments into an intentional focus list without changing Todoist structure.

## Review

1. Use Todoist to fetch every incomplete task due today or overdue that is assigned to the user. Paginate until complete.
2. Fetch every incomplete task assigned to the user with the `triage` label. Paginate until complete.
3. If both lists are empty, say so and stop without changing anything.
4. Infer a few plain-language themes for the dated tasks. Show every task once beneath its theme, including its task number, project, due date, priority, and labels.
5. Show the labeled tasks as a separate **Triage backlog** step, grouped into a few plain-language themes with unique task numbers and the same details. Do not merge them into the dated-task themes.
6. Ask the user to select one or more task numbers from either list as today's focus. Do not make Todoist changes yet.
7. Keep selected tasks as focus. Treat every non-selected, non-recurring dated task as a triage candidate. Leave unselected tasks already in the triage backlog unchanged. Do not change recurring tasks.
8. Show the candidate list and ask for one explicit confirmation before updating Todoist.

## Apply confirmed changes

1. For each confirmed triage candidate, preserve its existing labels, add `triage` if absent, and remove only its due date. Do not change its deadline, project, section, parent, priority, description, or assignment.
2. For each selected non-recurring task that has `triage`, preserve its other labels and remove only `triage`. Leave its due date unchanged.
3. Todoist task updates replace the full label list. Always send the complete preserved label list, and batch updates within Todoist's limit.
4. Report the task names changed, whether `triage` was added or removed, and whether a due date was cleared. Report failures individually; do not retry unrelated tasks.

## Rules

- Reuse the existing `triage` label. Do not create labels, projects, sections, or filters.
- Keep the review conversational: wait for the focus selection, then wait for confirmation.
- If Todoist is unavailable, say so plainly and make no changes.
- Do not use the `focus` skill; this is a daily review, not a timeboxing workflow.
