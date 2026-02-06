---
allowed-tools: Read, Write, Bash(*), WebSearch, WebFetch
description: Validate startup ideas through conversational interview, market research, and 5-factor scoring. Generates validation report and PRD.
argument-hint: "[optional: idea description]"
model: sonnet
---

# Startup Idea Validator

I'll help you validate your startup idea through a structured interview and market research. This process uses a 5-factor framework to score your idea across Product, Acquisition, Market, Defendability, and Buildability.

**Scoring System:**
- Each factor: 0-3 points (0 = disqualifier, stops immediately)
- Total = Product × Acquisition × Market × Defendability × Buildability
- Zones: 0-9 🔴 Red, 10-19 🟡 Yellow, 20-49 🟢 Green, 50-99 🏆 Elite, 100+ 🦄 Unicorn
- Minimum to proceed: 10 points (Yellow zone)

---

## Phase 1: Initial Understanding

$ARGUMENTS

Let me start by understanding your idea.

**Question 1: What problem are you solving, and for whom?**

[Wait for response]

---

## Phase 2: Product Factor (10x Better)

Now let's evaluate if your solution is dramatically better than alternatives.

**Research Phase:** Let me research existing solutions...

[Use WebSearch to find:
1. "existing solutions for [problem]"
2. "competitors for [solution]"
3. "alternative approaches to [problem]"
4. "[industry] market leaders"
5. "new startups in [space]"]

**Based on my research, here are the current alternatives:**

[Summarize findings]

**Question 2: How is your solution 10x better than these alternatives?**

Consider:
- Is it 10x faster, cheaper, easier, or more effective?
- What's the unfair advantage or breakthrough insight?
- Why can't existing players easily replicate this?

[Wait for response]

**Challenge Question:** [Based on research, identify weakest aspect and challenge constructively]

[Wait for response]

**Product Score:**
- 0 points: Not meaningfully better ⚠️ DISQUALIFYING
- 1 point: Incrementally better (10-30% improvement)
- 2 points: Significantly better (2-5x improvement)
- 3 points: Transformatively better (10x+ improvement)

**Your Product Score: [0/1/2/3]**

[If 0: "⚠️ This is currently a disqualifying factor. A score of 0 means the idea isn't viable as-is. Can you think of any way to make your solution dramatically better than alternatives? Any pivot or adjustment that would create a 10x improvement?"]

[Wait for response if 0, potentially re-score if they have new insights]

---

## Phase 3: Acquisition Factor (Find Users)

Let's evaluate how you'll find and acquire users.

**Research Phase:** Let me research acquisition channels...

[Use WebSearch to find:
1. "how do [target users] discover new [product category]"
2. "[industry] customer acquisition strategies"
3. "viral growth examples in [space]"
4. "distribution channels for [product type]"
5. "marketing channels for [target demographic]"]

**Based on my research, here are common acquisition channels in your space:**

[Summarize findings]

**Question 3: How will you acquire your first 100 users? Your first 10,000?**

Consider:
- Do you have existing audience, distribution, or network?
- Are there natural viral loops or word-of-mouth mechanics?
- What's your unfair distribution advantage?
- Which acquisition channels are proven in this space?

[Wait for response]

**Challenge Question:** [Based on research, identify acquisition risks and challenge]

[Wait for response]

**Acquisition Score:**
- 0 points: No clear path to users ⚠️ DISQUALIFYING
- 1 point: Difficult acquisition (high CAC, slow growth)
- 2 points: Viable acquisition (proven channels, reasonable CAC)
- 3 points: Built-in virality or distribution advantage

**Your Acquisition Score: [0/1/2/3]**

[If 0: "⚠️ This is currently a disqualifying factor. A score of 0 means you have no viable way to reach users. Can you think of any distribution channels, partnerships, or growth strategies that could work? Any way to tap into existing user bases or communities?"]

[Wait for response if 0, potentially re-score if they have new insights]

---

## Phase 4: Market Factor (Size & Growth)

Let's evaluate the market opportunity.

**Research Phase:** Let me research the market...

[Use WebSearch to find:
1. "[industry] market size 2024"
2. "[product category] TAM SAM SOM"
3. "[space] market growth rate"
4. "[industry] trends and forecasts"
5. "venture capital investment in [space]"
6. "[target demographic] spending on [category]"]

**Based on my research, here's the market landscape:**

[Summarize findings with specific numbers]

**Question 4: What's the market size and growth trajectory?**

Consider:
- TAM (Total Addressable Market): Full market potential
- SAM (Serviceable Addressable Market): Your realistic segment
- SOM (Serviceable Obtainable Market): What you can capture in 3-5 years
- Is the market growing, flat, or declining?
- Are there tailwinds (trends, regulations, technology shifts)?

[Wait for response]

**Challenge Question:** [Based on research, challenge market assumptions]

[Wait for response]

**Market Score:**
- 0 points: Market too small or declining ⚠️ DISQUALIFYING
- 1 point: Small market (<$100M) or slow growth
- 2 points: Medium market ($100M-$1B) with growth
- 3 points: Large market (>$1B) with strong growth tailwinds

**Your Market Score: [0/1/2/3]**

[If 0: "⚠️ This is currently a disqualifying factor. A score of 0 means the market is too small or declining. Can you reframe the market opportunity? Perhaps you're defining it too narrowly, or there's an adjacent market that's larger? Any expansion opportunities?"]

[Wait for response if 0, potentially re-score if they have new insights]

---

