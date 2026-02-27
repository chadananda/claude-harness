# Phase 1: Viability Assessment

## Setup

Read `references/viability-scoring.md` for detailed scoring rubrics and challenge prompt templates.
Read `templates/viability-report.md` for the required output structure.
If `$ARGUMENTS` contains an idea description, use it as context — do not re-ask "what's your idea."
Announce to the user: "I'll walk you through a 6-question viability interview. Between questions I'll do market research and share what I find. This process scores your idea across 5 factors — a score under 10 means we iterate before proceeding."

## Interview Flow

Ask questions one at a time. After each response: run WebSearch, share findings, then challenge before scoring.
Never batch questions. Never skip the research step. Never score without showing evidence.

---

### Question 1: Problem & Customer

Ask: "What specific problem are you solving, and who experiences this problem most painfully?"

After response, WebSearch:
- "[problem description] existing solutions"
- "[target customer] biggest frustrations [category]"
- "[problem] Reddit OR forum complaints"
- "startups solving [problem]"

Share findings: name specific products, communities complaining about this problem, and any data on how widespread it is.
Confirm the problem is real and unsolved before moving on. If research shows the problem is already well-solved, flag it now.

---

### Question 2: Product Factor — 10x Better

Ask: "How is your solution 10x better than [name specific competitors from research]?"

WebSearch:
- "[competitor 1] features pricing reviews"
- "[competitor 2] G2 OR Capterra reviews complaints"
- "[solution approach] limitations"
- "why [category] solutions fail"

Share findings: what competitors charge, what users complain about, where the gaps are.
Challenge: identify the weakest product claim with specific evidence. Example: "Competitor X already does Y — how is your approach meaningfully different?"

Score using rubric from `references/viability-scoring.md`:
- 0: Not meaningfully better than existing options
- 1: Incrementally better (10-30% improvement)
- 2: Significantly better (2-5x improvement)
- 3: Transformatively better (10x+ improvement, clear breakthrough)

**If score is 0**: This is a disqualifying factor. Explain exactly why with evidence. Ask: "Can you describe a specific user scenario where your solution is dramatically better? Or is there a pivot that creates that 10x difference?" Wait for response. Re-score if new insight warrants it.

---

### Question 3: Acquisition Factor — First 100 and 10,000 Users

Ask: "How will you acquire your first 100 users? Your first 10,000?"

WebSearch:
- "how [target users] discover [product category] tools"
- "[product category] customer acquisition strategy"
- "distribution channels [industry]"
- "[target role] communities forums newsletters"
- "cost to acquire [target customer type]"

Share findings: name specific channels that work in this space, typical CAC, any viral patterns you found.
Challenge: acquisition cost realism, channel saturation, founder distribution advantage (or lack of it).

Score:
- 0: No viable path to users — no channel, no network, no budget
- 1: Difficult acquisition (high CAC, no differentiation, cold outreach only)
- 2: Viable acquisition (proven channels exist, reasonable CAC, clear plan)
- 3: Built-in distribution advantage (audience, virality, partnerships, existing channel)

**If score is 0**: Disqualifying. Ask: "Do you have any existing audience, community access, or partnerships? Is there a distribution channel you haven't mentioned?"

---

### Question 4: Market Factor — Size and Growth

Ask: "What's your estimate of the TAM, SAM, and SOM? Is this market growing?"

WebSearch:
- "[industry] market size 2024 2025"
- "[product category] TAM growth rate"
- "venture capital investment [space] 2023 2024"
- "[industry] trends forecast"
- "[target segment] spending [category]"

Share findings: cite specific numbers from reports, name which VCs are active in the space, call out any conflicting data.
Challenge: is the market definition too narrow (niche with no path to scale) or too broad (unfocused)? Push for a realistic SOM with a credible capture path.

Score:
- 0: Market too small (<$50M TAM) or in structural decline
- 1: Small market (<$100M) or slow/flat growth
- 2: Medium market ($100M-$1B) with meaningful growth
- 3: Large market (>$1B) with strong growth tailwinds or structural shift driving it

