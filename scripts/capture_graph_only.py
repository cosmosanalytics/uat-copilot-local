# -*- coding: utf-8 -*-
"""
Capture ONLY the graph canvas for each scenario, without stretching.
"""
import asyncio
import os
from playwright.async_api import async_playwright

async def capture_graphs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", headless=True)
        # 1600 x 900 viewport
        context = await browser.new_context(viewport={"width": 1600, "height": 900})
        page = await context.new_page()

        file_url = f"file:///{os.path.abspath('callcenter_ai_voice_agents.html').replace(os.sep, '/')}"
        print(f"Loading {file_url}...")
        await page.goto(file_url, wait_until="networkidle")

        assets_dir = os.path.abspath("docs/presentation_assets")
        os.makedirs(assets_dir, exist_ok=True)

        # Switch to Graph view mode
        await page.click("#btn-view-graph")
        await page.wait_for_timeout(400)

        # Graph canvas locator
        graph_el = page.locator("#unified-graph-canvas")

        # 1. Billing
        await page.click("#btn-usecase-billing")
        await page.wait_for_timeout(700)
        p1 = os.path.join(assets_dir, "graph_only_billing.png")
        await graph_el.screenshot(path=p1)
        print(f"Captured {p1}")

        # 2. Outage
        await page.click("#btn-usecase-outage")
        await page.wait_for_timeout(700)
        p2 = os.path.join(assets_dir, "graph_only_outage.png")
        await graph_el.screenshot(path=p2)
        print(f"Captured {p2}")

        # 3. Retention
        await page.click("#btn-usecase-retention")
        await page.wait_for_timeout(700)
        p3 = os.path.join(assets_dir, "graph_only_retention.png")
        await graph_el.screenshot(path=p3)
        print(f"Captured {p3}")

        await browser.close()
        print("Captured all 3 graph-only screenshots!")

if __name__ == "__main__":
    asyncio.run(capture_graphs())
