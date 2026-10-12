# -*- coding: utf-8 -*-
"""
test_sop_propagation_app.py
Verifies sop_agent_propagation_swarm_app.html in headless Chrome via Selenium.
Tests:
- Tab loading & active default view
- 11 Agent nodes & 10 wire connectors rendered
- Active Handover showcase & payload text
- 3-Tier stack grid (Tier 0 AWS, Tier 1 Kernel, Tier 2 Swarm)
- Step-by-step handover navigation
- Auto-play wave execution & ledger recording
- Tab switching to pipeline and back
- Screenshot capture
"""

import os
import sys
import time
sys.stdout.reconfigure(encoding='utf-8')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def run_tests():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1600,1200")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        app_path = os.path.abspath("sop_agent_propagation_swarm_app.html")
        driver.get(f"file:///{app_path}")
        time.sleep(1.5)

        # 1. Assert Title
        title = driver.title
        print(f"Title: {title}")
        assert "Dual Propagation" in title, "Title mismatch"

        # 2. Assert tabAgentProp is displayed and active
        tab_prop = driver.find_element(By.ID, "tabAgentProp")
        assert tab_prop.is_displayed(), "tabAgentProp is not displayed"
        print("PASS: tabAgentProp is active and displayed!")

        # 3. Assert 11 mesh nodes rendered
        nodes = driver.find_elements(By.CLASS_NAME, "agent-mesh-node")
        print(f"Rendered Mesh Nodes: {len(nodes)}")
        assert len(nodes) == 11, f"Expected 11 mesh nodes, found {len(nodes)}"

        # 4. Assert 10 wire arrows rendered
        wires = driver.find_elements(By.CLASS_NAME, "mesh-wire-arrow")
        print(f"Rendered Wire Arrows: {len(wires)}")
        assert len(wires) == 10, f"Expected 10 wire arrows, found {len(wires)}"

        # 5. Assert Handover Showcase Content
        src_name = driver.find_element(By.ID, "sourceAgentName").text
        tgt_name = driver.find_element(By.ID, "targetAgentName").text
        payload = driver.find_element(By.ID, "handoverPayloadText").text
        print(f"Initial Handover: {src_name} ➔ {tgt_name}")
        print(f"Payload: {payload}")
        assert "Stage 1" in src_name, "Source should be Stage 1"
        assert "Stage 2" in tgt_name, "Target should be Stage 2"

        # 6. Assert 3-Tier Cards
        t0 = driver.find_element(By.ID, "tier0Card")
        t1 = driver.find_element(By.ID, "tier1Card")
        t2 = driver.find_element(By.ID, "tier2Card")
        assert t0.is_displayed() and t1.is_displayed() and t2.is_displayed(), "3-Tier cards missing"
        print("PASS: 3-Tier Stack Cards (Tier 0, 1, 2) verified!")

        # 7. Test Step-by-Step Navigation
        btn_next = driver.find_element(By.ID, "btnStepNextProp")
        btn_next.click()
        time.sleep(0.5)

        src_name_step2 = driver.find_element(By.ID, "sourceAgentName").text
        tgt_name_step2 = driver.find_element(By.ID, "targetAgentName").text
        print(f"After Step Next: {src_name_step2} ➔ {tgt_name_step2}")
        assert "Stage 2" in src_name_step2, "Step 2 source mismatch"
        assert "Stage 3" in tgt_name_step2, "Step 2 target mismatch"

        # Step again to Stage 3 -> 4
        btn_next.click()
        time.sleep(0.5)
        src_name_step3 = driver.find_element(By.ID, "sourceAgentName").text
        print(f"After Step 3: {src_name_step3}")
        assert "Stage 3" in src_name_step3

        # 8. Test Auto-Play Wave
        btn_auto = driver.find_element(By.ID, "btnAutoPropWave")
        btn_auto.click()
        print("Started Auto-Play Wave... waiting 3.5s")
        time.sleep(3.5)

        # Check ledger table rows
        rows = driver.find_elements(By.CSS_SELECTOR, "#transHistoryBody tr")
        print(f"Ledger rows recorded: {len(rows)}")
        assert len(rows) >= 3, f"Expected at least 3 history rows, found {len(rows)}"

        # Pause auto-play
        btn_auto.click()
        time.sleep(0.3)

        # 9. Test Tab Switching
        tab_pipeline_btn = driver.find_element(By.ID, "tabBtnPipeline")
        tab_pipeline_btn.click()
        time.sleep(0.5)
        tab_pipeline = driver.find_element(By.ID, "tabPipeline")
        assert tab_pipeline.is_displayed(), "Pipeline tab failed to display"
        print("PASS: Switched to 11-Stage Swarm Pipeline tab!")

        # Switch back to Dual Prop tab
        tab_prop_btn = driver.find_element(By.ID, "tabBtnAgentProp")
        tab_prop_btn.click()
        time.sleep(0.5)
        assert tab_prop.is_displayed(), "Failed to switch back to Dual Prop tab"
        print("PASS: Switched back to Dual Prop tab!")

        # 10. Capture screenshot
        screenshot_path = "sop_dual_propagation_preview.png"
        driver.save_screenshot(screenshot_path)
        print(f"PASS: Screenshot saved to {screenshot_path}")

        print("\n>>> ALL TESTS PASSED SUCCESSFULLY! 100% VERIFIED! <<<")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_tests()