## Phase 5: Defendability Factor (Hard to Copy)

Let's evaluate your competitive moats.

**Research Phase:** Let me research competitive dynamics...

[Use WebSearch to find:
1. "moats and defensibility in [industry]"
2. "why [successful competitor] is defensible"
3. "barriers to entry in [space]"
4. "network effects in [product category]"
5. "data moats in [industry]"
6. "patents and IP in [space]"]

**Based on my research, here are defensibility patterns in your space:**

[Summarize findings]

**Question 5: What makes your solution hard to copy?**

Consider:
- Network effects (value grows with users)
- Data moats (unique proprietary data)
- Brand/reputation (hard-earned trust)
- Technology (patents, trade secrets, complexity)
- Switching costs (expensive/hard to leave)
- Scale economies (bigger = lower costs)
- Regulatory moats (licenses, compliance)

[Wait for response]

**Challenge Question:** [Based on research, identify copycat risks and challenge]

[Wait for response]

**Defendability Score:**
- 0 points: Easily copied by competitors ⚠️ DISQUALIFYING
- 1 point: Some barriers but vulnerable
- 2 points: Multiple moats, reasonable defensibility
- 3 points: Strong structural moats (network effects, data, high switching costs)

**Your Defendability Score: [0/1/2/3]**

[If 0: "⚠️ This is currently a disqualifying factor. A score of 0 means any competitor can copy you easily. Can you think of any moats you could build? Network effects, proprietary data, brand, switching costs, regulatory barriers, or technology advantages? Any way to make this harder to replicate?"]

[Wait for response if 0, potentially re-score if they have new insights]

---

## Phase 6: Buildability Factor (Can Execute)

Let's evaluate your ability to execute.

**Research Phase:** Let me research execution requirements...

[Use WebSearch to find:
1. "technical requirements for building [product type]"
2. "common challenges building [solution]"
3. "time to market for [product category]"
4. "team composition for [industry] startups"
5. "funding requirements for [space]"
6. "MVP examples in [category]"]

**Based on my research, here are common execution challenges:**

[Summarize findings]

**Question 6: Can you actually build this?**

Consider:
- Do you have the technical skills or team to build it?
- What's the MVP timeline? (Faster = better)
- What resources do you need? (Capital, expertise, partnerships)
- Are there insurmountable technical/regulatory hurdles?
- Have similar products been built successfully?

[Wait for response]

**Challenge Question:** [Based on research, identify execution risks and challenge]

[Wait for response]

**Buildability Score:**
- 0 points: Can't execute (missing critical skills/resources) ⚠️ DISQUALIFYING
- 1 point: Very difficult, long timeline, high resource needs
- 2 points: Challenging but achievable with reasonable resources
- 3 points: You have unfair execution advantage (domain expertise, existing assets)

**Your Buildability Score: [0/1/2/3]**

[If 0: "⚠️ This is currently a disqualifying factor. A score of 0 means you lack critical capabilities to build this. Can you acquire the missing skills/resources? Bring on a co-founder? Partner with someone who has the expertise? Simplify the MVP to something you CAN build?"]

[Wait for response if 0, potentially re-score if they have new insights]

---

## Phase 7: Final Calculation & Report

**Your Scores:**
- Product (10x Better): [X] / 3
- Acquisition (Find Users): [X] / 3
- Market (Size & Growth): [X] / 3
- Defendability (Hard to Copy): [X] / 3
- Buildability (Can Execute): [X] / 3

**Total Score: [Product × Acquisition × Market × Defendability × Buildability] = [X]**

**Zone: [🔴 Red / 🟡 Yellow / 🟢 Green / 🏆 Elite / 🦄 Unicorn]**

---

[If score < 10: "Your idea scored in the 🔴 Red Zone, which is below the viability threshold. This doesn't mean the idea is worthless, but it needs significant refinement before pursuing. Review the factors where you scored 0 or 1 - those are the critical areas to improve. I won't generate full deliverables for Red Zone ideas, but here's a brief assessment of the key challenges and potential paths forward:

[Brief summary of weaknesses and suggestions for improvement]

Would you like to iterate on any of these factors to see if we can improve the score?"]

[If score >= 10: Continue to generate deliverables]

---

## Generating Deliverables

Creating comprehensive validation report and PRD...

### File 1: validation-report.md

[Create detailed validation report with:
- Executive Summary
- Idea Overview
- 5-Factor Analysis (detailed scores with evidence)
- Market Research Summary
- Competitive Landscape
- Risk Assessment
- Recommendations
- Next Steps]

### File 2: PRD.md (Product Requirements Document)

[Create PRD with:
- Vision & Objectives
- Target Users & Personas
- Core Features (MVP)
- User Stories
- Success Metrics
- Technical Requirements
- Go-to-Market Strategy
- Milestones & Timeline
- Resource Requirements]

---

**✅ Validation Complete**

Your idea scored **[X] points** in the **[Zone]** zone.

**Deliverables created:**
- `validation-report.md` - Comprehensive validation analysis
- `PRD.md` - Product Requirements Document

**Recommended next steps:**
[Based on score zone, provide specific recommendations]

[If 10-19 Yellow: "Promising but needs refinement. Focus on improving [weakest factors]"]
[If 20-49 Green: "Solid idea worth pursuing. Build MVP and validate with users."]
[If 50-99 Elite: "Strong potential. This could be venture-backable. Start building immediately."]
[If 100+ Unicorn: "Exceptional opportunity. This has unicorn potential if executed well."]
