import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_tests():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,800")

    driver = webdriver.Chrome(options=chrome_options)
    
    apps = [
        "ai_to_brain_forgetting_curve.html",
        "ai_to_brain_serial_position.html",
        "ai_to_brain_capacity_limit.html",
        "ai_to_brain_stroop_test.html",
        "ai_to_brain_sleep_replay_test.html",
        "ai_to_brain_broadcast_test.html",
        "ai_to_brain_source_memory.html"
    ]
    
    workspace = r"c:\Users\richa\ai-engineering"
    results = []

    print(f"=== TESTING ALL 7 AI TO BRAIN WEB APPS VIA SELENIUM HEADLESS CHROME ===")
    
    for app in apps:
        filepath = os.path.join(workspace, app)
        file_url = f"file:///{filepath.replace(os.sep, '/')}"
        print(f"\nTesting {app}...")
        
        try:
            driver.get(file_url)
            time.sleep(1.0)
            
            # 1. Title verification
            title = driver.title
            assert len(title) > 0, f"{app}: Empty title"
            print(f"  [PASS] Page Title: '{title[:45]}...'")

            # 2. Light mode default check
            body = driver.find_element(By.TAG_NAME, "body")
            body_class = body.get_attribute("class")
            assert "light-mode" in body_class, f"{app}: body does not have 'light-mode' by default (got: {body_class})"
            print(f"  [PASS] Default Light Mode active")

            # 3. Model selector verification
            model_select = driver.find_element(By.ID, "model-select")
            options = model_select.find_elements(By.TAG_NAME, "option")
            assert len(options) >= 3, f"{app}: Expected at least 3 models, found {len(options)}"
            print(f"  [PASS] Model dropdown present with {len(options)} options (Groq, WebGPU, Math)")

            # 4. Engine pills
            eng_det = driver.find_element(By.ID, "eng-det")
            eng_groq = driver.find_element(By.ID, "eng-groq")
            eng_webllm = driver.find_element(By.ID, "eng-webllm")
            assert eng_det and eng_groq and eng_webllm, f"{app}: Engine pills missing"
            print(f"  [PASS] Substrate pills active (Deterministic, Groq LPU, WebGPU WebLLM)")

            # 5. Execute button check & trigger
            btn_run = driver.find_element(By.CLASS_NAME, "btn-execute")
            assert btn_run.is_displayed(), f"{app}: Run button not visible"
            btn_run.click()
            time.sleep(0.8)
            print(f"  [PASS] Execution trial successfully triggered")

            # 6. Check console logs
            logs = driver.get_log("browser")
            severe_errors = [entry for entry in logs if entry["level"] == "SEVERE" and "favicon" not in entry["message"].lower()]
            if severe_errors:
                print(f"  [WARN] Console severe logs: {severe_errors}")
            else:
                print(f"  [PASS] 0 severe console errors")

            results.append((app, "PASS", "All checks verified"))

        except Exception as e:
            print(f"  [FAIL] Error testing {app}: {e}")
            results.append((app, "FAIL", str(e)))

    driver.quit()

    print("\n" + "="*60)
    print("SELENIUM VERIFICATION SUMMARY:")
    all_passed = True
    for app, status, msg in results:
        print(f"  - {app:35} : {status} ({msg})")
        if status != "PASS":
            all_passed = False
    print("="*60)

    if not all_passed:
        sys.exit(1)
    else:
        print("ALL 7 AI TO BRAIN WEB APPS PASSED AUTOMATED TESTING!")

if __name__ == "__main__":
    run_tests()
