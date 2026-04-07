---
name: generate-explainer-video
description: "Generate polished explainer videos from a topic or URL. Given a subject, this skill autonomously researches content, builds a pedagogy-aware outline and narration script, captures screenshots and generates context-relevant visuals, then produces a video with slide-like framing, transitions, and optional AI talking-head presenter. Supports general and SEO audit modes."
argument-hint: "<topic or URL> [--duration 60] [--mode general|seo_audit]"
---

# Generate Explainer Video

Produce a polished explainer video from a topic string or URL. The video prioritizes clarity and information density over generic filler.

## Inputs

| Parameter | Default | Description |
|-----------|---------|-------------|
| `topic_or_url` | required | A topic string ("How DNS works") or a URL to explain |
| `duration_seconds` | 60 | Target video length in seconds |
| `mode` | general | `general` — what/why/how/tradeoffs; `seo_audit` — what's right, what's wrong, top 3 fixes |

Parse the user's message to extract these. If ambiguous, ask once.

## Output

A JSON object saved to `tmp/explainer_output.json`:

```json
{
  "video_url": "tmp/explainer_video.mp4",
  "status": "complete",
  "outline": [ { "section": "...", "duration_s": 12, "key_points": ["..."] } ],
  "script": "Full narration script text...",
  "key_visuals": [
    { "file": "tmp/slides/slide_01.png", "caption": "DNS resolution flow diagram" },
    { "file": "tmp/screenshots/hero.png", "caption": "Homepage above the fold" }
  ],
  "metadata": {
    "renderer": "cli-ffmpeg",
    "duration_seconds": 60,
    "source_urls": ["https://..."],
    "mode": "general",
    "generated_at": "2026-03-27T..."
  }
}
```

## Workflow — Execute Phases in Order

### Phase 0: Setup

1. Create working directories: `tmp/explainer/`, `tmp/slides/`, `tmp/screenshots/`
2. Parse inputs from user message
3. Determine if input is a URL (starts with http/https) or a topic string

### Phase 1: Research

**Goal:** Gather enough material to write an authoritative 60-second explanation.

**If input is a URL:**
1. Fetch the page content using WebFetch
2. Capture screenshots of the page using the browser tools (mcp__claude-in-chrome__*) or `scripts/capture_screenshots.py`:
   - Full page screenshot
   - Key sections (hero, navigation, main content, footer for SEO mode)
   - Identify and screenshot 3-5 important UI regions
3. Extract text, meta tags, headings, key data from the page
4. For SEO mode: also run Lighthouse or analyze meta tags, heading structure, image alt text, Core Web Vitals signals

**If input is a topic:**
1. Use WebSearch to find 3-5 authoritative sources
2. Use WebFetch to pull key content from top results
3. Identify diagrams, code examples, or data that would benefit from visualization

**Research output:** Save `tmp/explainer/research.md` with:
- Source URLs and their key contributions
- Raw facts, definitions, statistics
- Identified visual opportunities (what diagrams/screenshots to create)

### Phase 2: Outline & Script

**Goal:** Structure content for maximum clarity within the time budget.

**Pedagogy framework — every video answers:**
- **What is it?** — Definition and context (10% of duration)
- **Key terminology** — Define essential terms the viewer must know to follow the rest (10%)
- **Why does it matter?** — Relevance, impact, motivation (15%)
- **How does it work?** — Mechanics, architecture, flow (40%)
- **Main tradeoffs** — Limitations, alternatives, gotchas (25%)

**SEO audit mode replaces the framework with:**
- **What the site does right** (20%)
- **What's wrong** — specific issues with evidence (40%)
- **Top 3 fixes** — prioritized, actionable (40%)

**Steps:**
1. Divide duration into sections following the framework above
2. Write section titles and 2-4 key points per section
3. Write the full narration script:
   - Target ~150 words per minute (2.5 words/second)
   - For 60s video: ~150 words total
   - Use conversational but professional tone
   - Open with a hook, close with a takeaway
4. Save outline to `tmp/explainer/outline.json`
5. Save script to `tmp/explainer/script.txt`

### Phase 3: Visual Asset Generation

**Goal:** Create or collect every visual needed. Avoid generic stock imagery — every visual must be context-relevant.

**Visual types (choose based on content):**

