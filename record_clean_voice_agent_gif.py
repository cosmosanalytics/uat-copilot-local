# -*- coding: utf-8 -*-
"""
record_clean_voice_agent_gif.py
Records the Call Center AI Voice Agents Studio with the Single Unified UI:
- Upper Side: Real-Time Live Call (active caller, question chips, ASR, agent speech, voice synthesis)
- Lower Side: BG, KG, and CG highlighted for the current call with cross-graph edges
- Cross-Usecases Option: Macro Enterprise View
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
    draw.rounded_rectangle([(16, 12), (16 + 225, 36)], radius=6, fill=(30, 41, 59), outline=accent_rgb, width=1)
    draw.text((24, 15), step_label, font=FONT_BOLD_14, fill=(241, 245, 249))

    # Caption text
    draw.text((258, 16), caption_text, font=FONT_REG_12, fill=(226, 232, 240))

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

        # FRAME 1: Single UI Overview - Billing Call Active
        capture_uncovered_frame(
            page,
            "1. SINGLE UNIFIED UI",
            "Upper: Real-Time Live Call (Sarah Jenkins $150 dispute) &bull; Lower: KG, CG & BG highlighted for the current call!",
            (99, 102, 241)
        )

        # FRAME 2: Upper Live Call & Grounded Speech Playback
        page.click('#chip-q-billing')
        page.wait_for_timeout(1000)
        capture_uncovered_frame(
            page,
            "2. LIVE CALL GROUNDING",
            "Upper: Customer asks $150 fee waiver -> AI Agent grounds in SOP-04 Clause 4.2 ($2.4k LTV) -> Waives $150 with $0 hold.",
            (16, 185, 129)
        )

        # FRAME 3: Lower Graph Call Path Highlight (Sarah Jenkins -> SOP-04 -> +$2,250 ROI)
        page.click('#btn-focus-call')
        page.wait_for_timeout(1200)
        capture_uncovered_frame(
            page,
            "3. GRAPH HIGHLIGHTED",
            "Lower: SOP Rulebook (KG) + Call Record (CG) -> Reconciles +$2,250 Net Value (BG) & logs drift loop back to SOP-04!",
            (245, 158, 11)
        )

        # FRAME 4: Use Case 2 - Broadband Outage & Instant Tech Dispatch
        page.click('#btn-usecase-outage')
        page.wait_for_timeout(1200)
        capture_uncovered_frame(
            page,
            "4. USE CASE 2: OUTAGE",
            "Upper: Marcus Vance red LOS alarm -> Lower: Optical loss 31.4dB conforms to SOP-12 -> Auto-dispatches truck in 12s.",
            (14, 165, 233)
        )

        # FRAME 5: Use Case 3 - Enterprise Churn & ARR Retention
        page.click('#btn-usecase-retention')
        page.wait_for_timeout(1200)
        capture_uncovered_frame(
            page,
            "5. USE CASE 3: RETENTION",
            "Upper: Elena Rostova $18k cancellation -> Lower: SOP-28 Clause 2.4 locks 15% discount renewal -> Protects +$27,900 ARR.",
            (16, 185, 129)
        )

        # FRAME 6: Cross-Usecases View (All Domains Co-located in Corporate Core)
        page.click('#btn-usecase-cross')
        page.wait_for_timeout(1500)
        capture_uncovered_frame(
            page,
            "6. CROSS-USECASES VIEW",
            "Enterprise Macro View: Corporate AI Hub co-locates and cross-correlates Billing (SOP-04), Outage (SOP-12) & Retention (SOP-28).",
            (99, 102, 241)
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
