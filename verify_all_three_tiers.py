# -*- coding: utf-8 -*-
import os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1440,950')
driver = webdriver.Chrome(options=options)

def check_app(filename, tab_btn_id, list_pane_id, expected_count):
    path = os.path.abspath(filename)
    driver.get('file:///' + path.replace('\\', '/'))
    time.sleep(1)

    logs = driver.get_log('browser')
    errors = [l for l in logs if l['level'] == 'SEVERE']
    print(f"[{filename}] Console errors: {len(errors)}")

    # Click Skills Tab
    driver.find_element(By.ID, tab_btn_id).click()
    time.sleep(0.5)

    items = driver.find_elements(By.XPATH, f"//div[@id='{list_pane_id}']/div")
    print(f"[{filename}] Rendered Skill Items: {len(items)} (Expected: {expected_count})")
    assert len(items) == expected_count, f"Expected {expected_count}, got {len(items)}"
    return items

print("--- Testing Tier 0 App: aws_basics_studio_app.html ---")
items0 = check_app('aws_basics_studio_app.html', 'tabBtnSkills', 'skillsListPane', 7)

print("\n--- Testing Tier 1 App: agent_kernel_studio_app.html ---")
items1 = check_app('agent_kernel_studio_app.html', 'tabBtnSkills', 'kernelSkillsListPane', 14)
# Test filtering L1
driver.find_element(By.ID, 'filterL1').click()
time.sleep(0.3)
l1 = driver.find_elements(By.XPATH, "//div[@id='kernelSkillsListPane']/div")
print(f"[agent_kernel_studio_app.html] Filter L1 items: {len(l1)} (Expected: 7)")
assert len(l1) == 7

# Test filtering L0
driver.find_element(By.ID, 'filterL0').click()
time.sleep(0.3)
l0 = driver.find_elements(By.XPATH, "//div[@id='kernelSkillsListPane']/div")
print(f"[agent_kernel_studio_app.html] Filter L0 items: {len(l0)} (Expected: 7)")
assert len(l0) == 7

print("\n--- Testing Tier 2 App: multi_agent_system_studio_app.html ---")
items2 = check_app('multi_agent_system_studio_app.html', 'tabBtnSkills', 'swarmSkillsListPane', 20)
# Test filtering L2
driver.find_element(By.ID, 'filterL2').click()
time.sleep(0.3)
l2 = driver.find_elements(By.XPATH, "//div[@id='swarmSkillsListPane']/div")
print(f"[multi_agent_system_studio_app.html] Filter L2 items: {len(l2)} (Expected: 6)")
assert len(l2) == 6

# Test filtering L1
driver.find_element(By.ID, 'filterL1').click()
time.sleep(0.3)
l1_in_2 = driver.find_elements(By.XPATH, "//div[@id='swarmSkillsListPane']/div")
print(f"[multi_agent_system_studio_app.html] Filter L1 items: {len(l1_in_2)} (Expected: 7)")
assert len(l1_in_2) == 7

# Test filtering L0
driver.find_element(By.ID, 'filterL0').click()
time.sleep(0.3)
l0_in_2 = driver.find_elements(By.XPATH, "//div[@id='swarmSkillsListPane']/div")
print(f"[multi_agent_system_studio_app.html] Filter L0 items: {len(l0_in_2)} (Expected: 7)")
assert len(l0_in_2) == 7

driver.quit()
print("\nALL 3 TIER APPS VERIFIED SUCCESSFULLY WITH 100% ACCURACY!")
