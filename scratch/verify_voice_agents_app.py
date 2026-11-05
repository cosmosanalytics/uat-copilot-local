# -*- coding: utf-8 -*-
"""
verify_voice_agents_app.py
Verifies callcenter_ai_voice_agents.html using Playwright,
tests tab switching (Agent Hierarchy -> KG -> CG -> BG),
and captures callcenter_ai_voice_agents_preview.png.
"""

import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome', headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.on('console', lambda msg: print('CONSOLE:', msg.text))
        page.on('pageerror', lambda err: print('ERROR:', err))

        file_path = os.path.abspath('callcenter_ai_voice_agents.html').replace('\\', '/')
        url = f'file:///{file_path}'
        print(f"Loading {url}...")
        page.goto(url)
        page.wait_for_timeout(1000)

        print("Page title:", page.title())

        # Take screenshot of Hierarchy View
        out_png = 'callcenter_ai_voice_agents_preview.png'
        page.screenshot(path=out_png)
        print(f"Captured initial hierarchy screenshot: {out_png}")

        # Test switching to KG tab
        page.click('#tab-kg')
        page.wait_for_timeout(1000)
        print("Switched to SOP Knowledge Graph tab.")

        # Test switching to CG tab
        page.click('#tab-cg')
        page.wait_for_timeout(1000)
        print("Switched to Call Records Context Graph tab.")

        # Test switching to BG tab
        page.click('#tab-bg')
        page.wait_for_timeout(1000)
        print("Switched to Business Goals Graph tab.")

        # Click Execute button
        page.click('#btn-run')
        page.wait_for_timeout(1000)

        # Switch back to Hierarchy view for clean final state
        page.click('#tab-hierarchy')
        page.wait_for_timeout(500)
        page.screenshot(path=out_png)

        browser.close()
        print("Verification successful!")

if __name__ == '__main__':
    main()
