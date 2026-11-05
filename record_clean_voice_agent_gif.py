# -*- coding: utf-8 -*-
"""
record_clean_voice_agent_gif.py
Records the Call Center AI Voice Agents Studio with:
- Crisp LIGHT MODE
- ACTUAL multi-node network graphs in each spatial zone:
  - Upper-Left: Knowledge Graph network (SOP, Tier-1 Limit, VIP Limit, Agent Role)
  - Upper-Right: Context Graph network (Customer, Dispute Event, Decision, Churn Diary)
  - Center-Middle: Business Graph network (Goal, Reconciliation Engine, KPI FCR)
  - Bottom: 4 Improvement Potentials
  - Dashed Feedback Loop from Policy drift back up to SOP-04!
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
    new_canvas = Image.new('RGB', (app_w, total_h), (248, 250, 252)) # Crisp light bar

    draw = ImageDraw.Draw(new_canvas)

    # Accent color separator line between caption bar and app
    draw.rectangle([(0, caption_h - 3), (app_w, caption_h)], fill=accent_rgb)

    # Badge Pill
    draw.rounded_rectangle([(16, 12), (16 + 230, 36)], radius=6, fill=(241, 245, 249), outline=accent_rgb, width=1)
    draw.text((24, 15), step_label, font=FONT_BOLD_14, fill=(15, 23, 42))

    # Caption text
    draw.text((264, 16), caption_text, font=FONT_REG_12, fill=(51, 65, 85))

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

        # FRAME 1: Single UI Overview in Light Mode with Actual Multi-Node Graphs
        capture_uncovered_frame(
            page,
            "1. LIGHT MODE ACTUAL GRAPHS",
            "Upper: Live Call Console &bull; Lower: Actual Multi-Node Networks for KG (Upper-Left), CG (Upper-Right) & BG (Center-Middle)!",
            (79, 70, 229)
        )

        # FRAME 2: Live Inbound Call & Grounded Voice Speech
        page.click('#chip-q-billing')
        page.wait_for_timeout(1000)
        capture_uncovered_frame(
            page,
            "2. LIVE INBOUND CALL",
            "Sarah Jenkins asks $150 fee waiver -> AI Agent grounds in SOP-04 Clause 4.2 ($2.4k LTV) -> Waives $150 with $0 balance.",
            (16, 185, 129)
        )

        # FRAME 3: Policy Drift Loop from Bottom-Left back up to KG
        capture_uncovered_frame(
            page,
            "3. POLICY DRIFT LOOP",
            "Reconciliation: 47 repeated exceptions trigger automated update from Bottom Policy Drift back up to Knowledge Graph!",
            (219, 39, 119)
        )

        # FRAME 4: Use Case 2 - Broadband Outage & Field Dispatch
        page.click('#btn-usecase-outage')
        page.wait_for_timeout(1200)
        capture_uncovered_frame(
            page,
            "4. USE CASE 2: OUTAGE",
            "Marcus Vance red optical alarm -> 31.4dB loss conforms to SOP-12 -> Instant field truck roll dispatched in 12s.",
            (2, 132, 199)
        )

        # FRAME 5: Use Case 3 - Enterprise Churn & ARR Lock
        page.click('#btn-usecase-retention')
        page.wait_for_timeout(1200)
        capture_uncovered_frame(
            page,
            "5. USE CASE 3: RETENTION",
            "Elena Rostova cancellation -> SOP-28 Clause 2.4 locks 15% discount renewal -> Protects +$27,900 2-yr ARR.",
            (16, 185, 129)
        )

        # FRAME 6: Cross-Usecases View (All Domains Co-located in Corporate Core)
        page.click('#btn-usecase-cross')
        page.wait_for_timeout(1500)
        capture_uncovered_frame(
            page,
            "6. CROSS-USECASES VIEW",
            "Enterprise Macro View: Corporate AI Hub co-locates and cross-correlates Billing (SOP-04), Outage (SOP-12) & Retention (SOP-28).",
            (79, 70, 229)
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
            duration=2400,
            loop=0,
            optimize=True
        )
        print(f"Successfully generated clean {OUTPUT_GIF} ({os.path.getsize(OUTPUT_GIF)} bytes, {len(frames)} frames)")

if __name__ == '__main__':
    main()
