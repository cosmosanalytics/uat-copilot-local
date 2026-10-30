import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='chrome')
        page = await browser.new_page(viewport={'width': 1600, 'height': 900})
        await page.goto('file:///C:/Users/richa/ai-engineering/truth_langgraph_langsmith_studio.html')
        await page.wait_for_timeout(1000)

        # Clear Input 1 (title & text)
        await page.fill('#customDocTitleInput', '')
        await page.fill('#customDocTextInput', '')

        # Fill Input 2 with the Wikipedia link
        await page.fill('#customWebAddressInput', 'https://en.wikipedia.org/wiki/MPC')
        await page.wait_for_timeout(300)

        # Click Connect
        connect_btn = await page.query_selector("button[onclick*='applyCustomWebUrl']")
        if connect_btn:
            await connect_btn.click()
            await page.wait_for_timeout(800)

        # Inspect Document View content on the right
        doc_box = await page.query_selector('.doc-viewport')
        doc_text = await doc_box.inner_text() if doc_box else ""
        print("--- EXTRACTED DOCUMENT TEXT IN STEP 1 ---")
        print(doc_text[:400])

        # Capture Step 1 screenshot
        await page.screenshot(path='scratch/verified_link_intake_step1.png', full_page=False)
        print("\nCaptured scratch/verified_link_intake_step1.png")

        # Now switch to Step 2 to check the compiled Flowchart
        await page.click('#tabBtn2')
        await page.wait_for_timeout(800)

        dag_el = await page.query_selector('#mermaidGraphEl')
        dag_html = await dag_el.inner_html() if dag_el else ""
        print(f"\nStep 2 Mermaid SVG present? {'<svg' in dag_html}")

        # Capture Step 2 screenshot
        await page.screenshot(path='scratch/verified_link_intake_step2.png', full_page=False)
        print("Captured scratch/verified_link_intake_step2.png")

        await browser.close()

asyncio.run(main())
