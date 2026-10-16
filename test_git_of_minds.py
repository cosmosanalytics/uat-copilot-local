# -*- coding: utf-8 -*-
"""
test_git_of_minds.py
Headless browser verification for Git of Minds • Visual Git for Agentic Reasoning & Branching.
"""

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

file_path = os.path.abspath("git_of_minds_simulator.html")
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
    assert "Git of Minds" in title, f"Unexpected title: {title}"

    # 2. Test Commit Node Inspection
    print("\n--- Testing Commit Node Inspection ---")
    driver.execute_script("selectNode('root');")
    time.sleep(0.3)
    sha_text = driver.find_element(By.ID, "inspSha").text
    branch_text = driver.find_element(By.ID, "inspBranch").text
    print(f"Inspector: {sha_text} | {branch_text}")
    assert "c7f91a2" in sha_text, f"Unexpected SHA: {sha_text}"
    assert "main" in branch_text, f"Unexpected branch: {branch_text}"

    driver.execute_script("selectNode('agg1');")
    time.sleep(0.3)
    sha_agg = driver.find_element(By.ID, "inspSha").text
    branch_agg = driver.find_element(By.ID, "inspBranch").text
    print(f"Inspector on Aggressive: {sha_agg} | {branch_agg}")
    assert "b28e401" in sha_agg
    assert "aggressive" in branch_agg

    # 3. Test Git Operations
    print("\n--- Testing Git DAG Operations ---")
    driver.execute_script("runSpeculativeBranching();")
    time.sleep(0.3)
    driver.execute_script("cherryPickSelectedNode();")
    time.sleep(0.3)
    driver.execute_script("mergeSelectedBranches();")
    time.sleep(0.3)
    dag_status = driver.find_element(By.ID, "dagStatusLabel").text
    print(f"DAG Status: '{dag_status}'")
    assert "Branches" in dag_status

    # 4. Switch to Branch Comparator Tab
    print("\n--- Testing Branch Comparator Tab ---")
    driver.execute_script("switchTab('compare');")
    time.sleep(0.3)
    branch_cards = driver.find_elements(By.CLASS_NAME, "branch-card")
    print(f"Branch Cards Rendered: {len(branch_cards)} (Expected 3)")
    assert len(branch_cards) == 3, f"Expected 3 branch cards, got {len(branch_cards)}"

    # 5. Switch to Consensus Merge Tab
    print("\n--- Testing Consensus Merge Tab ---")
    driver.execute_script("switchTab('merge');")
    time.sleep(0.3)
    merge_heading = driver.find_element(By.CSS_SELECTOR, "#tab-merge h3").text
    print(f"Merge Tab Heading: '{merge_heading}'")
    assert "Merge Protocol" in merge_heading

    # 6. Switch to Code Tab
    print("\n--- Testing Python Wasm Code Viewer ---")
    driver.execute_script("switchTab('code');")
    time.sleep(0.3)
    code_text = driver.find_element(By.ID, "codeViewer").text
    print(f"Python Code Length: {len(code_text)} characters")
    assert "class GitOfMindsDAG:" in code_text and "class ThoughtCommit:" in code_text, "Code viewer missing DAG classes!"

    # 7. Switch back to Canvas and take screenshot
    driver.execute_script("switchTab('canvas');")
    time.sleep(0.5)
    screenshot_path = "git_of_minds_screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"\n[OK] Screenshot saved to {screenshot_path}")

    print("\n🎉 ALL GIT OF MINDS BROWSER CHECKS PASSED PERFECTLY!")

finally:
    driver.quit()
