import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=opts)
driver.set_window_size(1440, 1000)

apps = [
    {
        'file': 'brain_to_ai_adapts.html',
        'name': 'Adapts AI (+ Adapts)',
        'btn_id': 'btn-pivot',
        'result_id': 'dag-status',
        'expected': 'Cognitive Flexibility: Pivot Successful'
    },
    {
        'file': 'brain_to_ai_perceives.html',
        'name': 'Perceives AI (+ Perceives)',
        'btn_id': 'btn-filter',
        'result_id': 'filter-status',
        'expected': 'Perception Distilled · Forwarded to Agent Core'
    },
    {
        'file': 'brain_to_ai_stays_aware.html',
        'name': 'Stays Aware AI (+ Stays aware)',
        'btn_id': 'btn-sync',
        'result_id': 'swarm-status',
        'expected': 'Situational Equilibrium Locked · Quorum 100%'
    },
    {
        'file': 'brain_to_ai_vetoes.html',
        'name': 'Vetoes AI (Vetoes)',
        'btn_id': 'btn-veto',
        'result_id': 'veto-status',
        'expected': 'Ring-0 VETO Commited · Invariant Preserved'
    }
]

print("=== TESTING 4 NEW BRAIN-TO-AI TRANSLATION APPS ===")

all_passed = True

for app in apps:
    filepath = os.path.abspath(app['file'])
    print(f"\n--- Testing {app['name']} ({app['file']}) ---")
    driver.get('file:///' + filepath)
    time.sleep(1)

    print("Title:", driver.title)

    # 1. Check Light Mode
    is_light = driver.execute_script("return document.body.classList.contains('light-mode');")
    print("Light mode active by default:", is_light)
    if not is_light:
        print("FAIL: Light mode not active by default!")
        all_passed = False

    # 2. Check Model Selector
    sel = Select(driver.find_element(By.ID, 'model-select'))
    options = [o.text for o in sel.options]
    print(f"Model options count: {len(options)}")
    assert len(options) >= 7, "Model selector missing options"

    # 3. Test scenario presets
    presets = driver.find_elements(By.CSS_SELECTOR, '.btn-preset')
    print(f"Found {len(presets)} preset scenarios.")
    if len(presets) > 1:
        driver.execute_script("arguments[0].click();", presets[1])
        time.sleep(0.5)

    # 4. Click execution button
    btn = driver.find_element(By.ID, app['btn_id'])
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(2)

    status_text = driver.find_element(By.ID, app['result_id']).text
    print(f"Status result: {status_text}")
    assert app['expected'] in status_text, f"Expected '{app['expected']}' in '{status_text}'"

    # 5. Check Console Errors
    logs = driver.get_log('browser')
    severe = [l for l in logs if l['level'] == 'SEVERE']
    print(f"Severe console errors: {len(severe)}")
    if severe:
        for s in severe:
            print("  [ERROR]", s['message'])
        all_passed = False
    else:
        print(f"PASSED: {app['name']} working smoothly with 0 errors!")

driver.quit()

if all_passed:
    print("\nALL 4 NEW APPS PASSED END-TO-END AUTOMATED VERIFICATION!")
else:
    print("\nSOME TESTS FAILED.")
    exit(1)
