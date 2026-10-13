import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def test_app():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1400,900")

    driver = webdriver.Chrome(options=chrome_options)
    app_path = r"c:\Users\richa\ai-engineering\brain_ai_all_41_functions.html"
    file_url = f"file:///{app_path.replace(os.sep, '/')}"

    print(f"Testing {file_url}...")
    try:
        driver.get(file_url)
        time.sleep(1.0)

        # 1. Title verification
        print(f"[PASS] Title: {driver.title}")
        assert "41" in driver.title

        # 2. Light mode check
        body = driver.find_element(By.TAG_NAME, "body")
        assert "light-mode" in body.get_attribute("class")
        print("[PASS] Light mode active by default")

        # 3. Model selector
        model_select = driver.find_element(By.ID, "model-select")
        options = model_select.find_elements(By.TAG_NAME, "option")
        print(f"[PASS] Model select options: {len(options)}")
        assert len(options) >= 3

        # 4. Count function tags across 6 pillars
        fn_tags = driver.find_elements(By.CLASS_NAME, "fn-tag")
        print(f"[PASS] Found {len(fn_tags)} function tags in map (Expected: 41)")
        assert len(fn_tags) == 41, f"Expected 41 functions, got {len(fn_tags)}"

        # 5. Check categories count
        reactive = driver.find_elements(By.CSS_SELECTOR, ".fn-tag.reactive")
        proactive = driver.find_elements(By.CSS_SELECTOR, ".fn-tag.proactive")
        partly = driver.find_elements(By.CSS_SELECTOR, ".fn-tag.partly")
        notyet = driver.find_elements(By.CSS_SELECTOR, ".fn-tag.notyet")
        research = driver.find_elements(By.CSS_SELECTOR, ".fn-tag.research")

        print(f"[PASS] Categories breakdown: Reactive={len(reactive)}, Proactive={len(proactive)}, Partly={len(partly)}, NotYet={len(notyet)}, Research={len(research)}")
        assert len(reactive) == 21, f"Expected 21 reactive, got {len(reactive)}"
        assert len(proactive) == 7, f"Expected 7 proactive, got {len(proactive)}"
        assert len(partly) == 1, f"Expected 1 partly, got {len(partly)}"
        assert len(notyet) == 7, f"Expected 7 not yet, got {len(notyet)}"
        assert len(research) == 5, f"Expected 5 research, got {len(research)}"

        # 6. Test function selection & inspector update
        insight_btn = driver.find_element(By.ID, "fn-btn-insight")
        insight_btn.click()
        time.sleep(0.3)
        insp_name = driver.find_element(By.ID, "insp-name").text
        assert "Insight" in insp_name
        print(f"[PASS] Inspector updated to: {insp_name}")

        # 7. Execute Live Function Demo
        run_btn = driver.find_element(By.ID, "btn-run-fn")
        run_btn.click()
        time.sleep(0.8)
        log_text = driver.find_element(By.ID, "probe-log").text
        assert "MODULE EXECUTION TRACE" in log_text or "Insight" in log_text
        print("[PASS] Live function demo executed successfully with module trace")

        # 8. Test End-to-End Pipeline Demo
        pipeline_btn = driver.find_element(By.ID, "btn-pipeline-run")
        assert pipeline_btn.is_displayed()
        pipeline_btn.click()
        time.sleep(5.5)
        log_text_pipeline = driver.find_element(By.ID, "probe-log").text
        assert "COGNITIVE CYCLE COMPLETE" in log_text_pipeline
        print("[PASS] Full End-to-End 8-Stage Cognitive Pipeline fired successfully!")

        # 9. Test Multi-Agent Team Mode
        toggle_ma_btn = driver.find_element(By.ID, "btn-toggle-multiagent")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", toggle_ma_btn)
        time.sleep(0.4)
        ma_panel = driver.find_element(By.ID, "multiagent-panel")
        assert ma_panel.is_displayed(), "Multi-agent panel should be visible after toggle"
        print("[PASS] Multi-Agent Society of Mind panel opened")

        # Check 6 agent cards
        agent_cards = driver.find_elements(By.CLASS_NAME, "agent-card")
        assert len(agent_cards) == 6, f"Expected 6 pillar agents, got {len(agent_cards)}"
        print(f"[PASS] All 6 specialized pillar agents present ({len(agent_cards)} agents)")

        # Run multi-agent collaboration
        run_ma_btn = driver.find_element(By.ID, "btn-run-multiagent")
        driver.execute_script("arguments[0].click();", run_ma_btn)
        time.sleep(5.0) # Allow multi-agent session to progress
        chat_bubbles = driver.find_elements(By.CLASS_NAME, "agent-bubble")
        assert len(chat_bubbles) >= 4, f"Expected multi-agent chat bubbles, got {len(chat_bubbles)}"
        print(f"[PASS] Multi-agent collaboration session successfully executed with {len(chat_bubbles)} inter-agent turns!")

        # 10. Check console logs
        logs = driver.get_log("browser")
        severe_errors = [entry for entry in logs if entry["level"] == "SEVERE" and "favicon" not in entry["message"].lower()]
        if severe_errors:
            print(f"[WARN] Severe errors: {severe_errors}")
        else:
            print("[PASS] 0 severe console errors")

        print("\nALL VERIFICATIONS PASSED FOR BRAIN ⇄ AI 41 FUNCTIONS APP!")

    finally:
        driver.quit()

if __name__ == "__main__":
    test_app()
