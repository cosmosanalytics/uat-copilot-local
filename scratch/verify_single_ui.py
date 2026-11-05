# -*- coding: utf-8 -*-
"""
verify_single_ui.py
Verifies the single unified UI in callcenter_ai_voice_agents.html:
- Upper side: Real-time live call with sample questions, ASR transcript, agent speech
- Lower side: BG, KG, and CG highlighted for the current call
- Cross-usecase selector
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
        page.wait_for_timeout(1200)

        # 1. Verify Page Title
        print("Page Title:", page.title())
        assert "Call Center AI Voice Agents" in page.title()

        # 2. Verify Upper Call Section
        caller_text = page.text_content('#caller-id-pill')
        cust_speech = page.text_content('#cust-speech-text')
        agent_speech = page.text_content('#agent-speech-text')
        print("Upper Call -> Caller:", caller_text)
        print("Customer Speech:", cust_speech[:60])
        print("Agent Speech:", agent_speech[:60])
        assert "Sarah Jenkins" in caller_text

        # 3. Verify Lower Graph Section
        path_label = page.text_content('#active-call-highlight-label')
        net_val = page.text_content('#stat-netvalue')
        print("Lower Graph -> Path Label:", path_label)
        print("Net Value Stat:", net_val)
        assert "Sarah Jenkins" in path_label
        assert "+$2,250" in net_val

        # 4. Test Switching to Use Case 2: Broadband Outage
        print("Selecting Use Case 2 (Broadband Outage)...")
        page.click('#btn-usecase-outage')
        page.wait_for_timeout(800)

        caller_text_2 = page.text_content('#caller-id-pill')
        path_label_2 = page.text_content('#active-call-highlight-label')
        net_val_2 = page.text_content('#stat-netvalue')
        print(f"Outage Result -> Caller: {caller_text_2} | Path: {path_label_2} | Net: {net_val_2}")
        assert "Marcus Vance" in caller_text_2
        assert "SOP-12" in path_label_2

        # 5. Test Switching to Use Case 3: VIP Retention
        print("Selecting Use Case 3 (VIP Retention)...")
        page.click('#btn-usecase-retention')
        page.wait_for_timeout(800)

        caller_text_3 = page.text_content('#caller-id-pill')
        path_label_3 = page.text_content('#active-call-highlight-label')
        net_val_3 = page.text_content('#stat-netvalue')
        print(f"Retention Result -> Caller: {caller_text_3} | Path: {path_label_3} | Net: {net_val_3}")
        assert "Apex Logistics" in path_label_3
        assert "+$27,900" in net_val_3

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
        page.screenshot(path='scratch/single_ui_preview.png')
        print(f"Captured clean preview screenshot: {out_png}")

        browser.close()

        if errors:
            print(f"FAIL with errors: {errors}")
            sys.exit(1)
        else:
            print("SUCCESS: ALL SINGLE UI VERIFICATIONS PASSED WITH 0 ERRORS!")

if __name__ == '__main__':
    main()