**If score is 0**: Disqualifying. Ask: "Is there an adjacent or broader market framing that's larger? Or a timing argument — is this market about to emerge?"

---

### Question 5: Defendability Factor — Hard to Copy

Ask: "Once you've succeeded, what makes this hard for a competitor or a well-funded startup to copy?"

WebSearch:
- "moats defensibility [product category]"
- "why [successful competitor in space] is hard to compete with"
- "network effects [industry] examples"
- "[space] open source alternatives"
- "big tech [Google OR Microsoft OR Amazon] [product category]"

Share findings: what moat patterns exist in this space, whether big tech is a threat, whether open source undercuts the value prop.
Challenge: copycat risk, big-tech entry, open-source displacement. Be specific: "I found an open-source project doing X — does that eliminate your moat?"

Score:
- 0: Easily copied — no structural advantages, feature-level differentiation only
- 1: Some barriers but vulnerable (brand, partial switching costs)
- 2: Multiple moats with reasonable defensibility (switching costs + data or network)
- 3: Strong structural moats (network effects, proprietary data, high switching costs, regulatory)

**If score is 0**: Disqualifying. Ask: "What moat could you build over 12-18 months of execution? Data advantage? Community lock-in? Workflow depth?"

---

### Question 6: Buildability Factor — Can You Execute

Ask: "Can you actually build this? What's your unfair execution advantage — skills, domain expertise, existing assets?"

WebSearch:
- "technical requirements building [product type]"
- "[similar product] team size funding raised"
- "MVP timeline [product category]"
- "regulatory requirements [industry] SaaS"
- "[technology] complexity implementation"

Share findings: what it actually takes to build this (team, time, capital), what similar companies raised and when they shipped.
Challenge: execution risk, timeline realism, skill gaps, regulatory hurdles.

Score:
- 0: Critical capability gaps with no realistic path to fill them
- 1: Very difficult — long timeline, high capital requirements, major skill gaps
- 2: Challenging but achievable with realistic resources
- 3: Unfair execution advantage — domain expertise, existing assets, prior builds in this space

**If score is 0**: Disqualifying. Ask: "Is there a simpler MVP that removes the hard dependency? A co-founder who fills the gap? A no-code approach to validate first?"

---

## Scoring

Calculate: Product × Acquisition × Market × Defendability × Buildability = Total

Zones:
- 0-9 Red: Below viability threshold — iterate before proceeding
- 10-19 Yellow: Promising but needs refinement
- 20-49 Green: Solid — worth building and validating
- 50-99 Elite: Strong potential, venture-backable territory
- 100+ Unicorn: Exceptional — execute immediately

**Gate: score must be ≥10 to proceed to Phase 2.**

If Red zone: identify the 1-2 lowest-scoring factors. Ask targeted questions to help improve each score. Re-score after each significant new insight. Do not proceed to Phase 2 until score reaches Yellow or above.

When presenting scores, show each factor with a one-sentence justification referencing specific evidence from research.

---

## Output

Read `templates/viability-report.md`. Write `viability-report.md` in the current working directory.
Fill every section with specific data from research and interview responses.
No placeholder text. Every competitor named must be real and researched. Every market number must have a source.
Include all 5 factor scores with the evidence and research that determined each score.

---

## Transition

If running the full pipeline (idea or resume, not validate-only):
Announce total score, zone, and the one sentence each factor earned. Then proceed to Phase 2 by reading `skills/plan-strategy.md`.

If validate-only (`validate [idea]` argument):
Announce score and zone. Deliver `viability-report.md`. Provide next-step recommendations based on zone:
- Red: "Focus on improving [factor 1] and [factor 2] before building."
- Yellow: "Promising. Consider validating [weakest factor] with 10 customer conversations before Phase 2."
- Green+: "Solid foundation. Phase 2 strategy work will sharpen positioning and pricing."
