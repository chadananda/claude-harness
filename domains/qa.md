# Domain: qa — Autonomous Quality Assurance
Load @domains/writing-voice.md — applies to reports and logs.

## Core Principle
Claude declares victory too early. Theoretical success is not success. Code that "should work" doesn't count — only code verified through actual execution and visual inspection counts. Default stance: skeptical until proven otherwise.

## Visual-First Verification
Every page, component, and route must be visually verified using Playwright screenshots. Never trust that CSS/layout "should" be correct — render it and look. Compare against reference/target when available.

Use `webapp-testing` skill for all visual checks. Playwright headless + screenshots to tmp/.

### Screenshot Protocol
1. Capture full-page screenshot of every distinct route/state.
2. Compare against reference images or design specs when available.
3. Check: layout, spacing, colors, typography, responsiveness (mobile + desktop), missing images, broken icons, overflow, z-index issues.
4. Log findings with screenshot paths in `tmp/qa-report.md`.

## QA Task Categories (priority order)
1. **Visual regression** — screenshot all routes, compare to references or last known good.
2. **Functional verification** — click flows, form submissions, navigation, error states.
3. **Responsive testing** — viewport widths: 375px (mobile), 768px (tablet), 1280px (desktop).
4. **Performance** — Lighthouse CI or manual audit. Flag scores below 80.
5. **Accessibility** — axe-core scan via Playwright. Auto-fix safe violations (missing alt, missing labels).
6. **Dead code / unused deps** — scan for orphan exports, unused CSS, bloated node_modules.
7. **Link validation** — crawl internal links, flag 404s.
8. **Security basics** — dependency audit, hardcoded secrets, CSP headers.

## Skepticism Rules
- "Tests pass" is necessary but not sufficient — tests can be wrong or shallow.
- "No errors in console" means nothing if nobody opened the browser.
- "Matches the design" requires a side-by-side screenshot comparison, not code reading.
- "Responsive" means actually tested at 3+ widths, not "I used flexbox."
- After fixing something, re-verify the fix visually — don't assume.

## Reporting
Append findings to `tmp/qa-report.md` with timestamps. Format:
```
## [ISO timestamp] — QA Pass #N
Action: [what was checked/fixed]
Findings: [what was found]
Screenshots: [paths]
Status: [clean | issues found | fixed]
```
