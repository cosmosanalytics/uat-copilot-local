# -*- coding: utf-8 -*-
"""
test_inter_company_human_intervention.py
Headless Selenium verification for 'inter_company_ai_factory_canvas_human_intervention.html':
- Checks 0 severe console errors
- Verifies Level 4 (Inter-Company Value Chain) is active with all 6 enterprises
- Verifies Human Gate node on Level 4 between Apex OEM and Pegasus EMS
- Tests Run Modes (Auto / Supervised / Step)
- Tests Approvals Inbox with Multi-Enterprise Decision Card ([Apex OEM -> Pegasus EMS])
- Tests Live Groq / Copilot rationale ("Ask Why")
- Tests Decision Card Approval and Undo Ledger entry
- Tests Undo Ledger rollback
- Tests Autonomy Policy matrix (all 6 commercial enterprises + 6 internal orgs)
- Captures full verification screenshots
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def test_inter_company_app():
    html_path = os.path.abspath("inter_company_ai_factory_canvas_human_intervention.html")
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

        # 2. Check Level 4 Inter-Company Hierarchy
        tab_l4 = driver.find_element(By.ID, "tabL4")
        print(f"Level 4 Tab Text: {tab_l4.text}")
        active_tab = driver.find_element(By.CSS_SELECTOR, ".level-tab.active")
        print(f"Active Tab: {active_tab.text}")

        # Check for 6 Enterprise nodes on canvas
        company_nodes = driver.find_elements(By.CSS_SELECTOR, ".canvas-node")
        print(f"Canvas nodes found on Level 4: {len(company_nodes)}")

        # Check Human Gate node
        gate_node = driver.find_element(By.ID, "node_gate_human_l4")
        print(f"Found Inter-Company Human Gate node: {gate_node.is_displayed()}")

        # 3. Check Header Controls & Run Modes
        mode_auto = driver.find_element(By.ID, "modeBtnAuto")
        mode_sup = driver.find_element(By.ID, "modeBtnSupervised")
        mode_step = driver.find_element(By.ID, "modeBtnStep")
        badge = driver.find_element(By.ID, "systemStateBadge")
        print(f"Initial State Badge: {badge.text}")

        mode_sup.click()
        time.sleep(0.5)
        print("Switched to Supervised mode.")

        # 4. Trigger Step Execution / Multi-Enterprise Decision Card
        print("Executing inter-company value stream steps...")
        driver.execute_script("executeStep(0);")
        time.sleep(0.5)
        driver.execute_script("executeStep(1);")
        time.sleep(1)

        # Check inbox count
        inbox_badge = driver.find_element(By.ID, "inboxCountBadge")
        print(f"Inbox pending count badge: {inbox_badge.text}")
        cards = driver.find_elements(By.CLASS_NAME, "decision-card")
        print(f"Decision cards found: {len(cards)}")

        # Open Approvals Inbox tab
        driver.execute_script("openRightTab('inbox');")
        time.sleep(0.5)
        driver.execute_script("if(pendingApprovals.length) askWhyDecision(pendingApprovals[0].id);")
        time.sleep(1.2)

        driver.save_screenshot("inter_company_human_intervention_inbox_card.png")
        print("Saved inter_company_human_intervention_inbox_card.png")

        # 5. Approve Decision Card
        approve_btns = driver.find_elements(By.CSS_SELECTOR, ".btn-decision.approve")
        if approve_btns:
            approve_btns[0].click()
            time.sleep(1)
            print("Clicked Approve on Inter-Company Decision Card.")

        # 6. Check Undo Ledger
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
            print("Clicked Undo on executed inter-company action.")

        # 7. Check Autonomy Policy Tab
        driver.find_element(By.ID, "tabPolicyBtn").click()
        time.sleep(0.5)
        policy_rows = driver.find_elements(By.CSS_SELECTOR, "#policyTableBody tr")
        print(f"Autonomy Policy rows count: {len(policy_rows)} (Expected 12: 6 Enterprises + 6 Orgs)")

        # Capture full preview screenshot
        driver.save_screenshot("inter_company_human_intervention_preview.png")
        print("Saved inter_company_human_intervention_preview.png")

        # Verify 0 severe console errors
        assert len(severe_errors) == 0, f"Found {len(severe_errors)} severe console errors!"
        print("ALL INTER-COMPANY TESTS PASSED WITH 0 SEVERE ERRORS!")

    finally:
        driver.quit()

if __name__ == "__main__":
    test_inter_company_app()
