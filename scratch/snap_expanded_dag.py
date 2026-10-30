import asyncio
from playwright.async_api import async_playwright

async def snap():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='chrome')
        page = await browser.new_page(viewport={'width': 1600, 'height': 900})
        await page.goto('file:///C:/Users/richa/ai-engineering/truth_langgraph_langsmith_studio.html')
        
        # Enter Today.com URL and click connect
        await page.fill('#customWebAddressInput', 'https://www.today.com/popculture/where-mountain-meets-moon-wbna33436633')
        btn = await page.query_selector("button[onclick*='applyCustomWebUrl']")
        await btn.click()
        await page.wait_for_timeout(600)

        # Switch to Step 2
        await page.click('#tabBtn2')
        await page.wait_for_timeout(800)

        svg = await page.query_selector('#mermaidGraphEl svg')
        if svg:
            box = await svg.bounding_box()
            container = await page.query_selector('.mermaid-svg-container')
            c_box = await container.bounding_box()
            print('Mountain Meets Moon Container:', c_box)
            print('Mountain Meets Moon SVG:', box)
            print(f'Width: {box["width"] / c_box["width"]:.1%}, Height: {box["height"] / c_box["height"]:.1%}')

        await page.screenshot(path='scratch/verified_flowchart_expanded_big.png', full_page=False)
        print("Captured scratch/verified_flowchart_expanded_big.png")

        await browser.close()

asyncio.run(snap())
