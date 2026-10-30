# -*- coding: utf-8 -*-
"""
Test entering ANY random excerpt URL (e.g., The Great Gatsby Wikipedia or Project Gutenberg)
into the web address input bar of App 8 and App 9 to verify live web extraction & dynamic DAG!
"""
import sys
import os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome')
    page = browser.new_page(viewport={'width': 1600, 'height': 900})
    abs_path = os.path.abspath('truth_policy_flowchart_studio.html').replace('\\', '/')
    page.goto(f'file:///{abs_path}')
    page.wait_for_timeout(1000)

    # Test 1: Enter The Great Gatsby Wikipedia URL into Input 2 and click Connect!
    print("Testing dynamic live crawl of Gatsby URL...")
    test_url = "https://en.wikipedia.org/wiki/The_Great_Gatsby"
    page.locator("#customWebAddressInput").fill(test_url)
    page.locator("#connectWebBtn").click()

    # Wait for crawl and synthesis (giving up to 6 seconds for live web proxy)
    page.wait_for_timeout(5000)

    # Check extracted title and text
    title_val = page.locator("#customDocTitleInput").input_value()
    text_val = page.locator("#customDocTextInput").input_value()
    print("Extracted Title:", title_val)
    print("Extracted Text sample:", text_val[:200].replace('\n', ' '))

    # Screenshot Step 1
    page.screenshot(path="scratch/test_gatsby_live_step1.png")

    # Navigate to Step 2
    page.locator("#tabBtn2").click()
    page.wait_for_timeout(1000)

    # Check Flowchart SVG content
    flowchart_text = page.locator("#mermaidContainer").inner_text()
    print("\nGenerated Flowchart Content:")
    print(flowchart_text[:400])

    page.screenshot(path="scratch/test_gatsby_live_step2.png")
    print("Captured test_gatsby_live_step1.png and test_gatsby_live_step2.png!")

    browser.close()
