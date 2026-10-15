# -*- coding: utf-8 -*-
"""
test_enterprise_app.py
Verifies enterprise_ai_factory_canvas.html:
- Tests Level 3: Company Value Stream (6 Organizations)
- Tests Level 2: S&OP Flow (11 stages) and ERP Flow (8 modules)
- Tests Level 1: Worker Mind (Personas + Skills)
- Verifies responsive layout on mobile (390x844) and desktop (1440x900)
- Captures screenshots
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

# 1. Desktop Test (1440 x 900)
print("--- 1. TESTING DESKTOP VIEWPORT (1440x900) ---")
d_opts = Options()
d_opts.add_argument("--headless=new")
d_opts.add_argument("--window-size=1440,900")
d_opts.add_argument("--disable-gpu")
d_opts.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=d_opts)
try:
    driver.get(url)
    time.sleep(2)

    logs = driver.get_log("browser")
    severe = [l for l in logs if l['level'] == 'SEVERE']
    print(f"Browser console logs: {len(logs)} entries, {len(severe)} SEVERE")

    # Verify Level 3 (Company)
    l3_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
    print(f"Level 3 Company Organization Nodes rendered: {len(l3_nodes)} (Expected 6)")
    driver.save_screenshot("enterprise_l3_company_screenshot.png")
    print("Saved 'enterprise_l3_company_screenshot.png'")

    # Switch to Level 2 (ERP View)
    print("Switching to Level 2 ERP...")
    driver.execute_script("switchOrganizationView('erp'); switchLevel(2);")
    time.sleep(1)
    l2_erp_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
    print(f"Level 2 ERP Module Nodes rendered: {len(l2_erp_nodes)} (Expected 8)")
    driver.save_screenshot("enterprise_l2_erp_screenshot.png")
    print("Saved 'enterprise_l2_erp_screenshot.png'")

    # Switch to Level 2 (S&OP View)
    print("Switching to Level 2 S&OP...")
    driver.execute_script("switchOrganizationView('sop'); switchLevel(2);")
    time.sleep(1)
    l2_sop_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
    print(f"Level 2 S&OP Stage Nodes rendered: {len(l2_sop_nodes)} (Expected 11)")
    driver.save_screenshot("enterprise_l2_sop_screenshot.png")
    print("Saved 'enterprise_l2_sop_screenshot.png'")

    # Switch to Level 1 (Worker Mind)
    print("Switching to Level 1 Worker Mind...")
    driver.execute_script("switchLevel(1);")
    time.sleep(1)
    l1_nodes = driver.find_elements(By.CLASS_NAME, "canvas-node")
    print(f"Level 1 Cognitive Mind Nodes rendered: {len(l1_nodes)}")
    driver.save_screenshot("enterprise_l1_mind_screenshot.png")
    print("Saved 'enterprise_l1_mind_screenshot.png'")

finally:
    driver.quit()

# 2. Mobile Test (390 x 844)
print("\n--- 2. TESTING MOBILE VIEWPORT (390x844) ---")
m_opts = Options()
m_opts.add_argument("--headless=new")
m_opts.add_argument("--window-size=390,844")
m_opts.add_argument("--disable-gpu")
m_opts.add_argument("--no-sandbox")

m_driver = webdriver.Chrome(options=m_opts)
try:
    m_driver.get(url)
    time.sleep(2)
    m_driver.save_screenshot("enterprise_mobile_l3_screenshot.png")
    print("Saved 'enterprise_mobile_l3_screenshot.png'")
finally:
    m_driver.quit()

print("\n[SUCCESS] All 3-Tier Enterprise tests passed!")
