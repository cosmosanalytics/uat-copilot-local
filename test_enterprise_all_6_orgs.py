# -*- coding: utf-8 -*-
"""
test_enterprise_all_6_orgs.py
Verifies the 3-Tier Enterprise AI Factory Architecture:
1. Level 3: Company Level Process (6 Organizations playing roles in Enterprise Value Stream)
2. Level 2: Organization Level Process (ALWAYS S&OP: 11 Workers / 11 Steps)
3. Level 1: Mind Level Process (Cognition: Debate Personas + Cognitive Skills + Deterministic Harness)
"""

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

file_path = os.path.abspath("enterprise_ai_factory_canvas.html")
url = f"file:///{file_path.replace(os.sep, '/')}"

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1440,900")
opts.add_argument("--disable-gpu")
opts.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=opts)
try:
    driver.get(url)
    time.sleep(2)

    logs = driver.get_log("browser")
    severe = [l for l in logs if l['level'] == 'SEVERE']
    print(f"Browser console logs: {len(logs)} entries, {len(severe)} SEVERE")
    assert len(severe) == 0, f"Found severe console logs: {severe}"

    # 1. Level 3: Company Level (6 Organizations)
    print("\n--- Verifying Level 3: Company Process ---")
    l3_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
    print(f"Level 3 Organizations: {len(l3_nodes)} (Expected 6)")
    assert len(l3_nodes) == 6, f"Expected 6 organizations at Level 3, found {len(l3_nodes)}"

    # Check that S&OP is clearly distinguished
    sop_node = driver.find_element(By.ID, "node_sop")
    assert "core-org" in sop_node.get_attribute("class"), "S&OP node must have core-org class"
    print("  -> Verified S&OP organization has core-org highlighting on Level 3 canvas.")

    # Check breadcrumb at Level 3
    crumb_l3 = driver.find_element(By.ID, "crumbL3").text
    print(f"  -> Level 3 Breadcrumb: '{crumb_l3}'")

    driver.save_screenshot("enterprise_l3_company_screenshot.png")
    print("Saved 'enterprise_l3_company_screenshot.png'")

    # 2. Level 2: Organization Level (ALWAYS S&OP - 11 Workers)
    print("\n--- Verifying Level 2: Organization Level is ALWAYS S&OP ---")
    driver.execute_script("switchLevel(2);")
    time.sleep(0.8)

    l2_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
    print(f"Level 2 Workers: {len(l2_nodes)} (Expected 11 S&OP Steps)")
    assert len(l2_nodes) == 11, f"Expected 11 S&OP workers at Level 2, found {len(l2_nodes)}"

    # Verify workers are indeed the 11 S&OP stages
    expected_stages = [f"sop_{i}" for i in range(1, 12)]
    actual_ids = [n.get_attribute("id").replace("node_", "") for n in l2_nodes]
    assert actual_ids == expected_stages, f"Level 2 workers do not match S&OP stages: {actual_ids}"
    print(f"  -> Verified all 11 S&OP stages present: {actual_ids}")

    # Check breadcrumb at Level 2
    crumb_l2 = driver.find_element(By.ID, "crumbL2").text
    print(f"  -> Level 2 Breadcrumb: '{crumb_l2}'")
    assert "S&OP" in crumb_l2, f"Expected S&OP in breadcrumb, got {crumb_l2}"

    driver.save_screenshot("enterprise_l2_sop_screenshot.png")
    print("Saved 'enterprise_l2_sop_screenshot.png'")

    # Test drill-down from Company level to Level 2
    driver.execute_script("switchLevel(3);")
    time.sleep(0.5)
    driver.execute_script("openOrganizationFromCompany('erp');") # Any org drill goes to Level 2 S&OP
    time.sleep(0.5)
    l2_nodes_after = driver.find_elements(By.CLASS_NAME, "canvas-node")
    assert len(l2_nodes_after) == 11, "Level 2 must always be S&OP (11 workers)"
    print("  -> Verified drilling from Company level always resolves to S&OP (11 workers).")

    # 3. Level 1: Mind Level Process (Cognition)
    print("\n--- Verifying Level 1: Worker Mind Process ---")
    test_workers = ["sop_1", "sop_6", "sop_10"]
    for wid in test_workers:
        print(f"Testing Worker Mind: {wid}...")
        driver.execute_script(f"selectNode('{wid}'); switchLevel(1);")
        time.sleep(0.5)

        mind_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
        print(f"  -> Mind nodes rendered: {len(mind_nodes)} (Personas + Core Harness + Skills)")
        assert len(mind_nodes) >= 5, f"Expected at least 5 mind nodes for {wid}, got {len(mind_nodes)}"

        crumb_l1 = driver.find_element(By.ID, "crumbL1").text
        print(f"  -> Level 1 Breadcrumb: '{crumb_l1}'")

        # Test return to Level 2
        driver.execute_script("switchLevel(2);")
        time.sleep(0.4)
        l2_check = driver.find_elements(By.CLASS_NAME, "canvas-node")
        assert len(l2_check) == 11, "Must return cleanly to Level 2 S&OP"

    driver.execute_script("selectNode('sop_1'); switchLevel(1);")
    time.sleep(0.5)
    driver.save_screenshot("enterprise_l1_mind_screenshot.png")
    print("\nSaved 'enterprise_l1_mind_screenshot.png'")

    print("\n[SUCCESS] 3-Tier Enterprise AI Factory Architecture Verified 100%!")
    print("  Level 3 (Company): 6 Organizations in Value Stream")
    print("  Level 2 (Organization): ALWAYS S&OP (11 Workers)")
    print("  Level 1 (Mind): Cognitive Skills + Internal Personas")

finally:
    driver.quit()
