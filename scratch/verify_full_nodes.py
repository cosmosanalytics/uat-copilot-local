# -*- coding: utf-8 -*-
"""
Test with Little House on the Prairie excerpt (from user's screenshot):
'The Ingalls family goes West. A long time ago, before all the cities and towns were built...'
Verify that the flowchart displays all text in full without any '...' truncation!
"""
import sys
import os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

little_house_text = """A long time ago, when all the grandfathers and grandmothers of relatively young boys and girls were either tiny babies or not even born yet, a family lived in the Big Woods of Wisconsin. In a little gray house made of logs lived Pa, Ma, Mary, Laura, and baby Carrie.
So far as the little girls could see, there was only the woods, with no houses and no roads. The nearest village was four days away through the dark forest.
In the long winter evenings Pa talked to Ma about the Western country. "Let's go see the West," he said. "The land is flat and the grass grows thick and high. Animals run freely and there are no settlers. Only Indians live there."
Pa did not like to stay where there were too many people. He liked a country where the animals lived without fear. He liked to see them looking at him in the forest and eating fruit from the trees.
Ma hated to leave the comfortable house with the glass windows and the cozy stove, but she said, "If you think best, Charles, we will go."
So Pa traded the farm in the Big Woods. He made a stout wagon cover of clean white canvas, and he fitted it snugly over the wagon bows."""

with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome')
    page = browser.new_page(viewport={'width': 1600, 'height': 900})
    abs_path = os.path.abspath('truth_langgraph_langsmith_studio.html').replace('\\', '/')
    page.goto(f'file:///{abs_path}')
    page.wait_for_timeout(1000)

    # Input the title and excerpt text
    page.locator('#customDocTitleInput').fill('Little House on the Prairie (Big Woods Excerpt)')
    page.locator('#customDocTextInput').fill(little_house_text)
    
    # Click Compile
    page.locator('button.btn-primary').first.click()
    page.wait_for_timeout(1500)

    # Step 2 is active
    page.screenshot(path='scratch/verify_full_node_contents.png')

    # Get Mermaid inner text
    dag_text = page.locator('#mermaidGraphEl').inner_text()
    print('Flowchart Text in Nodes:\n', dag_text)

    # Assert no ellipses '...' exist in the extracted node sentences
    assert '...' not in dag_text, "There should be NO '...' truncation in the flowchart nodes!"
    print("\nVerified: Zero '...' truncation found! All contents displayed in full!")

    browser.close()