| Type | When to use | How to create |
|------|------------|---------------|
| Screenshot | URL input, showing real UI | Browser tools or `scripts/capture_screenshots.py` |
| Diagram | Architecture, flow, process | Generate with Pillow via `scripts/render_slides.py` using `type: diagram` |
| Code snippet | Technical topics | Render as styled code block on slide |
| Chart/data | Statistics, comparisons | Render as bar/pie chart on slide |
| Annotated screenshot | Highlighting specific UI elements | Screenshot + overlay highlights |
| Key metric | Single important number | Large-font centered slide |

**Steps:**
1. For each outline section, determine 1-2 visuals needed
2. Capture any remaining screenshots not gathered in Phase 1
3. For annotated screenshots: use `scripts/capture_screenshots.py --highlight` to add bounding box overlays
4. Prepare a slide spec JSON for Phase 4

### Phase 4: Slide Rendering

**Goal:** Generate polished slide images for every section of the video.

Use `scripts/render_slides.py` to generate slide PNGs from a JSON specification:

```bash
python3 scripts/render_slides.py tmp/explainer/slides_spec.json tmp/slides/
```

**Slide spec format** (`tmp/explainer/slides_spec.json`):

```json
{
  "settings": {
    "width": 1920,
    "height": 1080,
    "background_color": "#1a1a2e",
    "accent_color": "#e94560",
    "text_color": "#ffffff",
    "font_heading": "Helvetica-Bold",
    "font_body": "Helvetica"
  },
  "slides": [
    {
      "type": "title",
      "title": "How DNS Works",
      "subtitle": "The Internet's Phone Book",
      "section_label": "EXPLAINER"
    },
    {
      "type": "bullets",
      "title": "Why DNS Matters",
      "bullets": ["Every web request starts with DNS", "Misconfiguration = downtime"],
      "image_path": "tmp/screenshots/dns_flow.png"
    },
    {
      "type": "code",
      "title": "DNS Lookup Example",
      "code": "$ dig example.com\n;; ANSWER SECTION:\nexample.com. 300 IN A 93.184.216.34",
      "language": "bash"
    },
    {
      "type": "diagram",
      "title": "Resolution Flow",
      "nodes": ["Browser", "Resolver", "Root NS", "TLD NS", "Auth NS"],
      "edges": [[0,1], [1,2], [2,3], [3,4], [4,1]],
      "edge_labels": ["query", "recurse", ".com?", "ns.example.com", "93.184.216.34"]
    },
    {
      "type": "key_metric",
      "metric": "4.3 billion",
      "label": "DNS queries per day on Cloudflare alone",
      "source": "Cloudflare 2024 Report"
    },
    {
      "type": "image_full",
      "title": "Homepage Analysis",
      "image_path": "tmp/screenshots/hero.png",
      "caption": "Above-the-fold layout"
    },
    {
      "type": "comparison",
      "title": "Tradeoffs",
      "left_title": "Recursive DNS",
      "left_items": ["Simple for clients", "Caching benefits"],
      "right_title": "Iterative DNS",
      "right_items": ["Less load on resolver", "More control"]
    },
    {
      "type": "takeaway",
      "title": "Key Takeaway",
      "text": "DNS is the invisible backbone of the internet. Understanding it helps you debug faster and build more resilient systems."
    }
  ]
}
```

**Supported slide types:** `title`, `bullets`, `code`, `diagram`, `key_metric`, `image_full`, `comparison`, `takeaway`, `terminology`, `seo_scorecard`

**Terminology slide type** — for defining key terms the viewer needs to internalize:
```json
{
  "type": "terminology",
  "title": "Key Terms",
  "terms": [
    { "term": "DNS Resolver", "definition": "Server that receives queries from clients and tracks down the answer through recursive lookups" },
    { "term": "TTL", "definition": "Time To Live — how long a DNS record is cached before re-querying" },
    { "term": "Authoritative NS", "definition": "The server that holds the actual DNS records for a domain" }
  ]
}
```

**SEO-specific slide type:**
```json
{
  "type": "seo_scorecard",
  "title": "SEO Audit Summary",
  "scores": { "Performance": 72, "SEO": 85, "Accessibility": 64 },
  "issues": ["Missing meta descriptions on 12 pages", "No structured data"],
  "fixes": ["Add unique meta descriptions", "Implement JSON-LD schema", "Fix image alt text"]
}
```

### Phase 5: Video Composition

**Goal:** Assemble slides into a polished video with transitions.

Use `scripts/compose_video.py`:

