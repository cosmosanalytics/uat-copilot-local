"""
test_skills_13_to_19_apps.py
Headless Selenium verification for Skills 13 through 19 web applications:
1. academy_guide_app.html
2. doc_coauthoring_app.html
3. docx_studio_app.html
4. pdf_studio_app.html
5. pptx_studio_app.html
6. web_artifacts_builder_app.html
7. xlsx_studio_app.html
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

APPS = [
    ("academy_guide_app.html", "Claude Academy Guide", "goalInput", "btnSynthesize"),
    ("doc_coauthoring_app.html", "Doc Co-Authoring Studio", "topicInput", "btnSynthesize"),
    ("docx_studio_app.html", "DOCX Document Studio", "docInput", "btnSynthesize"),
    ("pdf_studio_app.html", "PDF Processing Studio", "pdfInput", "btnSynthesize"),
    ("pptx_studio_app.html", "PPTX Presentation Studio", "deckInput", "btnSynthesize"),
    ("web_artifacts_builder_app.html", "Web Artifacts Builder", "artifactInput", "btnSynthesize"),
    ("xlsx_studio_app.html", "XLSX Spreadsheet Studio", "sheetInput", "btnSynthesize")
]

def test_all_apps():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1440,900")
    
    driver = webdriver.Chrome(options=chrome_options)
    cwd = os.getcwd()

    all_passed = True

    try:
        for filename, expected_title, input_id, synth_id in APPS:
            file_path = os.path.join(cwd, filename)
            url = f"file:///{file_path.replace(os.sep, '/')}"
            print(f"\n--- Testing {filename} ---")
            driver.get(url)
            time.sleep(1)

            # 1. Verify title
            title = driver.title
            print(f"Page Title: {title}")
            assert expected_title in title, f"Title mismatch! Got {title}, expected {expected_title}"

            # 2. Verify light mode default
            theme = driver.execute_script("return document.documentElement.getAttribute('data-theme');")
            print(f"Default Theme: {theme}")
            assert theme == "light", f"Expected light theme default, got {theme}"

            # 3. Test theme toggle
            toggle_btn = driver.find_element(By.ID, "btnThemeToggle")
            toggle_btn.click()
            time.sleep(0.3)
            new_theme = driver.execute_script("return document.documentElement.getAttribute('data-theme');")
            print(f"Theme after toggle: {new_theme}")
            assert new_theme == "dark", f"Expected dark theme after toggle, got {new_theme}"

            # Toggle back
            toggle_btn.click()
            time.sleep(0.3)
            back_theme = driver.execute_script("return document.documentElement.getAttribute('data-theme');")
            assert back_theme == "light", "Expected theme to return to light"

            # 4. Verify input area is pre-filled (no empty input)
            input_el = driver.find_element(By.ID, input_id)
            input_val = input_el.get_attribute("value")
            print(f"Input Pre-filled Length: {len(input_val)} chars")
            assert len(input_val) > 10, f"Input is empty or too short: {input_val}"

            # 5. Check console errors
            logs = driver.get_log('browser')
            severe_errors = [l for l in logs if l.get('level') == 'SEVERE']
            if severe_errors:
                print(f"WARNING: Severe console logs in {filename}: {severe_errors}")
            else:
                print(f"Console Logs: Clean (0 severe errors)")

            print(f"PASSED: {filename}")

    except Exception as e:
        print(f"\nTEST FAILED with error: {e}")
        all_passed = False
    finally:
        driver.quit()

    if all_passed:
        print("\n==========================================")
        print("ALL 7 APPS VERIFIED SUCCESSFULLY VIA SELENIUM!")
        print("==========================================")
    else:
        sys.exit(1)

if __name__ == "__main__":
    test_all_apps()
