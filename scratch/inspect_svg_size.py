import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='chrome')
        page = await browser.new_page(viewport={'width': 1600, 'height': 900})
        await page.goto('file:///C:/Users/richa/ai-engineering/truth_langgraph_langsmith_studio.html')
        await page.click('#tabBtn2')
        await page.wait_for_timeout(800)

        svg = await page.query_selector('#mermaidGraphEl svg')
        if svg:
            box = await svg.bounding_box()
            container = await page.query_selector('.mermaid-svg-container')
            c_box = await container.bounding_box()
            print('Container box:', c_box)
            print('SVG box:', box)
            print(f'Width ratio: {box["width"] / c_box["width"]:.1%}')
            print(f'Height ratio: {box["height"] / c_box["height"]:.1%}')

        await browser.close()

asyncio.run(inspect())
