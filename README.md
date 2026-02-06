# TDD/BDD Claude Code Workflow Setup

A battle-tested multi-agent orchestration system that enforces strict Test-Driven Development inside Claude Code. Instead of hoping Claude writes tests, this system makes it structurally impossible to skip them. The result is a coordinated team of specialized agents that deliver production-ready, minimal, well-tested code through a disciplined Red-Green-Refactor cycle.

**Author:** Chad Jones ([xswarm.ai](https://xswarm.ai))

---

## Why This Exists

Claude Code is remarkably capable out of the box, but it has a fundamental tension with TDD: it *wants to be helpful*, which means it tends to write implementation and tests together, skip the red phase, or produce more code than necessary. If you've ever watched Claude cheerfully generate a 200-line solution when 40 lines would do, or write tests that suspiciously mirror the implementation rather than driving it, you know the problem.

This system solves that problem architecturally rather than hoping a prompt will stick. By splitting responsibilities across specialized agents with strict protocols, we create a workflow where TDD isn't optional — it's the only path through the pipeline.

The approach draws on three insights that emerged from months of iteration:

1. **Agents with narrow responsibilities follow rules better than one agent doing everything.** A coder agent that only implements from specs doesn't need to resist the temptation to skip tests — it literally can't see the tests. The TDD protocol lives in a shared document that each agent loads independently.

2. **Token efficiency matters enormously.** Every line of agent instruction burns tokens on every invocation. The system went through a major consolidation pass (documented below) that cut per-task overhead by ~70% while preserving behavior. Concise agents are better agents.

3. **The human should make decisions, not corrections.** Rather than letting Claude guess and then fixing the output, the "stuck" protocol forces an immediate pause whenever ambiguity arises. You make one clear decision, and the system executes it. This turns out to be far faster than reviewing and revising autonomous guesses.

---

## How It Works

The system operates as a pipeline of specialized agents coordinated by a slim orchestrator. When you ask Claude Code to build something, here's what actually happens:

### The Orchestrator (`CLAUDE.md`)

The orchestrator is deliberately tiny — 8 lines that `@`-include three topic files. It exists to route work: simple requests get handled directly, complex projects get routed to the `/plan` skill, and the resulting tasks get farmed out to team-lead agents running in parallel.

The topic files handle conventions, workflow, and agent configuration separately so that changes to one concern don't require re-reading the others. This matters because CLAUDE.md is loaded into every conversation's system prompt — every byte counts.

```
CLAUDE.md (8 lines, just @ includes)
├── @CLAUDE_conventions.md  — file organization, git discipline
├── @CLAUDE_workflow.md     — autonomy rules, task management, workflow steps
└── @CLAUDE_agents.md       — agent inventory, skills, project type detection
```

### The Planning System (`/plan` skill)

Planning uses Claude Code's native Task system with DAG dependencies. This wasn't always the case — an earlier version used a 1200-line planning agent that wrote to JSON files and a separate checklist system. That approach worked but burned enormous token budgets and created stale artifacts.

The current `/plan` skill is 180 lines. It runs an interactive requirements-gathering phase (where the user approves scope before any code gets written), then decomposes work into right-sized tasks with proper dependency ordering. Pure functions get scheduled first so you get fast test feedback early. No task exceeds 60 minutes.

The skill includes an anti-hallucination checklist that forces verification of every dependency and import path before they appear in a task spec. This prevents the maddening scenario where a coder agent tries to import a module that doesn't exist because the planner assumed it did.

### The Team Pipeline

Each task gets its own team-lead agent running on the Opus model (worth the cost for orchestration decisions). The team-lead coordinates a four-step pipeline:

**Step 1 — Coder** implements from the specification. The coder receives everything it needs: file paths, import statements, code patterns to follow, success criteria. It doesn't research, doesn't make architectural decisions, doesn't choose libraries. It builds exactly what the spec says, following strict TDD: write a failing test, make it pass, refactor.

**Step 2 — Reviewer** merges what used to be two separate agents (critic + refactor) into one. It reviews for quality, applies fixes directly, then runs 2-3 minimization passes. Tests run after every change. This consolidation cut agent overhead nearly in half while giving the reviewer more context about the code it's improving.

**Step 3 — Tester** runs conditionally. For web and TUI projects, it does visual verification with Playwright or VHS. For libraries and APIs, it's skipped because the coder and reviewer already verified unit tests twice. This avoids wasting time spinning up Playwright for a pure function library.

**Step 4 — Doc** always runs. It adds JSDoc to public functions and creates a README.md in the component folder. Documentation lives with the code, not in an external system.

### The Stuck Protocol

Every agent in the system is hardwired to invoke the `stuck` agent the moment anything goes wrong. There are no fallbacks, no "try something else" loops, no silent failures. The stuck agent is the only one authorized to use `AskUserQuestion`, and it presents the problem with clear options for the human to choose from.

This sounds rigid, but in practice it's liberating. You never come back to find Claude went down a wrong path for 10 minutes. Problems surface immediately, you make a 5-second decision, and work continues. The error handling is tiered: agents self-fix trivial issues (typos, wrong paths) on one attempt within 30 seconds, but anything requiring a real decision escalates instantly.

---

## The TDD Protocol

The shared TDD protocol lives at `agents/TDD.md` and is loaded by every coding agent via `@TDD.md`. It enforces strict Red-Green-Refactor:

1. **Never write implementation without a failing test.** No exceptions.
2. **One test at a time.** Write one test, see it fail, make it pass, refactor. Then next test.
3. **Run tests at every phase.** Never say "this would fail" — execute and show output.
4. **Minimum code to pass.** Don't anticipate future tests. Triangulate via successive tests.
5. **When a test fails, fix the code — not the test.** Only change a test if the expectation itself was wrong, and state why before changing.
6. **Refactoring changes structure, not behavior.** If a test breaks during refactor, undo.
7. **Report each phase explicitly:** RED (test name + failure), GREEN (what changed + all pass), REFACTOR (what improved + all pass).

The protocol also specifies BDD conventions — `describe` blocks for context, `it` blocks for behavior, test bodies structured as given/when/then, one assertion per test. Tests should describe observable behavior, not implementation details, because implementation-coupled tests are worse than no tests at all.

### Why Not Just Tell Claude to Do TDD?

You can, and it sort of works. The problem is context pressure. In a long conversation, Claude's attention drifts. A system prompt saying "do TDD" competes with 200k tokens of conversation history. By the time you're implementing the fifth feature, the TDD instruction has been pushed to the margins of attention.

The agent architecture solves this by giving each coding invocation a fresh context with the TDD protocol loaded at high priority. The coder agent's entire identity is "implement from spec using TDD." It doesn't have competing instructions about planning, reviewing, or documenting. This separation of concerns applies to attention as much as it does to code.

---

## File Structure

```
~/.claude/
├── CLAUDE.md                  # Slim orchestrator (8 lines, @ includes)
├── CLAUDE_conventions.md      # Project structure, git discipline
├── CLAUDE_workflow.md         # Autonomy rules, task management
├── CLAUDE_agents.md           # Agent list, skills, project types
├── settings.json              # Permissions, hooks, status line
├── notify.py                  # Desktop notifications
├── .gitignore                 # Excludes Claude-managed runtime files
│
├── agents/
│   ├── TDD.md                 # Shared TDD protocol (loaded by coding agents)
│   ├── coder.md               # Implementation specialist (95 lines)
│   ├── reviewer.md            # Code review + minimization (113 lines)
│   ├── tester.md              # Unit tests + visual verification (105 lines)
│   ├── team-lead.md           # Pipeline orchestrator (111 lines)
│   ├── doc.md                 # Documentation specialist (390 lines)
│   └── stuck.md               # Human escalation (144 lines)
│
├── commands/
│   ├── commit.md              # Trunk-style development workflow
│   ├── review.md              # Multi-agent code review
│   ├── seo.md                 # Markdown SEO analysis
│   ├── validate-product.md    # Startup idea validation
│   └── cleanup-tmp.md         # Temporary file cleanup
│
├── hooks/
│   ├── warn-root-files.py     # Prevents agents from creating root-level files
│   └── cleanup-tmp-scripts.py # Cleans up after task completion
│
└── skills/
    ├── plan/                  # Requirements gathering + task decomposition
    ├── agent-builder/         # Custom subagent creation guide
    ├── doc-coauthoring/       # Structured documentation co-authoring (Anthropic)
    ├── docx/                  # Word document manipulation (Anthropic)
    ├── frontend-design/       # Production-grade UI with bold aesthetics (Anthropic)
    ├── mcp-builder/           # MCP server development guide (Anthropic)
    ├── modern-python/         # uv/ruff/ty Python tooling (Trail of Bits)
    ├── pdf/                   # PDF manipulation toolkit (Anthropic)
    ├── pptx/                  # PowerPoint manipulation (Anthropic)
    ├── project-cleanup/       # File structure organization
    ├── property-based-testing/ # Hypothesis/QuickCheck patterns (Trail of Bits)
    ├── security-scan/         # Gitleaks secret detection
    ├── skill-creator/         # Skill authoring guide (Anthropic)
    ├── systematic-debugging/  # 4-phase root cause analysis (Superpowers)
    ├── tui-viewer/            # TUI screenshot verification
    ├── using-git-worktrees/   # Parallel branch isolation (Superpowers)
    ├── web-artifacts-builder/ # React/Tailwind/shadcn artifacts (Anthropic)
    ├── webapp-testing/        # Playwright browser testing (Anthropic)
    └── xlsx/                  # Spreadsheet manipulation (Anthropic)
```

The `.gitignore` excludes all Claude-managed runtime directories (cache, debug, todos, session state, telemetry, history, etc.) so the repository contains only your authored configuration.

### Skills: Sources and Activation Scoping

Skills are loaded on-demand — Claude scans each skill's description (~100 tokens) and only loads the full content when it detects relevance to the current task. This means 20 skills cost almost nothing at idle. The key is proper scoping in each skill's `description` field:

**Coding workflow skills** activate only during development tasks:
- **systematic-debugging** — Triggers on bugs, test failures, unexpected behavior. From [Superpowers](https://github.com/obra/superpowers) (46K+ stars, MIT).
- **using-git-worktrees** — Triggers when starting feature work needing branch isolation. From [Superpowers](https://github.com/obra/superpowers).
- **property-based-testing** — Triggers when writing tests for serialization, parsing, or validation patterns. From [Trail of Bits](https://github.com/trailofbits/skills) (CC BY-SA 4.0).
- **security-scan** — Mandatory before any coder agent completes. Custom.

**Language-specific skills** activate only for their language:
- **modern-python** — Triggers only for Python projects (uv, ruff, ty tooling). From [Trail of Bits](https://github.com/trailofbits/skills).
- **frontend-design** — Triggers for React/Tailwind web UI work. From [Anthropic](https://github.com/anthropics/skills).
- **web-artifacts-builder** — Triggers for complex React/TypeScript artifacts. From [Anthropic](https://github.com/anthropics/skills).

**Document/format skills** activate only when working with that format:
- **docx**, **pdf**, **pptx**, **xlsx** — From [Anthropic](https://github.com/anthropics/skills).
- **doc-coauthoring** — Triggers for structured documentation writing. From [Anthropic](https://github.com/anthropics/skills).

**Meta skills** (rarely triggered):
- **plan**, **skill-creator**, **agent-builder**, **project-cleanup**, **tui-viewer**, **mcp-builder**, **webapp-testing** — Each scoped to its specific use case.

---

## Installation

Clone this repository into your home directory as `~/.claude`:

```bash
# Back up existing config if you have one
[ -d ~/.claude ] && mv ~/.claude ~/.claude.backup

# Clone
git clone https://github.com/chadananda/claude-code-tdd.git ~/.claude
```

Or cherry-pick the pieces you want. The system is modular — you can adopt just the TDD protocol, just the agent pipeline, or the full orchestration system.

### Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed and authenticated
- `gitleaks` for the security scan step (`brew install gitleaks` on macOS)
- For visual testing: Playwright MCP server configured, or VHS for TUI projects

### Configuration

The `settings.json` has three layers:

**Permissions** — A single `"Bash"` entry permits all shell commands. Earlier iterations had 24 specific `Bash(command:*)` entries that were all redundant. The deny list prevents writing to system temp directories (agents should use project-local `./tmp/` instead).

**Hooks** — Three hook types keep agents on track:
- `PreToolUse` on Write/Edit: blocks writes to `/tmp`, warns when agents try to create files in the project root
- `PostToolUse` on TaskUpdate: cleans up temporary scripts after task completion
- `Notification`: desktop notification when agents complete (useful when you're doing other work while agents run)

**Status Line** — Shows current directory, model, version, and git branch/status at a glance.

---

## Design Decisions and Trade-offs

### Why Merge Critic + Refactor into Reviewer?

The original pipeline ran six sequential agent calls per task: coder, tester, critic, coder (again for refactoring), refactor, doc. The critic would produce a review document, then the coder would be re-invoked to apply the suggestions, then the refactor agent would minimize. This burned tokens and time, and the coder's second pass often missed context from the review.

The merged reviewer agent does all three jobs — review, fix, minimize — in one invocation with full context. It reads the code, identifies issues, applies fixes directly (running tests after each change), then runs minimization passes. Fewer context switches, fewer tokens, better results.

### Why Is the Tester Conditional?

For a library of pure functions, spinning up Playwright to "visually verify" is nonsensical. The coder already ran tests (TDD requires it), and the reviewer re-ran them after every change. That's two verification passes before the tester even gets invoked.

The tester adds value for web projects (where visual correctness matters and can't be captured in unit tests) and TUI projects (where terminal rendering is the feature). For everything else, it's skipped.

### Why Opus for the Team-Lead?

The team-lead makes routing decisions: is this a web project? Did the coder's output look complete enough for review? Should the tester be invoked? These judgment calls benefit from stronger reasoning. The coding agents run on Sonnet because they're executing mechanical work from detailed specs — they don't need to reason about what to do, just do it well.

### Why a Shared TDD Protocol File?

Earlier iterations embedded TDD rules directly in each agent's instructions. This created maintenance headaches (update one, forget the others) and token waste (the same 40 lines loaded three times in the pipeline). The shared `TDD.md` file is loaded via `@TDD.md` by agents that need it, and ignored by agents that don't (team-lead, doc, stuck).

### Why Native Tasks Instead of JSON Files?

Claude Code's built-in Task system provides DAG dependencies, status tracking, and blocking semantics. The old approach wrote execution plans to `.claude/context/execution-plan.json` and checklists to `.claude/context/task-checklist.md` — custom infrastructure that duplicated what Tasks already does. The migration deleted ~1600 lines of planning machinery and replaced it with 180 lines in the `/plan` skill.

---

## The Consolidation Story

This system started as ~4100 lines of agent and configuration content. Through a systematic audit, it was reduced to ~1300 lines — a 70% reduction. Here's what was cut and why:

| Before | After | What Changed |
|--------|-------|-------------|
| `agents/plan.md` (1213 lines) | Deleted | Replaced by `/plan` skill (180 lines) using native Tasks |
| `agents/critic.md` (299 lines) | Deleted | Merged into `reviewer.md` (113 lines) |
| `agents/refactor.md` (344 lines) | Deleted | Merged into `reviewer.md` |
| `agents/coder.md` (513 lines) | 95 lines | Cut verbose examples and inline security docs |
| `agents/tester.md` (456 lines) | 105 lines | Added unit test mode, condensed visual testing |
| `agents/team-lead.md` (356 lines) | 111 lines | 4-step pipeline, removed redundant coder pass |
| `CLAUDE.md` (122 lines) | 8 + 83 lines | Split into topic files with @ includes |
| `settings.json` (93 lines) | 70 lines | Removed 24 redundant permission entries |
| `context/` directory | Deleted | Stale artifacts from old planning system |
| Gemini API scripts | Deleted | Opus 4.6 replaced Gemini for planning |

The lesson: agent files should be as short as possible because they're loaded into context on every invocation. A 500-line agent file with extensive examples burns 2000+ tokens before a single line of actual work happens. The examples were useful during development but unnecessary once the system was stable.

---

## Adapting This for Your Workflow

### If You Don't Want Strict TDD

Edit `agents/TDD.md` to relax the rules. You might keep the test-first principle but drop the one-test-at-a-time constraint for faster iteration. The rest of the pipeline (review, minimize, document) works independently of TDD.

### If You Want Different Agent Models

Model selection is in each agent's frontmatter. Change `model: sonnet` to `model: opus` for agents where you want stronger reasoning, or `model: haiku` for agents where speed matters more than quality (doc is a good candidate).

### If You Want to Add Agents

Create a new `.md` file in `agents/` with YAML frontmatter specifying name, description, tools, and model. Reference it from the team-lead pipeline if it should run on every task, or invoke it ad-hoc.

### If You Want Project-Specific Behavior

Create a `.claude/` directory in your project with a local `CLAUDE.md`. Project-level instructions override global ones. This is useful for specifying project-specific test commands, directory structures, or coding conventions.

---

## Lessons Learned

**Agents that can't do something won't try to.** The coder can't make architectural decisions because it doesn't have the context or instructions for it. Constraints aren't limitations — they're what make the system reliable.

**Token budgets are architecture decisions.** A 1200-line planning agent consumed more tokens per invocation than the entire current system combined. Conciseness isn't just aesthetic; it directly affects how many tasks you can run before hitting context limits.

**The stuck protocol is the most important agent.** Everything else can be tweaked, but the guarantee that problems surface immediately rather than compounding silently is what makes the whole system trustworthy.

**Parallel execution is free performance.** Once tasks are properly decomposed with dependency mapping, running them in parallel doesn't cost more tokens — it just finishes sooner. The planning overhead pays for itself on any project with 3+ tasks.

**Documentation should be mandatory, not optional.** Making doc the final pipeline step means every deliverable arrives documented. This compounds over time as the codebase builds up a knowledge base that both humans and AI agents can reference.

---

## License

MIT

## Author

**Chad Jones** — [xswarm.ai](https://xswarm.ai) — [chadananda@gmail.com](mailto:chadananda@gmail.com)

Built with Claude Code, refined through hundreds of iterations, and used daily for real projects. Contributions and ideas welcome.
