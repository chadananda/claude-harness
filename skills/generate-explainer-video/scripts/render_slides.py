#!/usr/bin/env python3
"""Render slide images from a JSON specification using Pillow.

Usage:
    python3 render_slides.py <slides_spec.json> <output_dir>
    python3 render_slides.py --help

Reads a JSON spec with global settings and a list of slides, then generates
one PNG per slide in the output directory. Supports: title, bullets, code,
diagram, key_metric, image_full, comparison, takeaway, seo_scorecard.
"""

import json
import math
import os
import sys
import textwrap
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Font helpers
# ---------------------------------------------------------------------------

_FONT_CACHE = {}

FONT_SEARCH_PATHS = [
    "/System/Library/Fonts",
    "/Library/Fonts",
    os.path.expanduser("~/Library/Fonts"),
    "/usr/share/fonts/truetype",
    "/usr/share/fonts",
]


def _find_font(name: str) -> str | None:
    """Search common font directories for a .ttf/.otf matching *name*."""
    targets = [name, name.replace("-", ""), name.replace(" ", "")]
    for d in FONT_SEARCH_PATHS:
        if not os.path.isdir(d):
            continue
        for root, _, files in os.walk(d):
            for f in files:
                if not f.lower().endswith((".ttf", ".otf", ".ttc")):
                    continue
                stem = os.path.splitext(f)[0]
                if stem in targets or stem.lower() in [t.lower() for t in targets]:
                    return os.path.join(root, f)
    return None


def load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    key = (name, size)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    path = _find_font(name)
    if path:
        font = ImageFont.truetype(path, size)
    else:
        try:
            font = ImageFont.truetype(name, size)
        except OSError:
            font = ImageFont.load_default()
    _FONT_CACHE[key] = font
    return font


# ---------------------------------------------------------------------------
# Drawing primitives
# ---------------------------------------------------------------------------


