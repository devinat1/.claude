# Skills

Original agent skills for learning loops, code review, interview practice, and productivity workflows.

## Quickstart (30-second setup)

1. Run the skills.sh installer:

```bash
npx skills@latest add devinat1/.claude
```

1. Pick the skills you want and which coding agents to install them on. **Include `setup-devinat1-skills`.**
2. Run `/setup-devinat1-skills` in your agent. It will ask for:
  - Agent memory project ID (for the learning loop)
  - Blog content directory (for `/blog` and `/update-blog-refs`)
  - MCP integrations (agentmemory, Granola, Todoist)
3. For Claude Code users who clone this repo directly:

```bash
git clone git@github.com:devinat1/.claude.git ~/.claude
./scripts/link-skills.sh
```

## Skills

### Learning

Skills that diagnose gaps, scaffold labs, grade exams, and log progress.

- **[learn](./skills/learning/learn/SKILL.md)** — Diagnose where understanding bottoms out, then fan out to walkthroughs, labs, exams, or agent memory logging.
- **[lab-creator](./skills/learning/lab-creator/SKILL.md)** — Scaffold a single hands-on lab targeting one concept.
- **[grader](./skills/learning/grader/SKILL.md)** — Administer exams or grade labs; update agent memory.
- **[break-it](./skills/learning/break-it/SKILL.md)** — Load-test a system-design concept until it breaks; log thresholds to agent memory.

### Engineering

Code review slash commands and repo tooling.

- **[onboard](./skills/engineering/onboard/SKILL.md)** — Produce a concise onboarding doc for the current codebase.
- **[clean](./skills/engineering/clean/SKILL.md)** — Review code for clean naming conventions.
- **[ddd](./skills/engineering/ddd/SKILL.md)** — Review code against DDD aggregate rules.
- **[oop](./skills/engineering/oop/SKILL.md)** — Review code against *Elegant Objects* principles.
- **[rate](./skills/engineering/rate/SKILL.md)** — Rate branch diff against multiple review principles.
- **[scale](./skills/engineering/scale/SKILL.md)** — Analyze scale limits and upgrade paths.
- **[graphite](./skills/engineering/graphite/SKILL.md)** — Split branch work into a Graphite PR stack.
- **[thermo-nuclear-code-quality-review](./skills/engineering/thermo-nuclear-code-quality-review/SKILL.md)** — Greptile-gated pre-PR maintainability review.
- **[webmcp-bridge](./skills/engineering/webmcp-bridge/SKILL.md)** — Use external browser harnesses with the generic WebMCP bridge and generated-tool cache.

### Interview

Mock interview practice.

- **[system](./skills/interview/system/SKILL.md)** — System design interview simulator with Socratic probing.
- **[leetcode-readiness](./skills/interview/leetcode-readiness/SKILL.md)** — Assess LeetCode progress and maintain a targeted weekly problem plan.
- **[interviewer](./skills/interview/interviewer/SKILL.md)** — Brutal mock interviewer on any topic.
- **[vc-pitch-drill](./skills/interview/vc-pitch-drill/SKILL.md)** — Pre-seed VC pitch practice with direct investor-style drills.

### Productivity

Workflow tools beyond code review.

- **[safeguard](./skills/productivity/safeguard/SKILL.md)** — Interview before non-trivial builds; ends with Build Brief, then implement.
- **[skill-radar](./skills/productivity/skill-radar/SKILL.md)** — Suggest relevant local skills, then plugins, and ask before using either.
- **[pragmatic](./skills/productivity/pragmatic/SKILL.md)** — Two-person founder reality check before implementation.
- **[clarify](./skills/productivity/clarify/SKILL.md)** — Interview until purpose and constraints are clear.
- **[dissenter](./skills/productivity/dissenter/SKILL.md)** — Compare an original decision analysis with credible dissent.
- **[benchmark-coverage](./skills/productivity/benchmark-coverage/SKILL.md)** — Match prompts to source-backed benchmarks and assess recorded model results.
- **[coherent](./skills/productivity/coherent/SKILL.md)** — Challenge hidden assumptions and missing links before compressing explanations.
- **[confounding-variables](./skills/productivity/confounding-variables/SKILL.md)** — Identify themes and candidate confounders in pasted text.
- **[confounding-audit](./skills/productivity/confounding-audit/SKILL.md)** — Separate tangled claims and conceptual connections without a verdict.
- **[linear](./skills/productivity/linear/SKILL.md)** — Convert conversations into reviewed Linear tickets and updates.
- **[meeting-feedback](./skills/productivity/meeting-feedback/SKILL.md)** — Evaluate meeting communication via Granola.
- **[focus](./skills/productivity/focus/SKILL.md)** — ADHD work assistant: stuck sessions, Focusmate timeboxing, overcommitment guard via Todoist.
- **[todo-triage](./skills/productivity/todo-triage/SKILL.md)** — Review today’s Todoist work, choose focus, and triage the rest.
- **[mentor](./skills/productivity/mentor/SKILL.md)** — Collaborate through one task with tiny next actions, adapting feedback and pace with memory.
- **[ramble](./skills/productivity/ramble/SKILL.md)** — Extract conversation items into Todoist tasks.
- **[experience](./skills/productivity/experience/SKILL.md)** — Log session diagnostics to agent memory.
- **[momtest](./skills/productivity/momtest/SKILL.md)** — Audit customer calls against The Mom Test.
- **[literature-review](./skills/productivity/literature-review/SKILL.md)** — Exhaustive prior-work discovery (academic-heavy, four lanes to saturation); no novelty verdict.
- **[research-gap](./skills/productivity/research-gap/SKILL.md)** — Novelty assessment from a literature-review report (runs discovery first if none in chat).
- **[research-advisor](./skills/productivity/research-advisor/SKILL.md)** — Direct PhD-advisor-style drill that sharpens research questions and claims.
- **[obsidian](./skills/productivity/obsidian/SKILL.md)** — State vault read/write via Obsidian CLI for Zettelkasten workflows.

### Writing

Blog workflow.

- **[blog](./skills/writing/blog/SKILL.md)** — Turn a conversation into a blog post.
- **[post](./skills/writing/post/SKILL.md)** — Draft approved X and LinkedIn posts from current context and schedule them through Postiz.
- **[update-blog-on-leetcode](./skills/writing/update-blog-on-leetcode/SKILL.md)** — Sync LeetCode notes from State vault to the public blog.
- **[update-blog-refs](./skills/writing/update-blog-refs/SKILL.md)** — Suggest related links between blog posts.
- **[youtube](./skills/writing/youtube/SKILL.md)** — Context → YouTube teleprompter script with hook, CTA, and paced line breaks.
- **[apset](./skills/writing/apset/SKILL.md)** — Interview current work into APSET (Area, Problem, System, Evaluation, Takeaway).

### Setup

- **[setup-devinat1-skills](./skills/setup/setup-devinat1-skills/SKILL.md)** — Scaffold per-repo config (`docs/agents/`) for agent memory project ID, blog directory, and MCP integrations. Run once per repo.
