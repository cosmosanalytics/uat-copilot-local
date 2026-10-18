# -*- coding: utf-8 -*-
"""
test_enterprise_all_6_orgs.py
Verifies the 4-Tier Enterprise AI Factory Fractal Value Chain Architecture:
1. Level 4: Value Chain Level Process (6 Companies: SilicoFab, MicroPCB, Apex OEM, Pegasus EMS, TransGlobal, OmniCloud)
2. Level 3: Company Level Process (6 Organizations: CRM, S&OP, ERP, MES, WMS, Finance)
3. Level 2: Organization Level Process (Selected at Company level: 4, 11, 8, 5, 5, 5 Workers)
4. Level 1: Mind Level Process (Cognition: Debate Personas + Cognitive Skills + Deterministic Harness)
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

    # 1. Level 4: Value Chain Level (6 Companies)
    print("\n--- Verifying Level 4: Multi-Enterprise Value Chain ---")
    l4_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
    print(f"Level 4 Companies: {len(l4_nodes)} (Expected 6)")
    assert len(l4_nodes) == 6, f"Expected 6 companies at Level 4, found {len(l4_nodes)}"

    crumb_l4 = driver.find_element(By.ID, "crumbL4").text
    print(f"  -> Level 4 Breadcrumb: '{crumb_l4}'")

    driver.save_screenshot("enterprise_l4_value_chain_screenshot.png")
    print("Saved 'enterprise_l4_value_chain_screenshot.png'")

    # 2. Drill down into Apex OEM (comp_3) at Level 3
    print("\n--- Drilling down into Apex OEM (Level 3 Company Process) ---")
    driver.execute_script("openCompanyFromValueChain('comp_3');")
    time.sleep(0.6)

    l3_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
    print(f"Level 3 Organizations: {len(l3_nodes)} (Expected 6)")
    assert len(l3_nodes) == 6, f"Expected 6 organizations at Level 3, found {len(l3_nodes)}"

    crumb_l3 = driver.find_element(By.ID, "crumbL3").text
    print(f"  -> Level 3 Breadcrumb: '{crumb_l3}'")
    assert "Apex" in crumb_l3, f"Expected Apex in breadcrumb, got: {crumb_l3}"

    driver.save_screenshot("enterprise_l3_company_screenshot.png")
    print("Saved 'enterprise_l3_company_screenshot.png'")

    # 3. Level 2: Test that Org level dynamically loads whichever organization is selected at Company level
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

    # 4. Navigate back up to Level 4 via breadcrumb or switchLevel(4)
    print("\n--- Verifying Upward Navigation back to Level 4 Value Chain ---")
    driver.execute_script("switchLevel(4);")
    time.sleep(0.5)
    l4_return_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
    assert len(l4_return_nodes) == 6, f"Expected 6 companies on return to Level 4, found {len(l4_return_nodes)}"
    print(f"Successfully returned to Level 4: {len(l4_return_nodes)} Companies rendered.")

    # 5. Verify BOM Modal
    print("\n--- Verifying 4-Tier BOM Modal ---")
    driver.execute_script("showBomModal();")
    time.sleep(0.5)
    bom_modal = driver.find_element(By.ID, "bomModal")
    assert bom_modal.is_displayed(), "BOM Modal is not displayed!"
    bom_text = bom_modal.text
    print(f"BOM modal contains 'Level 4': {'Level 4' in bom_text or 'L4 Value Chain' in bom_text}")
    assert "L4 Value Chain" in bom_text, "Expected 'L4 Value Chain' in BOM Modal!"
    driver.execute_script("hideBomModal();")

    print("\n🎉 ALL 4-TIER FRACTAL ARCHITECTURAL CHECKS PASSED PERFECTLY!")

finally:
    driver.quit()
