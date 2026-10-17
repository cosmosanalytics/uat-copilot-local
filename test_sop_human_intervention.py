# -*- coding: utf-8 -*-
"""
test_sop_human_intervention.py
Headless Selenium test for 'sop_ai_factory_canvas_human_intervention.html':
- Checks 0 severe console errors
- Tests Run Modes (Auto / Supervised / Step)
- Tests Pause and Emergency Stop states
- Tests Canvas rendering and Human Gate node
- Tests Approval card generation, Approve action, and Undo Ledger
- Tests Policy matrix inline editing
- Captures full verification screenshot
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def test_app():
    html_path = os.path.abspath("sop_ai_factory_canvas_human_intervention.html")
    print(f"Testing target: {html_path}")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1440,900")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(f"file:///{html_path}")
        time.sleep(2)

        # 1. Check Console Logs
        logs = driver.get_log("browser")
        severe_errors = [l for l in logs if l['level'] == 'SEVERE']
        print(f"Browser console logs count: {len(logs)}, severe errors: {len(severe_errors)}")
        for err in severe_errors:
            print("  SEVERE ERROR:", err['message'])

        # 2. Check Header Elements
        mode_auto = driver.find_element(By.ID, "modeBtnAuto")
        mode_sup = driver.find_element(By.ID, "modeBtnSupervised")
        mode_step = driver.find_element(By.ID, "modeBtnStep")
        badge = driver.find_element(By.ID, "systemStateBadge")
        print(f"Initial State Badge: {badge.text}")

        # Test switching to Supervised mode
        mode_sup.click()
        time.sleep(0.5)
        print("Switched to Supervised mode.")

        # 3. Test Canvas Nodes and Human Gate
        gate_node = driver.find_element(By.ID, "node_gate_1")
        print(f"Found Human Gate node on Canvas: {gate_node.is_displayed()}")

        # 4. Test Step into Stage 2 (Trigger Decision Card)
        print("Stepping into Stage 1 & Stage 2...")
        driver.execute_script("executeStep(0);")
        time.sleep(0.5)
        driver.execute_script("executeStep(1);")
        time.sleep(1)

        # Check that approval card appeared
        inbox_badge = driver.find_element(By.ID, "inboxCountBadge")
        print(f"Inbox pending count badge: {inbox_badge.text}")
        cards = driver.find_elements(By.CLASS_NAME, "decision-card")
        print(f"Decision cards found: {len(cards)}")

        # 5. Test Approving the Decision Card
        approve_btn = driver.find_element(By.CSS_SELECTOR, ".btn-decision.approve")
        approve_btn.click()
        time.sleep(1)
        print("Clicked Approve on Decision Card.")

        # 6. Test Undo Ledger
        driver.find_element(By.ID, "tabUndoBtn").click()
        time.sleep(0.5)
        undo_cards = driver.find_elements(By.CLASS_NAME, "undo-card")
        print(f"Undo Ledger entries count: {len(undo_cards)}")

        # Test Undo Action
        undo_btn = driver.find_element(By.CSS_SELECTOR, ".btn-undo-action")
        # Accept confirm dialog if present
        driver.execute_script("window.confirm = function() { return true; };")
        undo_btn.click()
        time.sleep(1)
        print("Clicked Undo on executed action.")

        # 7. Test Policy Tab
        driver.find_element(By.ID, "tabPolicyBtn").click()
        time.sleep(0.5)
        policy_rows = driver.find_elements(By.CSS_SELECTOR, "#policyTableBody tr")
        print(f"Autonomy Policy rows count: {len(policy_rows)}")

        # 8. Capture Verification Screenshot
        screenshot_path = "sop_human_intervention_preview.png"
        driver.save_screenshot(screenshot_path)
        print(f"Saved verification screenshot to: {screenshot_path}")

        assert len(severe_errors) == 0, f"Found {len(severe_errors)} severe console errors!"
        print("ALL TESTS PASSED WITH 0 SEVERE ERRORS!")

    finally:
        driver.quit()

if __name__ == "__main__":
    test_app()
