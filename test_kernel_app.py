# -*- coding: utf-8 -*-
import os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1440,950')
driver = webdriver.Chrome(options=options)

path = os.path.abspath('agent_kernel_studio_app.html')
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
print('Found preset chips:', len(chips))
if len(chips) > 1:
    chips[1].click()
    time.sleep(0.3)
    val = driver.find_element(By.ID, 'kernelGoalInput').get_attribute('value')
    print('Preset 1 loaded goal length:', len(val))

# 2. Test Virtual Context Pager Tab
driver.find_element(By.ID, 'tabBtnPager').click()
time.sleep(0.3)
frames = driver.find_elements(By.CSS_SELECTOR, '#pagerGrid .frame-card')
print('Context pager frames rendered:', len(frames))

# 3. Test Episodic Ledger Tab
driver.find_element(By.ID, 'tabBtnLedger').click()
time.sleep(0.3)
blocks = driver.find_elements(By.CSS_SELECTOR, '#ledgerChain .block-card')
print('Episodic ledger blocks rendered:', len(blocks))

# 4. Test Dedicated SKILL.md Library Tab
driver.find_element(By.ID, 'tabBtnSkills').click()
time.sleep(0.5)

skill_items = driver.find_elements(By.XPATH, "//div[@id='kernelSkillsListPane']/div")
print('Dedicated Kernel SKILL.md items:', len(skill_items))

active_title = driver.find_element(By.ID, 'kernelSkillHeaderTitle').text
print('Active SKILL.md title:', active_title)

# Filter Executive
driver.find_element(By.ID, 'filterExecutive').click()
time.sleep(0.3)
exec_items = driver.find_elements(By.XPATH, "//div[@id='kernelSkillsListPane']/div")
print('Executive suite items:', len(exec_items))

# Filter Memory
driver.find_element(By.ID, 'filterMemory').click()
time.sleep(0.3)
mem_items = driver.find_elements(By.XPATH, "//div[@id='kernelSkillsListPane']/div")
print('Memory suite items:', len(mem_items))

# Click item in memory suite
if len(mem_items) > 0:
    mem_items[0].click()
    time.sleep(0.3)
    new_title = driver.find_element(By.ID, 'kernelSkillHeaderTitle').text
    print('Selected Memory skill title:', new_title)

# Reset to all and click tab 1 for full executive view
driver.find_element(By.ID, 'filterAll').click()
time.sleep(0.2)
driver.find_element(By.ID, 'tabBtnExecutive').click()
time.sleep(0.5)

driver.save_screenshot('agent_kernel_studio_preview.png')
print('Saved screenshot: agent_kernel_studio_preview.png')

# Also capture skills library screenshot
driver.find_element(By.ID, 'tabBtnSkills').click()
time.sleep(0.5)
driver.save_screenshot('agent_kernel_skills_library_preview.png')
print('Saved screenshot: agent_kernel_skills_library_preview.png')

driver.quit()
