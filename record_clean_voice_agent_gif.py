# -*- coding: utf-8 -*-
"""
record_clean_voice_agent_gif.py
Records the Call Center AI Voice Agents Studio with:
- ZERO opaque bars covering any UI elements.
- The web app is 100% visible from top header to bottom metrics.
- External captions placed in a dedicated top header strip ABOVE the web app.
- Features: Real-Time Live Call Simulator with Sample Questions grounded in KG & CG.
"""

import os
import sys
import time
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

FRAME_DIR = "scratch/voice_agent_clean_frames"
OUTPUT_GIF = "callcenter_use_cases_tour.gif"
PREVIEW_PNG = "callcenter_use_cases_preview.png"

os.makedirs(FRAME_DIR, exist_ok=True)

for f in os.listdir(FRAME_DIR):
    if f.endswith('.png'):
        try:
            os.remove(os.path.join(FRAME_DIR, f))
        except:
            pass

FONT_BOLD_14 = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 14)
FONT_REG_12 = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 12)

frames = []
frame_idx = 0

def capture_uncovered_frame(page, step_label, caption_text, accent_rgb=(16, 185, 129)):
    global frame_idx
    raw_path = os.path.join(FRAME_DIR, f"raw_{frame_idx:04d}.png")
    out_path = os.path.join(FRAME_DIR, f"frame_{frame_idx:04d}.png")
    
    # 1. Capture the 100% full, untouched web app
    page.screenshot(path=raw_path)
    app_img = Image.open(raw_path)
    app_w, app_h = app_img.size

    # 2. Add an EXTERNAL caption bar ABOVE the web app (Height + 54px)
    caption_h = 54
    total_h = app_h + caption_h
    new_canvas = Image.new('RGB', (app_w, total_h), (15, 23, 42)) # Clean dark top bar

    draw = ImageDraw.Draw(new_canvas)

    # Accent color separator line between caption bar and app
    draw.rectangle([(0, caption_h - 3), (app_w, caption_h)], fill=accent_rgb)

    # Badge Pill
    draw.rounded_rectangle([(16, 12), (16 + 210, 36)], radius=6, fill=(30, 41, 59), outline=accent_rgb, width=1)
    draw.text((24, 15), step_label, font=FONT_BOLD_14, fill=(241, 245, 249))

    # Caption text
    draw.text((242, 16), caption_text, font=FONT_REG_12, fill=(226, 232, 240))

    # 3. Paste the untouched, 100% visible web app directly underneath
    new_canvas.paste(app_img, (0, caption_h))

    new_canvas.save(out_path)
    frames.append(out_path)
    frame_idx += 1
    print(f"Captured clean frame {frame_idx}: {step_label}")

def main():
    file_path = os.path.abspath('callcenter_ai_voice_agents.html').replace('\\', '/')
    url = f'file:///{file_path}'

    print("Launching Chromium for clean recording...")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome', headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 820})
        page.goto(url)
        page.wait_for_timeout(1500)

        # FRAME 1: Full Triad Architecture (100% UI Visible)
        capture_uncovered_frame(
            page,
            "ARCHITECTURE VIEW",
            "Triad Graph Hierarchy: KG (What should happen) + CG (What actually happened) -> BG (Reconciles should vs actual)",
            (99, 102, 241)
        )

        # FRAME 2: Real-Time Live Call Simulator - Billing Dispute Sample Question
        page.click('#tab-call')
        page.wait_for_timeout(1200)
        capture_uncovered_frame(
            page,
            "LIVE CALL SIMULATOR",
            "Real-Time Call: Sarah asks sample question ($150 roaming waiver). Agent grounds in SOP-04 & Sarah's $2.4k LTV to waive fee.",
            (16, 185, 129)
        )

        # FRAME 3: Real-Time Live Call Simulator - Broadband Outage Sample Question
        page.click('#sample-btn-outage')
        page.wait_for_timeout(1000)
        capture_uncovered_frame(
            page,
            "REAL-TIME OUTAGE CALL",
            "Sample Call 2: Blinking optical light -> Agent queries telemetry (31.4dB loss) & SOP-12 to auto-dispatch field tech in 12s.",
            (14, 165, 233)
        )

        # FRAME 4: SOP Knowledge Graph Tab (100% Separate Graph Canvas)
        page.click('#tab-kg')
        page.wait_for_timeout(1500)
        capture_uncovered_frame(
            page,
            "TAB 2: SOP RULEBOOK",
            "SOP Knowledge Graph (KG): Formal rulebook defining Tier-1 limits ($50), Supervisor limits ($250) & Roles.",
            (59, 130, 246)
        )

        # FRAME 5: Call Records Context Graph Tab (100% Separate Graph Canvas)
        page.click('#tab-cg')
        page.wait_for_timeout(1500)
        capture_uncovered_frame(
            page,
            "TAB 3: CALL DIARY",
            "Call Records Context Graph (CG): Empirical decision chain (Event: $150 bill -> Decision: $50 offer -> Exception: $150 waiver -> Retained).",
            (245, 158, 11)
        )

        # FRAME 6: Business Goals Graph Tab (100% Separate Graph Canvas)
        page.click('#tab-bg')
        page.wait_for_timeout(1500)
        capture_uncovered_frame(
            page,
            "TAB 4: BUSINESS ROI",
            "Business Graph (BG): Reconciles should vs actual -> +$2,250 Net Value ($2,400 LTV retained - $150 fee concession).",
            (16, 185, 129)
        )

        # FRAME 7: Policy Drift Feedback Loop Highlight
        page.click('#tab-hierarchy')
        page.select_option('#preset-select', 'billing_dispute')
        page.wait_for_timeout(1000)
        capture_uncovered_frame(
            page,
            "POLICY DRIFT LOOP",
            "Improvement: 47 repeated exceptions trigger automated update to SOP-04 in KG ($50 -> $150), eliminating 45s hold!",
            (99, 102, 241)
        )

        # FRAME 8: Use Case 3 - VIP Retention Preset
        page.select_option('#preset-select', 'vip_retention')
        page.wait_for_timeout(1000)
        capture_uncovered_frame(
            page,
            "USE CASE: RETENTION",
            "Enterprise churn threat: Voice agent matches 15% discount renewal under SOP-28 -> Protects +$27,900 ARR.",
            (16, 185, 129)
        )

        browser.close()

    print("Compiling clean frames into animated GIF...")
    pil_images = [Image.open(f) for f in frames]
    if pil_images:
        pil_images[0].save(PREVIEW_PNG)
        print(f"Saved clean preview to {PREVIEW_PNG}")

        pil_images[0].save(
            OUTPUT_GIF,
            save_all=True,
            append_images=pil_images[1:],
            duration=2200,
            loop=0,
            optimize=True
        )
        print(f"Successfully generated clean {OUTPUT_GIF} ({os.path.getsize(OUTPUT_GIF)} bytes, {len(frames)} frames)")

if __name__ == '__main__':
    main()
