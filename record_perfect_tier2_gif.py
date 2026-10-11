# -*- coding: utf-8 -*-
"""
record_perfect_tier2_gif.py
Records an animated GIF showing BOTH:
1. Bottom-up Tier Propagation across all 3 tiers simultaneously (Tier 0 Cloud Hardware -> Tier 1 Kernel OS -> Tier 2 Watts-Strogatz Swarm).
2. Large-format Watts-Strogatz Small-World Topology propagation showing the 3 specialist pods (Finance, Compliance, Operations) and golden packet pulses traversing the inter-cluster liaison bridges.
"""

import os
import time
import io
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

GIF_OUTPUT_PATH = "tier2_swarm_and_small_world_propagation.gif"

def record():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    # Use window size where all 3 tiers fit on screen
    chrome_options.add_argument('--window-size=1440,1220')

    driver = webdriver.Chrome(options=chrome_options)
    app_url = 'file:///' + os.path.abspath('multi_agent_system_studio_app.html').replace('\\', '/')
    driver.get(app_url)
    time.sleep(1.2)

    frames = []

    def capture_frame():
        png = driver.get_screenshot_as_png()
        return Image.open(io.BytesIO(png))

    # --- PART 1: Unified All-Tiers Matrix (Bottom-Up Tier Propagation) ---
    print("Recording Part 1: Bottom-up Tier Propagation across Tiers 0, 1, 2...")
    frames.append(capture_frame())

    # Click Coordinate Multi-Agent Swarm
    btn = driver.find_element(By.ID, 'btnDispatchSwarm')
    driver.execute_script("arguments[0].click();", btn)

    # Capture tier propagation as Tier 0 -> Tier 1 -> Tier 2 light up
    # Total duration ~3.6s, capture ~12 frames
    t0 = time.time()
    while time.time() - t0 < 3.8:
        frames.append(capture_frame())
        time.sleep(0.28)

    # --- PART 2: Watts-Strogatz Small-World Topology Tab ---
    print("Recording Part 2: Watts-Strogatz Small-World Network & Packet Propagation...")
    tab_topo = driver.find_element(By.ID, 'tabBtnTopology')
    driver.execute_script("arguments[0].click();", tab_topo)
    time.sleep(0.3)
    frames.append(capture_frame())

    # Trigger explicit packet animation across the small-world shortcut bridges
    driver.execute_script("animateLiaisonPackets(2400);")
    
    # Capture packets traveling across the gold liaison lines
    t1 = time.time()
    while time.time() - t1 < 2.6:
        frames.append(capture_frame())
        time.sleep(0.18)

    driver.quit()
    print(f"Captured {len(frames)} frames. Processing and optimizing GIF...")

    # Process and crop/resize frames
    # Let's crop to the main interactive area (ignoring excess whitespace at bottom/margins)
    # or resize to a crisp resolution (e.g. 1024x720 or 960x680)
    resized = []
    for idx, f in enumerate(frames):
        # Resize smoothly
        rf = f.resize((960, 680), Image.Resampling.LANCZOS).convert('RGB')
        qf = rf.quantize(colors=128)
        resized.append(qf)

    # Save animated GIF
    resized[0].save(
        GIF_OUTPUT_PATH,
        save_all=True,
        append_images=resized[1:],
        duration=220,  # ~4.5 fps for smooth, easily readable playback
        loop=0,
        optimize=True
    )

    size_mb = os.path.getsize(GIF_OUTPUT_PATH) / (1024 * 1024)
    print(f"Successfully generated {GIF_OUTPUT_PATH} ({size_mb:.2f} MB, {len(resized)} frames)")

if __name__ == '__main__':
    record()
