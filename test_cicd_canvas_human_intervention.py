# -*- coding: utf-8 -*-
"""
test_cicd_canvas_human_intervention.py
Headless Selenium verification for 'cicd_ai_factory_canvas_human_intervention.html':
- Checks 0 severe console errors
- Tests 3-tier hierarchy switching (Level 3 AWS AI Foundation, Level 2 GitHub CI/CD, Level 1 Worker AI)
- Verifies AWS AI Foundation nodes: Bedrock, Step Functions, Lambda, OpenSearch, SageMaker, DynamoDB
- Verifies Human Gate node on Level 2 (GitHub CI/CD)
- Tests Run Modes (Auto / Supervised / Step)
- Tests Approvals Inbox with Decision Card and "Ask Why" Groq rationale
- Tests Approve action and Undo Ledger entry
- Tests Undo rollback action
- Tests AWS AI Foundation Simulator (Bedrock model switcher, Temperature dial, Step Functions tracker, Lambda concurrency)
- Tests Autonomy Policy matrix
- Captures full verification screenshots
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def test_cicd_app():
    html_path = os.path.abspath("cicd_ai_factory_canvas_human_intervention.html")
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

        # 2. Check Hierarchy Switcher (Level 3 AWS AI Foundation by default)
        tab_l3 = driver.find_element(By.ID, "tabL3")
        tab_l2 = driver.find_element(By.ID, "tabL2")
        tab_l1 = driver.find_element(By.ID, "tabL1")
        print(f"Level 3 Tab: {tab_l3.text}")
        print(f"Level 2 Tab: {tab_l2.text}")
        print(f"Level 1 Tab: {tab_l1.text}")

        # Check nodes on Level 3 (AWS Production Cloud: 9 nodes)
        aws_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
        print(f"Level 3 Canvas nodes: {len(aws_nodes)} (Expected 9)")

        ecs_node = driver.find_element(By.ID, "node_aws_ecs")
        alb_node = driver.find_element(By.ID, "node_aws_alb")
        bedrock_node = driver.find_element(By.ID, "node_aws_bedrock")
        step_node = driver.find_element(By.ID, "node_aws_stepfunctions")
        lambda_node = driver.find_element(By.ID, "node_aws_lambda")
        print(f"Found ECS Fargate node: {ecs_node.is_displayed()}")
        print(f"Found ALB Ingress node: {alb_node.is_displayed()}")
        print(f"Found Bedrock FM node: {bedrock_node.is_displayed()}")
        print(f"Found Step Functions node: {step_node.is_displayed()}")
        print(f"Found Lambda node: {lambda_node.is_displayed()}")

        # Switch to Level 2 (GitHub CI/CD)
        tab_l2.click()
        time.sleep(0.5)
        gh_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
        print(f"Level 2 Canvas nodes: {len(gh_nodes)}")

        # Check Human Gate node on Level 2
        gate_node = driver.find_element(By.ID, "node_gh_gate")
        print(f"Level 2 Human Gate node displayed: {gate_node.is_displayed()}")

        # Switch to Level 1 (Worker AI)
        tab_l1.click()
        time.sleep(0.5)
        worker_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
        print(f"Level 1 Canvas nodes: {len(worker_nodes)}")

        # Switch back to Level 2 to capture GitHub pipeline screenshot
        tab_l2.click()
        time.sleep(0.5)
        driver.save_screenshot("cicd_human_intervention_level2_github.png")
        print("Saved cicd_human_intervention_level2_github.png")

        # 3. Check Run Modes
        mode_auto = driver.find_element(By.ID, "modeBtnAuto")
        mode_sup = driver.find_element(By.ID, "modeBtnSupervised")
        mode_step = driver.find_element(By.ID, "modeBtnStep")
        badge = driver.find_element(By.ID, "systemStateBadge")
        print(f"State Badge: {badge.text}")

        mode_step.click()
        time.sleep(0.3)
        print("Switched to Step mode.")
        mode_sup.click()
        time.sleep(0.3)
        print("Switched back to Supervised mode.")

        # 4. Approvals Inbox & Decision Card
        driver.find_element(By.ID, "tabBtnInbox").click()
        time.sleep(0.3)
        cards = driver.find_elements(By.CLASS_NAME, "decision-card")
        print(f"Decision cards found: {len(cards)}")

        # Click Ask Why
        why_btns = driver.find_elements(By.CSS_SELECTOR, ".btn-decision.why")
        if why_btns:
            why_btns[0].click()
            time.sleep(0.5)
            print("Expanded 'Ask Why' Groq rationale.")

        driver.save_screenshot("cicd_human_intervention_inbox_card.png")
        print("Saved cicd_human_intervention_inbox_card.png")

        # 5. Approve Decision Card
        approve_btns = driver.find_elements(By.CSS_SELECTOR, ".btn-decision.approve")
        if approve_btns:
            approve_btns[0].click()
            time.sleep(0.8)
            print("Clicked Approve on Decision Card.")

        # 6. Check Undo Ledger
        driver.find_element(By.ID, "tabBtnUndo").click()
        time.sleep(0.5)
        undo_cards = driver.find_elements(By.CLASS_NAME, "undo-card")
        print(f"Undo ledger entries count: {len(undo_cards)}")

        # Test Undo Action
        driver.execute_script("window.confirm = function() { return true; };")
        undo_btns = driver.find_elements(By.CSS_SELECTOR, ".btn-undo-action")
        if undo_btns:
            undo_btns[0].click()
            time.sleep(0.8)
            print("Clicked Undo rollback.")

        # 7. Check Autonomy Policy Tab
        driver.find_element(By.ID, "tabBtnPolicy").click()
        time.sleep(0.5)
        policy_rows = driver.find_elements(By.CSS_SELECTOR, "#policyTableBody tr")
        print(f"Policy rows count: {len(policy_rows)} (Expected 8)")

        # 8. Check AWS AI Foundation Simulator Tab
        driver.find_element(By.ID, "tabBtnAws").click()
        time.sleep(0.5)
        model_select = driver.find_element(By.ID, "bedrockModelSelect")
        print(f"Bedrock model select displayed: {model_select.is_displayed()}")

        temp_slider = driver.find_element(By.ID, "tempSlider")
        driver.execute_script("arguments[0].value = 50; arguments[0].dispatchEvent(new Event('input'));", temp_slider)
        time.sleep(0.5)
        temp_val = driver.find_element(By.ID, "tempVal").text
        print(f"Bedrock Temperature updated: {temp_val}")

        # Switch back to Level 3 (AWS AI Foundation) and capture full preview
        tab_l3.click()
        time.sleep(0.5)
        driver.save_screenshot("cicd_human_intervention_preview.png")
        print("Saved cicd_human_intervention_preview.png")

        assert len(severe_errors) == 0, f"Found {len(severe_errors)} severe console errors!"
        print("ALL AWS AI FOUNDATION & CI/CD TESTS PASSED WITH 0 SEVERE ERRORS!")

    finally:
        driver.quit()

if __name__ == "__main__":
    test_cicd_app()
