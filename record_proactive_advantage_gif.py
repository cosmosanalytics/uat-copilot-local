"""
record_proactive_advantage_gif.py
Records a high-quality animated GIF of the 4 use cases running side by side
in agent_extended_cognitive_pyramid.html to showcase the advantages of the proactive system.
"""

import os
import sys
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

OUTPUT_GIF = "proactive_system_advantages_recording.gif"
FRAME_DIR = "gif_frames_proactive"

def record_gif():
    os.makedirs(FRAME_DIR, exist_ok=True)
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1280,920")
    chrome_options.add_argument("--force-device-scale-factor=1")

    driver = webdriver.Chrome(options=chrome_options)
    captured_frames = []

    try:
        app_path = os.path.abspath("agent_extended_cognitive_pyramid.html")
        driver.get(f"file:///{app_path}")
        time.sleep(1.0)

        # 1. Switch to Advantage Benchmark Tab via JS
        tab_btn = driver.find_element(By.ID, "tab-btn-benchmark")
        driver.execute_script("arguments[0].click();", tab_btn)
        time.sleep(0.4)

        # Scroll to benchmark view
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.3)

        frame_idx = 0

        # Cycle through all 4 test cases
        test_cases = [
            ("deadlock", "tc-deadlock"),
            ("token", "tc-token"),
            ("swarm", "tc-swarm"),
            ("plasticity", "tc-plasticity")
        ]

        for tc_key, tc_id in test_cases:
            print(f"Recording Use Case: {tc_key}...")

            # Select test case via JS click to avoid sticky header interception
            card_el = driver.find_element(By.ID, tc_id)
            driver.execute_script("arguments[0].click();", card_el)
            time.sleep(0.3)

            # Frame 0: Idle state
            fpath = os.path.join(FRAME_DIR, f"frame_{frame_idx:03d}_{tc_key}_idle.png")
            driver.save_screenshot(fpath)
            captured_frames.append((fpath, 600))
            frame_idx += 1

            # Click Run Side-by-Side Duel via JS
            run_btn = driver.find_element(By.ID, "run-race-btn")
            driver.execute_script("arguments[0].click();", run_btn)

            # Capture progression frames as duel runs
            for step_i in range(6):
                time.sleep(0.65)
                fpath = os.path.join(FRAME_DIR, f"frame_{frame_idx:03d}_{tc_key}_step{step_i}.png")
                driver.save_screenshot(fpath)
                captured_frames.append((fpath, 400))
                frame_idx += 1

            # Final completed frame for this test case
            time.sleep(0.8)
            fpath = os.path.join(FRAME_DIR, f"frame_{frame_idx:03d}_{tc_key}_final.png")
            driver.save_screenshot(fpath)
            captured_frames.append((fpath, 1200))
            frame_idx += 1

        # Scroll down to capture the scorecard banner
        scorecard = driver.find_element(By.CLASS_NAME, "scorecard-banner")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", scorecard)
        time.sleep(0.5)

        # Final Summary Frame
        fpath = os.path.join(FRAME_DIR, f"frame_{frame_idx:03d}_scorecard.png")
        driver.save_screenshot(fpath)
        captured_frames.append((fpath, 2400)) # 2.4s hold on scorecard

        print(f"Captured {len(captured_frames)} raw frames.")

        # Build GIF using PIL
        pil_images = []
        durations = []

        target_size = (960, 690)

        for fpath, dur in captured_frames:
            img = Image.open(fpath).convert("RGB")
            img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
            img_quant = img_resized.quantize(colors=128, method=Image.Resampling.LANCZOS)
            pil_images.append(img_quant)
            durations.append(dur)

        print(f"Compiling {OUTPUT_GIF}...")
        pil_images[0].save(
            OUTPUT_GIF,
            save_all=True,
            append_images=pil_images[1:],
            duration=durations,
            loop=0,
            optimize=True
        )

        gif_size_mb = os.path.getsize(OUTPUT_GIF) / (1024 * 1024)
        print(f"SUCCESS: {OUTPUT_GIF} created successfully! File size: {gif_size_mb:.2f} MB")

    finally:
        driver.quit()

if __name__ == "__main__":
    record_gif()
