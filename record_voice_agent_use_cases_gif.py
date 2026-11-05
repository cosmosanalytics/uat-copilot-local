# -*- coding: utf-8 -*-
"""
record_voice_agent_use_cases_gif.py
Records high-fidelity annotated walkthrough of Call Center AI Voice Agent Use Cases:
  - Generates clear, high-contrast, large-font visual annotations on every frame
  - Highlights the Triad Graph Synthesis Hierarchy (KG + CG -> BG -> 4 Outcomes)
  - Features Use Case 1 (Billing Dispute & Policy Drift Feedback Loop)
  - Features Layer 1 (SOP KG), Layer 2 (Call Record CG), Layer 3 (Business Graph)
  - Features Use Case 2 (Broadband Outage Bottleneck Elimination)
  - Features Use Case 3 (VIP Retention & ARR Protection)
"""

import os
import sys
import time
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

FRAME_DIR = "scratch/voice_agent_gif_frames"
OUTPUT_GIF = "callcenter_use_cases_tour.gif"
PREVIEW_PNG = "callcenter_use_cases_preview.png"

os.makedirs(FRAME_DIR, exist_ok=True)

# Clean previous frames
for f in os.listdir(FRAME_DIR):
    if f.endswith('.png'):
        try:
            os.remove(os.path.join(FRAME_DIR, f))
        except:
            pass

# Load high-visibility Windows TrueType fonts
FONT_BOLD_22 = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22)
FONT_BOLD_16 = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16)
FONT_BOLD_13 = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)
FONT_BOLD_11 = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 11)
FONT_REG_14 = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 14)
FONT_REG_12 = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 12)

frames = []
frame_idx = 0

def annotate_and_save_frame(raw_path, step_badge, title, subtitle, callouts=[], accent_color=(16, 185, 129)):
    global frame_idx
    out_path = os.path.join(FRAME_DIR, f"annotated_{frame_idx:04d}.png")

    im = Image.open(raw_path).convert('RGBA')
    w, h = im.size

    # Transparent overlay for callout boxes
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    draw_base = ImageDraw.Draw(im)

    # 1. TOP HEADER BANNER (82px)
    banner_h = 82
    draw_base.rectangle([(0, 0), (w, banner_h)], fill=(15, 23, 42))
    # Accent indicator bar
    draw_base.rectangle([(0, banner_h - 5), (w, banner_h)], fill=accent_color)

    # Step Badge Pill
    badge_text = f" {step_badge} "
    badge_w = int(draw_base.textlength(badge_text, font=FONT_BOLD_11)) + 16
    draw_base.rounded_rectangle([(20, 12), (20 + badge_w, 34)], radius=5, fill=(30, 41, 59), outline=(99, 102, 241), width=1)
    draw_base.text((28, 15), badge_text, font=FONT_BOLD_11, fill=(165, 180, 252))

    # Title & Subtitle
    draw_base.text((20 + badge_w + 14, 10), title, font=FONT_BOLD_22, fill=(255, 255, 255))
    draw_base.text((24, 46), subtitle, font=FONT_REG_14, fill=(203, 213, 225))

    # 2. IN-SCENE CALLOUT OVERLAYS (Floating high-contrast cards)
    for c in callouts:
        cx, cy, cw, ch, c_title, c_text, c_bg, c_border = c
        # Card Background
        draw_overlay.rounded_rectangle([(cx, cy), (cx + cw, cy + ch)], radius=8, fill=c_bg, outline=c_border, width=2)
        # Card Header
        draw_base.text((cx + 12, cy + 8), c_title, font=FONT_BOLD_13, fill=(255, 255, 255))
        # Card Content Text
        draw_base.text((cx + 12, cy + 28), c_text, font=FONT_REG_12, fill=(241, 245, 249))

    # Composite overlay
    final_im = Image.alpha_composite(im, overlay).convert('RGB')
    final_im.save(out_path)
    frames.append(out_path)
    frame_idx += 1
    print(f"Annotated frame {frame_idx}: {title}")

