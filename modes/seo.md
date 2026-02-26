# Mode: seo — SEO Analysis & Optimization

## Methodology
Analyze sites across 7 weighted categories. Read reference files from `modes/seo/` on demand — they contain thresholds, schema status, and frameworks Claude doesn't know natively.

| Category | Weight | Reference |
|----------|--------|-----------|
| Technical SEO | 25% | — |
| Content Quality (E-E-A-T) | 25% | `seo/eeat.md` |
| On-Page SEO | 20% | `seo/quality-gates.md` |
| Schema / Structured Data | 10% | `seo/schema.md` |
| Performance (CWV) | 10% | `seo/cwv.md` |
| Images | 5% | — |
| AI Search Readiness (GEO) | 5% | `seo/geo.md` |

## Critical Rules (things Claude gets wrong without guidance)
- INP replaced FID (March 2024). FID fully removed Sept 2024. NEVER reference FID.
- HowTo schema deprecated (Sept 2023) — never recommend.
- FAQ schema restricted to government/health sites only (Aug 2023).
- SpecialAnnouncement deprecated (July 2025). ClaimReview, VehicleListing, Dataset retired (June-Late 2025).
- Mobile-first indexing 100% complete (July 2024) — ALL sites crawled as mobile.
- E-E-A-T now applies to ALL competitive queries, not just YMYL (Dec 2025 core update).
- Brand mentions correlate 3x more with AI visibility than backlinks (Ahrefs Dec 2025).
- AI crawlers do NOT execute JavaScript — SSR is critical for AI search visibility.
- Location pages: WARNING at 30+, HARD STOP at 50+ (doorway page risk).
- Always use JSON-LD for schema (Google's explicit recommendation).

## Analysis Workflow
1. Fetch page/site with WebFetch. Detect business type (SaaS, local, ecommerce, publisher, agency).
2. Load relevant reference files for the analysis categories needed.
3. Score each category. Generate SEO Health Score (0-100) as weighted aggregate.
4. Prioritize findings: Critical (blocks indexing/causes penalties) → High (fix within 1 week) → Medium (1 month) → Low (backlog).
5. Output actionable report with specific fixes, not vague advice.

## GEO Quick Wins (AI Search Optimization)
- Add "What is [topic]?" definition in first 60 words — AI systems extract this.
- Create 134-167 word self-contained answer blocks — optimal citation length.
- Question-based H2/H3 headings match AI query patterns.
- Include specific statistics with sources — citability signal.
- Allow GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot in robots.txt.
- Create `/llms.txt` for structured AI crawler guidance.
- Person schema for authors strengthens E-E-A-T signals for AI.

## Output Format
SEO Health Score: XX/100 with category breakdown table, then prioritized findings (Critical → Low) with specific actionable fixes. Lead with quick wins.
