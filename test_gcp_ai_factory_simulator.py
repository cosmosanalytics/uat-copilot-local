# -*- coding: utf-8 -*-
"""
test_gcp_ai_factory_simulator.py
Headless browser verification for The AI Agent Factory • In-Browser Google Cloud Simulator.
"""

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

file_path = os.path.abspath("ai_factory_gcp_simulator.html")
url = f"file:///{file_path.replace(os.sep, '/')}"

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1440,900")
opts.add_argument("--disable-gpu")
opts.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=opts)
try:
    print(f"Loading {url}...")
    driver.get(url)
    time.sleep(2)

    logs = driver.get_log("browser")
    severe = [l for l in logs if l['level'] == 'SEVERE']
    print(f"Browser console logs: {len(logs)} entries, {len(severe)} SEVERE")
    if severe:
        print("Severe logs:", severe)
    assert len(severe) == 0, f"Found severe console errors: {severe}"

    # 1. Verify Title & Header
    title = driver.title
    print(f"Page Title: '{title}'")
    assert "Google Cloud Simulator" in title, f"Unexpected title: {title}"

    # 2. Verify Preset Application & 7 Steps Pipeline
    print("\n--- Verifying Order Intake & 7 Steps Pipeline ---")
    driver.execute_script("applyOrderPreset('server');")
    time.sleep(1)

    nodes = driver.find_elements(By.CLASS_NAME, "flow-node")
    print(f"Flow nodes on canvas after 'server' preset: {len(nodes)} (Expected >= 5)")
    assert len(nodes) >= 5, f"Expected at least 5 nodes, got {len(nodes)}"

    receipt_text = driver.find_element(By.ID, "receiptContent").text
    print("Receipt Content Preview:\n" + receipt_text[:200] + "...")
    assert "GOOGLE CLOUD BILL OF MATERIALS" in receipt_text, "Receipt missing Google Cloud BOM!"

    # 3. Test Step Flow Animation on Canvas
    print("\n--- Testing Visual Flow Step Execution ---")
    driver.execute_script("stepVisualFlow();")
    time.sleep(0.6)
    completed_nodes = driver.find_elements(By.CSS_SELECTOR, ".flow-node.completed")
    print(f"Completed nodes after 1 step: {len(completed_nodes)}")
    assert len(completed_nodes) >= 1, "Expected at least 1 completed node after stepVisualFlow!"

    # 4. Switch to Tests Tab and Run All 8 GCP Tests
    print("\n--- Testing Google Cloud Simulator Test Suite (8 Primitives) ---")
    driver.execute_script("switchTab('tests');")
    time.sleep(0.3)
    driver.execute_script("runAllSimulatorTests();")
    time.sleep(1.5)

    test_cards = driver.find_elements(By.CLASS_NAME, "test-card")
    print(f"Total Google Cloud Simulator Test Cards: {len(test_cards)} (Expected 8)")
    assert len(test_cards) == 8, f"Expected 8 test cards, got {len(test_cards)}"

    pass_badges = driver.find_elements(By.CSS_SELECTOR, ".test-badge.pass")
    print(f"Passing Google Cloud Tests: {len(pass_badges)}/8")
    assert len(pass_badges) == 8, f"Expected all 8 tests to pass, but only {len(pass_badges)} passed!"

    # 5. Switch to Softmax Tab
    print("\n--- Testing Vertex AI Softmax Temperature ---")
    driver.execute_script("switchTab('temp');")
    time.sleep(0.3)
    driver.execute_script("onTemperatureChange(0.7);")
    time.sleep(0.3)
    bars = driver.find_elements(By.CLASS_NAME, "dist-bar-row")
    print(f"Distribution Bars Rendered: {len(bars)} (Expected 5)")
    assert len(bars) == 5, f"Expected 5 distribution bars, got {len(bars)}"

    # 6. Switch to Code Tab
    print("\n--- Testing Python Google Cloud SDK Code Viewer ---")
    driver.execute_script("switchTab('code');")
    time.sleep(0.3)
    code_text = driver.find_element(By.ID, "codeViewer").text
    print(f"Code Viewer Length: {len(code_text)} characters")
    assert "GoogleCloudFirestore" in code_text and "GoogleCloudPubSub" in code_text, "Code viewer missing GCP primitives!"

    # 7. Switch back to Canvas and take screenshot
    driver.execute_script("switchTab('canvas');")
    time.sleep(0.5)
    screenshot_path = "ai_factory_gcp_screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"\nSaved screenshot to '{screenshot_path}'")

    print("\n🎉 ALL IN-BROWSER GOOGLE CLOUD SIMULATOR CHECKS PASSED PERFECTLY!")

finally:
    driver.quit()
