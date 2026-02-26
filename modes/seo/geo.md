# AI Search / GEO Optimization (February 2026)

Generative Engine Optimization — optimizing for AI-generated answers (Google AI Overviews, ChatGPT, Perplexity, Bing Copilot).

## Key Statistics
- AI Overviews: 1.5B users/month, 200+ countries, 50%+ of queries
- ChatGPT: 900M weekly active users
- Perplexity: 500M+ monthly queries
- AI-referred sessions: +527% (Jan-May 2025)
- Only 11% of domains cited by BOTH ChatGPT and Google AI Overviews for same query — platform-specific optimization essential

## Critical Insight: Brand Mentions > Backlinks
Brand mentions correlate 3x more strongly with AI visibility than backlinks (Ahrefs Dec 2025, 75k brands).
| Signal | Correlation |
|--------|-------------|
| YouTube mentions | ~0.737 (strongest) |
| Reddit mentions | High |
| Wikipedia presence | High |
| Domain Rating (backlinks) | ~0.266 (weak) |

## GEO Analysis Criteria
1. **Citability (25%)**: Optimal passage 134-167 words. Clear quotable sentences with facts/stats. Self-contained answer blocks. Direct answer in first 40-60 words. "X is..." definition patterns.
2. **Structural Readability (20%)**: 92% of AIO citations from top-10 pages, but 47% from below position 5. Clean H1→H2→H3, question-based headings, short paragraphs (2-4 sentences), tables for comparison, lists for steps.
3. **Multi-Modal (15%)**: +156% selection rate. Text + images, video, infographics, interactive tools.
4. **Authority & Brand (20%)**: Author byline + credentials, dates, source citations, entity presence (Wikipedia, Reddit, YouTube, LinkedIn).
5. **Technical Accessibility (20%)**: AI crawlers do NOT execute JS — SSR critical. Check robots.txt for AI crawlers, llms.txt presence.

## AI Crawlers (robots.txt)
| Crawler | Owner | Purpose |
|---------|-------|---------|
| GPTBot | OpenAI | Training |
| OAI-SearchBot | OpenAI | Search features |
| ChatGPT-User | OpenAI | Browsing |
| ClaudeBot | Anthropic | Web features |
| PerplexityBot | Perplexity | AI search |
Allow GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot for AI visibility. Blocking GPTBot prevents training but NOT ChatGPT citation (that's ChatGPT-User).

## llms.txt Standard
Location: `/llms.txt` at domain root. Provides AI crawlers structured content guidance. Format: title, description, sections with page links.

## RSL 1.0 (Dec 2025)
Really Simple Licensing — machine-readable AI licensing terms. Backed by Reddit, Yahoo, Medium, Quora, Cloudflare, Akamai, Creative Commons.

## Platform-Specific Optimization
| Platform | Key Sources | Focus |
|----------|-------------|-------|
| Google AI Overviews | Top-10 ranking (92%) | Traditional SEO + passage optimization |
| ChatGPT | Wikipedia (47.9%), Reddit (11.3%) | Entity presence, authoritative sources |
| Perplexity | Reddit (46.7%), Wikipedia | Community validation, discussions |
| Bing Copilot | Bing index | Bing SEO, IndexNow |

## Quick Wins
1. "What is [topic]?" definition in first 60 words
2. 134-167 word self-contained answer blocks
3. Question-based H2/H3 headings
4. Specific statistics with sources
5. Publication/update dates
6. Person schema for authors
7. Allow key AI crawlers in robots.txt
8. Create `/llms.txt`
