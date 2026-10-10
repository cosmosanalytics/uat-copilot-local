# -*- coding: utf-8 -*-
import os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1440,950')
driver = webdriver.Chrome(options=options)

path = os.path.abspath('multi_agent_system_studio_app.html')
driver.get('file:///' + path.replace('\\', '/'))
time.sleep(1)

# Check console errors
logs = driver.get_log('browser')
errors = [l for l in logs if l['level'] == 'SEVERE']
print('Console errors:', len(errors))
for e in errors:
    print('  ', e['message'])

# 1. Test Preset 1
chips = driver.find_elements(By.CSS_SELECTOR, '.preset-chips .chip')
print('Found swarm preset chips:', len(chips))
if len(chips) > 1:
    chips[1].click()
    time.sleep(0.3)
    val = driver.find_element(By.ID, 'swarmGoalInput').get_attribute('value')
    print('Preset 1 loaded goal length:', len(val))

# 2. Test Whiteboard Tab
driver.find_element(By.ID, 'tabBtnWhiteboard').click()
time.sleep(0.3)
lanes = driver.find_elements(By.CSS_SELECTOR, '#whiteboardLanes .whiteboard-lane')
print('Whiteboard lanes rendered:', len(lanes))

# 3. Test Quorum Tab
driver.find_element(By.ID, 'tabBtnQuorum').click()
time.sleep(0.3)
votes = driver.find_elements(By.CSS_SELECTOR, '#quorumGrid .vote-card')
print('Quorum votes rendered:', len(votes))

# 4. Test Dedicated SKILL.md Library Tab
driver.find_element(By.ID, 'tabBtnSkills').click()
time.sleep(0.5)

skill_items = driver.find_elements(By.XPATH, "//div[@id='swarmSkillsListPane']/div")
print('Dedicated Swarm SKILL.md items:', len(skill_items))

active_title = driver.find_element(By.ID, 'swarmSkillHeaderTitle').text
print('Active Swarm SKILL.md title:', active_title)

# Filter Architecture
driver.find_element(By.ID, 'filterArch').click()
time.sleep(0.3)
arch_items = driver.find_elements(By.XPATH, "//div[@id='swarmSkillsListPane']/div")
print('Architecture items:', len(arch_items))

# Filter Governance
driver.find_element(By.ID, 'filterGov').click()
time.sleep(0.3)
gov_items = driver.find_elements(By.XPATH, "//div[@id='swarmSkillsListPane']/div")
print('Governance items:', len(gov_items))

# Click an item
if len(gov_items) > 0:
    gov_items[0].click()
    time.sleep(0.3)
    new_title = driver.find_element(By.ID, 'swarmSkillHeaderTitle').text
    print('Selected Swarm skill title:', new_title)

# Reset to all and capture skills library screenshot
driver.find_element(By.ID, 'filterAll').click()
time.sleep(0.3)
driver.save_screenshot('multi_agent_skills_library_preview.png')
print('Saved screenshot: multi_agent_skills_library_preview.png')

# Switch back to topology tab and capture main screenshot
driver.find_element(By.ID, 'tabBtnTopology').click()
time.sleep(0.5)
driver.save_screenshot('multi_agent_studio_preview.png')
print('Saved screenshot: multi_agent_studio_preview.png')

driver.quit()
