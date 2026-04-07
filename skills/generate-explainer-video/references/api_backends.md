# Video API Backend Integration

When a user has an API key for a cloud video renderer, use it instead of the local CLI pipeline. The API replaces Phases 4-5 (slide rendering + video composition) while using the same outline and script from Phases 2-3.

## Synthesia

**Env var:** `SYNTHESIA_API_KEY`

### Create Video

```bash
curl -X POST https://api.synthesia.io/v2/videos \
  -H "Authorization: $SYNTHESIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Explainer: <topic>",
    "description": "<one-line summary>",
    "visibility": "private",
    "input": [
      {
        "scriptText": "<narration for this slide>",
        "avatar": "anna_costume1_cameraA",
        "background": "off_white",
        "avatarSettings": {
          "horizontalAlign": "right",
          "scale": 0.5,
          "style": "rectangular"
        }
      }
    ]
  }'
```

Each element in `input[]` is one scene/slide. To add custom backgrounds:
- Upload slide images as background via the Media Library API first
- Reference them with `"background": "<media_id>"`

### Poll for completion

```bash
curl https://api.synthesia.io/v2/videos/<video_id> \
  -H "Authorization: $SYNTHESIA_API_KEY"
```

Status progresses: `pending` → `in_progress` → `complete`. The `download` field contains the MP4 URL when complete. Poll every 30 seconds; typical render time is 2-5 minutes for a 60s video.

### Avatar options

Common avatars: `anna_costume1_cameraA`, `james_costume1_cameraA`, `lily_costume1_cameraA`. Use the list avatars endpoint to discover more:

```bash
curl https://api.synthesia.io/v2/avatars \
  -H "Authorization: $SYNTHESIA_API_KEY"
```

### Best practices
- Keep each scene's script under 200 words for natural pacing
- Use `avatarSettings.style: "circular"` for overlay on data-heavy slides
- Set `avatarSettings.scale: 0.3` when the slide content needs more space

---

## HeyGen

**Env var:** `HEYGEN_API_KEY`

### Create Video

```bash
curl -X POST https://api.heygen.com/v2/video/generate \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video_inputs": [
      {
        "character": {
          "type": "avatar",
          "avatar_id": "Angela-inTshirt-20220820",
          "avatar_style": "normal"
        },
        "voice": {
          "type": "text",
          "input_text": "<narration for this scene>",
          "voice_id": "1bd001e7e50f421d891986aad5c1e1d"
        },
        "background": {
          "type": "image",
          "url": "<slide_image_url>"
        }
      }
    ],
    "dimension": { "width": 1920, "height": 1080 }
  }'
```

### Poll for completion

```bash
curl https://api.heygen.com/v1/video_status.get?video_id=<id> \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### Notes
- Upload slide images to a public URL (or use HeyGen's asset upload) before referencing as background
- HeyGen supports picture-in-picture avatar placement via the `character.avatar_style` field
- Voice cloning available with `voice.type: "audio"` for custom voice

---

## Canva

**Env var:** `CANVA_API_KEY`

Canva's API is design-focused rather than video-focused. Use it for generating polished slide designs that get exported as images, then compose locally with ffmpeg.

### Create Design

```bash
curl -X POST https://api.canva.com/rest/v1/designs \
  -H "Authorization: Bearer $CANVA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "design_type": { "type": "preset", "name": "Presentation" },
    "title": "Explainer: <topic>"
  }'
```

### Export as images

```bash
curl -X POST https://api.canva.com/rest/v1/exports \
  -H "Authorization: Bearer $CANVA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "design_id": "<design_id>",
    "format": { "type": "png" }
  }'
```

Then use the exported PNGs with the local `compose_video.py` script.

### Notes
- Canva API doesn't support AI avatars — use for design only, compose video locally
- Best for: branded templates, when the user has a Canva brand kit

---

## Google NotebookLM (Free)

NotebookLM is a free multi-purpose tool useful for research synthesis and supplementary asset generation. Avoid its podcast-style audio overviews for narration (too chatty, talks around the subject), but leverage its other capabilities.

### Research synthesis (Phase 1)

1. Create a notebook at https://notebooklm.google.com
2. Add multiple web sources about the topic
3. Use its summary and Q&A features to extract key concepts and relationships
4. Copy the synthesized notes into `tmp/explainer/research.md`

### Asset generation

NotebookLM can generate supplementary assets that feed into the video pipeline:
- **Slideshows** — use as inspiration or starting structure for the outline, export slides as images to incorporate into the video
- **Quizzes** — useful for "test your understanding" closing slides or interactive follow-up content
- **Study guides / FAQs** — good source material for identifying what key questions the video should answer
- **Timelines** — helpful for historical or biographical topics, can inform diagram slides
- **Briefing docs** — concise summaries that help structure the narration script

### Workflow integration

Use NotebookLM early in the pipeline (Phases 1-2) to accelerate research and outlining. Export any generated assets (slides, timelines) and incorporate them into the slide spec for rendering.

### What NOT to use it for
- **Audio overviews / podcast narration** — too conversational, not information-dense enough. Use edge-tts or macOS `say` for direct scripted narration instead.

---

## Narration Options

For narration, the script should be read directly as written — no improvisation, no filler.

### Free: macOS built-in TTS
```bash
# High-quality macOS voices (Samantha, Alex, Ava are best)
say -o tmp/explainer/narration.aiff -v Samantha "$(cat tmp/explainer/script.txt)"
ffmpeg -i tmp/explainer/narration.aiff tmp/explainer/narration.mp3

# Then pass to compose_video.py with --audio flag
python3 scripts/compose_video.py \
  --slides-dir tmp/slides/ --output tmp/explainer_video.mp4 \
  --duration 60 --audio tmp/explainer/narration.mp3
```

### Free: edge-tts (Microsoft Edge voices, high quality)
```bash
pip install edge-tts
edge-tts --text "$(cat tmp/explainer/script.txt)" --voice en-US-GuyNeural --write-media tmp/explainer/narration.mp3
```

---

## Fallback Order

**Cost-optimized (default):**
1. **CLI (ffmpeg) + edge-tts** — Free, natural voice, recommended
2. **CLI (ffmpeg) + macOS `say`** — Free, decent quality
3. **CLI (ffmpeg) only** — Free, silent video with slide-based learning

**Premium (when API keys available):**
4. **Synthesia** — Full video with AI avatar, best quality, paid
5. **HeyGen** — Full video with AI avatar, good alternative, paid
6. **Canva** — Polished slide designs, compose locally, paid

When no API keys are set, the skill defaults to CLI mode automatically.
