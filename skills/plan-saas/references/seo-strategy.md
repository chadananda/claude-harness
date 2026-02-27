# SaaS SEO Strategy

## The SaaS SEO Funnel

| Stage | Intent | Keyword Pattern | Content Type | Conversion Goal |
|-------|--------|----------------|-------------|-----------------|
| **BOFU** (Bottom) | Buy/switch | "best [category]", "[competitor] alternative", "[product] vs [product]", "[category] pricing" | Comparison pages, alternative pages, pricing page, case studies | Free trial signup |
| **MOFU** (Middle) | Evaluate | "how to [solve problem]", "what is [concept]", "[category] guide", "[tool] tutorial" | How-to guides, ultimate guides, tutorials, templates | Email capture, lead magnet |
| **TOFU** (Top) | Awareness | "[broad topic]", "[industry trend]", "[role] tips" | Blog posts, thought leadership, data studies | Brand awareness, email subscribe |

**Priority: BOFU first, then MOFU, then TOFU.** BOFU content converts directly to trials. Most startups write TOFU first because it's easier — but it's furthest from revenue and slowest to compound. A single BOFU comparison page can drive more signups than 20 TOFU blog posts.

## Keyword Research Methodology

Step 1 — Seed keywords: `[problem]`, `[solution category]`, `[competitor names]`, `[current workaround]`

Step 2 — BOFU expansion:
- `[competitor] alternative` / `[competitor] alternatives`
- `best [category] for [use case]` / `best [category] [year]`
- `[product A] vs [product B]`
- `[category] pricing` / `[category] cost`
- `[category] reviews`

Step 3 — MOFU expansion:
- `how to [solve problem]`
- `[category] guide` / `[category] tutorial`
- `[process] template` / `[topic] best practices`
- `what is [concept]`

Step 4 — TOFU expansion:
- `[industry] trends [year]`
- `[role] challenges`
- `[broad topic] statistics` / `[industry] benchmark`

Step 5 — Validation:
- Google autocomplete and "People also ask" reveal real query phrasing
- YouTube autocomplete reveals video search demand (often different phrasing than text search)
- If page 1 results are all DR 70+ domains, target a long-tail variation for a new site

Step 6 — Prioritize by: (search volume × conversion intent) ÷ keyword difficulty. BOFU keywords with moderate volume and low competition outperform high-volume TOFU keywords every time.

## Pillar / Cluster Architecture

**Pillar page**: Comprehensive guide (3,000-5,000 words) targeting a high-volume MOFU keyword. Covers the topic exhaustively — a reader should not need to go elsewhere.

**Cluster articles**: 8-15 supporting articles targeting long-tail variations of the pillar topic. Each is 800-1,500 words, fully answers one specific question.

**Internal link rules**:
- Every cluster article links to its pillar (with keyword-rich anchor text)
- Pillar page links to all cluster articles
- Clusters cross-link to each other where semantically relevant
- Every BOFU page links to the most relevant pillar

**Why this works**: Google rewards comprehensive topical coverage over isolated articles. A site with deep coverage of one topic outranks a site with shallow coverage of many topics.

**For a new SaaS**: Start with 2-3 pillar topics that map directly to your product's core use cases. Build out those clusters before expanding to new topic areas.

## Programmatic SEO Opportunities

Template-based pages at scale — each template type can generate dozens to hundreds of indexed pages:

| Template | Example | Traffic Intent |
|----------|---------|---------------|
| `[Product] for [Industry]` | "Project management for agencies" | BOFU — vertical-specific buyers |
| `[Product] vs [Competitor]` | "Notion vs Obsidian" | BOFU — switchers in evaluation |
| `[Use Case] Template` | "Sprint planning template" | MOFU — users solving a problem |
| `[Industry] [Metric] Benchmarks` | "SaaS churn rate benchmarks 2025" | TOFU — attracts links, builds authority |
| `[Location] [Service]` | "CRM software for UK companies" | BOFU — geo-targeted buyers |

Requirement: each page must have unique, substantive content. Thin pages with swapped keywords get penalized. Minimum viable unique content per page: real data, real examples, or a genuinely useful tool/template.

## GEO (Generative Engine Optimization) / AEO (Answer Engine Optimization)

AI search engines (ChatGPT, Perplexity, Claude, Gemini) are indexing and citing web content. Optimize for AI citation:

1. **Definition-first paragraphs**: Open articles with "What is [topic]?" answered in the first 60 words. AI systems extract these for direct answers.

2. **Self-contained answer blocks**: 134-167 words that fully answer one question without requiring surrounding context. This length is optimal for AI citation — long enough to be comprehensive, short enough to quote directly.

3. **Question-based headings**: H2/H3 phrased as natural language questions ("How do I migrate from [competitor]?", "What's the difference between X and Y?") — these match AI query patterns.

4. **Statistics with named sources**: AI systems preferentially cite content with specific numbers and attributed sources. "According to [Source], X% of [population] does Y in [year]" gets cited; vague claims don't.

5. **Structured data markup**: FAQ schema (for Q&A content), HowTo schema (for tutorials), Product schema (for the product pages themselves). Helps AI parse content intent.

6. **AI crawler access in robots.txt**: Explicitly allow GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, GoogleBot-Extended. Blocking these opts you out of AI search citation.

7. **`/llms.txt` file**: Create a structured plain-text summary of your site — what you do, key pages, product description. Emerging standard for AI crawler guidance (analogous to robots.txt for AI).

## Per-Article Promotion Checklist

After publishing each article:
1. Share on owned social channels with a hook that surfaces one specific insight (not just the title)
2. Post in 2-3 relevant communities where the ICP hangs out — answer a question using the article as supporting resource, not direct self-promotion
3. Email newsletter subscribers within 48 hours of publish
4. Repurpose into 3-5 social posts (one atomic insight each — quotes, stats, frameworks from the article)
5. Reach out to any external source, tool, or person mentioned in the article — notify them they're featured; a percentage will share or link
6. Check for internal linking opportunities — which existing pages should link to this new article?
