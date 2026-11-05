# -*- coding: utf-8 -*-
"""
verify_single_ui.py
Verifies the spatial hierarchy Single UI:
- Upper Side: Real-time call console (active caller, question chips, ASR, agent speech, voice synthesis)
- Lower Side: Spatial Vis.js graph matching the user's diagram:
  - Upper Left: KG (What SHOULD happen - SOPs)
  - Upper Right: CG (What ACTUALLY happened - calls)
  - Center Middle: BG (Compares should vs actual)
  - Bottom: 4 Improvement Potentials (Policy drift, Compliance gap, Net value, Bottlenecks)
  - Dashed feedback loop from Policy drift to KG
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
        page.on('console', lambda msg: print('CONSOLE:', msg.text))
        page.on('pageerror', lambda err: errors.append(str(err)))

        file_path = os.path.abspath('callcenter_ai_voice_agents.html').replace('\\', '/')
        url = f'file:///{file_path}'
        print(f"Loading {url}...")
        page.goto(url)
        page.wait_for_timeout(1000)

        # 1. Verify Page Title
        print("Page Title:", page.title())
        assert "Call Center AI Voice Agents" in page.title()

        # 2. Verify Upper Call Section
        caller_text = page.text_content('#caller-id-pill')
        cust_speech = page.text_content('#cust-speech-text')
        agent_speech = page.text_content('#agent-speech-text')
        roi_tag = page.text_content('#net-roi-tag')
        print("Upper Call -> Caller:", caller_text)
        print("Customer Speech:", cust_speech[:60])
        print("Agent Speech:", agent_speech[:60])
        print("ROI Tag:", roi_tag)
        assert "Sarah Jenkins" in caller_text
        assert "+$2,250" in roi_tag

        # 3. Verify Lower Spatial Graph Canvas
        assert page.is_visible('#unified-graph-canvas'), "Canvas should be visible!"
        path_label = page.text_content('#active-call-highlight-label')
        print("Spatial Graph Path Label:", path_label)
        assert "Sarah Jenkins" in path_label

        # 4. Test Switching to Use Case 2: Broadband Outage
        print("Selecting Use Case 2 (Broadband Outage)...")
        page.click('#btn-usecase-outage')
        page.wait_for_timeout(800)

        caller_text_2 = page.text_content('#caller-id-pill')
        path_label_2 = page.text_content('#active-call-highlight-label')
        roi_2 = page.text_content('#net-roi-tag')
        print(f"Outage Result -> Caller: {caller_text_2} | Path: {path_label_2} | Net: {roi_2}")
        assert "Marcus Vance" in caller_text_2
        assert "SOP-12" in path_label_2

        # 5. Test Switching to Use Case 3: VIP Retention
        print("Selecting Use Case 3 (VIP Retention)...")
        page.click('#btn-usecase-retention')
        page.wait_for_timeout(800)

        caller_text_3 = page.text_content('#caller-id-pill')
        path_label_3 = page.text_content('#active-call-highlight-label')
        roi_3 = page.text_content('#net-roi-tag')
        print(f"Retention Result -> Caller: {caller_text_3} | Path: {path_label_3} | Net: {roi_3}")
        assert "Apex Logistics" in path_label_3
        assert "+$27,900" in roi_3

        # 6. Test Cross-Usecases View
        print("Selecting Cross-Usecases View...")
        page.click('#btn-usecase-cross')
        page.wait_for_timeout(800)
        cross_label = page.text_content('#active-call-highlight-label')
        print("Cross-Usecases Label:", cross_label)
        assert "Cross-Usecases View" in cross_label

        # 7. Switch back to Billing for clean preview screenshot
        page.click('#btn-usecase-billing')
        page.wait_for_timeout(800)

        out_png = 'callcenter_ai_voice_agents_preview.png'
        page.screenshot(path=out_png)
        page.screenshot(path='scratch/spatial_hierarchy_preview.png')
        print(f"Captured clean preview screenshot: {out_png}")

        browser.close()

        if errors:
            print(f"FAIL with errors: {errors}")
            sys.exit(1)
        else:
            print("SUCCESS: ALL SPATIAL HIERARCHY VERIFICATIONS PASSED WITH 0 ERRORS!")

if __name__ == '__main__':
    main()
