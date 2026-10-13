from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=opts)
driver.set_window_size(1440, 1000)

apps = [
    "brain_to_ai_somatic_marker.html",
    "brain_to_ai_theory_of_mind.html",
    "brain_to_ai_consolidation.html",
    "brain_to_ai_homeostasis.html"
]

for app in apps:
    driver.get('file:///' + os.path.abspath(app))
    time.sleep(1)
    body_cls = driver.find_element(By.TAG_NAME, 'body').get_attribute('class')
    print(app, '-> Default Body Class:', body_cls)
    assert 'light-mode' in body_cls, f"Expected light-mode in {app}"

    # Click toggle button
    theme_btn = driver.find_element(By.ID, 'theme-btn')
    print('  Theme button icon:', theme_btn.text.encode('ascii', errors='replace').decode('ascii'))
    driver.execute_script("arguments[0].click();", theme_btn)
    time.sleep(0.5)
    toggled_cls = driver.find_element(By.TAG_NAME, 'body').get_attribute('class')
    print('  After toggle class:', toggled_cls)

    # Click back to light
    driver.execute_script("arguments[0].click();", theme_btn)
    time.sleep(0.5)
    restored_cls = driver.find_element(By.TAG_NAME, 'body').get_attribute('class')
    print('  Restored to light mode:', 'light-mode' in restored_cls)

    logs = driver.get_log('browser')
    severe = [l for l in logs if l['level'] == 'SEVERE']
    print('  Console errors:', len(severe))

driver.quit()
print('ALL 4 APPS VERIFIED IN LIGHT MODE!')
