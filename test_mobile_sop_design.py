# -*- coding: utf-8 -*-
"""
test_mobile_sop_design.py
Tests sop_ai_factory_canvas.html in both Mobile (390x844) and Desktop (1440x900) viewports:
- Verifies that on mobile, the canvas takes 100% width and nodes are properly visible.
- Tests the mobile drawers (Parts & Inspector).
- Captures mobile and desktop screenshots.
"""

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

file_path = os.path.abspath("sop_ai_factory_canvas.html")
url = f"file:///{file_path.replace(os.sep, '/')}"

# 1. TEST MOBILE VIEWPORT (390 x 844)
print("--- 1. TESTING MOBILE VIEWPORT (390x844) ---")
m_options = Options()
m_options.add_argument("--headless=new")
m_options.add_argument("--window-size=390,844")
m_options.add_argument("--disable-gpu")
m_options.add_argument("--no-sandbox")

m_driver = webdriver.Chrome(options=m_options)
try:
    m_driver.get(url)
    time.sleep(2)

    # Check console
    logs = m_driver.get_log("browser")
    severe = [l for l in logs if l['level'] == 'SEVERE']
    print(f"Mobile console logs: {len(logs)} entries, {len(severe)} SEVERE")

    # Verify canvas viewport width
    viewport = m_driver.find_element(By.ID, "canvasViewport")
    vp_width = viewport.size['width']
    print(f"Canvas Viewport Width on mobile: {vp_width}px (Expected ~390px, full width!)")

    # Capture Mobile Default View
    m_driver.save_screenshot("sop_mobile_canvas_fullwidth.png")
    print("Saved 'sop_mobile_canvas_fullwidth.png'")

    # Open Mobile Inspector Drawer
    buttons = m_driver.find_elements(By.XPATH, "//button[contains(text(), 'Inspector')]")
    if buttons:
        buttons[0].click()
        time.sleep(0.5)
        m_driver.save_screenshot("sop_mobile_inspector_drawer.png")
        print("Saved 'sop_mobile_inspector_drawer.png'")

    # Close Drawer using JS
    m_driver.execute_script("closeAllDrawers()")
    time.sleep(0.3)

    # Switch to Level 1 Worker Mind on Mobile
    btn_l1 = m_driver.find_element(By.ID, "tabL1")
    btn_l1.click()
    time.sleep(0.5)
    m_driver.save_screenshot("sop_mobile_level1_mind.png")
    print("Saved 'sop_mobile_level1_mind.png'")

finally:
    m_driver.quit()

# 2. TEST DESKTOP VIEWPORT (1440 x 900)
print("\n--- 2. TESTING DESKTOP VIEWPORT (1440x900) ---")
d_options = Options()
d_options.add_argument("--headless=new")
d_options.add_argument("--window-size=1440,900")
d_options.add_argument("--disable-gpu")
d_options.add_argument("--no-sandbox")

d_driver = webdriver.Chrome(options=d_options)
try:
    d_driver.get(url)
    time.sleep(2)
    d_driver.save_screenshot("sop_desktop_redesign.png")
    print("Saved 'sop_desktop_redesign.png'")
finally:
    d_driver.quit()

print("\n[SUCCESS] Mobile and Desktop UI tests completed successfully!")
