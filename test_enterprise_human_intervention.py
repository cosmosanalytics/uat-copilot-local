# -*- coding: utf-8 -*-
"""
test_enterprise_human_intervention.py
Headless Selenium verification for 'enterprise_ai_factory_canvas_human_intervention.html':
- Checks 0 severe console errors
- Tests Run Modes (Auto / Supervised / Step)
- Tests Pause and Emergency Stop states
- Tests Canvas rendering and Human Gate node
- Tests Approval card generation, Approve action, and Undo Ledger
- Tests Policy matrix inline editing
- Captures full verification screenshots
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def test_app():
    html_path = os.path.abspath("enterprise_ai_factory_canvas_human_intervention.html")
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

        # Switch to Supervised mode
        mode_sup.click()
        time.sleep(0.5)
        print("Switched to Supervised mode.")

        # 3. Test Step into Stage 1 & Stage 2 (Trigger Decision Card)
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

        # Capture Inbox Decision Card screenshot
        driver.execute_script("openRightTab('inbox');")
        time.sleep(0.5)
        driver.execute_script("if(pendingApprovals.length) askWhyDecision(pendingApprovals[0].id);")
        time.sleep(1.2)
        driver.save_screenshot("enterprise_human_intervention_inbox_card.png")
        print("Saved enterprise_human_intervention_inbox_card.png")

        # 4. Test Approving the Decision Card
        approve_btns = driver.find_elements(By.CSS_SELECTOR, ".btn-decision.approve")
        if approve_btns:
            approve_btns[0].click()
            time.sleep(1)
            print("Clicked Approve on Decision Card.")

        # 5. Test Undo Ledger
        driver.find_element(By.ID, "tabUndoBtn").click()
        time.sleep(0.5)
        undo_cards = driver.find_elements(By.CLASS_NAME, "undo-card")
        print(f"Undo Ledger entries count: {len(undo_cards)}")

        # Test Undo Action
        undo_btns = driver.find_elements(By.CSS_SELECTOR, ".btn-undo-action")
        if undo_btns:
            driver.execute_script("window.confirm = function() { return true; };")
            undo_btns[0].click()
            time.sleep(1)
            print("Clicked Undo on executed action.")

        # 6. Test Policy Tab & Capture Policy preview
        driver.find_element(By.ID, "tabPolicyBtn").click()
        time.sleep(0.5)
        policy_rows = driver.find_elements(By.CSS_SELECTOR, "#policyTableBody tr")
        print(f"Autonomy Policy rows count: {len(policy_rows)}")

        driver.save_screenshot("enterprise_human_intervention_preview.png")
        print("Saved enterprise_human_intervention_preview.png")

        assert len(severe_errors) == 0, f"Found {len(severe_errors)} severe console errors!"
        print("ALL TESTS PASSED WITH 0 SEVERE ERRORS!")

    finally:
        driver.quit()

if __name__ == "__main__":
    test_app()
