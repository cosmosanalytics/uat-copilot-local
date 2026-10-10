import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1280,900")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)

files_to_test = [
    "academy_guide_app.html",
    "doc_coauthoring_app.html",
    "docx_studio_app.html"
]

all_passed = True

for fname in files_to_test:
    abs_path = os.path.abspath(fname)
    url = f"file:///{abs_path.replace(os.sep, '/')}"
    print(f"\n--- Testing {fname} ---")
    driver.get(url)
    time.sleep(1.5)

    title = driver.title
    print(f"Page Title: {title}")

    # Check for console errors
    logs = driver.get_log("browser")
    severe_errors = [l for l in logs if l["level"] == "SEVERE"]
    if severe_errors:
        print(f"FAILED (Severe Errors): {severe_errors}")
        all_passed = False
    else:
        print("Console Logs: Clean (0 severe errors)")

    # Test Instant synthesis to ensure preview stays active and updates
    try:
        # Click instant
        instant_btn = driver.find_element(By.ID, "btnInstant")
        instant_btn.click()
        time.sleep(0.5)

        synth_btn = driver.find_element(By.CSS_SELECTOR, "button[id^='btnSynth'], button[id='btnSynthesize'], button.btn-action, button.btn-synthesize")
        synth_btn.click()
        time.sleep(1)

        # Check for any new severe errors
        new_logs = driver.get_log("browser")
        new_severe = [l for l in new_logs if l["level"] == "SEVERE"]
        if new_severe:
            print(f"FAILED on Synthesize (Severe Errors): {new_severe}")
            all_passed = False
        else:
            print("Synthesis Test: Clean (0 errors)")

        print(f"PASSED: {fname}")
    except Exception as e:
        print(f"Error testing interaction on {fname}: {e}")
        all_passed = False

driver.quit()

if all_passed:
    print("\n==========================================")
    print("ALL 3 APPS VERIFIED SUCCESSFULLY VIA SELENIUM!")
    print("==========================================")
else:
    print("\nSome apps failed.")
    exit(1)
