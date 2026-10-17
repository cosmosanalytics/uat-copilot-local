# -*- coding: utf-8 -*-
"""
test_ambient_everyday_app.py
Automated headless Selenium browser test for Ambient AI Everyday Ergonomics.
"""

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

file_path = os.path.abspath("ambient_ai_everyday_cognitive_ergonomics.html")
url = f"file:///{file_path.replace(os.sep, '/')}"

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1440,950")
opts.add_argument("--disable-gpu")
opts.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=opts)
try:
    print(f"Loading {url} in headless Chrome...")
    driver.get(url)
    time.sleep(2)

    # 1. Console check
    logs = driver.get_log("browser")
    severe = [l for l in logs if l['level'] == 'SEVERE']
    print(f"Console logs: {len(logs)}, severe errors: {len(severe)}")
    if severe:
        print("Severe errors:", severe)
    assert len(severe) == 0, f"Found severe console errors: {severe}"

    # 2. Check Page Title
    title = driver.title
    print(f"Page Title: '{title}'")
    assert "Ambient AI Everyday Ergonomics" in title

    # 3. Test all 6 domains
    domain_keys = ['inbox', 'sheet', 'calendar', 'contract', 'git', 'choice']
    print("\n--- Testing All 6 Everyday Cognitive Load Domains ---")
    for k in domain_keys:
        driver.execute_script(f"selectDomain('{k}');")
        time.sleep(0.3)
        sol_title = driver.find_element(By.ID, "solutionTitleText").text
        slots_text = driver.find_element(By.ID, "labelSlotsUsed").text
        print(f"Domain '{k}': '{sol_title}' (Slots: {slots_text})")
        assert "Ambient" in sol_title

    # 4. Take Screenshot
    screenshot_path = os.path.abspath("ambient_everyday_screenshot.png")
    driver.save_screenshot(screenshot_path)
    print(f"\n[SUCCESS] Screenshot saved to: {screenshot_path}")

    # 5. Final console check
    final_logs = driver.get_log("browser")
    final_severe = [l for l in final_logs if l['level'] == 'SEVERE']
    assert len(final_severe) == 0, f"Found severe errors: {final_severe}"

    print("\n[VERIFIED] Ambient Everyday Ergonomics app passed all tests with 100% success!")

finally:
    driver.quit()
