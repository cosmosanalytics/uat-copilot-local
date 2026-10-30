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

        # Clear Input 1
        await page.fill('#customDocTitleInput', '')
        await page.fill('#customDocTextInput', '')

        # Paste TODAY.com URL into Input 2
        url = 'https://www.today.com/popculture/where-mountain-meets-moon-wbna33436633'
        await page.fill('#customWebAddressInput', url)
        await page.wait_for_timeout(300)

        # Click Connect
        btn = await page.query_selector("button[onclick*='applyCustomWebUrl']")
        await btn.click()
        await page.wait_for_timeout(800)

        # Inspect Document View
        doc_box = await page.query_selector('.doc-viewport')
        doc_text = await doc_box.inner_text() if doc_box else ""
        print("=== STEP 1 DOCUMENT VIEW CONTENT ===")
        print(doc_text[:350])

        # Screenshot Step 1
        await page.screenshot(path='scratch/verified_today_com_step1.png', full_page=False)

        # Switch to Step 2
        await page.click('#tabBtn2')
        await page.wait_for_timeout(800)

        dag_el = await page.query_selector('#mermaidGraphEl')
        dag_text = await dag_el.inner_text() if dag_el else ""
        print("\n=== STEP 2 MERMAID DAG ===")
        print(dag_text)

        # Screenshot Step 2
        await page.screenshot(path='scratch/verified_today_com_step2.png', full_page=False)

        await browser.close()
        print("\nTest completed successfully!")

asyncio.run(main())
