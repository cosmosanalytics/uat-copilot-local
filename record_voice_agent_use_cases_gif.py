# -*- coding: utf-8 -*-
"""
record_voice_agent_use_cases_gif.py
Records an annotated walkthrough demonstrating Call Center AI Voice Agent Use Cases
and how continuous improvement is achieved via the Triad Graph Synthesis Hierarchy:
  1. Hierarchy Overview: KG (What should happen) + CG (What actually happened) -> BG (Reconciles should vs actual)
  2. Use Case 1 (Billing Dispute): Overcharge Exception & Policy Drift Feedback Loop updating the SOP.
  3. SOP Knowledge Graph View: Rulebook, approval limits, exception clauses.
  4. Call Records Context Graph View: Empirical decision traces (Event -> Decision -> Exception -> Outcome).
  5. Business Graph View: Net Value calculation (+$2,250 ROI) & SLA reconciliation.
  6. Use Case 2 (Broadband Outage): Eliminating 180s diagnostic bottleneck via telemetry auto-dispatch.
  7. Use Case 3 (VIP Retention): Protecting $27.9K ARR with multi-agent copilot.
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

frames = []
frame_idx = 0

def capture_annotated_frame(page, title, subtitle="", highlight_color=(16, 185, 129)):
    global frame_idx
    raw_path = os.path.join(FRAME_DIR, f"raw_{frame_idx:04d}.png")
    out_path = os.path.join(FRAME_DIR, f"frame_{frame_idx:04d}.png")
    page.screenshot(path=raw_path)

    # Open with PIL and draw header banner
    im = Image.open(raw_path)
    draw = ImageDraw.Draw(im)
    w, h = im.size

    banner_h = 54
    # Dark banner background
    draw.rectangle([(0, 0), (w, banner_h)], fill=(15, 23, 42))
    # Accent indicator line
    draw.rectangle([(0, banner_h - 4), (w, banner_h)], fill=highlight_color)

    # Use default font or basic font
    draw.text((24, 10), title, fill=(255, 255, 255))
    if subtitle:
        draw.text((24, 30), subtitle, fill=(148, 163, 184))

    im.save(out_path)
    frames.append(out_path)
    frame_idx += 1
    print(f"Captured frame {frame_idx}: {title}")

def main():
    file_path = os.path.abspath('callcenter_ai_voice_agents.html').replace('\\', '/')
    url = f'file:///{file_path}'

    print("Launching Chromium via Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome', headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        page.goto(url)
        page.wait_for_timeout(1500)

        # -------------------------------------------------------------
        # FRAME 1: INTRO & TRIAD ARCHITECTURE
        # -------------------------------------------------------------
        capture_annotated_frame(
            page,
            "TRIAD GRAPH SYNTHESIS ARCHITECTURE",
            "KG (What SHOULD happen) + CG (What ACTUALLY happened) -> BG (Evaluates business impact)",
            (99, 102, 241)
        )

        # -------------------------------------------------------------
        # FRAME 2: USE CASE 1 (BILLING DISPUTE & POLICY DRIFT)
        # -------------------------------------------------------------
        page.select_option('#preset-select', 'billing_dispute')
        page.wait_for_timeout(1000)
        capture_annotated_frame(
            page,
            "USE CASE 1: BILLING DISPUTE & POLICY DRIFT FEEDBACK LOOP",
            "High-LTV customer billed $150. SOP limit is $50. Supervisor authorizes $150 exception.",
            (245, 158, 11)
        )

        # -------------------------------------------------------------
        # FRAME 3: POLICY DRIFT & CONTINUOUS IMPROVEMENT HIGHLIGHT
        # -------------------------------------------------------------
        capture_annotated_frame(
            page,
            "IMPROVEMENT: POLICY DRIFT CLOSES THE LOOP TO SOPs",
            "47 exceptions detected -> System auto-updates SOP-04 to allow $150 limit, eliminating 45s hold!",
            (99, 102, 241)
        )

        # -------------------------------------------------------------
        # FRAME 4: SOP KNOWLEDGE GRAPH (RULEBOOK)
        # -------------------------------------------------------------
        page.click('#tab-kg')
        page.wait_for_timeout(1500)
        capture_annotated_frame(
            page,
            "LAYER 1: SOP KNOWLEDGE GRAPH (THE RULEBOOK)",
            "Formalizes policies, allowable limits (Tier-1: $50, Supervisor: $250) and role authorizations.",
            (59, 130, 246)
        )

        # -------------------------------------------------------------
        # FRAME 5: CALL RECORDS CONTEXT GRAPH (DIARY)
        # -------------------------------------------------------------
        page.click('#tab-cg')
        page.wait_for_timeout(1500)
        capture_annotated_frame(
            page,
            "LAYER 2: CALL RECORDS CONTEXT GRAPH (THE DIARY)",
            "Traces empirical events: Disputed $150 -> $50 Offer -> Churn Threat -> Supervisor Exception -> Retained.",
            (245, 158, 11)
        )

        # -------------------------------------------------------------
        # FRAME 6: BUSINESS GRAPH & ROI (THE BALANCE SHEET)
        # -------------------------------------------------------------
        page.click('#tab-bg')
        page.wait_for_timeout(1500)
        capture_annotated_frame(
            page,
            "LAYER 3: BUSINESS GRAPH & ROI EVALUATION",
            "Reconciles Rulebook vs Diary: +$2,250 Net Value ($2,400 LTV protected - $150 concession fee).",
            (16, 185, 129)
        )

        # -------------------------------------------------------------
        # FRAME 7: USE CASE 2 (BROADBAND OUTAGE & BOTTLENECK ELIMINATION)
        # -------------------------------------------------------------
        page.click('#tab-hierarchy')
        page.select_option('#preset-select', 'tech_outage')
        page.wait_for_timeout(1200)
        capture_annotated_frame(
            page,
            "USE CASE 2: BROADBAND OUTAGE & BOTTLENECK ELIMINATION",
            "Customer reports optical loss. Eliminates 180s phone diagnostic by automating line test in 12s.",
            (14, 165, 233)
        )

        # -------------------------------------------------------------
        # FRAME 8: USE CASE 2 CONTEXT GRAPH (AUTONOMOUS DISPATCH)
        # -------------------------------------------------------------
        page.click('#tab-cg')
        page.wait_for_timeout(1500)
        capture_annotated_frame(
            page,
            "USE CASE 2 CONTEXT GRAPH: AUTONOMOUS TECH DISPATCH",
            "Event: Red Light -> Line Test Run -> Tech Dispatched Today 2 PM (AHT slashed from 4.5m to 1.5m).",
            (14, 165, 233)
        )

        # -------------------------------------------------------------
        # FRAME 9: USE CASE 3 (VIP RETENTION & ARR PROTECTION)
        # -------------------------------------------------------------
        page.click('#tab-hierarchy')
        page.select_option('#preset-select', 'vip_retention')
        page.wait_for_timeout(1200)
        capture_annotated_frame(
            page,
            "USE CASE 3: VIP ACCOUNT CHURN & ARR RETENTION",
            "$18,000/yr enterprise client requests cancellation. Copilot matches 15% 2-year renewal contract.",
            (139, 92, 246)
        )

        # -------------------------------------------------------------
        # FRAME 10: USE CASE 3 BUSINESS GRAPH (ARR METRICS)
        # -------------------------------------------------------------
        page.click('#tab-bg')
        page.wait_for_timeout(1500)
        capture_annotated_frame(
            page,
            "USE CASE 3 BUSINESS VALUE: +$27,900 ARR PROTECTED",
            "Compliance: 100% legal terms approved. Net ROI: $30,600 contract locked with 15% discount.",
            (16, 185, 129)
        )

        # -------------------------------------------------------------
        # FRAME 11: MULTI-AGENT EXECUTION EVALUATION
        # -------------------------------------------------------------
        page.click('#tab-hierarchy')
        page.wait_for_timeout(800)
        page.click('#btn-run')
        page.wait_for_timeout(1000)
        capture_annotated_frame(
            page,
            "CONTINUOUS ENTERPRISE LEARNING & AI VOICE AGENTS",
            "Autonomous reconciliation transforms unstructured phone calls into self-improving SOP rulebooks.",
            (16, 185, 129)
        )

        browser.close()

    print("Compiling frames into high-quality animated GIF...")
    pil_images = [Image.open(f) for f in frames]
    if pil_images:
        # Save preview png
        pil_images[0].save(PREVIEW_PNG)
        print(f"Saved preview image to {PREVIEW_PNG}")

        # Save GIF with durations (1800ms per frame)
        pil_images[0].save(
            OUTPUT_GIF,
            save_all=True,
            append_images=pil_images[1:],
            duration=1800,
            loop=0,
            optimize=True
        )
        print(f"Successfully created {OUTPUT_GIF} ({os.path.getsize(OUTPUT_GIF)} bytes, {len(frames)} frames)")

if __name__ == '__main__':
    main()
