# -*- coding: utf-8 -*-
"""
test_end_to_end_simulator.py
Headless browser verification for End-to-End GitHub + AWS Simulator.
Verifies all 10 boxes, the end-to-end lap execution, and 0 severe console errors.
"""

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

file_path = os.path.abspath("end_to_end_github_aws_simulator.html")
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
    assert "End-to-End GitHub + AWS" in title

    # 3. Test Running One Complete Lap
    print("\n--- Testing Complete Lap Execution ---")
    driver.execute_script("runOneCompleteLap();")
    time.sleep(2)
    lap_text = driver.find_element(By.ID, "lapCounterText").text
    print(f"Lap Counter: '{lap_text}'")
    assert "Lap #2" in lap_text

    # 4. Test All 10 Boxes from Page 3
    print("\n--- Testing All 10 Progressive Boxes ---")
    for box_num in range(1, 11):
        driver.execute_script(f"selectBox({box_num});")
        time.sleep(0.3)
        box_title = driver.find_element(By.ID, "activeBoxTitle").text
        level_pill = driver.find_element(By.ID, "activeBoxLevelPill").text
        print(f"Box {box_num} loaded: '{box_title}' [{level_pill}]")
        assert f"Box {box_num}:" in box_title

    # 5. Take Screenshot
    screenshot_path = os.path.abspath("end_to_end_simulator_screenshot.png")
    driver.save_screenshot(screenshot_path)
    print(f"\n[SUCCESS] Screenshot saved to: {screenshot_path}")

    # 6. Final console check
    final_logs = driver.get_log("browser")
    final_severe = [l for l in final_logs if l['level'] == 'SEVERE']
    assert len(final_severe) == 0, f"Found severe console errors: {final_severe}"

    print("\n[VERIFIED] All 10 boxes and end-to-end loop passed 100% successfully!")

finally:
    driver.quit()
