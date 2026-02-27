# Phase 3: Technical Architecture & MVP Scope

## Setup

Read `viability-report.md` and `strategy-brief.md` from the current working directory. Both must exist — if either is missing, tell the user and stop.
Read `references/saas-tech-stacks.md` for stack recommendations and known anti-patterns.
Read `templates/software-prd.md` to understand the required output structure before writing anything.

Open with a one-sentence context summary: "[Product name] targeting [ICP] at [$price/mo] — here's what I know so far..." then proceed.

## Tech Stack Recommendation

Apply these opinionated defaults. Justify any deviation. Accept user overrides — it's their project.

**Frontend**: Vue or Svelte over React for MVPs (simpler, less boilerplate, faster to ship). Use React only if the team has strong existing experience or the product demands a rich ecosystem.

**Backend**: Node.js or Bun for API-heavy products. Python (FastAPI) for data-intensive, ML-adjacent, or scraping products. Pick one — don't mix languages at MVP.

**Database**: PostgreSQL as the default. Add Redis only if session caching or job queuing is a core requirement. Skip NoSQL unless the data is genuinely document-heavy (CMS, dynamic schemas).

**Auth**: Use a managed service — Clerk, Supabase Auth, or Auth0. Do not build auth from scratch. This is non-negotiable for MVPs.

**Payments**: Stripe. No alternatives. Integration risk is not worth any cost savings at MVP scale.

**Hosting**: PaaS over raw cloud. Railway or Render for full-stack. Vercel for frontend-heavy. Fly.io for containerized workloads. Avoid raw AWS/GCP until the product ships and scales.

**Email**: Resend or Postmark for transactional (receipts, magic links, notifications). ConvertKit or Loops for marketing/drip. Don't use the same service for both.

**Monitoring**: Sentry for error tracking from day one. Add Posthog or Plausible for product analytics. Both have generous free tiers.

WebSearch: Validate the recommended stack against the specific product type. Search "[product category] tech stack", "[competitor] engineering blog", "SaaS [product type] architecture". If you find stack-specific anti-patterns or better fits, adjust and explain why.

Present the stack as a short table with one-line rationale per choice. Ask: "Does this stack match your team's experience? Any services you're already paying for or want to avoid?"

## MVP Scope (MoSCoW)

Use the ICP and positioning from `strategy-brief.md` to define scope ruthlessly. Every feature decision should be tied to the core value proposition.

### Must Have — launch blockers

Include only:
- The one or two features that directly deliver the core value prop
- Auth and billing (non-negotiable SaaS infrastructure)
- A landing page built on the positioning from Phase 2

If a feature does not directly deliver the core value prop, it does not belong here. Move it down.

### Should Have — weeks 2–4 post-launch

Features that improve activation or retention once the core loop is proven:
- Analytics and basic monitoring dashboard
- In-app onboarding or guided setup
- Basic admin or user management panel

### Won't Have — explicitly out of scope

Name the obvious-seeming features that are scope traps for this specific product. Common examples: mobile app, AI/ML features (unless core), API access, white-labeling, marketplace, integrations marketplace, team/org management, SSO.

For each item, give a one-sentence reason why it's excluded. This prevents scope creep conversations later.

Ask the user: "Does this scope feel right? Anything I've cut that you feel is truly core to the launch?"

## User Stories

Group stories by epic. Each epic maps to a Must Have feature. Write 3–5 stories per epic, 3–6 epics total. Use this format:

```
As a [specific role from ICP], I want to [action] so that [concrete benefit].
Acceptance criteria:
- [ ] [specific, testable criterion]
- [ ] [specific, testable criterion]
- [ ] [specific, testable criterion]
```

Keep roles specific — not "user" but the actual ICP persona name from Phase 2. Keep acceptance criteria testable by a developer, not vague goals.

## Architecture

Write a high-level architecture section in prose + lists (no diagrams needed):

**System components**: List each service (frontend, API, database, auth, background workers if any) and one sentence on its role.

**Core data flow**: Walk through the primary user journey (signup → core action → value delivered) as a numbered sequence of system interactions.

**External integrations**: List each third-party service, what it handles, and which API or SDK connects it.

**Data model**: Name the 5–10 core tables or collections with their primary fields and key relationships. Keep it to what's needed for the Must Have scope — no premature normalization.

**API surface**: Group key endpoints by resource. Format as `METHOD /resource` with one-line description. Cover auth, core features, and billing webhooks.

## Development Milestones

Define 4–6 milestones with calendar week estimates. Base estimates on actual feature complexity from the Must Have scope, not generic templates. Adjust if the product is unusually simple or complex.

Typical structure:
- M1 (Week 1–2): Repo setup, auth, CI/CD, landing page
- M2 (Week 3–5): Core feature(s) — the Must Have value prop
- M3 (Week 5–6): Billing integration and subscription flows
- M4 (Week 7–8): Polish, error handling, beta invite flow
- M5 (Week 8): Beta launch — invite first 10–20 users

Each milestone: name, week range, list of deliverables, definition of done.

## Infrastructure Cost Estimate

Two columns: 0–100 users (launch) and ~1,000 users (early scale). Use real current pricing.

| Service | 0–100 users/mo | ~1,000 users/mo |
|---------|---------------|-----------------|
| Hosting (PaaS) | $X | $X |
| Database | $X | $X |
| Auth | $X | $X |
| Payments | % per transaction | % per transaction |
| Email (transactional) | $X | $X |
| Monitoring | $X | $X |
| **Total burn** | **$X** | **$X** |

WebSearch pricing pages for the specific services chosen. Use real numbers, not "approximately free."

## Output

Read `templates/software-prd.md`. Write `software-prd.md` in the current working directory.

Fill every section with specifics. Real framework names, real service names, real prices, real endpoint names. No placeholder text. If a section is not applicable to this product, write one sentence explaining why and leave it blank — do not omit sections.

Confirm completion: "software-prd.md written. Ready for Phase 4 (marketing) when you are."
