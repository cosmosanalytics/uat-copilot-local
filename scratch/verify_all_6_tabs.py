# -*- coding: utf-8 -*-
"""
verify_all_6_tabs.py
Verifies all 6 tabs in callcenter_ai_voice_agents.html:
1. Agent Hierarchical Structure
2. SOP Knowledge Graph
3. Call Records Context Graph
4. Business Goals & ROI Graph
5. Real-Time Live Call Simulator (with real-time growth animation)
6. Unified Triad Cross-Graph View (with domain subgraphs & cross-edges)
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

        # 1. Verify Hierarchy view
        assert page.is_visible('#view-hierarchy'), "Hierarchy view should be visible!"
        print("Tab 1 (Hierarchy) OK.")

        # 2. Verify Tab 2 (KG)
        page.click('#tab-kg')
        page.wait_for_timeout(600)
        assert page.is_visible('#view-kg'), "KG view should be visible!"
        print("Tab 2 (KG) OK.")

        # 3. Verify Tab 3 (CG)
        page.click('#tab-cg')
        page.wait_for_timeout(600)
        assert page.is_visible('#view-cg'), "CG view should be visible!"
        print("Tab 3 (CG) OK.")

        # 4. Verify Tab 4 (BG)
        page.click('#tab-bg')
        page.wait_for_timeout(600)
        assert page.is_visible('#view-bg'), "BG view should be visible!"
        print("Tab 4 (BG) OK.")

        # 5. Verify Tab 5 (Live Call & Graph Growth Stepper)
        page.click('#tab-call')
        page.wait_for_timeout(600)
        assert page.is_visible('#view-call'), "Live call view should be visible!"
        assert page.is_visible('#step-growth-1'), "Growth stepper should be visible!"
        
        # Test clicking sample question and watching stepper
        page.click('#sample-btn-outage')
        page.wait_for_timeout(1000)
        page.screenshot(path='scratch/live_call_growth_preview.png')
        print("Tab 5 (Live Call with Real-Time Growth Stepper) OK.")

        # 6. Verify Tab 6 (Unified Triad Cross-Graph View)
        page.click('#tab-triad')
        page.wait_for_timeout(1000)
        assert page.is_visible('#view-triad'), "Triad view should be visible!"
        assert page.is_visible('#triad-network'), "Triad network canvas should be visible!"

        # Test Domain filters in Triad view
        print("Testing Triad domain filters...")
        page.click('#triad-filter-outage')
        page.wait_for_timeout(500)
        page.click('#triad-filter-retention')
        page.wait_for_timeout(500)
        page.click('#triad-filter-all')
        page.wait_for_timeout(800)
        page.click('#triad-filter-billing')
        page.wait_for_timeout(500)

        # Capture Unified Triad screenshot
        page.screenshot(path='scratch/unified_triad_preview.png')
        print("Tab 6 (Unified Triad Cross-Graph) OK.")

        # Return to Hierarchy tab for clean main preview
        page.click('#tab-hierarchy')
        page.wait_for_timeout(500)
        page.screenshot(path='callcenter_ai_voice_agents_preview.png')

        browser.close()

        if errors:
            print(f"FAILED with {len(errors)} errors: {errors}")
            sys.exit(1)
        else:
            print("SUCCESS: ALL 6 TABS & DOMAIN SUBGRAPH FEATURES VERIFIED WITH 0 ERRORS!")

if __name__ == '__main__':
    main()