def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = xy
    r = min(radius, (x1 - x0) // 2, (y1 - y0) // 2)
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Word-wrap *text* so each line fits within *max_width* pixels."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = f"{current} {word}".strip()
        bbox = font.getbbox(test)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def draw_text_block(draw, x, y, text, font, color, max_width, line_spacing=1.4):
    """Draw word-wrapped text. Returns the y position after the last line."""
    lines = wrap_text(text, font, max_width)
    for line in lines:
        draw.text((x, y), line, font=font, fill=color)
        bbox = font.getbbox(line)
        y += int((bbox[3] - bbox[1]) * line_spacing)
    return y


# ---------------------------------------------------------------------------
# Slide renderers
# ---------------------------------------------------------------------------

class SlideRenderer:
    def __init__(self, settings: dict):
        self.w = settings.get("width", 1920)
        self.h = settings.get("height", 1080)
        self.bg = settings.get("background_color", "#1a1a2e")
        self.accent = settings.get("accent_color", "#e94560")
        self.text_color = settings.get("text_color", "#ffffff")
        self.heading_font = settings.get("font_heading", "Helvetica-Bold")
        self.body_font = settings.get("font_body", "Helvetica")
        self.margin = 80
        self.content_w = self.w - 2 * self.margin

    def new_canvas(self) -> tuple[Image.Image, ImageDraw.Draw]:
        img = Image.new("RGB", (self.w, self.h), self.bg)
        draw = ImageDraw.Draw(img)
        return img, draw

    def draw_section_label(self, draw, label: str):
        if not label:
            return
        font = load_font(self.body_font, 18)
        draw.text((self.margin, 30), label.upper(), font=font, fill=self.accent)

    def draw_title(self, draw, title: str, y=None, size=56):
        font = load_font(self.heading_font, size)
        ty = y or self.margin
        draw_text_block(draw, self.margin, ty, title, font, self.text_color, self.content_w)
        lines = wrap_text(title, font, self.content_w)
        bbox = font.getbbox("Ag")
        return ty + len(lines) * int((bbox[3] - bbox[1]) * 1.4) + 20

    def draw_accent_bar(self, draw, y, width=120, height=4):
        draw.rectangle([self.margin, y, self.margin + width, y + height], fill=self.accent)
        return y + height + 16

    # --- Slide type: title ---
    def render_title(self, slide: dict) -> Image.Image:
        img, draw = self.new_canvas()
        self.draw_section_label(draw, slide.get("section_label", ""))
        font_title = load_font(self.heading_font, 72)
        # Center vertically
        title = slide.get("title", "")
        subtitle = slide.get("subtitle", "")
        lines_t = wrap_text(title, font_title, self.content_w)
        bbox_t = font_title.getbbox("Ag")
        line_h_t = int((bbox_t[3] - bbox_t[1]) * 1.4)
        total_h = len(lines_t) * line_h_t + (40 if subtitle else 0)
        start_y = (self.h - total_h) // 2
        for i, line in enumerate(lines_t):
            lw = font_title.getbbox(line)[2] - font_title.getbbox(line)[0]
            draw.text(((self.w - lw) // 2, start_y + i * line_h_t), line, font=font_title, fill=self.text_color)
        if subtitle:
            font_sub = load_font(self.body_font, 32)
            sw = font_sub.getbbox(subtitle)[2] - font_sub.getbbox(subtitle)[0]
            draw.text(((self.w - sw) // 2, start_y + len(lines_t) * line_h_t + 20), subtitle, font=font_sub, fill=self.accent)
        # Accent bar at bottom
        bar_y = self.h - 60
        bar_w = 200
        draw.rectangle([(self.w - bar_w) // 2, bar_y, (self.w + bar_w) // 2, bar_y + 4], fill=self.accent)
        return img

    # --- Slide type: bullets ---
    def render_bullets(self, slide: dict) -> Image.Image:
        img, draw = self.new_canvas()
        y = self.draw_title(draw, slide.get("title", ""))
        y = self.draw_accent_bar(draw, y)
        bullets = slide.get("bullets", [])
        image_path = slide.get("image_path")
        text_w = self.content_w
        if image_path and os.path.isfile(image_path):
            text_w = self.content_w // 2 - 20
        font = load_font(self.body_font, 30)
        for bullet in bullets:
            draw.text((self.margin, y), "\u2022", font=font, fill=self.accent)
            y = draw_text_block(draw, self.margin + 30, y, bullet, font, self.text_color, text_w - 30)
            y += 8
        if image_path and os.path.isfile(image_path):
            try:
                im = Image.open(image_path)
                max_w = self.content_w // 2 - 20
                max_h = self.h - self.margin * 2 - 80
                im.thumbnail((max_w, max_h), Image.LANCZOS)
                ix = self.w - self.margin - im.width
                iy = (self.h - im.height) // 2
                # Border
                draw.rectangle([ix - 3, iy - 3, ix + im.width + 3, iy + im.height + 3], outline=self.accent, width=2)
                img.paste(im, (ix, iy))
            except Exception:
                pass
        return img

    # --- Slide type: code ---
    def render_code(self, slide: dict) -> Image.Image:
        img, draw = self.new_canvas()
        y = self.draw_title(draw, slide.get("title", ""))
        y = self.draw_accent_bar(draw, y)
        code = slide.get("code", "")
        # Code block background
        code_margin = self.margin + 20
        pad = 24
        font = load_font("Courier New", 24)
        lines = code.split("\n")
        bbox = font.getbbox("Ag")
        line_h = int((bbox[3] - bbox[1]) * 1.3)
        block_h = len(lines) * line_h + 2 * pad
        draw_rounded_rect(draw, [code_margin, y, self.w - code_margin, y + block_h], 12, fill="#282c34")
        cy = y + pad
        # Simple keyword highlighting
        for line in lines:
            draw.text((code_margin + pad, cy), line, font=font, fill="#abb2bf")
            cy += line_h
        return img

    # --- Slide type: diagram ---
    def render_diagram(self, slide: dict) -> Image.Image:
        img, draw = self.new_canvas()
        y = self.draw_title(draw, slide.get("title", ""))
        y = self.draw_accent_bar(draw, y)
        nodes = slide.get("nodes", [])
        edges = slide.get("edges", [])
        edge_labels = slide.get("edge_labels", [])
        if not nodes:
            return img
        n = len(nodes)
        # Layout nodes in a horizontal line or circle
        cx, cy = self.w // 2, (y + self.h) // 2
        radius = min(self.content_w // 2 - 60, (self.h - y) // 2 - 80)
        positions = []
        if n <= 5:
            # Horizontal layout
            spacing = self.content_w // (n + 1)
            for i in range(n):
                px = self.margin + spacing * (i + 1)
                positions.append((px, cy))
        else:
            # Circle layout
            for i in range(n):
                angle = 2 * math.pi * i / n - math.pi / 2
                px = int(cx + radius * math.cos(angle))
                py = int(cy + radius * math.sin(angle))
                positions.append((px, py))
        node_r = 50
        font = load_font(self.body_font, 18)
        edge_font = load_font(self.body_font, 14)
        # Draw edges
        for idx, (src, dst) in enumerate(edges):
            if src >= n or dst >= n:
                continue
            x1, y1 = positions[src]
            x2, y2 = positions[dst]
            draw.line([(x1, y1), (x2, y2)], fill=self.accent, width=2)
            # Edge label
            if idx < len(edge_labels) and edge_labels[idx]:
                mx, my = (x1 + x2) // 2, (y1 + y2) // 2 - 14
                draw.text((mx, my), edge_labels[idx], font=edge_font, fill=self.accent)
            # Arrowhead
            dx, dy = x2 - x1, y2 - y1
            dist = max(math.sqrt(dx * dx + dy * dy), 1)
            ux, uy = dx / dist, dy / dist
            ax, ay = x2 - ux * node_r, y2 - uy * node_r
            draw.polygon([
                (ax, ay),
                (ax - uy * 8 - ux * 14, ay + ux * 8 - uy * 14),
                (ax + uy * 8 - ux * 14, ay - ux * 8 - uy * 14),
            ], fill=self.accent)
        # Draw nodes
        for i, (px, py) in enumerate(positions):
            draw.ellipse([px - node_r, py - node_r, px + node_r, py + node_r], fill="#2d3436", outline=self.accent, width=2)
            label = nodes[i] if i < len(nodes) else ""
            tw = font.getbbox(label)[2] - font.getbbox(label)[0]
            th = font.getbbox(label)[3] - font.getbbox(label)[1]
            draw.text((px - tw // 2, py - th // 2), label, font=font, fill=self.text_color)
        return img

    # --- Slide type: key_metric ---
    def render_key_metric(self, slide: dict) -> Image.Image:
        img, draw = self.new_canvas()
        metric = slide.get("metric", "")
        label = slide.get("label", "")
        source = slide.get("source", "")
        font_big = load_font(self.heading_font, 96)
        font_label = load_font(self.body_font, 32)
        font_src = load_font(self.body_font, 20)
        # Center metric
        mw = font_big.getbbox(metric)[2] - font_big.getbbox(metric)[0]
        mh = font_big.getbbox(metric)[3] - font_big.getbbox(metric)[1]
        draw.text(((self.w - mw) // 2, self.h // 2 - mh - 30), metric, font=font_big, fill=self.accent)
        # Label
        lw = font_label.getbbox(label)[2] - font_label.getbbox(label)[0]
        draw.text(((self.w - lw) // 2, self.h // 2 + 30), label, font=font_label, fill=self.text_color)
        # Source
        if source:
            sw = font_src.getbbox(source)[2] - font_src.getbbox(source)[0]
            draw.text(((self.w - sw) // 2, self.h - 80), f"Source: {source}", font=font_src, fill="#888888")
        return img

    # --- Slide type: image_full ---
    def render_image_full(self, slide: dict) -> Image.Image:
        img, draw = self.new_canvas()
        y = self.draw_title(draw, slide.get("title", ""), size=40)
        image_path = slide.get("image_path", "")
        caption = slide.get("caption", "")
        if image_path and os.path.isfile(image_path):
            try:
                im = Image.open(image_path)
                max_w = self.content_w
                max_h = self.h - y - self.margin - (40 if caption else 0)
                im.thumbnail((max_w, max_h), Image.LANCZOS)
                ix = (self.w - im.width) // 2
                iy = y + 10
                draw.rectangle([ix - 3, iy - 3, ix + im.width + 3, iy + im.height + 3], outline=self.accent, width=2)
                img.paste(im, (ix, iy))
                if caption:
                    font_cap = load_font(self.body_font, 22)
                    cw = font_cap.getbbox(caption)[2] - font_cap.getbbox(caption)[0]
                    draw.text(((self.w - cw) // 2, iy + im.height + 12), caption, font=font_cap, fill="#aaaaaa")
            except Exception:
                draw_text_block(draw, self.margin, y + 40, f"[Image not found: {image_path}]",
                                load_font(self.body_font, 28), "#ff6666", self.content_w)
        return img

    # --- Slide type: comparison ---
    def render_comparison(self, slide: dict) -> Image.Image:
        img, draw = self.new_canvas()
        y = self.draw_title(draw, slide.get("title", ""))
        y = self.draw_accent_bar(draw, y)
        mid = self.w // 2
        # Divider
        draw.line([(mid, y), (mid, self.h - self.margin)], fill=self.accent, width=2)
        font_h = load_font(self.heading_font, 32)
        font_b = load_font(self.body_font, 26)
        half_w = mid - self.margin - 30
        # Left column
        lt = slide.get("left_title", "")
        draw.text((self.margin, y), lt, font=font_h, fill=self.accent)
        ly = y + 50
        for item in slide.get("left_items", []):
            draw.text((self.margin, ly), "\u2022", font=font_b, fill=self.accent)
            ly = draw_text_block(draw, self.margin + 28, ly, item, font_b, self.text_color, half_w)
            ly += 6
        # Right column
        rt = slide.get("right_title", "")
        draw.text((mid + 20, y), rt, font=font_h, fill=self.accent)
        ry = y + 50
        for item in slide.get("right_items", []):
            draw.text((mid + 20, ry), "\u2022", font=font_b, fill=self.accent)
            ry = draw_text_block(draw, mid + 48, ry, item, font_b, self.text_color, half_w)
            ry += 6
        return img

    # --- Slide type: takeaway ---
    def render_takeaway(self, slide: dict) -> Image.Image:
        img, draw = self.new_canvas()
        # Large accent icon area
        icon_y = self.h // 4
        icon_size = 60
        draw.rectangle([(self.w // 2 - icon_size, icon_y - icon_size),
                         (self.w // 2 + icon_size, icon_y + icon_size)],
                        fill=self.accent)
        font_icon = load_font(self.heading_font, 64)
        draw.text((self.w // 2 - 22, icon_y - 36), "\u2713", font=font_icon, fill=self.bg)
        y = icon_y + icon_size + 40
        title = slide.get("title", "Key Takeaway")
        font_t = load_font(self.heading_font, 48)
        tw = font_t.getbbox(title)[2] - font_t.getbbox(title)[0]
        draw.text(((self.w - tw) // 2, y), title, font=font_t, fill=self.text_color)
        y += 80
        text = slide.get("text", "")
        font_b = load_font(self.body_font, 30)
        max_w = int(self.content_w * 0.75)
        lines = wrap_text(text, font_b, max_w)
        bbox = font_b.getbbox("Ag")
        lh = int((bbox[3] - bbox[1]) * 1.5)
        for line in lines:
            lw = font_b.getbbox(line)[2] - font_b.getbbox(line)[0]
            draw.text(((self.w - lw) // 2, y), line, font=font_b, fill=self.text_color)
            y += lh
        return img

    # --- Slide type: terminology ---
    def render_terminology(self, slide: dict) -> Image.Image:
        img, draw = self.new_canvas()
        y = self.draw_title(draw, slide.get("title", "Key Terms"))
        y = self.draw_accent_bar(draw, y)
        terms = slide.get("terms", [])
        font_term = load_font(self.heading_font, 30)
        font_def = load_font(self.body_font, 24)
        max_w = self.content_w - 40
        for entry in terms:
            term = entry.get("term", "")
            defn = entry.get("definition", "")
            # Term in accent color, bold
            draw.text((self.margin + 20, y), term, font=font_term, fill=self.accent)
            bbox = font_term.getbbox(term)
            y += int((bbox[3] - bbox[1]) * 1.3)
            # Definition in body color, indented
            y = draw_text_block(draw, self.margin + 40, y, defn, font_def, self.text_color, max_w - 40)
            y += 20
            # Subtle separator line
            draw.line([(self.margin + 40, y), (self.margin + 200, y)], fill="#444444", width=1)
            y += 16
            if y > self.h - self.margin - 40:
                break
        return img

    # --- Slide type: seo_scorecard ---
    def render_seo_scorecard(self, slide: dict) -> Image.Image:
        img, draw = self.new_canvas()
        y = self.draw_title(draw, slide.get("title", "SEO Scorecard"))
        y = self.draw_accent_bar(draw, y)
        scores = slide.get("scores", {})
        issues = slide.get("issues", [])
        fixes = slide.get("fixes", [])
        # Score circles
        if scores:
            n = len(scores)
            spacing = self.content_w // (n + 1)
            font_score = load_font(self.heading_font, 42)
            font_label = load_font(self.body_font, 20)
            for i, (name, val) in enumerate(scores.items()):
                cx = self.margin + spacing * (i + 1)
                cy_s = y + 60
                r = 45
                # Color based on score
                if val >= 80:
                    color = "#00b894"
                elif val >= 50:
                    color = "#fdcb6e"
                else:
                    color = "#e94560"
                draw.ellipse([cx - r, cy_s - r, cx + r, cy_s + r], outline=color, width=4)
                sv = str(val)
                sw = font_score.getbbox(sv)[2] - font_score.getbbox(sv)[0]
                sh = font_score.getbbox(sv)[3] - font_score.getbbox(sv)[1]
                draw.text((cx - sw // 2, cy_s - sh // 2), sv, font=font_score, fill=color)
                nw = font_label.getbbox(name)[2] - font_label.getbbox(name)[0]
                draw.text((cx - nw // 2, cy_s + r + 10), name, font=font_label, fill=self.text_color)
            y += 180
        # Issues and fixes in two columns
        mid = self.w // 2
        font_h = load_font(self.heading_font, 26)
        font_b = load_font(self.body_font, 22)
        half_w = mid - self.margin - 20
        draw.text((self.margin, y), "ISSUES", font=font_h, fill="#e94560")
        iy = y + 40
        for issue in issues[:5]:
            draw.text((self.margin, iy), "\u2717", font=font_b, fill="#e94560")
            iy = draw_text_block(draw, self.margin + 26, iy, issue, font_b, self.text_color, half_w)
            iy += 6
        draw.text((mid + 20, y), "TOP FIXES", font=font_h, fill="#00b894")
        fy = y + 40
        for j, fix in enumerate(fixes[:3]):
            num = f"{j + 1}."
            draw.text((mid + 20, fy), num, font=font_b, fill="#00b894")
            fy = draw_text_block(draw, mid + 50, fy, fix, font_b, self.text_color, half_w)
            fy += 6
        return img

    def render_slide(self, slide: dict) -> Image.Image:
        stype = slide.get("type", "bullets")
        renderers = {
            "title": self.render_title,
            "bullets": self.render_bullets,
            "code": self.render_code,
            "diagram": self.render_diagram,
            "key_metric": self.render_key_metric,
            "image_full": self.render_image_full,
            "comparison": self.render_comparison,
            "takeaway": self.render_takeaway,
            "terminology": self.render_terminology,
            "seo_scorecard": self.render_seo_scorecard,
        }
        renderer = renderers.get(stype, self.render_bullets)
        return renderer(slide)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3 or "--help" in sys.argv:
        print(__doc__)
        print("Arguments:")
        print("  <slides_spec.json>  Path to the JSON slide specification")
        print("  <output_dir>        Directory to write slide PNGs into")
        sys.exit(0 if "--help" in sys.argv else 1)

    spec_path = sys.argv[1]
    output_dir = sys.argv[2]

    with open(spec_path) as f:
        spec = json.load(f)

    os.makedirs(output_dir, exist_ok=True)

    settings = spec.get("settings", {})
    renderer = SlideRenderer(settings)
    slides = spec.get("slides", [])

    for i, slide in enumerate(slides):
        img = renderer.render_slide(slide)
        out_path = os.path.join(output_dir, f"slide_{i + 1:02d}.png")
        img.save(out_path, "PNG")
        print(f"  [{i + 1}/{len(slides)}] {out_path}")

    print(f"\nGenerated {len(slides)} slides in {output_dir}")


if __name__ == "__main__":
    main()
