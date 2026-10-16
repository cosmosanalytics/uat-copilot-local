# -*- coding: utf-8 -*-
"""
test_chaos_agent_mesh.py
Headless browser verification for The Self-Healing AI Agent Mesh simulator.
"""

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

file_path = os.path.abspath("chaos_agent_mesh_simulator.html")
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
    assert "Self-Healing AI Agent Mesh" in title, f"Unexpected title: {title}"

    # 2. Test Chaos Attack Toggles
    print("\n--- Testing Chaos Attack Vector Arming ---")
    driver.execute_script("toggleAttack('poison');")
    time.sleep(0.2)
    driver.execute_script("toggleAttack('latency');")
    time.sleep(0.2)
    btn_poison = driver.find_element(By.ID, "attack-poison")
    assert "active" in btn_poison.get_attribute("class"), "Attack card failed to activate!"

    # 3. Test Chaos Monkey Assault & Self-Healing
    print("\n--- Testing Chaos Monkey Assault Execution ---")
    driver.execute_script("runChaosMonkeyAssault();")
    time.sleep(1.0)
    status_text = driver.find_element(By.ID, "meshHealthText").text
    print(f"Mesh Status during/after attack: '{status_text}'")
    assert "ASSAULT" in status_text or "HEALED" in status_text, f"Unexpected status: {status_text}"

    # Wait for auto-healing
    time.sleep(2.0)
    healed_text = driver.find_element(By.ID, "meshHealthText").text
    print(f"Mesh Status after auto-healing: '{healed_text}'")
    assert "HEALED" in healed_text or "Healthy" in healed_text

    # 4. Switch to Scorecard Tab
    print("\n--- Testing Fault Tolerance Scorecard Tab ---")
    driver.execute_script("switchTab('scorecard');")
    time.sleep(0.3)
    resilience_val = driver.find_element(By.ID, "valResilience").text
    mttd_val = driver.find_element(By.ID, "valMttd").text
    print(f"Resilience Score: {resilience_val} | MTTD: {mttd_val}")
    assert "98" in resilience_val, f"Unexpected resilience value: {resilience_val}"

    # 5. Switch to Patches Tab
    print("\n--- Testing Inoculation Patches Tab ---")
    driver.execute_script("switchTab('patches');")
    time.sleep(0.3)
    patch_text = driver.find_element(By.ID, "patchViewer").text
    print(f"Patch Viewer Length: {len(patch_text)} characters")
    assert "SelfHealingGuardrailMiddleware" in patch_text, "Patch viewer missing guardrail middleware!"

    # 6. Switch to Code Tab
    print("\n--- Testing Python Chaos Wasm Code Viewer ---")
    driver.execute_script("switchTab('code');")
    time.sleep(0.3)
    code_text = driver.find_element(By.ID, "codeViewer").text
    print(f"Python Code Viewer Length: {len(code_text)} characters")
    assert "class ChaosCircuitBreaker:" in code_text and "class QuorumReferee:" in code_text, "Code viewer missing chaos test suite!"

    # 7. Switch back to Canvas and take screenshot
    driver.execute_script("switchTab('canvas');")
    time.sleep(0.5)
    screenshot_path = "chaos_agent_mesh_screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"\n[OK] Screenshot saved to {screenshot_path}")

    print("\n🎉 ALL CHAOS AGENT MESH BROWSER CHECKS PASSED PERFECTLY!")

finally:
    driver.quit()
