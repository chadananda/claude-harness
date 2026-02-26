Comprehensive SEO analysis. Activates seo mode — read `modes/seo.md` first for methodology, scoring, and critical rules. Load reference files from `modes/seo/` as needed during analysis.

## Commands

| Command | What |
|---------|------|
| `/seo <url>` | Full site audit (technical, content, schema, CWV, GEO) |
| `/seo page <url>` | Deep single-page analysis |
| `/seo <file>` | Analyze markdown article for SEO and readability |
| `/seo geo <url>` | AI search / GEO optimization analysis |
| `/seo schema <url>` | Schema markup detection, validation, generation |
| `/seo technical <url>` | Technical SEO audit (crawlability, indexability, CWV, security) |
| `/seo content <url>` | E-E-A-T and content quality analysis |
| `/seo plan <type>` | Strategic SEO plan (saas, local, ecommerce, publisher, agency) |

## Workflow

1. Read `modes/seo.md` for methodology and critical rules
2. Fetch target with WebFetch. Detect business type from homepage signals.
3. Load relevant reference files (`modes/seo/{cwv,schema,eeat,quality-gates,geo}.md`) for the analysis categories needed
4. Analyze across 7 weighted categories. Score 0-100.
5. Prioritize: Critical → High → Medium → Low
6. Output actionable report — specific fixes, not vague advice. Lead with quick wins.

For markdown files: extract structure, check headings, word count, readability, keyword placement, internal linking, then apply quality gates from reference files.
