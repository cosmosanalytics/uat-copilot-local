import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def test_app(url, app_prefix):
    print(f"\nTesting {app_prefix}: {url}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='chrome')
        page = await browser.new_page(viewport={'width': 1600, 'height': 900})
        await page.goto(url)
        await page.wait_for_timeout(1000)

        keys = ['it_security', 'fintech_dispute', 'cloud_devops']
        for k in keys:
            # Step 1: Click starter template
            await page.click('#tabBtn1')
            await page.wait_for_timeout(300)
            btn = await page.query_selector(f"button[onclick*=\"loadStarterTemplate('{k}')\"]")
            if btn:
                await btn.click()
                await page.wait_for_timeout(500)
            
            # Step 2: Switch to Step 2 (Flowchart & Policy Tree)
            await page.click('#tabBtn2')
            await page.wait_for_timeout(800)

            # Query text inside Mermaid target
            dag_el = await page.query_selector('#mermaidGraphEl')
            dag_html = await dag_el.inner_html() if dag_el else ""
            print(f"[{app_prefix} - {k}] SVG length: {len(dag_html)}, contains svg? {'<svg' in dag_html}")

            # Capture screenshot
            shot_path = f"scratch/{app_prefix}_{k}_flowchart.png"
            await page.screenshot(path=shot_path, full_page=False)
            print(f"  -> Captured {shot_path}")

        await browser.close()

async def main():
    await test_app('file:///C:/Users/richa/ai-engineering/truth_policy_flowchart_studio.html', 'app8')
    await test_app('file:///C:/Users/richa/ai-engineering/truth_langgraph_langsmith_studio.html', 'app9')

asyncio.run(main())
