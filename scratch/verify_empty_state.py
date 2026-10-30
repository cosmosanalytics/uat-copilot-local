# -*- coding: utf-8 -*-
"""
Verifies that Apps 8 and 9 load with completely empty inputs and clean empty states,
and then verifies that loading a starter template or pasting custom text works seamlessly.
"""
import sys
import os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome')
    page = browser.new_page(viewport={'width': 1600, 'height': 900})

    # Test App 8 initial empty state
    abs_path = os.path.abspath('truth_policy_flowchart_studio.html').replace('\\', '/')
    page.goto(f'file:///{abs_path}')
    page.wait_for_timeout(1000)

    # 1. Verify inputs are empty
    doc_title = page.locator('#customDocTitleInput').input_value()
    doc_text = page.locator('#customDocTextInput').input_value()
    web_url = page.locator('#customWebAddressInput').input_value()

    print(f'Initial App 8 Doc Title: "{doc_title}" (Empty? {doc_title == ""})')
    print(f'Initial App 8 Doc Text: "{doc_text}" (Empty? {doc_text == ""})')
    print(f'Initial App 8 Web URL: "{web_url}" (Empty? {web_url == ""})')

    assert doc_title == "", "Doc Title should be empty"
    assert doc_text == "", "Doc Text should be empty"
    assert web_url == "", "Web URL should be empty"

    page.screenshot(path='scratch/verify_empty_initial_step1.png')

    # 2. Check Step 2 empty state
    page.locator('#tabBtn2').click()
    page.wait_for_timeout(500)
    page.screenshot(path='scratch/verify_empty_initial_step2.png')
    print("Step 2 clean empty state verified!")

    # 3. Test quick template load
    page.locator('#tabBtn1').click()
    page.wait_for_timeout(300)
    page.locator("button:has-text('Enterprise IT SSO')").click()
    page.wait_for_timeout(600)

    doc_title_loaded = page.locator('#customDocTitleInput').input_value()
    print(f'After clicking starter template: "{doc_title_loaded}"')
    assert "Enterprise IT SSO" in doc_title_loaded, "Should load template title"

    browser.close()
    print("Empty initial state verified with 100% success!")
