# My Claude Code Setup

A catalog of every skill, plugin, agent, command, MCP integration, and CLAUDE.md behavior configured in this environment.

---

## Plugins

### superpowers (v5.0.7)
Official plugin providing structured development workflows. Includes skills for:

| Skill | Purpose |
|-------|---------|
| `brainstorming` | Explores intent, requirements, and design before any creative/implementation work |
| `writing-plans` | Produces step-by-step implementation plans from specs or requirements |
| `executing-plans` | Executes written plans in sessions with review checkpoints |
| `test-driven-development` | Enforces TDD — write tests before implementation code |
| `systematic-debugging` | Structured debugging before proposing fixes |
| `subagent-driven-development` | Executes plan tasks via independent parallel subagents |
| `dispatching-parallel-agents` | Runs 2+ independent tasks concurrently |
| `using-git-worktrees` | Creates isolated git worktrees for feature work |
| `finishing-a-development-branch` | Guides merge/PR/cleanup decisions when work is done |
| `verification-before-completion` | Requires running verification commands before claiming success |
| `requesting-code-review` | Validates work against requirements before merging |
| `receiving-code-review` | Handles incoming review feedback with technical rigor |
| `writing-skills` | Creates and verifies new skills before deployment |
| `using-superpowers` | Session startup — establishes how to discover and invoke skills |

### frontend-design
Official plugin for building distinctive, production-grade frontend interfaces. Generates creative, polished UI code that avoids generic AI aesthetics. Use when building web components, pages, or applications.

### claude-md-management (v1.0.0)
Official plugin for maintaining CLAUDE.md files:

| Skill | Purpose |
|-------|---------|
| `revise-claude-md` | Updates CLAUDE.md with learnings from the current session |
| `claude-md-improver` | Audits and improves CLAUDE.md files across repositories |

### learning-toolkit (local, v1.0.0)
Local plugin for guided learning through code. Provides a unified `/learn` skill with four modes:

- **Socratic** — Probing questions rated 1-5, one at a time
- **Chunking** — Breaks topics into concept lists with implementation challenges
- **Gap Analysis** — Diagnostic questions to map knowledge gaps with targeted exercises
- **Syntax Hints** — Brief syntax examples, progressively more specific

### vercel-plugin (v0.32.5)
Vercel platform plugin with extensive skill coverage:

| Skill | Purpose |
|-------|---------|
| `ai-architect` | Architect AI-powered apps on Vercel (AI SDK, providers, agents, MCP) |
| `ai-gateway` | Configure model routing, provider failover, cost tracking |
| `ai-sdk` | Build AI features — chat, text gen, tool calling, streaming, embeddings |
| `auth` | Authentication integration (Clerk, Descope, Auth0) |
| `bootstrap` | Bootstrap repos with Vercel-linked resources |
| `chat-sdk` | Build multi-platform chat bots (Slack, Telegram, Discord, etc.) |
| `deploy` | Deploy to Vercel (preview or production) |
| `deployments-cicd` | Deployment strategies, CI/CD, rollbacks |
| `env` / `env-vars` | Manage Vercel environment variables |
| `marketplace` | Discover and install Vercel Marketplace integrations |
| `next-cache-components` | Next.js 16 Cache Components, PPR, `use cache` |
| `next-forge` | next-forge monorepo SaaS starter guidance |
| `next-upgrade` | Upgrade Next.js versions with codemods |
| `nextjs` | Next.js App Router expert guidance |
| `performance-optimizer` | Core Web Vitals, caching, image/font optimization |
| `react-best-practices` | TSX quality checklist (hooks, a11y, performance, TS) |
| `routing-middleware` | Framework-agnostic request interception |
| `runtime-cache` | Per-region key-value cache with tag-based invalidation |
| `shadcn` | shadcn/ui CLI, components, theming, Tailwind |
| `status` | Show Vercel project status and recent deployments |
| `turbopack` | Turbopack bundler configuration and debugging |
| `vercel-agent` | AI-powered code review and incident investigation |
| `vercel-cli` | Vercel CLI expert guidance |
| `vercel-functions` | Serverless, Edge, Fluid Compute, Cron Jobs |
| `vercel-sandbox` | Sandboxed code execution in Firecracker microVMs |
| `vercel-storage` | Blob, Edge Config, Neon Postgres, Upstash Redis |
| `verification` | End-to-end flow verification (browser to data to response) |
| `workflow` | Durable workflows with pause/resume, retries, step-based execution |

