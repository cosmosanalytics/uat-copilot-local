# -*- coding: utf-8 -*-
import os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1440,950')
driver = webdriver.Chrome(options=options)

path = os.path.abspath('aws_basics_studio_app.html')
driver.get('file:///' + path.replace('\\', '/'))
time.sleep(1)

# Check console errors
logs = driver.get_log('browser')
errors = [l for l in logs if l['level'] == 'SEVERE']
print('Console errors:', len(errors))
for e in errors:
    print('  ', e['message'])

# Switch to skills tab
driver.find_element(By.ID, 'tabBtnSkills').click()
time.sleep(0.5)

# Check innerHTML
html = driver.execute_script("return document.getElementById('skillsListPane').innerHTML;")
print('skillsListPane HTML length:', len(html))

items = driver.find_elements(By.XPATH, "//div[@id='skillsListPane']/div")
print('Found items:', len(items))

title = driver.find_element(By.ID, 'skillHeaderTitle').text
print('Active skill title:', title)

content = driver.find_element(By.ID, 'skillContentPre').text
print('Content length:', len(content), 'First 100 chars:', repr(content[:100]))

# Filter L1
driver.find_element(By.ID, 'filterL1').click()
time.sleep(0.3)
l1_items = driver.find_elements(By.XPATH, "//div[@id='skillsListPane']/div")
print('L1 items:', len(l1_items))

# Filter L2
driver.find_element(By.ID, 'filterL2').click()
time.sleep(0.3)
l2_items = driver.find_elements(By.XPATH, "//div[@id='skillsListPane']/div")
print('L2 items:', len(l2_items))

# Filter L0
driver.find_element(By.ID, 'filterL0').click()
time.sleep(0.3)
l0_items = driver.find_elements(By.XPATH, "//div[@id='skillsListPane']/div")
print('L0 items:', len(l0_items))

# Click item 2
if len(l0_items) > 1:
    l0_items[1].click()
    time.sleep(0.3)
    new_title = driver.find_element(By.ID, 'skillHeaderTitle').text
    print('New title after click:', new_title)

driver.save_screenshot('skills_library_tab_preview.png')
print('Screenshot saved!')
driver.quit()
