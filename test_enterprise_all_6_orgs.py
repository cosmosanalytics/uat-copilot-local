# -*- coding: utf-8 -*-
"""
test_enterprise_all_6_orgs.py
Verifies the 3-Tier Enterprise AI Factory Architecture:
1. Level 3: Company Level Process (6 Organizations playing roles in Enterprise Value Stream)
2. Level 2: Organization Level Process (Selected at Company level: CRM, S&OP, ERP, MES, WMS, Finance)
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

    crumb_l3 = driver.find_element(By.ID, "crumbL3").text
    print(f"  -> Level 3 Breadcrumb: '{crumb_l3}'")

    driver.save_screenshot("enterprise_l3_company_screenshot.png")
    print("Saved 'enterprise_l3_company_screenshot.png'")

    # 2. Level 2: Test that Org level dynamically loads whichever organization is selected at Company level
    org_specs = [
        ("crm", 4, "CRM & Commercial Ops"),
        ("sop", 11, "S&OP Planning Engine"),
        ("erp", 8, "ERP Core Transactions"),
        ("mes", 5, "MES Shop Floor"),
        ("wms", 5, "WMS & Logistics"),
        ("fin", 5, "Finance & Treasury")
    ]

    print("\n--- Verifying Level 2 & Level 1 Across All 6 Organizations ---")
    for org_id, expected_count, org_name in org_specs:
        print(f"\nSelecting Org '{org_name}' ({org_id}) at Company Level...")
        # Start at company level
        driver.execute_script("switchLevel(3);")
        time.sleep(0.3)

        # Open organization from company level
        driver.execute_script(f"openOrganizationFromCompany('{org_id}');")
        time.sleep(0.6)

        # Verify Level 2 rendered workers for this organization
        l2_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
        print(f"  -> Level 2 Workers rendered: {len(l2_nodes)} (Expected: {expected_count})")
        assert len(l2_nodes) == expected_count, f"Mismatch for {org_name}: got {len(l2_nodes)}, expected {expected_count}"

        # Check breadcrumb at Level 2
        crumb_l2 = driver.find_element(By.ID, "crumbL2").text
        print(f"  -> Breadcrumb: '{crumb_l2}'")
        assert org_name.split()[0] in crumb_l2 or org_id.upper() in crumb_l2, f"Org name mismatch in breadcrumb: {crumb_l2}"

        # Drill into first worker's Level 1 Mind
        first_worker_id = l2_nodes[0].get_attribute("id").replace("node_", "")
        print(f"  -> Drilling into Level 1 Mind for worker: {first_worker_id}...")
        driver.execute_script(f"selectNode('{first_worker_id}'); switchLevel(1);")
        time.sleep(0.5)

        mind_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
        print(f"  -> Mind nodes rendered: {len(mind_nodes)} (Personas + Core Harness + Skills)")
        assert len(mind_nodes) >= 5, f"Expected at least 5 mind nodes for {first_worker_id}, got {len(mind_nodes)}"

        crumb_l1 = driver.find_element(By.ID, "crumbL1").text
        print(f"  -> Level 1 Breadcrumb: '{crumb_l1}'")

        # Return to Level 2
        driver.execute_script("switchLevel(2);")
        time.sleep(0.3)
        l2_return_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
        assert len(l2_return_nodes) == expected_count, f"Return to Level 2 failed for {org_name}"

    # Capture screenshots of key Level 2 organization views
    driver.execute_script("openOrganizationFromCompany('erp');")
    time.sleep(0.5)
    driver.save_screenshot("enterprise_l2_erp_screenshot.png")
    print("\nSaved 'enterprise_l2_erp_screenshot.png'")

    driver.execute_script("openOrganizationFromCompany('sop');")
    time.sleep(0.5)
    driver.save_screenshot("enterprise_l2_sop_screenshot.png")
    print("Saved 'enterprise_l2_sop_screenshot.png'")

    driver.execute_script("selectNode('sop_1'); switchLevel(1);")
    time.sleep(0.5)
    driver.save_screenshot("enterprise_l1_mind_screenshot.png")
    print("Saved 'enterprise_l1_mind_screenshot.png'")

    print("\n[SUCCESS] 3-Tier Enterprise AI Factory Architecture Verified 100%!")
    print("  Level 3 (Company): 6 Organizations in Value Stream")
    print("  Level 2 (Organization): Dynamically selected at Company level (CRM, S&OP, ERP, MES, WMS, Finance)")
    print("  Level 1 (Mind): Cognitive Skills + Internal Debate Personas + Deterministic Harness")

finally:
    driver.quit()
