# -*- coding: utf-8 -*-
"""
verify_callcenter_studio.py
Verifies callcenter_macro_graph_studio.html using Playwright,
tests canvas rendering, critical path toggle, and optimization tab,
and captures callcenter_macro_graph_preview.png.
"""

import os
import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome', headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})

        abs_path = os.path.abspath('callcenter_macro_graph_studio.html').replace('\\', '/')
        url = f'file:///{abs_path}'
        print(f"Loading {url}...")
        page.goto(url)
        page.wait_for_timeout(1500)

        title = page.title()
        print(f"Title: {title}")

        # Check nodes count on canvas
        nodes = page.locator('.graph-node')
        print(f"Rendered nodes on canvas: {nodes.count()}")

        # Click show voice critical path
        crit_btn = page.locator('#btnToggleCriticalPath')
        if crit_btn.count() > 0:
            crit_btn.click()
            print("Clicked: Show Voice Critical Path")
            page.wait_for_timeout(1000)

        # Click on a node to open inspection drawer (e.g. acd_queue_ingress)
        first_node = nodes.first
        if first_node.count() > 0:
            first_node.click()
            print("Clicked first node to open drawer")
            page.wait_for_timeout(500)

        # Capture high-res preview screenshot
        out_png = 'callcenter_macro_graph_preview.png'
        page.screenshot(path=out_png)
        print(f"Saved preview screenshot: {out_png} ({os.path.getsize(out_png)} bytes)")

        # Also test switching to Optimization tab
        page.click('#tabBtnOptimization')
        page.wait_for_timeout(800)
        opt_latency = page.locator('#optCritLatency').inner_text()
        print(f"Optimization Tab Latency Metric: {opt_latency}")

        # Switch back to canvas for clean final view
        page.click('#tabBtnCanvas')
        page.wait_for_timeout(500)

        browser.close()
        print("Verification complete!")

if __name__ == '__main__':
    main()
