# -*- coding: utf-8 -*-
"""
test_universal_ai_factory.py
Headless browser verification for The Universal AI Agent Factory • Clean Hexagonal Architecture.
"""

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

file_path = os.path.abspath("ai_factory_universal_core.html")
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
    assert "Universal AI Agent Factory" in title, f"Unexpected title: {title}"

    # 2. Verify Preset Application & Dual BOM
    print("\n--- Verifying Order Intake & Hexagonal BOM ---")
    driver.execute_script("applyOrderPreset('server');")
    time.sleep(0.5)

    receipt_text = driver.find_element(By.ID, "receiptContent").text
    print("Receipt Content Preview:\n" + receipt_text[:200] + "...")
    assert "INVARIANT CORE PROTOCOLS (88%)" in receipt_text, "Receipt missing Invariant Core BOM!"

    # 3. Test 7-Platform Hot Swapping
    print("\n--- Testing 7-Platform Substrate Hot Swapping ---")
    platforms = ['azure', 'gcp', 'cloudflare', 'kubernetes', 'databricks', 'oci', 'aws']
    for p in platforms:
        driver.execute_script(f"switchPlatform('{p}');")
        time.sleep(0.1)
    label = driver.find_element(By.ID, "activeAdapterLabel").text
    print(f"Active Adapter after cycle: '{label}' (Expected 'AWS Cloud')")
    assert label.lower() == "aws cloud", f"Expected AWS Cloud, got {label}"

    # 4. Test Visual Pulse & Execution on Hexagonal Canvas
    print("\n--- Testing Hexagonal Canvas Pulse & Transaction Execution ---")
    driver.execute_script("stepVisualPulse();")
    time.sleep(0.3)
    driver.execute_script("runFullVisualSimulation();")
    time.sleep(0.3)
    log_text = driver.find_element(By.ID, "telemetryLogText").text
    print("Telemetry Log:", log_text)
    assert "Success!" in log_text, "Visual simulation failed to log success!"

    # 5. Switch to Matrix Tab and Verify Table
    print("\n--- Testing Cross-Platform Substrate Matrix ---")
    driver.execute_script("switchTab('matrix');")
    time.sleep(0.3)
    rows = driver.find_elements(By.CSS_SELECTOR, ".matrix-table tbody tr")
    print(f"Matrix Rows: {len(rows)} (Expected 7 Invariant Ports)")
    assert len(rows) == 7, f"Expected 7 matrix rows, got {len(rows)}"

    # 6. Switch to Tests Tab and Run All 8 Invariant Tests
    print("\n--- Testing Core Invariant Test Suite ---")
    driver.execute_script("switchTab('tests');")
    time.sleep(0.3)
    driver.execute_script("runAllSimulatorTests();")
    time.sleep(1.0)

    test_cards = driver.find_elements(By.CLASS_NAME, "test-card")
    print(f"Total Test Cards: {len(test_cards)} (Expected 8)")
    assert len(test_cards) == 8, f"Expected 8 test cards, got {len(test_cards)}"

    pass_badges = driver.find_elements(By.CSS_SELECTOR, ".test-badge.pass")
    print(f"Passing Core Invariant Tests: {len(pass_badges)}/8")
    assert len(pass_badges) == 8, f"Expected all 8 tests to pass, but only {len(pass_badges)} passed!"

    # 7. Switch to Code Tab
    print("\n--- Testing Clean Hexagonal Python Code Viewer ---")
    driver.execute_script("switchTab('code');")
    time.sleep(0.3)
    code_text = driver.find_element(By.ID, "codeViewer").text
    print(f"Code Viewer Length: {len(code_text)} characters")
    assert "class UniversalAgentCore:" in code_text and "class IKeyValueStore(ABC):" in code_text, "Code viewer missing Hexagonal architecture!"

    # 8. Switch back to Canvas and take screenshot
    driver.execute_script("switchTab('canvas');")
    time.sleep(0.5)
    screenshot_path = "ai_factory_universal_screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"\n[OK] Screenshot saved to {screenshot_path}")

    print("\n🎉 ALL UNIVERSAL AI FACTORY BROWSER CHECKS PASSED PERFECTLY!")

finally:
    driver.quit()
