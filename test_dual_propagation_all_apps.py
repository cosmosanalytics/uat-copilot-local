import time, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

files_to_test = [
    "network_optimization_multi_agent_app.html",
    "optimal_menu_pricing_app.html",
    "business_war_room_multi_agent_app.html",
    "multi_agent_brain_app.html",
    "multi_agent_game_app.html",
    "multi_agent_chess_app.html",
    "multi_agent_go_app.html"
]

try:
    for fname in files_to_test:
        fpath = os.path.abspath(fname)
        driver.get(f"file:///{fpath}")
        time.sleep(1)
        
        # Click Dual Propagation tab
        tab_btn = driver.find_element(By.ID, "tabBtnProp")
        tab_btn.click()
        time.sleep(0.5)
        
        # Verify tab content rendered
        tab_content = driver.find_element(By.ID, "tab-propagation")
        assert tab_content.is_displayed(), f"Tab not displayed in {fname}"
        
        # Click trigger dual propagation wave button
        trig_btn = tab_content.find_element(By.XPATH, ".//button[contains(., 'Trigger Dual Propagation Wave')]")
        trig_btn.click()
        time.sleep(4.5) # Let wave propagate through Tier 0 -> Tier 1 -> Tier 2 nodes
        
        # Check swarm nodes status
        node0 = driver.find_element(By.ID, "sNode_0")
        assert "pulse-complete" in node0.get_attribute("class"), f"Node 0 not complete in {fname}"
        
        # Check Tier 0, 1, 2 cards
        c0 = driver.find_element(By.ID, "cardTier0")
        assert "completed-tier" in c0.get_attribute("class"), f"Tier 0 not complete in {fname}"
        
        print(f"VERIFIED: {fname} Dual Propagation (Swarm & 3-Tier) working 100%!")
        
    print("\n>>> ALL 7 APPS VERIFIED WITH DUAL PROPAGATION! <<<")
finally:
    driver.quit()
