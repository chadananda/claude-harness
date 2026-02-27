# Domain Auto-Switching Meta Harness for Claude Code

![Claude Harness](assets/header.png)

> *"The smallest set of high-signal tokens that maximize the likelihood of some desired outcome."*
> — Anthropic, [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

This is my actual `~/.claude` folder — the one I use every day for real work. It's a **harness**: a domain-aware orchestration system with six specialized domains that load rich, domain-specific workflows on demand while paying zero context cost when idle. TDD-enforced coding agents, SEO analysis with current-year knowledge, end-to-end SaaS planning — each domain brings deep expertise without polluting the others.

It's also the experimental playground for [xswarm](https://xswarm.ai) coding agents — autonomous agent swarms for software development.

**Author:** Chad Jones / [xswarm.ai](https://xswarm.ai) / [chadananda@gmail.com](mailto:chadananda@gmail.com)

---

## The Problem: CLAUDE.md Is a Multiplier

Here we observe the developer in their natural habitat — editing CLAUDE.md. They've just discovered that Claude can do SEO analysis, enforce TDD, review code, plan projects, and validate startup ideas. Naturally, they want all of it. And so they begin to type.

What follows is one of nature's most reliable tragedies.

### The Weight of Every Word

Every token in your CLAUDE.md loads into **every single conversation.** Not once — *every time.* Every agent spawn. Every subagent. Every tool call that touches context. Your CLAUDE.md is not a configuration file. It is a tax, levied on every single thing Claude does for you.

Consider the arithmetic. A modest CLAUDE.md — say, 200 lines covering TDD rules, SEO guidelines, documentation standards, and code review criteria — consumes roughly 800 tokens. That's the cost of a thoughtful paragraph of *actual work.* And it's paid before Claude has read a single line of your code. Before it's considered your question. Before it has done anything at all.

Now watch what happens when agents enter the picture. A typical development pipeline spawns 4 agents: coder, reviewer, tester, documentation. Each one loads your CLAUDE.md independently. That's 200 lines × 4 agents = **800 lines of instructions consumed before a single line of code is written.** Run three features in parallel with agent teams? That's 2,400 lines. Your harness is now using more tokens to *describe itself* than your agents use to *do the work.*

This is the multiplier problem, and you cannot edit your way out of it.

### The Cocktail Party Effect

But token cost, considerable as it is, is the *lesser* problem. The greater one is attention.

Picture Claude's context window as a cocktail party. Your actual task — "add a login endpoint" — is trying to have a conversation in the corner. But your CLAUDE.md has also invited everyone it's ever met. The SEO expert is loudly explaining that HowTo schema was deprecated in September 2023. The documentation specialist keeps interrupting to remind everyone about JSDoc placement rules. The SaaS planning advisor is in the kitchen drawing 5-factor scoring matrices on the napkins.

None of them are relevant. All of them are consuming attention.

This isn't metaphorical. Transformer attention is a finite resource. Every instruction in context competes with every other instruction — and with your actual code, your actual question, your actual task. Research consistently shows that instruction adherence degrades as context grows. Not because the model can't see the instructions, but because it's *spreading its attention across all of them simultaneously.* The instruction that matters is now one voice among dozens, and the model must figure out which voices to listen to while also doing its actual job.

At 50 lines of CLAUDE.md, this barely registers. At 200 lines, adherence to any single instruction drops measurably. At 500 lines — the size you'd need for genuinely deep multi-domain expertise — the model is attending a cocktail party so crowded that it can barely hear its own thoughts.

### The Depth-vs-Breadth Trap

And here the developer faces their cruelest dilemma.

You *want* deep expertise in each domain. You want Claude to know that INP replaced FID in March 2024, that FAQ schema is now restricted to government and health sites, that E-E-A-T applies to all competitive queries since the December 2025 core update. You want detailed TDD enforcement — not "do TDD" but red-green-refactor with specific rules about test isolation, minimum coverage, and refactor-only-when-green. You want pricing research methodology, community infiltration timelines, launch day hour-by-hour checklists.

But every line of depth in one domain is a line of noise in every other domain. The SEO schema deprecation rules — critical during a site audit — are pure static while Claude is writing a database migration. The TDD protocol — essential during feature development — is irrelevant distraction while Claude is scoring your startup idea.

So most developers make a quiet, practical compromise. They keep their instructions shallow. A line or two per domain. "Follow TDD." "Use good SEO practices." "Write clean code." And then they wonder why Claude's output is... generic. Correct-ish but not expert. Following the letter of the instruction without the depth to follow its spirit.

The shallow compromise is the natural consequence of a monolithic CLAUDE.md. Depth costs attention, attention is finite, and every domain's depth taxes every other domain's performance. **You cannot have both breadth and depth in a single file.** The architecture won't allow it.

### The Way Out

The solution is not better writing. It is not more aggressive compression. It is not finding the perfect 50 words that somehow encode deep expertise across six domains. You cannot compress your way out of a multiplier problem.

The solution is **isolation.** Each domain loads its own deep expertise only when that expertise is relevant, and pays zero cost — zero tokens, zero attention, zero dilution — when it isn't. A coding session loads TDD rules and agent pipelines. An SEO audit loads schema deprecations and Core Web Vitals thresholds. A SaaS planning session loads scoring rubrics and marketing frameworks. And none of them ever meet at the same cocktail party.

That's what domain switching does.

---

## Table of Contents

- [Domain Switching](#domain-switching) — The meta-harness architecture
- [dev](#dev--software-development) — TDD, agent pipeline, teams, stuck protocol
- [plan](#plan--project-planning) — Requirements gathering, task decomposition
- [doc](#doc--documentation) — Documentation rules, placement, structure
- [review](#review--code-review) — Code review criteria, YAGNI, minimization
- [seo](#seo--seo-analysis) — E-E-A-T, CWV, schema, GEO + reference files
- [plan-saas](#plan-saas--saas-project-planner) — 4-phase pipeline: validate → strategy → technical → marketing
- [Skills](#skills--lazy-loaded-capabilities) — 21 on-demand capabilities
- [The Compression Story](#the-compression-story) — 4,100 → 296 lines in 4 rounds
- [Getting Started](#getting-started)
- [Design Decisions](#design-decisions)
- [Making It Your Own](#making-it-your-own)

---

## Domain Switching

This harness solves the multiplier problem by keeping CLAUDE.md to **~15 lines** — a routing table, not an instruction manual. Claude classifies the activity, loads one domain file, and gets deep expertise for exactly that task. Everything else stays out of context.

```
                              CLAUDE.md (~15 lines)
                              The Orchestrator
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
              classify activity   no match?     explicit *domain?
                    │           just Claude         override
                    ▼               │               │
              ┌─────────────────────┴───────────────┘
              │
              ▼
     ┌────────────────────────────────────────────────────┐
     │  domains/                                            │
     │  ├── dev.md          ~25 lines + 251 lines agents  │
     │  ├── plan.md         ~10 lines                     │
     │  ├── doc.md          ~10 lines                     │
     │  ├── review.md       ~10 lines                     │
     │  ├── seo.md          ~45 lines + ~231 lines refs   │
     │  └── plan-saas.md    ~8 lines + ~1,770 lines refs  │
     └────────────────────────────────────────────────────┘
```

**How it works:** Claude reads the user's prompt, classifies the activity, and reads one domain file (a single Read call). No hooks, no regex, no external scripts. Claude is the best classifier — it understands intent, not just keywords. Explicit `*dev`, `*seo`, etc. override classification.

**The numbers:**

| Scenario | Context Loaded | Lines |
|----------|---------------|-------|
| Ad-hoc / questions / file ops | CLAUDE.md only | ~15 |
| Feature development | CLAUDE.md + domains/dev.md | ~40 |
| Documentation | CLAUDE.md + domains/doc.md | ~25 |
| Project planning | CLAUDE.md + domains/plan.md | ~25 |
| Code review | CLAUDE.md + domains/review.md | ~25 |
| SEO analysis | CLAUDE.md + domains/seo.md + refs | ~45 + ~40-60/ref |
| SaaS planning | CLAUDE.md + domain + skill + refs | ~75 + ~60-140/phase |

Most work pays **zero domain overhead**. A typical harness with equivalent domain coverage would load 300-500 lines into every conversation. This one loads 15. That's a 20-30x reduction on the multiplier — and because agents amplify the cost, the real savings in a multi-agent pipeline are even larger.

Each domain can be arbitrarily deep — the SaaS planner has 1,770 lines of domain knowledge across 18 files — without adding a single token to an SEO audit or a code review. Adding a new domain is just a markdown file plus a row in the routing table. No code changes.

### Principles-First Instructions

Every instruction across all domains follows one rule: **carry your own rationale.**

```
Bare:        Run tests after EVERY change.
Principled:  Run tests after EVERY change — catches regressions before they stack.
```

Bare rules get pattern-matched and dropped under context pressure. Principled rules get *reasoned about* — the model defends the rule because it understands what's at stake. One sentence of rationale costs ~10 tokens and dramatically improves adherence in long sessions. This approach is informed by Anthropic's [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) guide: *specific enough to guide behavior effectively, yet flexible enough to avoid brittle hardcoding.*

Two related disciplines underpin this:

- **[Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** — curating the optimal set of tokens during inference.
- **[Effective Harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)** — structuring scaffolding *around* agents for long-running work.

**Don't re-teach what the model knows.** Claude knows JSDoc syntax, README structure, team coordination. The harness states *rules and constraints* — things Claude would get wrong without guidance. Templates for things the model already knows are pure token waste.

---

## dev — Software Development

**~25 lines loaded** on activation, plus 251 lines of agent definitions on spawn.

The dev domain solves a specific problem: Claude Code is brilliant but treats you as its free human QA department. Without specific instructions, it writes code confidently, hands it to you, expects *you* to test it and iterate. We invert that. *Claude* writes the tests. *Claude* verifies its own work. *Claude* catches its own bugs. You make decisions. You approve plans. You don't manually test anything.

### The TDD Protocol

Lives at `agents/TDD.md` (32 lines). Loaded by every coding agent. Non-negotiable.

```
  RED → Write ONE failing test. Watch it fail.
  GREEN → Minimum code to pass. Not what you think you'll need later.
  REFACTOR → Clean up. Tests still pass? Good. If not, undo.
  Repeat. One test at a time.
```

**Why structural, not aspirational?** Telling Claude "DO TDD" works until context pressure wins. By the fifth feature, that instruction is buried under 200k tokens and Claude has reverted to "write everything at once." This system makes TDD *architectural* — each agent gets a fresh context with TDD.md at high priority. Prompts drift. Architecture doesn't.

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

Every agent is hardwired to escalate the moment anything goes wrong. No fallbacks. No silent failures.

| Tier | Response | Example |
|------|----------|---------|
| **Tier 1: Self-fix** | Fix once, 30s max | Typo, wrong path, missing import |
| **Tier 2: Stuck** | Instant human escalation | Design ambiguity, missing spec, 2+ failed attempts |

The `stuck` agent is the *only* agent allowed to ask you questions. It presents the problem clearly with options. You make a 5-second decision. Work resumes. Your role shifts from "unpaid QA" to "technical decision-maker."

---

## plan — Project Planning

**~10 lines loaded** on activation.

Interactive requirements gathering and task decomposition. Transforms vague requirements into executable task DAGs using native Claude Code Tasks.

- **Phase 0 (Interactive):** 5W1H analysis + MoSCoW prioritization + Given-When-Then scenarios. Resolves ambiguity before any code is written. Blocks until user approves.
- **Phase 1 (Autonomous):** Codebase research — finds existing utilities, coding patterns, dependency versions. Anti-hallucination checklist: verify every module, import path, and version before specifying.
- **Phase 2:** Task decomposition into XS/S/M units (no task > 60 min). Test-first ordering: pure functions before integration.
- **Phase 3:** Output native Tasks with DAG dependencies for parallel execution.

**Key principle:** Good specs enable mechanical execution. Every task spec includes file paths, imports, patterns to follow, and success criteria. Bad spec: "Implement JWT authentication." Good spec: "Size: S | File: src/routes/api/auth/login.ts | Imports: { hashPassword } from src/lib/auth/hash | Pattern: Follow src/routes/api/admin/auth/+server.ts lines 23-45 | Success: POST /api/auth/login returns 200+JWT on valid creds, 401 on invalid."

---

## doc — Documentation

**~10 lines loaded** on activation.

Documentation rules, placement conventions, and structure. Keeps docs co-located with code, concise, and practical. JSDoc for inline documentation, README for each component/feature.

---

## review — Code Review

**~10 lines loaded** on activation.

Multi-agent code review pipeline. Review criteria include correctness, security (OWASP top 10), YAGNI violations, dead code, and opportunities to minimize. The reviewer agent applies the same minimize-first philosophy from the dev domain: if code doesn't shrink, stop changing it.

---

## seo — SEO Analysis

**~45 lines loaded** on activation, plus ~231 lines across 5 reference files loaded on demand.

This domain demonstrates the **reference file pattern** — domain knowledge Claude doesn't have natively, loaded just-in-time per analysis category. SEO changes constantly: schema types get deprecated, Core Web Vitals thresholds shift, AI search optimization is brand new. The domain file contains methodology and critical rules. Reference files contain perishable knowledge.

### What's in the domain file (~45 lines)
- 7-category weighted scoring methodology (Technical 25%, Content/E-E-A-T 25%, On-Page 20%, Schema 10%, CWV 10%, Images 5%, GEO 5%)
- Critical rules Claude gets wrong: INP replaced FID, HowTo schema deprecated, FAQ schema restricted, mobile-first 100% complete, E-E-A-T applies to all competitive queries
- GEO quick wins for AI search optimization
- Analysis workflow and output format

### Reference files (loaded per category)
| File | Lines | Domain Knowledge |
|------|-------|-----------------|
| `seo/eeat.md` | ~50 | E-E-A-T evaluation framework |
| `seo/cwv.md` | ~40 | Core Web Vitals thresholds (current) |
| `seo/schema.md` | ~50 | Schema.org type status + deprecations |
| `seo/quality-gates.md` | ~40 | Content quality minimums |
| `seo/geo.md` | ~50 | AI search / Generative Engine Optimization |

Inspired by [claude-seo](https://github.com/AgriciDaniel/claude-seo), distilled from ~1,500 lines to ~276 lines of high-signal content.

---

## plan-saas — SaaS Project Planner

**~8 lines in domain file**, pointing to a comprehensive skill with **~1,770 lines across 18 files** — all loaded on demand per phase. Zero cost when not in use.

Takes a SaaS idea from napkin sketch to implementation-ready repo with a 12-month marketing calendar. Four linear phases, each producing a deliverable document that feeds into the next:

```
Phase 1: VALIDATE        Phase 2: STRATEGY       Phase 3: TECHNICAL      Phase 4: MARKETING
┌────────────────┐      ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
│ 6-question     │      │ 5-layer ICP    │      │ Tech stack     │      │ Keyword        │
│ interview with │─────▶│ Positioning    │─────▶│ MVP scope      │─────▶│ universe       │
│ web research   │      │ Pricing        │      │ User stories   │      │ Content        │
│ 5-factor score │      │ research       │      │ Architecture   │      │ calendar       │
│                │      │                │      │ Milestones     │      │ Guerrilla plan │
│ → viability-   │      │ → strategy-    │      │ → software-    │      │ → marketing-   │
│   report.md    │      │   brief.md     │      │   prd.md       │      │   prd.md       │
└────────────────┘      └────────────────┘      └────────────────┘      └────────────────┘
  Score ≥10 to proceed
```

### Phase 1: Validate
Absorbs the standalone `/validate-product` command. Tough-love interview — one question at a time with WebSearch between each to research competitors, market data, and channels. Scores across 5 factors (0-3 each, multiplicative):

| Factor | What it measures | Score 3 example |
|--------|-----------------|-----------------|
| Product | 10x better than alternatives | Creates new category, paradigm shift |
| Acquisition | Path to finding users | Built-in virality, distribution moat |
| Market | Size and growth | >$1B TAM with strong tailwinds |
| Defendability | Hard to copy | Structural moats: network effects, proprietary data |
| Buildability | Can execute | Unfair advantage: domain + skills + assets |

Zones: 0-9 Red (iterate), 10-19 Yellow (proceed with caution), 20-49 Green (build it), 50-99 Elite (raise capital), 100+ Unicorn.

### Phase 2: Strategy
Develops the Ideal Customer Profile using a 5-layer model (problem identity → buyer profile → psychographics → watering holes → buying behavior). Creates a positioning framework with tagline and elevator pitch. Researches competitor pricing pages to recommend specific tiers and prices with dollar amounts.

### Phase 3: Technical
Opinionated tech stack (Vue/Svelte over React, PostgreSQL default, PaaS hosting, managed auth/payments). Ruthless MVP scoping with MoSCoW — explicit "Won't Have" list with reasons to prevent scope creep. User stories with acceptance criteria. Architecture, data model, API surface. 4-6 development milestones with infrastructure cost estimates.

### Phase 4: Marketing
The most comprehensive phase — produces a complete GTM playbook:
- **Keyword universe** (20-30 keywords, BOFU/MOFU/TOFU classified)
- **Content architecture** (pillar/cluster model with internal linking strategy)
- **12-week content calendar** with specific article titles and target keywords
- **Guerrilla marketing** (build-in-public, viral waitlist, community infiltration, Product Hunt prep, micro-influencer outreach)
- **Channel strategy** (3 primary + 2 secondary with ICP-tied reasoning)
- **12-week launch sequence** with hour-by-hour launch day plan
- **Email sequences** (7-email onboarding drip + newsletter framework)
- **Metrics dashboard** (north star metric + weekly/monthly KPIs)

### The reference file architecture

```
skills/plan-saas/                        # 18 files, ~1,770 lines total
├── SKILL.md                             # Orchestrator: routing, phase gating
├── skills/                              # 4 sub-skills (~710 lines)
│   ├── plan-validate.md                 # Phase 1 interview + scoring
│   ├── plan-strategy.md                 # Phase 2 ICP + positioning + pricing
│   ├── plan-technical.md                # Phase 3 stack + MVP + architecture
│   └── plan-marketing.md                # Phase 4 GTM + content + launch
├── references/                          # 9 domain knowledge files (~790 lines)
│   ├── viability-scoring.md             # Scoring rubrics + challenge prompts
│   ├── icp-framework.md                 # 5-layer ICP model
│   ├── pricing-models.md               # SaaS pricing patterns + tier design
│   ├── saas-tech-stacks.md             # Stacks by product type + anti-patterns
│   ├── seo-strategy.md                 # SEO funnel + keyword research + GEO
│   ├── content-marketing.md            # Content types by funnel stage
│   ├── guerrilla-playbook.md           # Tactics + benchmarks
│   ├── distribution-channels.md        # Channel deep dives + prioritization
│   └── launch-sequence.md              # 12-week timeline + launch day plan
└── templates/                           # 4 output templates (~190 lines)
    ├── viability-report.md
    ├── strategy-brief.md
    ├── software-prd.md
    └── marketing-prd.md
```

Each phase loads only its relevant references (~60-140 lines), not the full ~790 lines. Same just-in-time pattern as the SEO domain, scaled up.

**Commands:** `/plan-saas [idea]` (full pipeline), `/plan-saas validate|strategy|technical|marketing` (individual phases), `/plan-saas resume` (detect and continue).

---

## Skills — Lazy-Loaded Capabilities

Skills only wake up when relevant. Claude scans each skill's description (~100 tokens) and ignores the rest until triggered. 21 skills cost almost nothing at idle.

```
skills/
├── [Development Workflow]
│   ├── plan/                    # Requirements + task decomposition
│   ├── plan-saas/               # SaaS idea → launch-ready (4-phase pipeline)
│   ├── bdd-playwright/          # Gherkin + ARIA locators + axe-core
│   ├── systematic-debugging/    # 4-phase root cause analysis
│   ├── using-git-worktrees/     # Parallel branch isolation
│   ├── property-based-testing/  # Hypothesis/QuickCheck
│   ├── notify-assistant/        # Ping OpenClaw on completion
│   └── security-scan/           # xswarm-ai-sanitize secret detection
│
├── [Language & Framework]
│   ├── modern-python/           # uv/ruff/ty tooling
│   ├── frontend-design/         # Bold UI, no "AI slop"
│   └── web-artifacts-builder/   # React/Tailwind/shadcn
│
├── [Documents & Formats]
│   ├── doc-coauthoring/         # Structured doc writing
│   ├── docx/ pdf/ pptx/ xlsx/  # Office formats
│
└── [Meta & Tooling]
    ├── agent-builder/           # Build your own agents
    ├── skill-creator/           # Build your own skills
    ├── mcp-builder/             # MCP server dev guide
    ├── project-cleanup/         # Organize messy projects
    ├── tui-viewer/              # TUI screenshot verification
    └── webapp-testing/          # Playwright browser testing
```

**Skill sources:** [Anthropic](https://github.com/anthropics/skills) • [Superpowers](https://github.com/obra/superpowers) (MIT) • [Trail of Bits](https://github.com/trailofbits/skills) (CC BY-SA 4.0)

---

## The Compression Story

Principles-first doesn't mean verbose. The harness grew organically to 4,100 lines, then was compressed to 296 — a 77% reduction — while *adding* principled rationale to every rule that lacked one. The insight: most of those 4,100 lines were templates, examples, and re-explanations of things Claude already knows. The principles themselves are cheap. Filler is expensive.

| Round | What Changed | Always-Loaded | Agent Pool |
|-------|-------------|---------------|------------|
| **1: Architectural** | Merged critics, replaced 1,213-line planner with 180-line skill | 181 | 1,066 |
| **2: Structural** | Removed model-known content, dropped templates | 68 | 464 |
| **3: Terse + Principled** | `Rule — reason.` format, cut filler, added rationale | 45 | 251 |
| **4: Dynamic Domains** | On-demand loading, ~15 line orchestrator | ~15 | 251 |

**The takeaway:** Agent instructions load on every invocation. A 500-line agent burns 2,000+ tokens before doing any work. But the answer isn't stripping reasons to save tokens — it's stripping everything *except* rules and reasons, and loading context *only when it's needed*. Principles are load-bearing structure. Templates and re-explanations are scaffolding you remove once the building stands.

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
- Just want domains? Copy `domains/` and the domain table from CLAUDE.md.
- Just want SaaS planning? Copy `skills/plan-saas/` + `domains/plan-saas.md`.

### Requirements

- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** CLI, installed and authenticated
- **No other dependencies** — secret scanning uses [xswarm-ai-sanitize](https://github.com/chadananda/xswarm-ai-sanitize) via npx
- *Optional:* Playwright MCP for web testing, VHS for TUI testing

---

## Design Decisions

<details>
<summary><b>Why domains instead of one big CLAUDE.md?</b></summary>
A monolithic CLAUDE.md with all domain knowledge loads everything into every conversation. SEO schema deprecation rules compete for attention during feature development. TDD agent pipelines create noise during content planning. Domains solve both the token cost problem (don't load what you don't need) and the attention quality problem (don't distract the model with irrelevant constraints). Each domain can be thousands of lines deep without affecting any other domain.
</details>

<details>
<summary><b>Why Claude classification instead of keyword hooks?</b></summary>
Keyword regex (like Carl's approach) misfires on ambiguous words and requires maintaining a Python hook. Claude itself is the best classifier — it understands intent, not just keywords. Zero external scripting, perfect accuracy, ~10 lines in CLAUDE.md.
</details>

<details>
<summary><b>Why reference sub-files for SEO and SaaS planning?</b></summary>
Both domains require knowledge Claude doesn't have natively — deprecated schema types, current CWV thresholds, SaaS pricing benchmarks, guerrilla marketing tactics with specific numbers. The domain file loads methodology and rules. Reference files load perishable domain knowledge on demand per sub-task. SEO: ~231 lines across 5 files. SaaS planning: ~790 lines across 9 files. Neither pollutes the other or loads when unused.
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

**Want to add a domain?** Create a `.md` file in `domains/` and add a row to the domain table in CLAUDE.md. That's it. No code changes. Your new domain can be 10 lines or 1,000 — it only loads when the activity matches.

**Don't like strict TDD?** Edit `agents/TDD.md`. Or delete it entirely.

**Want different models?** Each agent has a `model:` field in its frontmatter. Swap `sonnet` for `opus` where you want brains, `haiku` where you want speed.

**Want to add agents?** Create a `.md` file in `agents/` with YAML frontmatter (name, description, tools, model).

**Want project-specific behavior?** Create `.claude/CLAUDE.md` in your project root. Project-level instructions override global ones.

---

## The xswarm Connection

This repo is the petri dish for [xswarm](https://xswarm.ai) — an autonomous agent swarm framework for 2026. Everything here started as an experiment:

- **Domain switching** — isolated context loading makes each domain arbitrarily deep without cross-contamination.
- **Team-lead pipeline** — managers work better when they can't write code; they focus on routing and quality.
- **Stuck protocol** — agents that can't guess eliminated more wasted time than any other change.
- **TDD enforcement** — making test-first structural, not aspirational, changed everything.
- **Harness compression** — token efficiency is an architecture concern, not an optimization.

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
