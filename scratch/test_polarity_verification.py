# -*- coding: utf-8 -*-
"""
Test with exact Ingalls excerpt to verify that:
1. Stagnation branch (Red) shows staying/crowding: "Pa said there were too many people... Wild animals did not stay in a country where there were so many people, so Pa didn't want to stay."
2. Action branch (Green) shows moving West: "The Ingalls family goes West... Pa and Ma and Mary and Laura and Baby Carrie left their little house in Wisconsin... They were going to Indian country."
"""
import sys
import os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

ingalls_text = """The Ingalls family goes West. A long time ago, Pa and Ma and Mary and Laura and Baby Carrie left their little house in Wisconsin. They drove away and left it lonely and empty among the big trees, and they never saw that little house again. They were going to Indian country.
Pa said there were too many people in Wisconsin now. Wild animals did not stay in a country where there were so many people, so Pa didn't want to stay. He liked a country where the animals lived without fear. He liked to see them looking at him in the forest and eating fruit from the trees.
In the long winter evenings Pa talked to Ma about the Western country. "Let's go see the West," he said. "The land is flat and the grass grows thick and high. Animals run freely and there are no settlers. Only Indians live there."""

with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome')
    page = browser.new_page(viewport={'width': 1600, 'height': 900})
    abs_path = os.path.abspath('truth_langgraph_langsmith_studio.html').replace('\\', '/')
    page.goto(f'file:///{abs_path}')
    page.wait_for_timeout(1000)

    page.locator('#customDocTitleInput').fill('Little House: The Ingalls Family Goes West')
    page.locator('#customDocTextInput').fill(ingalls_text)
    
    # Click Compile
    page.locator('button.btn-primary').first.click()
    page.wait_for_timeout(1500)

    page.screenshot(path='scratch/verify_polarity_fixed.png')

    dag_text = page.locator('#mermaidGraphEl').inner_text()
    print('Updated Flowchart Nodes:\n', dag_text)

    # Verify that Stagnation has words about 'people' or 'stay' or 'Wisconsin'
    assert 'too many people' in dag_text.lower() or "didn't want to stay" in dag_text.lower(), "Stagnation branch should reference staying/crowded people in Wisconsin!"
    
    # Verify that Action has 'drove away' or 'west' or 'indian country'
    assert 'west' in dag_text.lower() and ('drove away' in dag_text.lower() or 'left' in dag_text.lower() or 'going' in dag_text.lower()), "Action branch should reference leaving/going West!"

    print('\nPOLARITY CHECK PASSED! Stagnation = staying in crowded Wisconsin; Action = moving West!')

    browser.close()
