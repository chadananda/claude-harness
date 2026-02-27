# Phase 2: Strategy & Positioning

## Setup

Read `viability-report.md` from the current working directory. This is your primary context for the entire phase — do not ask about anything already covered there.
Read `references/icp-framework.md` for the 5-layer ICP model and interview prompts.
Read `references/pricing-models.md` for SaaS pricing patterns and selection criteria.
Read `templates/strategy-brief.md` for the required output structure.

Open by summarizing Phase 1 findings to the user in 3-4 sentences: the idea, the score, the strongest factor, and the factor that needs the most attention in strategy work. Then say: "Now we'll sharpen who you're building for, how you position it, and what you'll charge."

---

## ICP Development

Work through the 5-layer model to build a precise Ideal Customer Profile. Research between layers, not just at the end. Ask the user 2-3 targeted questions during this section — not all at once.

### Layer 1: Problem Identity

Identify who has this problem most acutely and what triggers their search for a solution.

WebSearch:
- "[problem description] Reddit complaints"
- "[product category] who uses it"
- "when do [target users] need [solution]"
- "[problem] trigger event"

Share what you find: where are people complaining about this problem, what language do they use, what's the specific moment they realize they need a solution?

Ask the user: "What's the triggering event — what happens that makes someone suddenly need your product today rather than next month?"

---

### Layer 2: Buyer Profile

Define the buyer's professional context: company size, role/title, industry vertical, budget authority.

WebSearch:
- "job postings mentioning [problem or tool category]"
- "[target role] responsibilities [industry]"
- "[product category] typical buyer title"
- "[company size] [industry] software budget"

Share findings: what job titles show up most, what company sizes the problem fits, whether this is a department budget or individual decision.

Ask the user: "Who signs the check — is this an individual contributor buying on a credit card, or does it require manager or executive approval?"

---

### Layer 3: Psychographics

Understand what this buyer values, their risk tolerance, and how painful the status quo is.

Research their current workaround — what are they doing instead right now?

WebSearch:
- "[target role] current workflow [problem area]"
- "[target role] tools used for [task]"
- "why [target users] don't switch from [current solution]"
- "[product category] early adopters vs mainstream"

Determine: early adopter (will try new tools, tolerates rough edges) or pragmatist (needs proven, safe, references). This affects messaging and sales motion.

Note their status quo pain level — is this a "nice to have" or a "I cannot do my job without fixing this"?

---

### Layer 4: Watering Holes

Find the specific online and offline places where this ICP congregates. Be specific — name actual communities, not categories.

WebSearch:
- "[target role] Slack communities OR Discord"
- "[industry] forums subreddits"
- "[target role] newsletter podcast"
- "[product category] community"
- "[industry] conferences events 2025"

Output must include named, real watering holes: specific subreddit names, Slack group names, newsletters, LinkedIn groups, conferences, and podcasts. Generic answers ("they use LinkedIn") are not acceptable.

Ask the user: "Are you already a member of any of these communities? Do you have any presence or trust built with this audience?"

---

### Layer 5: Buying Behavior

Understand how this ICP evaluates and purchases software, who else is involved, and what the typical timeline looks like.

WebSearch:
- "[product category] self-serve vs sales-led"
- "how [target role] evaluates [category] software"
- "[target role] software buying process"
- "[product category] average sales cycle"
- "[product category] PLG OR sales-led growth"

Determine: product-led (sign up, try, buy) or sales-led (demo, proposal, contract). This determines the entire go-to-market motion.

Note: number of stakeholders in the decision, typical evaluation timeline, what proof they need (trial, case studies, security review, pilot).

---

## Positioning Framework

Synthesize ICP research into a complete positioning framework. Develop each element:

**Category**: What existing category does this fit, or what new category does it create? Entering an existing category is faster; creating a new one requires more education budget.

**For [ICP]**: One sentence describing the exact buyer. Be specific — "for B2B SaaS growth teams at Series A-C companies" not "for businesses."

**Who [problem]**: The specific frustration or unmet need. Use language from the Reddit/forum research — the words your ICP actually uses.

**Unlike [alternative]**: Name the primary alternative. This is what they're doing now, not necessarily a direct competitor.

**We [differentiator]**: The single most important way you're different. One thing, not a list.

**Value proposition**: One sentence combining the above. Formula: "We help [ICP] [achieve outcome] by [mechanism] unlike [alternative]."

**Tagline**: 5-7 words. Memorable. Outcome-focused. Avoid feature language.

**Elevator pitch** (30 seconds): Problem (1 sentence) → Solution (1 sentence) → Why us (1 sentence) → Ask (1 sentence).

Present the full framework to the user. Ask: "Does this resonate with how you'd describe it to a potential customer? What feels off?" Iterate on positioning if the user identifies a gap — positioning is useless if the founder won't say it.

---

## Pricing Strategy

Research competitor pricing before making any recommendations.

WebSearch for each major competitor's pricing page (aim for 3-5 competitors):
- "[competitor 1] pricing"
- "[competitor 2] pricing plans"
- "[product category] pricing comparison"
- "[product category] free tier OR freemium"
- "how much does [category] software cost"

Present a pricing landscape table: competitor name, model (flat/tiered/seat/usage/freemium), entry price, what's included, enterprise tier if visible.

Then recommend a specific pricing structure with justification:

**Model**: Which pricing model fits this product and buyer (flat-rate, tiered, per-seat, usage-based, freemium+paid, hybrid). Justify with: how value is delivered, how the ICP thinks about cost, what competitors use.

**Tiers**: Name each tier, price, what's included, and who it's for. Provide actual dollar amounts — "competitive pricing" is not a recommendation.

**Free tier**: Yes or no, and why. If yes: what's included and what's the conversion trigger. If no: trial instead, or neither.

**Anchor and expand**: Identify the tier most customers will start on and what drives upgrades.

Justify pricing with data: "Competitors charge $X-Y/mo for similar scope. Your differentiation on [factor] supports pricing at the higher end of that range" or "Your ICP is price-sensitive at the SMB level — start at $Z to reduce friction."

Ask the user: "Where does this feel off relative to what you'd be comfortable charging? Any concerns about the free tier recommendation?" Adjust if the user has strong business model constraints.

---

## Output

Read `templates/strategy-brief.md`. Write `strategy-brief.md` in the current working directory.
Fill every section with specific, researched content.
The ICP section must name real communities and use real language from research.
The positioning section must include all framework elements — no blanks.
The pricing section must cite actual competitor prices and give specific dollar amounts.
No placeholder text. No generic descriptions.

---

## Transition

If running the full pipeline: announce that strategy is complete, name the output file, give a one-sentence summary of the positioning and pricing recommendation. Then proceed to Phase 3 by reading `skills/plan-technical.md`.

If strategy-only (`strategy` argument): deliver `strategy-brief.md`, summarize the ICP in one paragraph, and suggest: "Run `/plan-saas technical` when you're ready to spec the build."
