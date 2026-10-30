import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

NOVEL_TEXT = """Far away from here, following the Jade River, there was once a black mountain that cut into the sky like a jagged piece of rough metal. The villagers called it Fruitless Mountain because nothing grew on it and birds and animals did not rest there.

Crowded in the corner of where Fruitless Mountain and the Jade River met was a village that was a shade of faded brown. This was because the land around the village was hard and poor. To coax rice out of the stubborn land, the fields had to be flooded with water. The villagers had to tramp in the mud, bending and stooping and planting day after day. Working in the mud so much made it spread everywhere and the hot sun dried it onto their clothes and hair and homes. Over time, everything in the village had become the dull color of dried mud.

One of the houses in this village was so small that its wood boards, held together by the roof, made one think of a bunch of matches tied with a piece of twine. Inside, there was barely enough room for three people to sit around the table - which was lucky because only three people lived there. One of them was a young girl called Minli.

Minli was not brown and dull like the rest of the village. She had glossy black hair with pink cheeks, shining eyes always eager for adventure, and a fast smile that flashed from her face. When people saw her lively and impulsive spirit, they thought her name, which meant quick thinking, suited her well. "Too well," her mother sighed, as Minli had a habit of quick acting as well."""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='chrome')
        page = await browser.new_page(viewport={'width': 1600, 'height': 900})
        await page.goto('file:///C:/Users/richa/ai-engineering/truth_langgraph_langsmith_studio.html')
        await page.wait_for_timeout(1000)

        # Fill novel title and text
        await page.fill('#customDocTitleInput', 'excerpt from the novel the mountain meets the moon')
        await page.fill('#customDocTextInput', NOVEL_TEXT)
        await page.fill('#customWebAddressInput', '')

        # Click compile button
        compile_btn = await page.query_selector("button[onclick*='synthesizeFromCustomInputs']")
        await compile_btn.click()
        await page.wait_for_timeout(800)

        # Switch to Step 2
        await page.click('#tabBtn2')
        await page.wait_for_timeout(800)

        # Inspect Mermaid flowchart and Cascade Tiers
        dag_el = await page.query_selector('#mermaidGraphEl')
        dag_text = await dag_el.inner_text() if dag_el else ""
        print("--- RENDERED MERMAID DAG ---")
        print(dag_text)

        tier_el = await page.query_selector('.cascade-tree-card, #cascadeTreeContainer')
        tier_text = await tier_el.inner_text() if tier_el else ""
        print("\n--- RENDERED CASCADE TIERS ---")
        print(tier_text[:600])

        # Capture screenshot
        await page.screenshot(path='scratch/verified_novel_synthesis_step2.png', full_page=False)
        print("\nCaptured scratch/verified_novel_synthesis_step2.png")

        await browser.close()

asyncio.run(main())
