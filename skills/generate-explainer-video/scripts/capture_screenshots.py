#!/usr/bin/env python3
"""Capture screenshots from URLs using Playwright.

Usage:
    python3 capture_screenshots.py <url> <output_dir> [options]
    python3 capture_screenshots.py --help

Options:
    --full-page             Capture full page (default: viewport only)
    --viewport WxH          Viewport size, default 1920x1080
    --mobile                Use mobile viewport (375x812)
    --highlight SELECTOR    CSS selector of element to highlight with overlay
    --element SELECTOR      Capture only this element
    --wait SECONDS          Wait before capturing, default 2
    --highlight-color COLOR Highlight overlay color, default rgba(233,69,96,0.3)

Examples:
    python3 capture_screenshots.py https://example.com ./screenshots
    python3 capture_screenshots.py https://example.com ./screenshots --full-page --highlight "nav"
    python3 capture_screenshots.py https://example.com ./screenshots --mobile --element ".hero"
"""

import os
import sys


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("url", help="URL to capture")
    parser.add_argument("output_dir", help="Directory to save screenshots")
    parser.add_argument("--full-page", action="store_true", help="Full page screenshot")
    parser.add_argument("--viewport", default="1920x1080", help="Viewport WxH")
    parser.add_argument("--mobile", action="store_true", help="Mobile viewport 375x812")
    parser.add_argument("--highlight", action="append", default=[],
                        help="CSS selector to highlight (can repeat)")
    parser.add_argument("--element", help="Capture only this CSS selector")
    parser.add_argument("--wait", type=float, default=2, help="Seconds to wait before capture")
    parser.add_argument("--highlight-color", default="rgba(233,69,96,0.3)")

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: Playwright required. Install: pip install playwright && playwright install chromium")
        sys.exit(1)

    if args.mobile:
        vw, vh = 375, 812
    else:
        parts = args.viewport.split("x")
        vw, vh = int(parts[0]), int(parts[1])

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": vw, "height": vh})
        page = context.new_page()

        print(f"Navigating to {args.url}...")
        page.goto(args.url, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(int(args.wait * 1000))

        # Main screenshot
        suffix = "mobile" if args.mobile else "desktop"
        main_path = os.path.join(args.output_dir, f"page_{suffix}.png")

        if args.element:
            el = page.query_selector(args.element)
            if el:
                el.screenshot(path=main_path)
                print(f"Element screenshot: {main_path}")
            else:
                print(f"WARNING: Element '{args.element}' not found, taking full page")
                page.screenshot(path=main_path, full_page=args.full_page)
        else:
            page.screenshot(path=main_path, full_page=args.full_page)
            print(f"Screenshot: {main_path}")

        # Highlight screenshots
        for i, selector in enumerate(args.highlight):
            elements = page.query_selector_all(selector)
            if not elements:
                print(f"WARNING: No elements found for '{selector}'")
                continue

            # Add highlight overlay via JS
            page.evaluate(f"""
                document.querySelectorAll('{selector}').forEach(el => {{
                    el.style.outline = '3px solid rgba(233,69,96,0.9)';
                    el.style.boxShadow = '0 0 0 4px {args.highlight_color}';
                }});
            """)
            page.wait_for_timeout(200)

            hl_path = os.path.join(args.output_dir, f"highlight_{i + 1}_{suffix}.png")
            if args.full_page:
                page.screenshot(path=hl_path, full_page=True)
            else:
                # Try to scroll element into view and capture viewport
                elements[0].scroll_into_view_if_needed()
                page.wait_for_timeout(300)
                page.screenshot(path=hl_path)
            print(f"Highlight screenshot: {hl_path}")

            # Remove highlight
            page.evaluate(f"""
                document.querySelectorAll('{selector}').forEach(el => {{
                    el.style.outline = '';
                    el.style.boxShadow = '';
                }});
            """)

        # Capture key sections automatically
        sections = ["header", "nav", "main", "footer", "[role='banner']", "[role='main']"]
        captured = 0
        for sel in sections:
            el = page.query_selector(sel)
            if el and el.is_visible():
                clean_sel = sel.replace("[", "").replace("]", "").replace("=", "_").replace("'", "")
                sec_path = os.path.join(args.output_dir, f"section_{clean_sel}_{suffix}.png")
                try:
                    el.screenshot(path=sec_path)
                    print(f"Section screenshot: {sec_path}")
                    captured += 1
                except Exception:
                    pass

        browser.close()
        print(f"\nDone. {captured + 1 + len(args.highlight)} screenshots saved to {args.output_dir}")


if __name__ == "__main__":
    main()