def main():
    file_path = os.path.abspath('callcenter_ai_voice_agents.html').replace('\\', '/')
    url = f'file:///{file_path}'

    print("Launching Chromium via Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome', headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 820})
        page.goto(url)
        page.wait_for_timeout(1500)

        # -------------------------------------------------------------
        # FRAME 1: TRIAD HIERARCHY OVERVIEW
        # -------------------------------------------------------------
        raw1 = os.path.join(FRAME_DIR, "raw_01.png")
        page.screenshot(path=raw1)
        annotate_and_save_frame(
            raw1,
            "ARCHITECTURE OVERVIEW",
            "TRIAD GRAPH SYNTHESIS HIERARCHY",
            "Reconciles What SHOULD happen (SOPs) with What ACTUALLY happened (Call Records) to drive business value.",
            callouts=[
                (120, 160, 420, 52, "📋 KNOWLEDGE GRAPH (KG)", "Rulebook: Official SOPs, spending limits & approval roles.", (30, 27, 75, 240), (99, 102, 241)),
                (740, 160, 420, 52, "📞 CONTEXT GRAPH (CG)", "Diary: What actually occurred during live phone calls.", (6, 78, 59, 240), (16, 185, 129)),
                (430, 280, 420, 52, "⚖️ BUSINESS GRAPH (BG)", "Evaluator: Compares should vs actual to compute ROI & gaps.", (69, 26, 3, 240), (245, 158, 11))
            ],
            accent_color=(99, 102, 241)
        )

        # -------------------------------------------------------------
        # FRAME 2: USE CASE 1 (BILLING DISPUTE SCENARIO)
        # -------------------------------------------------------------
        page.select_option('#preset-select', 'billing_dispute')
        page.wait_for_timeout(800)
        raw2 = os.path.join(FRAME_DIR, "raw_02.png")
        page.screenshot(path=raw2)
        annotate_and_save_frame(
            raw2,
            "USE CASE 1: CONFLICT",
            "BILLING DISPUTE: $150 OVERCHARGE vs $50 SOP LIMIT",
            "Customer Sarah ($2,400 LTV) demands full $150 roaming fee waiver. Agent SOP is capped at $50.",
            callouts=[
                (380, 310, 520, 52, "⚠️ POLICY CONFLICT & CHURN RISK", "SOP limits agent to $50 • Customer demands $150 or cancels account.", (127, 29, 29, 245), (239, 68, 68)),
                (60, 500, 540, 54, "🛡️ SUPERVISOR EXCEPTION GRANTED", "Supervisor authorizes $150 credit under Section 4.2 High-LTV Hardship rule.", (30, 41, 59, 245), (16, 185, 129))
            ],
            accent_color=(245, 158, 11)
        )

        # -------------------------------------------------------------
        # FRAME 3: POLICY DRIFT FEEDBACK LOOP (HOW IMPROVEMENT IS ACHIEVED)
        # -------------------------------------------------------------
        raw3 = os.path.join(FRAME_DIR, "raw_03.png")
        page.screenshot(path=raw3)
        annotate_and_save_frame(
            raw3,
            "USE CASE 1: IMPROVEMENT",
            "POLICY DRIFT: CONTINUOUS LEARNING CLOSES THE LOOP TO KG",
            "47 supervisor exceptions detected this month. System automatically proposes updating SOP-04 in the Knowledge Graph.",
            callouts=[
                (60, 490, 560, 60, "💡 CONTINUOUS IMPROVEMENT (POLICY DRIFT)", "47 exceptions to $50 limit -> Updates SOP-04 to allow $150 limit for LTV > $2k.", (49, 46, 129, 250), (99, 102, 241)),
                (680, 490, 520, 60, "⚡ BOTTLENECK ELIMINATED", "Removes 45s supervisor transfer hold on future calls, saving 35 hrs/mo!", (69, 26, 3, 250), (245, 158, 11))
            ],
            accent_color=(99, 102, 241)
        )

        # -------------------------------------------------------------
        # FRAME 4: SOP KNOWLEDGE GRAPH VIEW (RULEBOOK)
        # -------------------------------------------------------------
        page.click('#tab-kg')
        page.wait_for_timeout(1500)
        raw4 = os.path.join(FRAME_DIR, "raw_04.png")
        page.screenshot(path=raw4)
        annotate_and_save_frame(
            raw4,
            "LAYER 1: RULEBOOK",
            "SOP KNOWLEDGE GRAPH (KG) - WHAT SHOULD HAPPEN",
            "Visualizing the official rulebook: Tier-1 Agent limit ($50), Supervisor limit ($250), and hardship exception rules.",
            callouts=[
                (60, 160, 520, 54, "📘 SOP-04 BILLING DISPUTE POLICY", "Governs allowable fee waivers & role authorization limits.", (30, 58, 138, 240), (59, 130, 246)),
                (700, 160, 500, 54, "🔒 ROLE AUTHORITY CAPS", "Tier-1 Agent limit: $50 • Supervisor limit: $250.", (4, 120, 87, 240), (16, 185, 129))
            ],
            accent_color=(59, 130, 246)
        )

        # -------------------------------------------------------------
        # FRAME 5: CALL RECORDS CONTEXT GRAPH VIEW (DIARY)
        # -------------------------------------------------------------
        page.click('#tab-cg')
        page.wait_for_timeout(1500)
        raw5 = os.path.join(FRAME_DIR, "raw_05.png")
        page.screenshot(path=raw5)
        annotate_and_save_frame(
            raw5,
            "LAYER 2: DIARY",
            "CALL RECORDS CONTEXT GRAPH (CG) - WHAT ACTUALLY HAPPENED",
            "Temporal decision chain: Event ($150 dispute) -> Agent Decision ($50 offer) -> Rejection -> Supervisor Exception ($150) -> Retained.",
            callouts=[
                (60, 160, 540, 54, "📞 EMPIRICAL DECISION SEQUENCE", "Captures chronological turns, objection reasons, and approvals.", (120, 53, 15, 240), (245, 158, 11)),
                (660, 160, 540, 54, "✅ FINAL CALL OUTCOME", "Customer Sarah retained • $150 credit applied • Precedent established.", (19, 78, 74, 240), (20, 184, 166))
            ],
            accent_color=(245, 158, 11)
        )

        # -------------------------------------------------------------
        # FRAME 6: BUSINESS GRAPH & ROI (THE BALANCE SHEET)
        # -------------------------------------------------------------
        page.click('#tab-bg')
        page.wait_for_timeout(1500)
        raw6 = os.path.join(FRAME_DIR, "raw_06.png")
        page.screenshot(path=raw6)
        annotate_and_save_frame(
            raw6,
            "LAYER 3: BALANCE SHEET",
            "BUSINESS GRAPH (BG) - MEASURING NET ROI & KPIs",
            "Reconciles Rulebook vs Diary: Calculates net business value, handle time efficiency, and churn prevention.",
            callouts=[
                (60, 160, 560, 54, "💰 NET VALUE EQUATION", "Retained LTV ($2,400) - Concession ($150) = +$2,250 Net Value.", (6, 78, 59, 240), (16, 185, 129)),
                (680, 160, 520, 54, "📈 OPERATIONAL KPIs", "FCR 100% • AHT 4m 12s (-45s faster) • CSAT 5/5.", (49, 46, 129, 240), (99, 102, 241))
            ],
            accent_color=(16, 185, 129)
        )

        # -------------------------------------------------------------
        # FRAME 7: USE CASE 2 (BROADBAND OUTAGE - BOTTLENECK ELIMINATION)
        # -------------------------------------------------------------
        page.click('#tab-hierarchy')
        page.select_option('#preset-select', 'tech_outage')
        page.wait_for_timeout(1000)
        raw7 = os.path.join(FRAME_DIR, "raw_07.png")
        page.screenshot(path=raw7)
        annotate_and_save_frame(
            raw7,
            "USE CASE 2: BOTTLENECK",
            "BROADBAND OUTAGE: ELIMINATING 180s MANUAL TRIAGE",
            "Customer reports optical loss. Eliminates redundant telephone questioning by triggering auto-dispatch in 12s.",
            callouts=[
                (60, 490, 560, 60, "⏱️ 180s PHONE BOTTLENECK ELIMINATED", "Bypasses obsolete manual script asking customer to reboot and check cords.", (120, 53, 15, 245), (245, 158, 11)),
                (660, 490, 540, 60, "🚀 AUTONOMOUS DISPATCH FAST-PATH", "Line telemetry triggers field tech truck roll in 12s (AHT 4.5m -> 1.5m).", (12, 74, 110, 245), (14, 165, 233))
            ],
            accent_color=(14, 165, 233)
        )

        # -------------------------------------------------------------
        # FRAME 8: USE CASE 3 (VIP RETENTION - ARR PROTECTION)
        # -------------------------------------------------------------
        page.select_option('#preset-select', 'vip_retention')
        page.wait_for_timeout(1000)
        raw8 = os.path.join(FRAME_DIR, "raw_08.png")
        page.screenshot(path=raw8)
        annotate_and_save_frame(
            raw8,
            "USE CASE 3: ARR PROTECTION",
            "VIP ACCOUNT RETENTION: PROTECTING +$27,900 ARR",
            "$18,000/yr enterprise client requests cancellation. Copilot delivers approved 15% discount contract during the live call.",
            callouts=[
                (60, 490, 560, 60, "💼 $30,600 2-YEAR CONTRACT LOCKED", "Secures 2-year renewal with 15% discount (under 20% SOP ceiling).", (6, 78, 59, 245), (16, 185, 129)),
                (660, 490, 540, 60, "⚖️ ZERO COMPLIANCE GAP", "Contract extension pre-authorized by legal terms with instant SMS e-signature.", (49, 46, 129, 245), (99, 102, 241))
            ],
            accent_color=(16, 185, 129)
        )

        browser.close()

    print("Compiling annotated frames into high-quality animated GIF...")
    pil_images = [Image.open(f) for f in frames]
    if pil_images:
        # Save preview image
        pil_images[0].save(PREVIEW_PNG)
        print(f"Saved preview to {PREVIEW_PNG}")

        # Save GIF with 2200ms per frame for readable pacing
        pil_images[0].save(
            OUTPUT_GIF,
            save_all=True,
            append_images=pil_images[1:],
            duration=2200,
            loop=0,
            optimize=True
        )
        print(f"Successfully generated {OUTPUT_GIF} ({os.path.getsize(OUTPUT_GIF)} bytes, {len(frames)} frames)")

if __name__ == '__main__':
    main()
