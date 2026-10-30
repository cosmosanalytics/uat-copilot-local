import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='chrome')
        page = await browser.new_page()
        await page.goto('file:///C:/Users/richa/ai-engineering/truth_langgraph_langsmith_studio.html')
        await page.fill('#customDocTitleInput', '')
        await page.fill('#customDocTextInput', '')
        await page.fill('#customWebAddressInput', 'https://en.wikipedia.org/wiki/MPC')
        btn = await page.query_selector("button[onclick*='applyCustomWebUrl']")
        await btn.click()
        await page.wait_for_timeout(500)
        
        doc_box = await page.query_selector('.doc-viewport')
        print(await doc_box.inner_text())
        await browser.close()

asyncio.run(main())