---

## Custom Commands (Slash Commands)

| Command | Purpose |
|---------|---------|
| `/blog` | Converts the current conversation into a blog post, studying existing writing style from your blog directory |
| `/bob` | Reviews/writes code against Robert C. Martin's Clean Code, Clean Architecture, and SOLID principles |
| `/branch` | Shows the git diff of the current branch against main |
| `/capacity-planning-dimensions` | Question bank for the capacity planning phase of system design interviews (used by `/system`) |
| `/clean` | Reviews code for clean naming conventions — descriptive, intention-revealing names |
| `/ddd` | Reviews code against Domain-Driven Design aggregate rules (identity references, single-aggregate transactions) |
| `/experience` | Updates your skills tracker with diagnostic feedback from the current session (background agent) |
| `/idiomatic` | Reviews code for idiomatic violations, citing relevant style guides and specs |
| `/interviewer` | Simulates a brutal mock interviewer — adapts to system design, behavioral, coding, or knowledge topics |
| `/oop` | Reviews code against principles from _Elegant Objects_ by Yegor Bugayenko |
| `/overwhelmed` | Decomposes overwhelming Todoist tasks using Socratic questioning |
| `/process` | Quizzes you on concepts from the current conversation to build retention |
| `/ramble` | Extracts actionable items from the conversation and creates them as Todoist tasks |
| `/rate` | Rates your branch diff (1-5) against `/bob`, `/clean`, `/ddd`, `/oop`, and `/idiomatic` principles |
| `/scale` | Analyzes your branch code for scale limits, upgrade paths, system design diagrams, and learning resources |
| `/system` | Full system design interview simulator with Socratic method, structured phases, and a final scorecard |

---

## Agents

| Agent | Purpose |
|-------|---------|
| `socratic-code-teacher` | Guides understanding of code, architecture, and implementation through Socratic questioning — never explains directly, always asks |

---

## MCP Integrations

Connected services available via MCP servers:

| Service | Capabilities |
|---------|-------------|
| **Excalidraw** | Create/export diagrams, save/read checkpoints |
| **Gmail** | Search, read, draft emails |
| **Google Calendar** | List, create, update, delete events; suggest meeting times |
| **Google Drive** | Search, read, create, download files |
| **Granola** | Fetch meeting notes and transcripts |
| **Linear** | Full project management — issues, projects, documents, comments, milestones, labels, teams |
| **Todoist** | Task management (used by `/overwhelmed` and `/ramble`) |
| **Vercel** | Deployment and project management |

---

## CLAUDE.md Behaviors

### Thinking Check
Every prompt is scored on three dimensions (1-5 each) before responding:
- **Specificity of Intent** — How precisely the prompt describes what/where
- **Decision Ownership** — Whether the user has made key decisions
- **Diagnostic Effort** — Whether the user has investigated and formed a hypothesis

If the average is below 3, Claude coaches via the Socratic method instead of answering directly. Skipped for slash commands.

### Skills Tracker
At natural breakpoints in sessions with meaningful skill signals, a one-time reminder is offered to update the skills tracker via `/experience`.

---

## Memory System

Persistent file-based memory at `~/.claude/projects/-Users-devinat1--claude/memory/` with types:
- **user** — Role, goals, preferences
- **feedback** — Corrections and confirmed approaches
- **project** — Ongoing work context, decisions, deadlines
- **reference** — Pointers to external systems

Indexed via `MEMORY.md`, currently tracking a skills tracker diagnostic.
