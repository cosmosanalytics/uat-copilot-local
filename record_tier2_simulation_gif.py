# -*- coding: utf-8 -*-
"""
record_tier2_simulation_gif.py
Records a high-quality GIF of multi_agent_system_studio_app.html showing both:
1. Bottom-up Multi-Tier Propagation (Tier 0 Cloud Primitives -> Tier 1 Kernel OS -> Tier 2 Swarm Governance)
2. Small-World Watts-Strogatz Topology Propagation (golden packet pulses traveling across inter-cluster liaison bridges)
Captures successive frames using Selenium Headless Chrome and compiles into an optimized animated GIF with Pillow.
"""

import os
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

GIF_OUTPUT_PATH = "tier2_swarm_and_small_world_propagation.gif"

def record_gif():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1360,940')

    driver = webdriver.Chrome(options=chrome_options)
    app_url = 'file:///' + os.path.abspath('multi_agent_system_studio_app.html').replace('\\', '/')
    driver.get(app_url)
    time.sleep(1.5)

    frames = []

    # Frame 0: Idle State on Unified All-Tiers Matrix tab
    print("Capturing Frame 0: Initial Idle State...")
    png_bytes = driver.get_screenshot_as_png()
    img = Image.open(io_bytes := io_stream(png_bytes))
    frames.append(img.copy())

    # Click the Coordinate Swarm button
    dispatch_btn = driver.find_element(By.ID, 'btnDispatchSwarm')
    driver.execute_script("arguments[0].click();", dispatch_btn)
    print("Swarm execution triggered!")

    # Capture frames over ~4.5 seconds to capture all stages and packet pulses
    start_time = time.time()
    frame_interval = 0.16  # ~6 frames per second
    target_duration = 4.8

    while time.time() - start_time < target_duration:
        png_bytes = driver.get_screenshot_as_png()
        img = Image.open(io_stream(png_bytes))
        frames.append(img.copy())
        time.sleep(frame_interval)

    # Capture final settled frame
    time.sleep(0.5)
    png_bytes = driver.get_screenshot_as_png()
    frames.append(Image.open(io_stream(png_bytes)).copy())
    driver.quit()

    print(f"Total frames captured: {len(frames)}. Compiling GIF...")

    # Resize frames slightly for optimal file size and crisp playback
    resized_frames = []
    for f in frames:
        # Resize to 960x664 for crisp email / Slack / web compatibility
        rf = f.resize((960, 664), Image.Resampling.LANCZOS).convert('RGB')
        # Quantize to 128 colors with dithering for compact GIF
        qf = rf.quantize(colors=128)
        resized_frames.append(qf)

    # Save as animated GIF
    resized_frames[0].save(
        GIF_OUTPUT_PATH,
        save_all=True,
        append_images=resized_frames[1:],
        duration=180,  # 180ms per frame
        loop=0,
        optimize=True
    )

    size_mb = os.path.getsize(GIF_OUTPUT_PATH) / (1024 * 1024)
    print(f"Successfully generated {GIF_OUTPUT_PATH} ({size_mb:.2f} MB)")

def io_stream(b):
    import io
    return io.BytesIO(b)

if __name__ == "__main__":
    record_gif()
