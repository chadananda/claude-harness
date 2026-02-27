# Phase 4: Go-to-Market & Marketing Calendar

## Setup

Read `viability-report.md`, `strategy-brief.md`, and `software-prd.md` from the current working directory. All three must exist — if any is missing, tell the user and stop.

Read ALL marketing reference files before beginning:
- `references/seo-strategy.md`
- `references/content-marketing.md`
- `references/guerrilla-playbook.md`
- `references/distribution-channels.md`
- `references/launch-sequence.md`

Read `templates/marketing-prd.md` for the required output structure.

Open with a full-picture summary: "[Product] for [ICP] at [$price/mo], launching with [MVP features], solving [core problem], competing against [named competitors]." Then proceed.

## Keyword Universe

Build a keyword table of 20–30 keywords. Use WebSearch with these query patterns:
- "[problem the product solves]"
- "best [product category]"
- "how to [job-to-be-done]"
- "[top competitor] alternative"
- "[use case] software" or "[use case] tool"

For each keyword, estimate search volume (use qualitative tiers: <500/mo, 500–5K, 5K–50K, 50K+), difficulty (low/medium/high based on SERP competition), and funnel stage.

| Keyword | Volume (est.) | Difficulty | Funnel Stage | Priority |
|---------|--------------|------------|--------------|----------|

Funnel stages: BOFU (buying intent — "buy", "pricing", "alternative", "best X for Y"), MOFU (evaluating — "how to", "guide", "comparison"), TOFU (awareness — broad problem or industry terms).

Prioritize BOFU first — closest to revenue, most valuable at launch. Then MOFU. TOFU is a long game; deprioritize at MVP stage.

## Content Architecture

Design a pillar/cluster model from the keyword universe:

**Pillar pages (2–3 total)**: Comprehensive guides targeting high-volume MOFU keywords (2,000–4,000 words). Each pillar should be the definitive resource on a core topic the ICP searches for. Name the actual pillar titles.

**Cluster articles (5–8 per pillar)**: Shorter pieces (800–1,500 words) targeting long-tail variations and BOFU keywords. Each cluster links back to its pillar. Name specific article titles — not "article about X" but the actual H1.

**Internal linking strategy**: Every cluster article links to its pillar in the first 200 words. Pillar pages link to each cluster in a "related guides" section. Cross-link clusters that share themes.

**High-value standalone pages**: Competitor comparison pages ("[Product] vs [Competitor]"), use-case pages ("[Product] for [industry]"), and a pricing page built around BOFU keywords.

## 12-Week Content Calendar

Week-by-week plan with specific titles and keywords. Each entry:

| Week | Title | Target Keyword | Funnel Stage | Type | Distribution |
|------|-------|---------------|--------------|------|--------------|

**Weeks 1–4 (Foundation)**: Publish pillar pages and 2–3 BOFU articles. These take longest and have the longest ranking ramp — start immediately.

**Weeks 5–8 (Cluster expansion)**: Ship cluster articles, comparison pages, and use-case landing pages. Interlink aggressively as new content publishes.

**Weeks 9–12 (Scale)**: TOFU thought leadership pieces, guest post targets, and the first content amplification via community and social.

Distribution column should name the actual channel: "post in [community]", "LinkedIn + Twitter thread", "pitch to [newsletter type]", "email list."

## Programmatic SEO

Identify template page opportunities: patterns where one content template scales across many variations.

Common patterns for SaaS: "[Product] for [industry]" (10–20 industries), "[Competitor] alternative" (5–10 competitors), "[Job title] guide to [problem]", "[City/region] [service category]" if location-relevant.

For each pattern, estimate: number of pages, effort to build, expected search volume per page.

Only recommend programmatic SEO if the volume/effort ratio is worth it at MVP stage. For most early-stage SaaS, 1–2 patterns max.

## GEO and AEO Optimization

GEO (Generative Engine Optimization — appearing in AI-generated answers):
- Structure content with definition-first paragraphs: answer the question in the first sentence, then expand.
- Use question-based H2/H3 headings that mirror exact search queries.
- Include structured "what is X", "how does X work", "who uses X" sections on pillar pages.
- Add entity optimization: mention product category, use cases, and competitor names naturally.

AEO (Answer Engine Optimization — featured snippets and voice search):
- Add FAQ sections to every pillar and cluster article (5–8 Q&A pairs each).
- Use FAQ schema markup on all content pages.
- Write answer paragraphs of 40–60 words — the ideal featured snippet length.