```bash
python3 scripts/compose_video.py \
  --slides-dir tmp/slides/ \
  --output tmp/explainer_video.mp4 \
  --duration 60 \
  --transition crossfade \
  --transition-duration 0.5
```

**The script:**
- Distributes duration evenly across slides (or uses per-slide durations from spec)
- Applies crossfade transitions between slides
- Adds subtle ken-burns (pan/zoom) effect for visual interest
- Outputs 1080p MP4 at 30fps

**Optional audio:** If a TTS audio file is provided:
```bash
python3 scripts/compose_video.py \
  --slides-dir tmp/slides/ \
  --output tmp/explainer_video.mp4 \
  --duration 60 \
  --audio tmp/explainer/narration.mp3
```

### Phase 6: API Renderer (Optional)

If the user has configured a video API backend, use it instead of the CLI pipeline. Check for environment variables:

- `SYNTHESIA_API_KEY` — Use Synthesia API for AI avatar presenter
- `HEYGEN_API_KEY` — Use HeyGen API for AI avatar presenter
- `CANVA_API_KEY` — Use Canva API for polished templates

When an API key is available, read `references/api_backends.md` for integration details. The API renderer replaces Phases 4-5 but uses the same outline and script from Phases 2-3.

**Fallback order:** Synthesia → HeyGen → Canva → CLI (ffmpeg)

### Phase 7: Output Assembly

1. Generate the output JSON (see Output section above)
2. Save to `tmp/explainer_output.json`
3. Report to user:
   - Video file path
   - Duration and slide count
   - List of key visuals with captions
   - The narration script
   - Suggestion to add TTS narration if not already included

## Design Principles

### Color Palettes by Topic Category

| Category | Primary | Accent | Background |
|----------|---------|--------|------------|
| Technical/Engineering | #0f3460 | #e94560 | #1a1a2e |
| Business/Marketing | #2d3436 | #00b894 | #ffffff |
| Science/Education | #2c3e50 | #f39c12 | #ecf0f1 |
| SEO/Web | #1e272e | #0be881 | #f5f6fa |
| Finance | #2d3436 | #6c5ce7 | #dfe6e9 |
| Healthcare | #2d3436 | #00cec9 | #f0f0f0 |

Choose palette based on topic. Override if user specifies brand colors.

### Slide Design Rules

- **Section titles**: Always visible — top-left or centered, consistent position across slides
- **Font sizes**: Headings 48-64px, body 28-36px, captions 20-24px, code 24-28px monospace
- **Margins**: 80px on all sides minimum
- **Image placement**: Right half or bottom 60% of slide; never stretch, always maintain aspect ratio
- **Code blocks**: Dark background (#282c34), syntax-highlighted, rounded corners
- **Diagrams**: Use accent color for arrows/connections, white/light for nodes
- **Transitions**: Crossfade only — no wipes, spins, or other distracting effects

### Content Density Guidelines

| Duration | Slides | Words | Sections |
|----------|--------|-------|----------|
| 30s | 4-5 | ~75 | 3 |
| 60s | 6-8 | ~150 | 4 |
| 90s | 9-12 | ~225 | 5 |
| 120s | 12-16 | ~300 | 6 |

### Screenshot Best Practices

- Capture at 1920x1080 viewport
- For SEO audits: capture mobile (375px) and desktop views
- Highlight regions with semi-transparent colored overlays (accent color at 30% opacity)
- Add annotation arrows or numbered callouts for complex UIs
- Never use a screenshot without a caption explaining what it shows

## Anti-Patterns

- **Generic stock imagery**: Every visual must relate directly to the topic. If a specific screenshot or diagram is possible, use it.
- **Wall of text slides**: Maximum 5 bullet points per slide, 8 words per bullet.
- **Missing context**: Every slide must have a section title so viewers always know where they are.
- **Monotone pacing**: Vary slide types — alternate between text, visuals, metrics, and diagrams.
- **Unexplained screenshots**: Every screenshot needs a caption and optional annotation.

## Dependencies

Required (verify before starting):
- **Python 3.8+** with **Pillow** (`pip install Pillow`)
- **ffmpeg** (for video composition)
- **Playwright** (`pip install playwright && playwright install chromium`) — for screenshots

Optional:
- **TTS engine** (say on macOS, espeak on Linux, or cloud TTS API) — for narration audio
- **Synthesia/HeyGen/Canva API key** — for AI avatar or polished templates
