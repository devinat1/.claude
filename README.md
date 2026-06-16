# devinat1 Skills

Agent skills for learning loops, code review, interview practice, and productivity workflows.

## Quickstart (30-second setup)

1. Run the skills.sh installer:

```bash
npx skills@latest add devinat1/.claude
```

2. Pick the skills you want and which coding agents to install them on. **Include `setup-devinat1-skills`.**

3. Run `/setup-devinat1-skills` in your agent. It will ask for:
   - Skills tracker path (for the learning loop)
   - Blog content directory (for `/blog` and `/update-blog-refs`)
   - MCP integrations (Granola, Todoist)

4. For Claude Code users who clone this repo directly:

```bash
git clone git@github.com:devinat1/.claude.git ~/.claude
./scripts/link-skills.sh
```

## Dependencies (optional)

These skills are **not** bundled. Install separately if you want them:

```bash
npx skills@latest add mattpocock/skills
./scripts/link-external-skills.sh   # symlinks into ~/.claude/skills for Claude Code
```

Recommended from [mattpocock/skills](https://github.com/mattpocock/skills): `tdd`, `diagnose`, `grill-with-docs`, `grill-me`, `handoff`, `to-issues`, `to-prd`, `triage`, `improve-codebase-architecture`, `prototype`, `teach`, `write-a-skill`, `zoom-out`, `caveman`.

Also commonly used: `find-skills`, `postiz`, `design-an-interface`.

## Personal config

[`settings.json`](settings.json) in this repo is the author's personal Claude Code config. Do not copy it blindly when installing skills elsewhere.

## Reference

### Learning

Skills that diagnose gaps, scaffold labs, grade exams, and log progress.

- **[learn](./skills/learning/learn/SKILL.md)** — Diagnose where understanding bottoms out, then fan out to walkthroughs, labs, exams, or blind-spot logging.
- **[lab-creator](./skills/learning/lab-creator/SKILL.md)** — Scaffold a single hands-on lab targeting one concept.
- **[grader](./skills/learning/grader/SKILL.md)** — Administer exams or grade labs; update the skills tracker.
- **[break-it](./skills/learning/break-it/SKILL.md)** — Load-test a system-design concept until it breaks; patch in the pattern.

### Engineering

Code review slash commands and repo tooling.

- **[onboard](./skills/engineering/onboard/SKILL.md)** — Produce a concise onboarding doc for the current codebase.
- **[clean](./skills/engineering/clean/SKILL.md)** — Review code for clean naming conventions.
- **[ddd](./skills/engineering/ddd/SKILL.md)** — Review code against DDD aggregate rules.
- **[oop](./skills/engineering/oop/SKILL.md)** — Review code against _Elegant Objects_ principles.
- **[rate](./skills/engineering/rate/SKILL.md)** — Rate branch diff against multiple review principles.
- **[scale](./skills/engineering/scale/SKILL.md)** — Analyze scale limits and upgrade paths.
- **[graphite](./skills/engineering/graphite/SKILL.md)** — Split branch work into a Graphite PR stack.
- **[thermo-nuclear-code-quality-review](./skills/engineering/thermo-nuclear-code-quality-review/SKILL.md)** — Extremely strict maintainability review.

### Interview

Mock interview practice.

- **[system](./skills/interview/system/SKILL.md)** — System design interview simulator with Socratic probing.
- **[interviewer](./skills/interview/interviewer/SKILL.md)** — Brutal mock interviewer on any topic.

### Productivity

Workflow tools beyond code review.

- **[clarify](./skills/productivity/clarify/SKILL.md)** — Interview until purpose and constraints are clear.
- **[meeting-feedback](./skills/productivity/meeting-feedback/SKILL.md)** — Evaluate meeting communication via Granola.
- **[overwhelmed](./skills/productivity/overwhelmed/SKILL.md)** — Decompose Todoist tasks tagged `overwhelmed`.
- **[ramble](./skills/productivity/ramble/SKILL.md)** — Extract conversation items into Todoist tasks.
- **[experience](./skills/productivity/experience/SKILL.md)** — Update skills tracker from session signals.
- **[momtest](./skills/productivity/momtest/SKILL.md)** — Audit customer calls against The Mom Test.

### Writing

Blog workflow.

- **[blog](./skills/writing/blog/SKILL.md)** — Turn a conversation into a blog post.
- **[update-blog-refs](./skills/writing/update-blog-refs/SKILL.md)** — Suggest related links between blog posts.

### Setup

- **[setup-devinat1-skills](./skills/setup/setup-devinat1-skills/SKILL.md)** — Scaffold per-repo config (`docs/agents/`) for tracker path, blog directory, and MCP integrations. Run once per repo.