## Guerrilla Marketing Plan

Pull the ICP watering holes from `strategy-brief.md`. Every tactic below should name specific communities, not generic channel types.

### Pre-Launch (Weeks 1–4)

**Build-in-public**: Post weekly progress updates on Twitter/X and LinkedIn. Share what you're building and why — problems encountered, decisions made, early user conversations. Cadence: 2–3 posts per week. Never pitch — share and teach.

**Waitlist mechanics**: Set up a referral waitlist (ReferralHero or a simple viral loop). Offer early access tiers: first 100 get [concrete benefit], refer 3 people to skip the queue. Give the waitlist a specific name to create identity.

**Community presence**: Name 3–5 specific communities from the ICP watering holes. In weeks 1–4, contribute genuinely without pitching — answer questions, share useful resources, build credibility. Do not post about the product yet.

**Cold outreach**: Identify the first 20 ideal customers. Find them in communities, on LinkedIn, or via Twitter. Personalized 3-sentence email: context about them, the problem you're solving, ask for a 20-minute call — not a demo. Expected response rate: 15–25% with good personalization.

### Launch Week (Week 8)

**Product Hunt**: Assign a hunter (ideally someone with 1K+ followers), schedule for a Tuesday–Thursday launch. Prep: 50+ supporters lined up before launch day, gallery with real product screenshots, first comment written in advance. Launch day: post in communities at 12:01 AM PST, personal outreach to network for upvotes.

**Community announcements**: Write specific posts for each named community. Each post should be native to that community's tone — not a press release. Lead with the problem, not the product. Include a "we built this because..." story.

**Micro-influencer outreach**: Identify 5–10 creators, bloggers, or newsletter authors who reach the ICP. Offer early access + a story angle, not a paid placement. Target people with 1K–50K engaged followers — response rate is higher than large accounts.

**Launch day social cadence**: Morning (announcement thread with story), midday (screenshot of early traction), evening (thank you + ask for feedback). Don't be silent after the initial post.

### Post-Launch (Weeks 9–12)

**Case studies**: Recruit 2–3 early users for detailed case studies. Format: before/after with specific metrics. Publish on the blog and distribute in communities as value, not ads.

**Referral program**: Launch a formal referral program once you have 25+ active users. Offer a month free per successful referral. Use Rewardful or a simple manual process at first.

**Partnership plays**: Identify 3–5 adjacent tools the ICP already uses. Reach out to their teams about a mutual listing swap (your tool in their integrations list, theirs in yours). This is a low-effort channel with compounding returns.

**Free tool play**: If applicable, build one small free tool that solves a peripheral problem the ICP has. Host it on your domain. Use it to capture emails and rank for BOFU keywords. Requires only 1–2 days of engineering work for simple tools.

## Channel Strategy

Select 3 primary channels and 2 secondary channels. Tie each choice to the ICP from `strategy-brief.md` — channels only work if the ICP actually uses them.

For each channel:
- Why it fits this specific ICP (evidence, not assumption)
- Expected time-to-first-results (organic SEO: 3–6 months; community: 2–4 weeks; cold outreach: 1–2 weeks)
- Effort level: high/medium/low
- Key metric to track

WebSearch: search "[ICP job title] where do you hang out online", "[product category] marketing channels", "[competitor] traffic sources" (use SimilarWeb or competing tools). Verify your channel assumptions against real data.

## 12-Week Launch Sequence

Week-by-week checklists. Be specific — not "set up social media" but "create Twitter/X account, write bio, pin a build-in-public intro thread."

**Weeks 1–4 (Foundation)**:
- Brand assets: logo, color palette, domain, social handles
- Content pipeline: write and schedule weeks 1–4 content calendar articles
- Waitlist page live with referral mechanics by end of week 1
- Community accounts active and contributing (not pitching) by week 2
- Cold outreach list built (100 names) and first 20 emails sent by week 3
- Collect 3–5 problem-validation interviews, document findings

**Weeks 5–7 (Pre-launch)**:
- Recruit 10–20 beta users from waitlist and cold outreach
- Collect first testimonials and usage data
- Product Hunt assets prepared: tagline tested, gallery finalized, supporter list at 30+
- Micro-influencer outreach sent: 10 pitches, 2–3 confirmations as goal
- Launch day announcement posts drafted for each community

