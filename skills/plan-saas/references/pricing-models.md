# SaaS Pricing Models

## Model Comparison

| Model | When to Use | Examples | Pros | Cons |
|-------|-------------|----------|------|------|
| **Flat-rate** | Simple product, single use case | Basecamp ($99/mo flat) | Easy to understand, predictable revenue | Leaves money on table with heavy users |
| **Tiered (feature)** | Multiple user segments with different needs | Most B2B SaaS | Captures different willingness-to-pay | Tier design is hard, feature gating annoys users |
| **Tiered (usage)** | Value scales with usage | Twilio, AWS | Aligns price with value delivered | Unpredictable bills scare customers |
| **Per-seat** | Collaborative tools where more users = more value | Slack, Notion | Predictable, scales with org size | Discourages adoption, invites seat sharing |
| **Freemium** | Low marginal cost, strong viral loop, large market | Dropbox, Canva | Massive top-of-funnel, viral growth | Most free users never convert (2-5% typical) |
| **Reverse trial** | Want freemium scale but need users to experience paid features | Ahrefs, Grammarly | Higher conversion than pure freemium | Users feel tricked if not handled well |

## Competitor Pricing Research Methodology

1. Find 5-8 competitors' pricing pages (search `[competitor] pricing`)
2. Document for each: model type, tier names, price points, feature differences between tiers
3. Identify patterns: what's the median Pro tier price? What model dominates the category?
4. Check review sites for pricing complaints: search `[competitor] "too expensive"`, `[competitor] pricing G2 reviews`, `[category] hidden fees`
5. Note what features are gated vs included on all tiers — this reveals what the market treats as table stakes

## Tier Design: Good / Better / Best

**Starter / Free tier** — acquisition and habit formation:
- Include: core value prop at limited scale — users must experience real value
- Limit on: usage volume, seats, or advanced features — NOT core functionality
- Free tier kills conversion when: the free tier is so good there's no reason to upgrade
- Free tier kills adoption when: it's too restricted to demonstrate value

**Pro / Growth tier** — primary revenue driver:
- Include: full feature set for the ICP use case, no artificial limitations
- Price: typically 20-30% below category market leader, 10-20% above cheapest option
- This tier should feel like the obvious choice — if users hesitate here, your value prop is unclear
- Most SaaS revenue comes from this tier; optimize it first

**Enterprise / Scale tier** — capture large-org willingness-to-pay:
- Include: SSO/SAML, audit logs, SLA guarantee, dedicated support, custom integrations, admin controls
- These features are table stakes for procurement at 200+ employee companies — without them, enterprise buyers can't buy
- Price: 2-3x Pro tier minimum, or custom/contact-us pricing for seat/usage negotiation
- Custom pricing unlocks: volume discounts, multi-year commitments, and removes price anchoring

## Pricing Psychology

- **Anchor high**: Display Enterprise tier first (or most prominently) — Pro feels like a deal by comparison
- **Annual discount**: 20% off annual vs monthly — improves cash flow, reduces churn, worth the discount
- **Price endings**: $49 feels materially cheaper than $50; $99 vs $100 — use .99 or .00, not .95
- **Value metric alignment**: Price on the metric that scales with value delivered (messages sent, contacts stored, projects active, API calls) not arbitrary limits like "users" when usage is the value
- **Don't compete on price**: Cheapest option attracts the most price-sensitive customers who churn at the next discount and demand the most support

## MVP Pricing Recommendations

- Launch with 2 tiers max (Free/Starter + Pro). Enterprise tier can be "contact us" placeholder.
- Price higher than feels comfortable — you can discount, but raising prices requires re-selling existing customers
- Founding member pricing: "50% off forever for first 100 customers" — creates urgency, rewards early adopters, builds brand advocates
- Willingness-to-pay interviews: ask 10 potential customers "at what price would this be too expensive?", "at what price would this seem suspiciously cheap?", "what price feels like good value?" — triangulate from answers
- Annual-only at launch: eliminates monthly churn risk while you're iterating; switch to monthly/annual once product is stable
