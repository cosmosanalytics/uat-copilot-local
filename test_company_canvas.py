# -*- coding: utf-8 -*-
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def test_apps():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1440,900")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=opts)

    try:
        # 1. Test company_ai_factory_canvas.html (Base 3-Tier App)
        p1 = os.path.abspath("company_ai_factory_canvas.html")
        driver.get(f"file:///{p1}")
        time.sleep(1.5)
        logs = driver.get_log("browser")
        severe = [l for l in logs if l['level'] == 'SEVERE']
        print(f"[company_ai_factory_canvas.html] Console logs: {len(logs)}, severe: {len(severe)}")
        assert len(severe) == 0, f"Severe errors in company_ai_factory_canvas.html: {severe}"

        # Verify only 3 tiers exist in switcher
        tabs = driver.find_elements(By.CLASS_NAME, "level-tab")
        tab_texts = [t.text for t in tabs]
        print(f"Tabs in switcher: {tab_texts}")
        assert not any("Level 4" in t for t in tab_texts), "Level 4 should NOT exist in company_ai_factory_canvas.html"

        # 2. Test company_ai_factory_canvas_human_intervention.html (3-Tier Human Intervention App)
        p2 = os.path.abspath("company_ai_factory_canvas_human_intervention.html")
        driver.get(f"file:///{p2}")
        time.sleep(1.5)
        logs2 = driver.get_log("browser")
        severe2 = [l for l in logs2 if l['level'] == 'SEVERE']
        print(f"[company_ai_factory_canvas_human_intervention.html] Console logs: {len(logs2)}, severe: {len(severe2)}")
        assert len(severe2) == 0, f"Severe errors in company_ai_factory_canvas_human_intervention.html: {severe2}"

        # Check Decision Cards
        cards = driver.find_elements(By.CLASS_NAME, "decision-card")
        print(f"Decision cards count: {len(cards)}")

        # Check Human Gate on canvas
        gate = driver.find_element(By.ID, "node_gate_human")
        print(f"Human Gate node on canvas: {gate.is_displayed()}")

        # Capture screenshots
        driver.save_screenshot("company_ai_factory_canvas_human_intervention_preview.png")
        print("Saved company_ai_factory_canvas_human_intervention_preview.png")

        print("ALL TESTS PASSED SUCCESSFULLY!")

    finally:
        driver.quit()

if __name__ == "__main__":
    test_apps()
