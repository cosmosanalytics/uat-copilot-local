# -*- coding: utf-8 -*-
"""
test_github_agent_collaboration.py
Headless browser verification for GitHub Agent Collaboration Simulator.
"""

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

file_path = os.path.abspath("github_agent_collaboration_simulator.html")
url = f"file:///{file_path.replace(os.sep, '/')}"

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1440,900")
opts.add_argument("--disable-gpu")
opts.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=opts)
try:
    print(f"Loading {url}...")
    driver.get(url)
    time.sleep(2)

    logs = driver.get_log("browser")
    severe = [l for l in logs if l['level'] == 'SEVERE']
    print(f"Browser console logs: {len(logs)} entries, {len(severe)} SEVERE")
    if severe:
        print("Severe logs:", severe)
    assert len(severe) == 0, f"Found severe console errors: {severe}"

    # 1. Verify Title & Header
    title = driver.title
    print(f"Page Title: '{title}'")
    assert "GitHub Agent Collaboration" in title, f"Unexpected title: {title}"

    # 2. Check PR Details & Author
    pr_title = driver.find_element(By.ID, "prTitleText").text
    print(f"PR Title: '{pr_title}'")
    assert "Quorum Consensus" in pr_title

    # 3. Test CI Failure Trigger
    print("\n--- Testing CI Failure Trigger ---")
    driver.execute_script("simulateCharlieCiFailure();")
    time.sleep(0.3)
    headline = driver.find_element(By.ID, "checksHeadline").text
    print(f"Checks Headline after failure: '{headline}'")
    assert "failed" in headline.lower()
    btn_merge = driver.find_element(By.ID, "btnMerge")
    assert not btn_merge.is_enabled(), "Merge button should be disabled when CI fails!"

    # 4. Test Security Review Block
    print("\n--- Testing Security Review Block ---")
    driver.execute_script("simulateBobSecurityBlock();")
    time.sleep(0.3)
    badge_bob = driver.find_element(By.ID, "bobBadge").text
    print(f"Bob Review Badge: '{badge_bob}'")
    assert "Changes Requested" in badge_bob

    # 5. Test Reset to Clean State and Squash Merge
    print("\n--- Testing Clean State & Squash Merge ---")
    driver.execute_script("simulateCleanApprovalState();")
    time.sleep(0.3)
    assert btn_merge.is_enabled(), "Merge button should be enabled after approvals!"

    driver.execute_script("executeSquashMerge();")
    time.sleep(0.5)
    status_text = driver.find_element(By.ID, "prStatusBadge").text
    print(f"PR Status after merge: '{status_text}'")
    assert "Merged" in status_text

    # 6. Test Tab Switching (Diff, Actions, Engine)
    print("\n--- Testing PR Tab Switching ---")
    driver.execute_script("switchPrTab('diff');")
    time.sleep(0.3)
    diff_rows = driver.find_elements(By.CLASS_NAME, "diff-row")
    print(f"Diff Rows Rendered: {len(diff_rows)}")
    assert len(diff_rows) >= 5, "Diff table has too few rows!"

    driver.execute_script("switchPrTab('actions');")
    time.sleep(0.3)
    ci_console_text = driver.find_element(By.ID, "ciConsole").text
    print(f"CI Console Length: {len(ci_console_text)} characters")
    assert "pytest" in ci_console_text.lower()

    driver.execute_script("switchPrTab('engine');")
    time.sleep(0.3)
    engine_text = driver.find_element(By.ID, "engineConsole").text
    assert "GitHubPullRequest" in engine_text

    # 7. Switch back to Conversation and take screenshot
    driver.execute_script("switchPrTab('conversation');")
    time.sleep(0.5)
    screenshot_path = "github_agent_collaboration_screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"\n[OK] Screenshot saved to {screenshot_path}")

    print("\n🎉 ALL GITHUB AGENT COLLABORATION BROWSER CHECKS PASSED PERFECTLY!")

finally:
    driver.quit()
