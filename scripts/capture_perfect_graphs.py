# -*- coding: utf-8 -*-
"""
Capture clean, uncompressed, unstretched graph-only screenshots for the PowerPoint deck.
"""
import asyncio
import os
from playwright.async_api import async_playwright

async def capture_all_graphs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", headless=True)
        # 1280 x 720 (16:9) viewport tailored for graph canvas
        context = await browser.new_context(viewport={"width": 1280, "height": 720})
        page = await context.new_page()

        file_url = f"file:///{os.path.abspath('callcenter_ai_voice_agents.html').replace(os.sep, '/')}"
        print(f"Loading {file_url}...")
        await page.goto(file_url, wait_until="networkidle")

        assets_dir = os.path.abspath("docs/presentation_assets")
        os.makedirs(assets_dir, exist_ok=True)

        # 1. Switch to Graph View Mode so graph takes 100% of container
        await page.click("#btn-view-graph")
        await page.wait_for_timeout(300)

        # Graph section locator (includes the clean color legends at top and the multi-node network)
        graph_section = page.locator("#section-graph-grounding")

        # 1. Billing
        print("Capturing Graph 1: Billing...")
        await page.click("#btn-usecase-billing")
        await page.wait_for_timeout(600)
        # Center the network properly
        await page.click("button:has-text('Center')")
        await page.wait_for_timeout(500)
        p1 = os.path.join(assets_dir, "graph_only_billing.png")
        await graph_section.screenshot(path=p1)
        print(f"Saved: {p1}")

        # 2. Outage
        print("Capturing Graph 2: Outage...")
        await page.click("#btn-usecase-outage")
        await page.wait_for_timeout(600)
        await page.click("button:has-text('Center')")
        await page.wait_for_timeout(500)
        p2 = os.path.join(assets_dir, "graph_only_outage.png")
        await graph_section.screenshot(path=p2)
        print(f"Saved: {p2}")

        # 3. Retention
        print("Capturing Graph 3: Retention...")
        await page.click("#btn-usecase-retention")
        await page.wait_for_timeout(600)
        await page.click("button:has-text('Center')")
        await page.wait_for_timeout(500)
        p3 = os.path.join(assets_dir, "graph_only_retention.png")
        await graph_section.screenshot(path=p3)
        print(f"Saved: {p3}")

        await browser.close()
        print("Graph-only screenshots captured successfully!")

if __name__ == "__main__":
    asyncio.run(capture_all_graphs())
