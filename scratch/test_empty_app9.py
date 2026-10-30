# -*- coding: utf-8 -*-
import sys
import os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome')
    page = browser.new_page(viewport={'width': 850, 'height': 500})
    abs_path = os.path.abspath('truth_langgraph_langsmith_studio.html').replace('\\', '/')
    page.goto(f'file:///{abs_path}')
    page.wait_for_timeout(1000)

    title_val = page.locator('#customDocTitleInput').input_value()
    text_val = page.locator('#customDocTextInput').input_value()
    url_val = page.locator('#customWebAddressInput').input_value()

    print(f'App 9 Title: "{title_val}"')
    print(f'App 9 Text: "{text_val}"')
    print(f'App 9 URL: "{url_val}"')

    page.screenshot(path='scratch/app9_mobile_empty_verified.png')

    assert title_val == '', 'Title must be empty'
    assert text_val == '', 'Text must be empty'
    assert url_val == '', 'URL must be empty'

    browser.close()
    print('Playwright test passed: completely blank inputs on initial load!')
