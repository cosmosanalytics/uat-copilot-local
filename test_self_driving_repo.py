# -*- coding: utf-8 -*-
"""
test_self_driving_repo.py
Automated headless Selenium browser test for Autonomous Self-Driving Repo Simulator.
"""

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

file_path = os.path.abspath("autonomous_self_driving_repo_simulator.html")
url = f"file:///{file_path.replace(os.sep, '/')}"

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1440,950")
opts.add_argument("--disable-gpu")
opts.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=opts)
try:
    print(f"Loading {url} in headless Chrome...")
    driver.get(url)
    time.sleep(2)

    # 1. Console errors check
    logs = driver.get_log("browser")
    severe = [l for l in logs if l['level'] == 'SEVERE']
    print(f"Console log count: {len(logs)}, severe errors: {len(severe)}")
    if severe:
        print("Severe errors:", severe)
    assert len(severe) == 0, f"Found severe console errors: {severe}"

    # 2. Verify Title and Header
    title = driver.title
    print(f"Page Title: '{title}'")
    assert "Autonomous Self-Driving Repo" in title, f"Unexpected title: {title}"

    repo_label = driver.find_element(By.ID, "repoNameLabel").text
    print(f"Repo label: '{repo_label}'")
    assert "autonomous" in repo_label.lower()

    # 3. Check Initial Stage
    active_stage_text = driver.find_element(By.ID, "activeStageLabel").text
    print(f"Initial Stage: '{active_stage_text}'")
    assert "stage 0" in active_stage_text.lower()

    # 4. Trigger Full Autonomous Loop
    print("\n--- Triggering Full 6-Stage Autonomous Loop ---")
    btn_run = driver.find_element(By.ID, "btnRunFullLoop")
    btn_run.click()

    # Wait for the autonomous loop to complete all 6 stages
    max_wait = 30
    start_t = time.time()
    completed = False
    while time.time() - start_t < max_wait:
        st_text = driver.find_element(By.ID, "activeStageLabel").text
        if "loop complete" in st_text.lower():
            completed = True
            break
        time.sleep(0.5)

    assert completed, f"Autonomous loop did not complete in {max_wait}s. Current label: {st_text}"
    print(f"[SUCCESS] Loop completed: '{st_text}' in {round(time.time() - start_t, 2)}s")

    # 5. Verify Commits & Files in Code Tab
    commits_text = driver.find_element(By.ID, "commitCountLabel").text
    print(f"Commits count: '{commits_text}'")
    assert "2 commits" in commits_text

    file_table_text = driver.find_element(By.ID, "fileTable").text
    assert "engine.py" in file_table_text
    assert "README.md" in file_table_text

    # 6. Verify Issues Tab
    driver.execute_script("switchTab('issues');")
    time.sleep(0.3)
    issues_text = driver.find_element(By.ID, "issuesListContainer").text
    print(f"Issues content preview: {issues_text[:120]}...")
    assert "#1 Bug: KeyError" in issues_text
    assert "Closed" in issues_text

    # 7. Verify PR Tab
    driver.execute_script("switchTab('pulls');")
    time.sleep(0.3)
    prs_text = driver.find_element(By.ID, "prListContainer").text
    print(f"PRs content preview: {prs_text[:120]}...")
    assert "#2 Fix concurrent TTL eviction" in prs_text
    assert "Merged" in prs_text
    assert "All checks have passed" in prs_text

    # 8. Verify Releases Tab
    driver.execute_script("switchTab('releases');")
    time.sleep(0.3)
    releases_text = driver.find_element(By.ID, "releasesContainer").text
    print(f"Releases content preview: {releases_text[:120]}...")
    assert "v1.0.1" in releases_text
    assert "v1.0.0" in releases_text

    # 9. Verify CI/CD Architecture Spec Tab
    driver.execute_script("switchTab('arch');")
    time.sleep(0.3)
    arch_text = driver.find_element(By.ID, "tabContentArch").text
    assert "What is Continuous Integration (CI)?" in arch_text
    assert "What is Continuous Deployment (CD)?" in arch_text

    # 10. Take Screenshot
    screenshot_path = os.path.abspath("self_driving_repo_screenshot.png")
    driver.save_screenshot(screenshot_path)
    print(f"[SUCCESS] Saved screenshot to {screenshot_path}")

    # 11. Final Console Check
    final_logs = driver.get_log("browser")
    final_severe = [l for l in final_logs if l['level'] == 'SEVERE']
    assert len(final_severe) == 0, f"Found severe console errors after execution: {final_severe}"

    print("\n[VERIFIED] All browser checks passed with 100% success!")

finally:
    driver.quit()
