# -*- coding: utf-8 -*-
"""
record_clean_voice_agent_gif.py
Records the Call Center AI Voice Agents Studio with:
1. Unified Triad Cross-Graph View (KG + CG + BG + Cross-Edges)
2. Domain Subgraph Navigation (Billing, Telecom, Enterprise, All-Domains)
3. Real-Time Animated Graph Growth Stepper in Live Calls
4. ZERO covered UI - 100% visible with external top header caption bar.
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
    draw.rounded_rectangle([(16, 12), (16 + 215, 36)], radius=6, fill=(30, 41, 59), outline=accent_rgb, width=1)
    draw.text((24, 15), step_label, font=FONT_BOLD_14, fill=(241, 245, 249))

    # Caption text
    draw.text((248, 16), caption_text, font=FONT_REG_12, fill=(226, 232, 240))

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
            "1. ARCHITECTURE VIEW",
            "Agent Hierarchy: KG (What should happen) + CG (What actually happened) -> BG (Reconciles should vs actual)",
            (99, 102, 241)
        )

        # FRAME 2: ORDER 1 - Unified Triad Cross-Graph View (Billing Domain)
        page.click('#tab-triad')
        page.wait_for_timeout(1500)
        capture_uncovered_frame(
            page,
            "2. UNIFIED TRIAD GRAPH",
            "Order 1: Co-locates SOP KG (Indigo), Call CG (Amber) & ROI BG (Emerald) with explicit cross-graph edges!",
            (99, 102, 241)
        )

        # FRAME 3: ORDER 2 - Domain Subgraph Navigation (All Domains Unified)
        page.click('#triad-filter-all')
        page.wait_for_timeout(1500)
        capture_uncovered_frame(
            page,
            "3. MACRO ENTERPRISE",
            "Order 2: Domain Subgraphs unified into Corporate AI Hub (Billing SOP-04, Telecom SOP-12 & Enterprise SOP-28).",
            (16, 185, 129)
        )

        # FRAME 4: ORDER 3 - Real-Time Live Call & Graph Growth Stepper
        page.click('#tab-call')
        page.wait_for_timeout(1200)
        capture_uncovered_frame(
            page,
            "4. LIVE CALL SIMULATOR",
            "Order 3: Inbound customer call streams into 4-stage Real-Time Graph Growth Engine (T0:CG -> T1:KG -> T2:Decision -> T3:ROI).",
            (245, 158, 11)
        )

        # FRAME 5: Sample Call 2 - Broadband Outage & Telemetry Bypass
        page.click('#sample-btn-outage')
        page.wait_for_timeout(1200)
        capture_uncovered_frame(
            page,
            "5. REAL-TIME OUTAGE CALL",
            "Telemetry Grounding: Optical loss 31.4dB bypasses 180s manual phone reboot -> Auto-dispatches field tech in 12s.",
            (14, 165, 233)
        )

        # FRAME 6: SOP Knowledge Graph Tab (Rulebook Canvas)
        page.click('#tab-kg')
        page.wait_for_timeout(1500)
        capture_uncovered_frame(
            page,
            "6. SOP RULEBOOK GRAPH",
            "SOP Knowledge Graph (KG): Authoritative rulebook defining Tier-1 limits ($50), Supervisor limits ($250) & Roles.",
            (59, 130, 246)
        )

        # FRAME 7: Call Records Context Graph Tab (Call Diary Canvas)
        page.click('#tab-cg')
        page.wait_for_timeout(1500)
        capture_uncovered_frame(
            page,
            "7. CALL DIARY GRAPH",
            "Call Records Context Graph (CG): Empirical decision chain tracking customer state, telemetry alarms & agent concessions.",
            (245, 158, 11)
        )

        # FRAME 8: Business Goals ROI & Policy Drift Feedback Loop
        page.click('#tab-bg')
        page.wait_for_timeout(1500)
        capture_uncovered_frame(
            page,
            "8. BUSINESS ROI & DRIFT",
            "Business Graph (BG): Reconciles Should vs Actual -> +$2,250 Net Value & emits automated SOP updates back to KG!",
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
