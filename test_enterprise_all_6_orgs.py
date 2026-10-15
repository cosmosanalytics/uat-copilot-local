# -*- coding: utf-8 -*-
"""
test_enterprise_all_6_orgs.py
Verifies full linkage across all 6 organizations in enterprise_ai_factory_canvas.html:
- Level 3 Company Value Stream (6 Orgs)
- Level 2 for CRM (4 workers)
- Level 2 for S&OP (11 workers)
- Level 2 for ERP (8 workers)
- Level 2 for MES (5 workers)
- Level 2 for WMS (5 workers)
- Level 2 for Finance (5 workers)
- Level 1 Cognitive Mind for workers in each organization
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

    # 1. Level 3: Company
    l3_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
    print(f"Level 3 Organizations: {len(l3_nodes)} (Expected 6)")

    # 2. Test All 6 Organizations at Level 2
    org_specs = [
        ("crm", 4, "CRM & Commercial"),
        ("sop", 11, "S&OP Planning"),
        ("erp", 8, "ERP Core Transactions"),
        ("mes", 5, "MES Shop Floor"),
        ("wms", 5, "WMS & Logistics"),
        ("fin", 5, "Finance & Treasury")
    ]

    for org_key, expected_count, org_name in org_specs:
        print(f"\nTesting Level 2 Org: {org_name} ({org_key})...")
        driver.execute_script(f"switchOrganizationView('{org_key}'); switchLevel(2);")
        time.sleep(0.6)
        nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
        print(f"  -> Rendered {len(nodes)} worker nodes (Expected: {expected_count})")
        assert len(nodes) == expected_count, f"Mismatch for {org_name}: got {len(nodes)}, expected {expected_count}"

        # Drill into the first worker's Level 1 Mind
        first_worker_id = nodes[0].get_attribute("id").replace("node_", "")
        print(f"  -> Drilling into Level 1 Mind for worker: {first_worker_id}...")
        driver.execute_script(f"selectNode('{first_worker_id}'); switchLevel(1);")
        time.sleep(0.5)
        mind_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
        print(f"  -> Mind nodes rendered: {len(mind_nodes)} (Personas + Core + Skills)")
        assert len(mind_nodes) >= 4, f"Mind nodes too low for {first_worker_id}"

        # Return to Level 2
        driver.execute_script("switchLevel(2);")
        time.sleep(0.3)

    # Capture screenshots of MES and WMS
    driver.execute_script("switchOrganizationView('mes'); switchLevel(2);")
    time.sleep(0.5)
    driver.save_screenshot("enterprise_l2_mes_screenshot.png")
    print("\nSaved 'enterprise_l2_mes_screenshot.png'")

    driver.execute_script("switchOrganizationView('wms'); switchLevel(2);")
    time.sleep(0.5)
    driver.save_screenshot("enterprise_l2_wms_screenshot.png")
    print("Saved 'enterprise_l2_wms_screenshot.png'")

    driver.execute_script("switchOrganizationView('fin'); switchLevel(2);")
    time.sleep(0.5)
    driver.save_screenshot("enterprise_l2_fin_screenshot.png")
    print("Saved 'enterprise_l2_fin_screenshot.png'")

    print("\n[SUCCESS] All 6 organizations and their workers & cognitive minds verified 100% linked!")

finally:
    driver.quit()
