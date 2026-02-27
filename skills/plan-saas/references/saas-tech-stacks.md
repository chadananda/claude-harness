# SaaS Tech Stacks

## Stack by Product Type

| Product Type | Frontend | Backend | Database | Key Services |
|-------------|----------|---------|----------|-------------|
| **CRUD SaaS** (CRM, PM tool) | Vue/Nuxt or Svelte/SvelteKit | Node.js or Python/FastAPI | PostgreSQL | Stripe, Resend, Clerk |
| **Marketplace** | Next.js or SvelteKit | Node.js + queue system | PostgreSQL + Redis | Stripe Connect, Algolia |
| **API-first** | Minimal dashboard only | Node.js/Bun or Go | PostgreSQL | API gateway, rate limiter |
| **Content platform** | Next.js or Astro | Node.js or Python | PostgreSQL + S3/R2 | CDN, image processing |
| **Real-time** (chat, collab) | Vue/React + WebSocket client | Node.js + WebSocket server | PostgreSQL + Redis pub/sub | WebSocket infra (Soketi, Ably) |
| **AI/ML product** | React or Vue | Python/FastAPI | PostgreSQL + vector DB | OpenAI/Anthropic API, GPU hosting |

## Technology Choice Rationale

**Vue/Svelte over React for MVPs**: Simpler mental model, less boilerplate, faster to ship. React is fine with team preference — but for solo founder or small team, simplicity wins. Don't let framework choice be a 3-week debate.

**PostgreSQL always**: Handles 95% of SaaS data models. JSON columns for flexible schema. Full-text search built in. ACID transactions. Don't add MongoDB "for flexibility" — PostgreSQL JSON does the same thing with transactions. Don't add a second database until PostgreSQL is genuinely the bottleneck.

**PaaS over raw cloud (Railway, Render, Fly.io)**: Deploy in minutes with a git push. AWS/GCP are for when you need specific managed services (SageMaker, BigQuery) or hit genuine PaaS limits. Premature cloud architecture is the #1 time sink for early-stage founders — infrastructure engineering before product-market fit is waste.

**Managed auth (Clerk, Supabase Auth, Auth0)**: Auth is a liability, not a feature. Security vulnerabilities, edge cases (SSO, MFA, magic links), and maintenance overhead are not worth owning. Build auth only if auth IS your product.

**Stripe for payments**: No alternative matches the developer experience, documentation, and reliability. Don't evaluate Paddle or Lemonsqueezy unless you specifically need merchant-of-record (automatic international tax handling) — even then, validate the tradeoffs first.

**Resend or Postmark for transactional email**: SendGrid has a notoriously poor deliverability reputation at small volumes and a hostile developer experience. Resend is the current best-in-class for developer-led teams.

## Anti-Patterns

1. **Premature microservices**: Kubernetes at 0 users is engineering theater. Monolith first — extract services only when you have production data showing which components need independent scaling.
2. **Over-engineering the data layer**: GraphQL, event sourcing, CQRS — skip all of it for MVP. Raw SQL or a lightweight query builder (Drizzle ORM, Prisma) is sufficient for years of scale.
3. **DIY commodities**: Auth, email, payments, file storage, search — these are solved problems. Use managed services. Your competitive advantage is your product logic, not reinventing Stripe.
4. **Premature optimization**: Don't add caching layers, CDN, read replicas, or job queues until you have performance data showing you need them. PostgreSQL on a $20/mo server handles thousands of concurrent users.
5. **Framework chasing**: The latest Rust web framework is interesting but your MVP takes 3x longer. Pick boring, well-documented technology with large communities — when you hit a problem at 2am, you need Stack Overflow answers, not a GitHub issue with no response.

## Infrastructure Essentials (Day 1)

| Tool | Purpose | Option |
|------|---------|--------|
| CI/CD | Run tests on every PR | GitHub Actions (free for public, $4/mo for private) |
| Error tracking | Know when things break before users tell you | Sentry free tier (5K errors/mo) |
| Uptime monitoring | Know when you're down | BetterStack or UptimeRobot free tier |
| Database backups | Automated daily backups | Most PaaS providers include this — verify on day 1 |
| Environment secrets | Never commit credentials | .env files + platform-native secrets manager |
| Structured logging | Debugging in production | JSON logs + PaaS log viewer — no Datadog until $10K MRR |

## Cost Estimation by Stage

| Service | Launch (0-100 users) | Growth (1K users) | Scale (10K users) |
|---------|---------------------|-------------------|-------------------|
| Hosting (PaaS) | $5-20/mo | $30-80/mo | $100-300/mo |
| Database (managed) | $0-15/mo | $25-50/mo | $50-150/mo |
| Auth (managed) | $0 (free tier) | $25-50/mo | $100-200/mo |
| Email (transactional) | $0 (free tier) | $10-25/mo | $25-75/mo |
| Stripe | 2.9% + $0.30/txn | 2.9% + $0.30/txn | 2.7% (volume) |
| Error tracking | $0 (free tier) | $0-26/mo | $26-80/mo |
| Domain + DNS | $12-20/yr | $12-20/yr | $12-20/yr |
| **Total (excl. Stripe)** | **$5-50/mo** | **$100-230/mo** | **$300-800/mo** |

Stripe fees are revenue-proportional — budget 3% of MRR as payment processing overhead from day one.