**Week 8 (Launch)**:
- Monday: final supporter outreach, share private preview with beta users
- Tuesday–Thursday: Product Hunt launch day (choose one)
- Launch day hour-by-hour: post at 12:01 AM, check-in at 6 AM, community posts at 9 AM, midday update, evening summary
- Respond to every comment and DM within the hour on launch day

**Weeks 9–12 (Post-launch)**:
- Week 9: Analyze which channels drove signups — double down on top two
- Week 10: Publish first case study, launch referral program
- Week 11: Partnership outreach to 5 adjacent tools
- Week 12: Review organic keyword rankings, assess paid acquisition readiness

## Paid Acquisition Framework

Do not start paid acquisition until organic channels demonstrate PMF signals: 25+ active users, measurable retention, NPS above 30.

When ready:
- Start at $20–30/day — enough data to optimize, low enough to not burn budget on bad creative
- Test one channel at a time with a $500 minimum budget and 2-week window before evaluating
- Scale only when CAC < LTV / 3

Channel priority:
1. Google Ads (BOFU keywords): highest intent, easiest to measure, start here
2. Retargeting (Meta or LinkedIn): re-engage site visitors, requires 1,000+ pixel events to work well
3. Content amplification (native ads, newsletter sponsorships): MOFU, builds awareness alongside organic

Track: CAC per channel, trial-to-paid conversion rate, LTV by acquisition source.

## Email Sequences

### 7-Email Onboarding Drip

Write specific subject lines and one-sentence content descriptions for each email. Adapt to the actual product's core feature and ICP.

- Email 1 (Day 0): Welcome + one-step quick start. Subject: "You're in — here's where to start." Get them to the first value moment within 5 minutes.
- Email 2 (Day 1): Core feature tutorial. Subject: "[Specific feature] in 3 steps." Short, visual if possible.
- Email 3 (Day 3): Use case story. Subject: "How [ICP persona] uses [product] to [outcome]." Build aspiration.
- Email 4 (Day 5): Pro tip or advanced feature. Subject: "Most people miss this in [product]." Reward early engagement.
- Email 5 (Day 7): Check-in + feedback ask. Subject: "Quick question." One question only — reply-based.
- Email 6 (Day 10): Social proof + case study. Subject: "[Specific result] in [timeframe]." Concrete outcome.
- Email 7 (Day 14): Upgrade nudge (freemium) or retention ask (paid). Subject: depends on model — see Phase 2 pricing.

### Weekly Newsletter Framework

Content mix per issue: one actionable insight relevant to the ICP (not about the product), one product update or tip, one curated external resource.

Subject line patterns that work for SaaS audiences: questions ("[Problem] — are you doing this?"), numbers ("5 [things] that [outcome]"), controversy ("[common belief] is wrong"), curiosity gaps ("The reason most [ICP] fail at [task]").

Send cadence: weekly, same day and time. Tuesday–Thursday, 9–11 AM in the ICP's primary timezone.

## Metrics Dashboard

### North Star Metric

Identify the one metric that best captures value delivery for this specific product — not revenue, but the leading indicator that predicts revenue. Examples: "weekly active projects created," "reports generated per user per week," "tasks automated per month." The NSM should be something users can see and feel, not an internal business metric.

### Weekly KPIs

- New signups (absolute count and source breakdown)
- Activation rate (% reaching the first value moment within 7 days)
- Core feature usage (tied to NSM)
- Support ticket volume (proxy for friction)

### Monthly KPIs

**Business**: MRR, MRR growth %, churn rate (logo and revenue), CAC, LTV, LTV:CAC ratio, NPS.

**Content**: Organic search sessions, keyword rankings moved (up/down/new), email list size and open rate, email-to-trial conversion rate.

**Channel-specific**: Track the 3 primary channels selected above with their designated key metrics. Review monthly, adjust quarterly.

## Output

Read `templates/marketing-prd.md`. Write `marketing-prd.md` in the current working directory.

This is the most comprehensive deliverable of the four phases. Fill every section with specifics: real keyword suggestions with real volume estimates, actual article titles (not "article about topic X"), named communities with URLs, named influencer types with follower tier, specific dollar amounts for all budgets, named tools for each recommended service.

No placeholder text. No "e.g." that isn't filled in. Every table must be populated.

Confirm completion: "marketing-prd.md written. All four phases complete. Your project plan is ready."
