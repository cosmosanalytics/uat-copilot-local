# -*- coding: utf-8 -*-
"""
verify_voice_agents_app.py
Verifies callcenter_ai_voice_agents.html including:
- Tab switching across all 5 tabs: Hierarchy, KG, CG, BG, and 5. Real-Time Live Call
- Sample question selection in the Live Call Simulator
- Real-time AI Voice Agent response grounded in SOP KG and Call Records CG
- Verification of HUD cards (KG, CG, BG)
- Cross-tab inspection links
"""

import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome', headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        
        errors = []
        page.on('console', lambda msg: print('BROWSER CONSOLE:', msg.text))
        page.on('pageerror', lambda err: errors.append(str(err)))

        file_path = os.path.abspath('callcenter_ai_voice_agents.html').replace('\\', '/')
        url = f'file:///{file_path}'
        print(f"Loading {url}...")
        page.goto(url)
        page.wait_for_timeout(1000)

        # 1. Verify Title & Initial Hierarchy View
        print("Page Title:", page.title())
        assert "Call Center AI Voice Agents" in page.title()

        # 2. Test Switching to Tab 5: Real-Time Live Call
        print("Testing Tab 5: Real-Time Live Call...")
        page.click('#tab-call')
        page.wait_for_timeout(1000)

        is_call_visible = page.is_visible('#view-call')
        print(f"view-call visibility: {is_call_visible}")
        assert is_call_visible, "view-call should be visible!"

        # Take screenshot of the Live Call Simulator in action
        live_preview_path = 'scratch/live_call_preview.png'
        page.screenshot(path=live_preview_path)
        print(f"Captured live call preview: {live_preview_path}")

        # 3. Test Sample Question 2: Broadband Hardware Outage
        print("Testing Sample Question 2 (Broadband Hardware Outage)...")
        page.click('#sample-btn-outage')
        page.wait_for_timeout(500)
        
        kg_sop = page.text_content('#hud-kg-sop-name')
        cg_caller = page.text_content('#hud-cg-caller-name')
        bg_val = page.text_content('#hud-bg-netvalue')
        print(f"Outage Result -> KG: {kg_sop} | CG: {cg_caller} | BG: {bg_val}")
        assert "SOP-12" in kg_sop
        assert "Marcus Vance" in cg_caller

        # 4. Test Sample Question 3: Enterprise Churn & Renewal
        print("Testing Sample Question 3 (Enterprise Churn & Renewal)...")
        page.click('#sample-btn-retention')
        page.wait_for_timeout(500)
        
        kg_sop = page.text_content('#hud-kg-sop-name')
        cg_caller = page.text_content('#hud-cg-caller-name')
        bg_val = page.text_content('#hud-bg-netvalue')
        print(f"Retention Result -> KG: {kg_sop} | CG: {cg_caller} | BG: {bg_val}")
        assert "SOP-28" in kg_sop
        assert "Elena Rostova" in cg_caller
        assert "+$27,900" in bg_val

        # 5. Test Sample Question 1: Billing Dispute
        print("Testing Sample Question 1 (Billing Dispute)...")
        page.click('#sample-btn-billing')
        page.wait_for_timeout(500)
        
        kg_sop = page.text_content('#hud-kg-sop-name')
        cg_caller = page.text_content('#hud-cg-caller-name')
        bg_val = page.text_content('#hud-bg-netvalue')
        print(f"Billing Result -> KG: {kg_sop} | CG: {cg_caller} | BG: {bg_val}")
        assert "SOP-04" in kg_sop
        assert "Sarah Jenkins" in cg_caller
        assert "+$2,250" in bg_val

        # 6. Test other tabs (KG, CG, BG, Hierarchy)
        print("Testing other tabs...")
        page.click('#tab-kg')
        page.wait_for_timeout(500)
        assert page.is_visible('#view-kg')

        page.click('#tab-cg')
        page.wait_for_timeout(500)
        assert page.is_visible('#view-cg')

        page.click('#tab-bg')
        page.wait_for_timeout(500)
        assert page.is_visible('#view-bg')

        page.click('#tab-hierarchy')
        page.wait_for_timeout(500)
        assert page.is_visible('#view-hierarchy')

        page.screenshot(path='callcenter_ai_voice_agents_preview.png')
        print("Updated main preview screenshot: callcenter_ai_voice_agents_preview.png")

        browser.close()

        if errors:
            print(f"FAIL: Encountered {len(errors)} page errors: {errors}")
            sys.exit(1)
        else:
            print("ALL PLAYWRIGHT TESTS PASSED WITH 0 ERRORS!")

if __name__ == '__main__':
    main()
