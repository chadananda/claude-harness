# Core Web Vitals Thresholds (February 2026)

## Current Metrics

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | ≤2.5s | 2.5s–4.0s | >4.0s |
| INP (Interaction to Next Paint) | ≤200ms | 200ms–500ms | >500ms |
| CLS (Cumulative Layout Shift) | ≤0.1 | 0.1–0.25 | >0.25 |

- INP replaced FID on March 12, 2024. FID fully removed Sept 9, 2024. INP is the sole interactivity metric.
- Evaluated at 75th percentile of real user data (CrUX field data).
- CWV are a tiebreaker ranking signal — matter most when content quality is similar.
- Thresholds unchanged since original definitions — ignore "tightened thresholds" claims.
- Dec 2025 core update appeared to weight mobile CWV more heavily.
- As of Oct 2025: 57.1% desktop / 49.7% mobile sites pass all three CWV.

## LCP Subparts (Feb 2025 CrUX Addition)

| Subpart | What It Measures | Target |
|---------|------------------|--------|
| TTFB | Server response time | <800ms |
| Resource Load Delay | TTFB to resource request start | Minimize |
| Resource Load Time | Download time for LCP resource | Depends on size |
| Element Render Delay | Resource loaded to rendered | Minimize |

Total LCP = TTFB + Resource Load Delay + Resource Load Time + Element Render Delay

## Common Bottlenecks

### LCP
Unoptimized hero images (WebP/AVIF + preload). Render-blocking CSS/JS (defer, async, critical CSS). Slow TTFB >200ms (edge CDN, caching). Third-party scripts. Web font delay (font-display: swap + preload).

### INP
Long JS tasks on main thread (break <50ms). Heavy event handlers (debounce, requestAnimationFrame). Excessive DOM >1,500 elements. Synchronous XHR/localStorage. Layout thrashing.

### CLS
Images/iframes without width/height. Dynamically injected content above fold. Web fonts without font-display: swap. Ads/embeds without reserved space.

## Measurement
- Field data (what Google uses for ranking): CrUX, PageSpeed Insights, Search Console CWV report
- Lab data (debugging): Lighthouse 13.0+, WebPageTest, Chrome DevTools
- CrUX Vis replaced old Looker Studio dashboard (Nov 2025)
- Soft Navigations API (Chrome 139+ experimental) — SPA CWV measurement, no ranking impact yet

## Tools
```bash
# PageSpeed Insights API
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL&key=API_KEY"
# Lighthouse CLI
npx lighthouse URL --output json --output-path report.json
```
