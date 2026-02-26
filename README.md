# claude-harness

### Principles-First Harness Engineering for Claude Code

> *"The smallest set of high-signal tokens that maximize the likelihood of some desired outcome."*
> — Anthropic, [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Hi. This is my actual `~/.claude` folder — the one I use every day for real work. It's a **harness**: a multi-agent orchestration system that makes Claude do TDD whether it wants to or not. Twenty curated skills, custom hooks, and hard-won opinions about how AI should write code.

It's also the experimental playground for [xswarm](https://xswarm.ai) coding agents — autonomous agent swarms for software development. The team-lead pipeline, the stuck protocol, the TDD enforcement architecture — these all started here as experiments and evolved into patterns I trust enough to ship.

**Author:** Chad Jones / [xswarm.ai](https://xswarm.ai) / [chadananda@gmail.com](mailto:chadananda@gmail.com)

---

## Principles-First Harness Engineering

The central idea: **every instruction should carry its own rationale.** Not "do this" but "do this — *because*." This isn't a formatting preference — it's the difference between compliance and judgment.

Bare rules get pattern-matched: "I see a rule, I follow it." When context pressure mounts (and it always does), bare rules are the first things the model drops. Principled rules get *reasoned about*: "I understand what this protects, so I apply it correctly even in edge cases the author didn't anticipate." The reason transforms mechanical compliance into informed judgment — the model defends the rule because it understands what's at stake.

```
Bare:        Run tests after EVERY change.
Principled:  Run tests after EVERY change — catches regressions before they stack.
```

This approach is informed by Anthropic's work on [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), which recommends the "right altitude" for instructions: *specific enough to guide behavior effectively, yet flexible enough to avoid brittle hardcoding.* A terse reason achieves both — the rule constrains, the reason generalizes.

### Harness Engineering

Anthropic describes two related disciplines:

- **[Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** — curating the optimal set of tokens during inference. System prompts, tools, message history, external data — everything in the context window.
- **[Effective Harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)** — structuring scaffolding *around* agents for long-running work: decomposition into phases, environmental setup, progress tracking across context windows.

This repo applies both to Claude Code's `~/.claude` configuration. The harness is the CLAUDE.md files, agent definitions, hooks, and skills that shape how Claude works before it writes a single line of code. Every byte gets loaded into every conversation, so the harness must be maximally compact — but *never at the cost of dropping rationale*. Principles are load-bearing; filler is not.

### Design Principles

**1. Principled instructions, terse delivery.** Every rule carries its reason in `Rule — reason.` format. Drop articles, filler, and verbose sentence structure. Never drop the "why." One sentence of rationale costs ~10 tokens and dramatically improves adherence in long sessions where bare directives erode.

**2. Don't re-teach what the model knows.** Claude knows JSDoc syntax, README structure, team coordination. The harness states *rules and constraints* — things Claude would get wrong without guidance. Templates for things the model already knows are pure token waste.

**3. Architecture over prompting.** Telling Claude "DO TDD" works until context pressure wins. This system makes TDD *structural* — each agent gets a fresh context with TDD.md at high priority. Separation of concerns isn't just for code — it's for attention.

### Token Budget

The harness uses **dynamic mode-based context loading** — inspired by Anthropic's "just-in-time context retrieval" pattern from their [context engineering guide](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents): *"maintain lightweight identifiers and dynamically load data at runtime using tools."*

| Scenario | Context Loaded | Lines |
|----------|---------------|-------|
| Ad-hoc / questions / file ops | CLAUDE.md only | ~15 |
| Feature dev | CLAUDE.md + modes/dev.md | ~40 |
| Documentation | CLAUDE.md + modes/doc.md | ~25 |
| Planning | CLAUDE.md + modes/plan.md | ~25 |
| Code review | CLAUDE.md + modes/review.md | ~25 |
| SEO analysis | CLAUDE.md + modes/seo.md + refs on demand | ~45 + ~40-60/ref |
| Agent files (6 agents + TDD.md) | Per spawn | 251 |
| Skills (20 directories) | On-demand | — |

Most work (ad-hoc tasks, questions, file ops) pays **zero mode overhead**. Modes can be arbitrarily rich without taxing unrelated work. New modes are just a markdown file — no code changes.

---

## The Problem

Claude Code is brilliant. It's also a golden retriever that desperately wants to please you. Without very specific instructions, it treats you as its free human QA department — writes code confidently, hands it to you, expects *you* to test it and iterate. You become the unpaid tester in an infinite feedback loop.

We invert that. *Claude* writes the tests. *Claude* verifies its own work. *Claude* catches its own bugs. You make decisions. You approve plans. You don't manually test anything.

Left to its own devices, Claude will also:
- Write 200 lines when 40 would do
- Generate tests that mirror the implementation rather than driving it
- "Forget" about test-first after the third feature (context pressure wins)
- Guess when confused instead of asking you

---

## How It Works

### `CLAUDE.md` — The Orchestrator

```
CLAUDE.md (~15 lines)
  └── modes/           "structured workflows, loaded on demand"
      ├── dev.md       "TDD, agents, tasks, teams" (~25 lines)
      ├── plan.md      "architecture, decomposition" (~10 lines)
      ├── doc.md       "documentation rules" (~10 lines)
      └── review.md    "code review criteria" (~10 lines)
```

The orchestrator's entire job is routing. Simple task? Handle it directly — no mode needed. Complex feature? Claude classifies the activity, reads the corresponding mode file (one Read call), and follows the enriched workflow. Ad-hoc tasks, questions, OS help, brainstorming — just Claude being Claude, zero overhead.

### Mode-Based Dynamic Context

**No hook needed for detection.** Claude reads the user's prompt, classifies the activity, and reads the corresponding mode file. This is simpler and more accurate than keyword regex.

| Mode | When | What Loads |
|------|------|------------|
| *(none)* | **Most work** | **Nothing extra** |
| **dev** | Building features | TDD, agents, tasks, teams, YAGNI, style |
| **plan** | Architecture/design | Planning methodology, decomposition |
| **doc** | Writing docs | Documentation rules, placement, structure |
| **review** | Reviewing code | Review criteria, YAGNI checks, minimize |
| **seo** | SEO analysis | E-E-A-T, CWV, schema, GEO + reference files |

Explicit `*dev`, `*doc`, `*plan`, `*review`, `*seo` override classification. No command or no match = no mode loaded.

### The Agent Pipeline

Each task gets its own team — a 4-step pipeline:

```
  CODER → REVIEWER → TESTER → DOC
  (47 lines) (48 lines) (39 lines) (22 lines)
```

**Coder** gets a complete spec and builds exactly what it says using strict TDD. No research, no architectural decisions, no creative liberties. Red, green, refactor.

**Reviewer** reviews, fixes, and minimizes in a single pass. Tests run after *every* change. If code doesn't shrink, it stops. Priority: reuse existing > remove dead code > inline single-use > consolidate > simplify.

**Tester** only shows up for web and TUI projects where visual correctness matters. Libraries get two verification passes already (coder TDD + reviewer re-test). Playwright would be overkill.

**Doc** writes JSDoc and README for every deliverable. Always. No exceptions.

### Agent Teams — Parallel Feature Work

When `/plan` decomposes work into multiple independent features, the system spins up an **agent team** — multiple Claude instances working in parallel, each owning a feature and running its own TDD pipeline simultaneously.

```
                  ┌── Teammate A (Feature 1) ──┐
  Team Lead ──────┼── Teammate B (Feature 2) ──┼── Synthesize
                  └── Teammate C (Feature 3) ──┘
```

Teams for independent parallel features; subagents for sequential work or lower token budget. Each teammate must own different files — same-file editing causes overwrites.

### The Stuck Protocol

Every agent is hardwired to escalate the moment anything goes wrong. No fallbacks. No silent failures. The `stuck` agent is the *only* agent allowed to ask you questions. It presents the problem clearly with options. You make a 5-second decision. Work resumes.

| Tier | Response | Example |
|------|----------|---------|
| **Tier 1: Self-fix** | Fix once, 30s max | Typo, wrong path, missing import |
| **Tier 2: Stuck** | Instant human escalation | Design ambiguity, missing spec, 2+ failed attempts |

This is the other half of inverting the human-AI relationship. Without it, Claude guesses when confused and hands you broken output to debug. With it, Claude stops and asks a *specific question with options*. Your role shifts from "unpaid QA" to "technical decision-maker."

---

## The TDD Protocol

Lives at `agents/TDD.md` (32 lines). Loaded by every coding agent via `@TDD.md`. Non-negotiable.

```
  RED → Write ONE failing test. Watch it fail.
  GREEN → Minimum code to pass. Not what you think you'll need later.
  REFACTOR → Clean up. Tests still pass? Good. If not, undo.
  Repeat. One test at a time.
```

**Why not just say "Do TDD" in the prompt?** Because by the fifth feature, that instruction is buried under 200k tokens and Claude has reverted to its "write everything at once" instinct. Prompts drift. Architecture doesn't. Each agent invocation gets a *fresh* context with TDD at high priority.

---

## What's In the Box

```
~/.claude/
├── CLAUDE.md                     # ~15-line orchestrator with mode table
├── settings.json                 # Permissions, hooks, env vars
├── notify.py                     # Desktop notification on agent completion
│
├── modes/                        # Dynamic context (loaded on demand)
│   ├── dev.md                   # TDD, agents, tasks, teams (~25 lines)
│   ├── plan.md                  # Architecture, decomposition (~10 lines)
│   ├── doc.md                   # Documentation rules (~10 lines)
│   ├── review.md                # Code review criteria (~10 lines)
│   ├── seo.md                   # SEO methodology + scoring (~45 lines)
│   └── seo/                     # SEO reference files (loaded on demand)
│       ├── cwv.md               # Core Web Vitals thresholds
│       ├── schema.md            # Schema.org type status + deprecations
│       ├── eeat.md              # E-E-A-T evaluation framework
│       ├── quality-gates.md     # Content quality minimums
│       └── geo.md               # AI search / GEO optimization
│
├── agents/                       # The team (251 lines total)
│   ├── TDD.md                   # Shared protocol (32 lines)
│   ├── coder.md                 # Builder (47 lines)
│   ├── reviewer.md              # Critic + minimizer (48 lines)
│   ├── tester.md                # Verifier, conditional (39 lines)
│   ├── team-lead.md             # Manager, runs on Opus (27 lines)
│   ├── doc.md                   # Documentarian (22 lines)
│   └── stuck.md                 # Human escalation (36 lines)
│
├── commands/                     # Slash commands
│   ├── commit.md                # Trunk-style git workflow
│   ├── review.md                # Multi-agent code review
│   ├── seo.md                   # SEO analysis suite (activates seo mode)
│   ├── validate-product.md      # Startup idea validation
│   └── cleanup-tmp.md           # Janitor duty
│
├── hooks/                        # Automated guardrails
│   ├── warn-root-files.py       # Block non-config files in project root
│   └── cleanup-tmp-scripts.py   # Tidy up after task completion
│
└── skills/                       # 20 on-demand capabilities
    ├── [Development Workflow]
    │   ├── plan/                 # Requirements + task decomposition
    │   ├── bdd-playwright/       # Gherkin + ARIA locators + axe-core
    │   ├── systematic-debugging/ # 4-phase root cause analysis
    │   ├── using-git-worktrees/  # Parallel branch isolation
    │   ├── property-based-testing/ # Hypothesis/QuickCheck
    │   ├── notify-assistant/     # Ping OpenClaw on completion
    │   └── security-scan/        # xswarm-ai-sanitize secret detection
    │
    ├── [Language & Framework]
    │   ├── modern-python/        # uv/ruff/ty tooling
    │   ├── frontend-design/      # Bold UI, no "AI slop"
    │   └── web-artifacts-builder/ # React/Tailwind/shadcn
    │
    ├── [Documents & Formats]
    │   ├── doc-coauthoring/      # Structured doc writing
    │   ├── docx/ pdf/ pptx/ xlsx/ # Office formats
    │
    └── [Meta & Tooling]
        ├── agent-builder/        # Build your own agents
        ├── skill-creator/        # Build your own skills
        ├── mcp-builder/          # MCP server dev guide
        ├── project-cleanup/      # Organize messy projects
        ├── tui-viewer/           # TUI screenshot verification
        └── webapp-testing/       # Playwright browser testing
```

### Skills Are Lazy-Loaded

Skills only wake up when relevant. Claude scans each skill's description (~100 tokens) and ignores the rest until triggered. Twenty skills cost almost nothing at idle.

**Skill sources:** [Anthropic](https://github.com/anthropics/skills) • [Superpowers](https://github.com/obra/superpowers) (MIT) • [Trail of Bits](https://github.com/trailofbits/skills) (CC BY-SA 4.0)

---

## The Compression Story

Principles-first doesn't mean verbose. The harness grew organically to 4,100 lines, then was compressed to 296 — a 77% reduction — while *adding* principled rationale to every rule that lacked one. The insight: most of those 4,100 lines were templates, examples, and re-explanations of things Claude already knows. The principles themselves are cheap. Filler is expensive.

### Round 1: Architectural (4,100 → 1,266 lines)
Merged critic + refactor into one reviewer. Replaced 1,213-line planning agent with 180-line `/plan` skill. Deleted stale `context/` directory. Dropped redundant second coder pass.

### Round 2: Structural (1,266 → 640 lines)
Removed content duplicating system context (plugin lists, skill references, team mechanics). Removed JSDoc/README templates from doc.md (390 → 56 lines) — Claude knows JSDoc. Merged CLAUDE_conventions.md into CLAUDE.md.

### Round 3: Terse + Principled (640 → 296 lines)
Dropped articles, filler words, verbose sentence structure. Adopted `Rule — reason.` format throughout. Every rule *gained* a rationale clause while the total line count *dropped* — because the filler removed was worth far more than the reasons added.

### Round 4: Dynamic Modes (static → on-demand)
Replaced static `@-includes` with mode-based dynamic context loading. CLAUDE.md shrunk from 28 lines (with workflow + agents includes) to ~15 lines. Mode content moved to `modes/` — loaded only when the activity matches. Ad-hoc work pays zero overhead. Inspired by [Carl](https://github.com/ChristopherKahler/carl) but using Claude's own classification instead of keyword regex hooks.

| What | Round 1 | Round 2 | Round 3 | Round 4 |
|------|---------|---------|---------|---------|
| Always-loaded (CLAUDE.md) | 181 | 68 | 45 | ~15 |
| Mode/workflow content | — | — | (in always-loaded) | ~55 + ~231 refs (on-demand) |
| Agent pool (all 7 files) | 1,066 | 464 | 251 | 251 |

**The takeaway:** Agent instructions load on every invocation. A 500-line agent burns 2,000+ tokens before doing any work. But the answer isn't stripping reasons to save tokens — it's stripping everything *except* rules and reasons, and loading context *only when it's needed*. Principles are load-bearing structure. Templates, examples, and re-explanations of model knowledge are scaffolding you can remove once the building stands.

---

## Getting Started

### The Quick Way

```bash
# Back up your existing config
[ -d ~/.claude ] && mv ~/.claude ~/.claude.backup

# Clone as your global config
git clone https://github.com/chadananda/claude-harness.git ~/.claude
```

### The Picky Way

Cherry-pick what you want. The system is modular:
- Just want TDD? Grab `agents/TDD.md` and reference it from your agents.
- Just want the pipeline? Take the `agents/` folder.
- Just want skills? Copy individual skill folders into `~/.claude/skills/`.
- Just want modes? Copy `modes/` and the mode table from CLAUDE.md.

### Requirements

- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** CLI, installed and authenticated
- **No other dependencies** — secret scanning uses [xswarm-ai-sanitize](https://github.com/chadananda/xswarm-ai-sanitize) via npx
- *Optional:* Playwright MCP for web testing, VHS for TUI testing

---

## Design Decisions

<details>
<summary><b>Why dynamic modes instead of static @-includes?</b></summary>
Static includes load ~45 lines into every conversation whether needed or not. Most conversations (questions, file ops, brainstorming) don't need TDD rules or agent rosters. Dynamic modes load structured workflows only when the activity warrants it — typically saving 67% on ad-hoc work while enabling richer mode content without taxing unrelated tasks.
</details>

<details>
<summary><b>Why Claude classification instead of keyword hooks?</b></summary>
Keyword regex (like Carl's approach) misfires on ambiguous words and requires maintaining a Python hook. Claude itself is the best classifier — it understands intent, not just keywords. Zero external scripting, perfect accuracy, ~10 lines in CLAUDE.md.
</details>

<details>
<summary><b>Why does the SEO mode have reference sub-files?</b></summary>
SEO requires domain knowledge Claude doesn't have natively — deprecated schema types, current CWV thresholds, GEO statistics, quality gates. The mode file (~45 lines) loads methodology and critical rules. Reference files (~231 lines across 5 files) load on demand per analysis category. Inspired by <a href="https://github.com/AgriciDaniel/claude-seo">claude-seo</a>, distilled from ~1,500 lines to ~276 lines of high-signal content.
</details>

<details>
<summary><b>Why merge Critic + Refactor into one Reviewer?</b></summary>
The original 6-step pipeline played telephone with tokens. The merged Reviewer does review, fix, and minimize in one invocation with full context. Half the token cost, better results.
</details>

<details>
<summary><b>Why is the Tester conditional?</b></summary>
For pure functions, the coder already tested via TDD and the reviewer re-tested after every change. Two verification passes. Playwright only adds value when visual correctness is the feature.
</details>

<details>
<summary><b>Why Opus for Team-Lead, Sonnet for everyone else?</b></summary>
Team-lead makes judgment calls: Is this a web project? Is output complete? Invoke tester? Stronger reasoning pays off. Coding agents execute detailed specs mechanically — Sonnet is perfect for that.
</details>

<details>
<summary><b>Why Claude's native Task system instead of JSON files?</b></summary>
Tasks already provide DAG dependencies, status tracking, and blocking semantics. The old approach reimplemented all of that in ~1,600 lines. When the platform does the thing, let the platform do the thing.
</details>

---

## Making It Your Own

**Don't like strict TDD?** Edit `agents/TDD.md`. Or delete it entirely.

**Want different models?** Each agent has a `model:` field in its frontmatter. Swap `sonnet` for `opus` where you want brains, `haiku` where you want speed.

**Want to add agents?** Create a `.md` file in `agents/` with YAML frontmatter (name, description, tools, model).

**Want to add a mode?** Create a `.md` file in `modes/` and add a row to the mode table in CLAUDE.md. No code changes needed.

**Want project-specific behavior?** Create `.claude/CLAUDE.md` in your project root. Project-level instructions override global ones.

---

## The xswarm Connection

This repo is the petri dish for [xswarm](https://xswarm.ai) — an autonomous agent swarm framework for 2026. Everything here started as an experiment:

- **Team-lead pipeline** — managers work better when they can't write code; they focus on routing and quality.
- **Stuck protocol** — agents that can't guess eliminated more wasted time than any other change.
- **TDD enforcement** — making test-first structural, not aspirational, changed everything.
- **Harness compression** — token efficiency is an architecture concern, not an optimization.
- **Dynamic modes** — just-in-time context loading eliminates overhead for work that doesn't need structured workflows.

Watch [xswarm.ai](https://xswarm.ai) for where this is heading: multi-agent orchestration for any software development task.

---

## Further Reading

- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic's guide to curating optimal token sets
- [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — Decomposition, progress tracking, multi-window agents
- [Equipping Agents with Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — Anthropic's agent skills architecture

---

## License

MIT. Take what you want. Credit appreciated but not required.

---

<p align="center">
<i>Built with Claude Code. Refined through hundreds of iterations. Shared in the spirit of "we're all figuring this out together."</i>
<br><br>
<b>Chad Jones</b> — <a href="https://xswarm.ai">xswarm.ai</a>
<br>
Contributions, ideas, and strongly-worded opinions about testing welcome.
</p>
