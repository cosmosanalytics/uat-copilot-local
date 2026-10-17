# -*- coding: utf-8 -*-
"""
test_ambient_ai_simulator.py
Automated headless Selenium browser test for Ambient AI Simulator.
"""

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

file_path = os.path.abspath("ambient_ai_cognitive_bandwidth_simulator.html")
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

    # 1. Console errors check
    logs = driver.get_log("browser")
    severe = [l for l in logs if l['level'] == 'SEVERE']
    print(f"Console logs: {len(logs)}, severe errors: {len(severe)}")
    if severe:
        print("Severe errors:", severe)
    assert len(severe) == 0, f"Found severe console errors: {severe}"

    # 2. Check Title
    title = driver.title
    print(f"Page Title: '{title}'")
    assert "Ambient AI Simulator" in title

    # 3. Check Initial Cognitive Load (Flow State)
    load_text = driver.find_element(By.ID, "humanLoadPercent").text
    print(f"Initial Human Cognitive Load: '{load_text}'")
    assert "18%" in load_text

    # 4. Switch to Chat Mode (Friction & Overload)
    print("\n--- Testing Chat Mode (High Cognitive Load) ---")
    driver.execute_script("setMode('chat');")
    time.sleep(0.5)
    chat_load = driver.find_element(By.ID, "humanLoadPercent").text
    print(f"Chat Mode Cognitive Load: '{chat_load}'")
    assert "92%" in chat_load
    assert "BURNOUT" in chat_load

    slot4 = driver.find_element(By.ID, "slot4").text
    print(f"Slot 4 state: '{slot4}'")
    assert "OVERFLOW" in slot4

    # 5. Switch back to Ambient Mode (Zero Drag)
    print("\n--- Testing Ambient Mode (Restoring Flow State) ---")
    driver.execute_script("setMode('ambient');")
    time.sleep(0.5)
    ambient_load = driver.find_element(By.ID, "humanLoadPercent").text
    print(f"Ambient Mode Cognitive Load: '{ambient_load}'")
    assert "18%" in ambient_load

    # 6. Test Scenario Dials
    print("\n--- Testing Steering Scenarios ---")
    driver.execute_script("triggerScenario('cost');")
    time.sleep(0.3)
    goal_text = driver.find_element(By.ID, "hudGoalText").text
    print(f"Cost Goal: '{goal_text}'")
    assert "Downscale Idle Workers" in goal_text

    driver.execute_script("triggerScenario('speed');")
    time.sleep(0.3)
    speed_goal = driver.find_element(By.ID, "hudGoalText").text
    print(f"Speed Goal: '{speed_goal}'")
    assert "Redis Layer" in speed_goal

    # 7. Take Screenshot
    screenshot_path = os.path.abspath("ambient_ai_simulator_screenshot.png")
    driver.save_screenshot(screenshot_path)
    print(f"\n[SUCCESS] Screenshot saved to {screenshot_path}")

    # 8. Final Console Check
    final_logs = driver.get_log("browser")
    final_severe = [l for l in final_logs if l['level'] == 'SEVERE']
    assert len(final_severe) == 0, f"Severe errors found after testing: {final_severe}"

    print("\n[VERIFIED] Ambient AI simulator passed all checks with 100% success!")

finally:
    driver.quit()
