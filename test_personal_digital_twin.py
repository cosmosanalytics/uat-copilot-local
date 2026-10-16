# -*- coding: utf-8 -*-
"""
test_personal_digital_twin.py
Headless browser verification for The Local-First Personal Digital Twin web app.
"""

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

file_path = os.path.abspath("personal_digital_twin_local.html")
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
    assert "Personal Digital Twin" in title, f"Unexpected title: {title}"

    # 2. Verify Storage Durability Center
    print("\n--- Testing Storage Durability Center ---")
    driver.execute_script("requestStoragePersistence();")
    time.sleep(0.5)
    pill_text = driver.find_element(By.ID, "durabilityPill").text
    print(f"Durability Pill: '{pill_text}'")
    assert "IMMUNITY" in pill_text or "ACTIVE" in pill_text or "SHIELD" in pill_text

    # 3. Test Knowledge Ingestion
    print("\n--- Testing Personal Knowledge Ingestion ---")
    driver.execute_script("applyKnowledgePreset('architect');")
    time.sleep(0.2)
    driver.execute_script("ingestNewKnowledge();")
    time.sleep(0.5)
    badge_text = driver.find_element(By.ID, "memoryCountBadge").text
    print(f"Memory Badge: '{badge_text}' (Expected >= 6)")
    assert "6" in badge_text or "7" in badge_text, f"Unexpected badge text: {badge_text}"

    # 4. Test Rehearsal Studio Chat & Scorecard
    print("\n--- Testing Rehearsal Studio Simulation ---")
    driver.execute_script("fillSuggestedAnswer();")
    time.sleep(0.3)
    driver.execute_script("sendChatMessage();")
    time.sleep(1.0)

    score_alignment = driver.find_element(By.ID, "scoreAlignment").text
    critique_text = driver.find_element(By.ID, "critiqueBox").text
    print(f"Alignment Score: {score_alignment}")
    print(f"Critique Preview: {critique_text[:120]}...")
    assert "96%" in score_alignment or "9" in score_alignment, f"Unexpected alignment score: {score_alignment}"
    assert len(critique_text) > 20, "Critique text is too short!"

    # 5. Test Tab Switching
    print("\n--- Testing Tab Switching (Vault, Decay, Engine) ---")
    driver.execute_script("switchTab('vault');")
    time.sleep(0.3)
    cards = driver.find_elements(By.CLASS_NAME, "memory-card")
    print(f"Rendered Memory Cards in Vault: {len(cards)} (Expected >= 6)")
    assert len(cards) >= 6, f"Expected at least 6 memory cards, got {len(cards)}"

    driver.execute_script("switchTab('decay');")
    time.sleep(0.3)
    slider_label = driver.find_element(By.ID, "sliderValLabel").text
    print(f"Decay Slider Label: '{slider_label}'")

    driver.execute_script("switchTab('engine');")
    time.sleep(0.3)
    code_text = driver.find_element(By.ID, "codeViewer").text
    print(f"Python Engine Length: {len(code_text)} characters")
    assert "class EbbinghausMemoryModel:" in code_text and "class PersonalDigitalTwinVault:" in code_text, "Code viewer missing digital twin engine!"

    # 6. Switch back to Studio and take screenshot
    driver.execute_script("switchTab('studio');")
    time.sleep(0.5)
    screenshot_path = "personal_digital_twin_screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"\n[OK] Screenshot saved to {screenshot_path}")

    print("\n🎉 ALL PERSONAL DIGITAL TWIN BROWSER CHECKS PASSED PERFECTLY!")

finally:
    driver.quit()
