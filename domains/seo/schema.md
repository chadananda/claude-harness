# Schema.org Types — Status & Recommendations (February 2026)

Schema.org v29.4 (Dec 8, 2025). Always use JSON-LD. Content with schema has ~2.5x higher chance of AI-generated answer citation (Google/Microsoft, March 2025).

## Active — Recommend freely
Organization, LocalBusiness, SoftwareApplication, WebApplication, Product, Offer, Service, Article, BlogPosting, NewsArticle, Review, AggregateRating, BreadcrumbList, WebSite, WebPage, Person, ContactPage, VideoObject, ImageObject, Event, JobPosting, Course, DiscussionForumPosting, ProductGroup, ProfilePage

## Restricted — Specific site types only
| Type | Restriction | Since |
|------|------------|-------|
| FAQPage | Government and healthcare sites ONLY | Aug 2023 |

## Deprecated — NEVER recommend
| Type | Since | Notes |
|------|-------|-------|
| HowTo | Sept 2023 | Rich results fully removed |
| SpecialAnnouncement | July 2025 | COVID-era, no longer processed |
| CourseInfo | June 2025 | Merged into Course |
| EstimatedSalary | June 2025 | No longer displayed |
| LearningVideo | June 2025 | Use VideoObject instead |
| ClaimReview | June 2025 | Fact-check rich results removed |
| VehicleListing | June 2025 | Discontinued |
| Practice Problem | Late 2025 | No longer displayed |
| Dataset | Late 2025 | Dataset Search discontinued |

## Recent Additions (2024-2026)
Product Certification (April 2025), ProductGroup (2025), ProfilePage (2025), DiscussionForumPosting (2024), LoyaltyProgram (June 2025), ConferenceEvent (Dec 2025), PerformingArtsEvent (Dec 2025)

## E-commerce Note
`returnPolicyCountry` in MerchantReturnPolicy required since March 2025. Content API for Shopping sunsets Aug 18, 2026 — migrate to Merchant API.

## Validation Checklist
1. `@context` is `"https://schema.org"` (not http)
2. `@type` is valid, non-deprecated
3. All required properties present
4. No placeholder text
5. URLs absolute, dates ISO 8601
6. Test: [Rich Results Test](https://search.google.com/test/rich-results), [Schema Validator](https://validator.schema.org/)
