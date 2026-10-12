# -*- coding: utf-8 -*-
"""
record_sop_dual_propagation_gif.py
Records an animated GIF demonstrating both:
1. Horizontal propagation over multi-agents (11 stages in Demand, Supply, Control pods)
2. Vertical propagation over 3 tiers (Tier 0 AWS -> Tier 1 Kernel -> Tier 2 Swarm)
"""

import os
import sys
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

OUTPUT_GIF = "sop_dual_propagation_recording.gif"
FRAME_DIR = "gif_frames_sop"

def capture_gif():
    os.makedirs(FRAME_DIR, exist_ok=True)
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1400,1050")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    frames = []

    try:
        app_path = os.path.abspath("sop_multi_agent_swarm_app.html")
        driver.get(f"file:///{app_path}")
        time.sleep(1.2)

        # Ensure propSpeedMs is fast enough for smooth capture
        driver.execute_script("propSpeedMs = 400;")

        # Focus element
        prop_card = driver.find_element(By.CLASS_NAME, "prop-engine-card")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'start'});", prop_card)
        time.sleep(0.3)

        # Steps to record: we want to showcase the key stages:
        # Step 1 (Stage 1 -> 2: Baseline Rollup)
        # Step 3 (Stage 3 -> 4: Consensus Uplift)
        # Step 5 (Stage 5 -> 6: Cross-Pod Liaison Bridge #1 Demand to Supply)
        # Step 7 (Stage 7 -> 8: BOM Explode to Firming)
        # Step 9 (Stage 9 -> 10: Cross-Pod Liaison Bridge #2 Supply to Control)
        # Step 10 (Stage 10 -> 11: Executive Sign-off & WORM Commit)
        target_steps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        frame_idx = 0

        for step_num in target_steps:
            # Set handover step
            driver.execute_script(f"""
                currentHandoverIndex = {step_num - 1};
                renderCurrentHandoverUI();
            """)
            time.sleep(0.1)

            # Sub-frame A: Tier 0 AWS active
            driver.execute_script("""
                const t0 = document.getElementById('tier0Card');
                const t1 = document.getElementById('tier1Card');
                const t2 = document.getElementById('tier2Card');
                const d0 = document.getElementById('tier0Dot');
                const d1 = document.getElementById('tier1Dot');
                const d2 = document.getElementById('tier2Dot');
                t0.classList.add('pulse-active'); d0.classList.add('active-pulse');
                t1.classList.remove('pulse-active'); d1.classList.remove('active-pulse');
                t2.classList.remove('pulse-active'); d2.classList.remove('active-pulse');
                document.getElementById('tierWaveStatusText').textContent = '⚡ TIER 0 AWS DYNAMODB CAS LOCK & WORM ACTIVE (STEP ' + (currentHandoverIndex + 1) + ')';
            """)
            time.sleep(0.15)
            fpath_a = os.path.join(FRAME_DIR, f"frame_{frame_idx:03d}_t0.png")
            driver.save_screenshot(fpath_a)
            frames.append((fpath_a, 350)) # 350ms duration
            frame_idx += 1

            # Sub-frame B: Tier 1 Kernel active
            driver.execute_script("""
                const t0 = document.getElementById('tier0Card');
                const t1 = document.getElementById('tier1Card');
                const t2 = document.getElementById('tier2Card');
                const d0 = document.getElementById('tier0Dot');
                const d1 = document.getElementById('tier1Dot');
                const d2 = document.getElementById('tier2Dot');
                t0.classList.remove('pulse-active'); d0.classList.remove('active-pulse');
                t1.classList.add('pulse-active'); d1.classList.add('active-pulse');
                t2.classList.remove('pulse-active'); d2.classList.remove('active-pulse');
                document.getElementById('tierWaveStatusText').textContent = '⚡ TIER 1 AGENT OS KERNEL: CEDAR GATE & HASH CHAIN (STEP ' + (currentHandoverIndex + 1) + ')';
            """)
            time.sleep(0.15)
            fpath_b = os.path.join(FRAME_DIR, f"frame_{frame_idx:03d}_t1.png")
            driver.save_screenshot(fpath_b)
            frames.append((fpath_b, 350))
            frame_idx += 1

            # Sub-frame C: Tier 2 Swarm active
            driver.execute_script("""
                const t0 = document.getElementById('tier0Card');
                const t1 = document.getElementById('tier1Card');
                const t2 = document.getElementById('tier2Card');
                const d0 = document.getElementById('tier0Dot');
                const d1 = document.getElementById('tier1Dot');
                const d2 = document.getElementById('tier2Dot');
                t0.classList.remove('pulse-active'); d0.classList.remove('active-pulse');
                t1.classList.remove('pulse-active'); d1.classList.remove('active-pulse');
                t2.classList.add('pulse-active'); d2.classList.add('active-pulse');
                document.getElementById('tierWaveStatusText').textContent = '⚡ TIER 2 SWARM LATTICE: WHITEBOARD & QUORUM CERTIFIED (STEP ' + (currentHandoverIndex + 1) + ')';
            """)
            time.sleep(0.15)
            fpath_c = os.path.join(FRAME_DIR, f"frame_{frame_idx:03d}_t2.png")
            driver.save_screenshot(fpath_c)
            frames.append((fpath_c, 450))
            frame_idx += 1

        print(f"Captured {len(frames)} frames. Compiling GIF...")

        # Process and compile GIF
        pil_images = []
        durations = []

        # Target width and height to optimize GIF file size and clarity
        target_w = 1100

        for fpath, dur in frames:
            img = Image.open(fpath)
            # Crop to relevant top area of UI containing Header, Pods, Mesh, Showcase, and 3-Tier Grid
            # The canvas height is 1050, let's crop top 0 to 920
            w, h = img.size
            crop_box = (0, 0, w, min(h, 920))
            cropped = img.crop(crop_box)
            # Resize proportionally
            ratio = target_w / float(cropped.size[0])
            target_h = int(float(cropped.size[1]) * float(ratio))
            resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
            # Convert to adaptive palette with dithering for high visual fidelity
            paletted = resized.convert("P", palette=Image.Palette.ADAPTIVE, colors=128)
            pil_images.append(paletted)
            durations.append(dur)

        # Save GIF
        pil_images[0].save(
            OUTPUT_GIF,
            save_all=True,
            append_images=pil_images[1:],
            duration=durations,
            loop=0,
            optimize=True
        )

        file_size_mb = os.path.getsize(OUTPUT_GIF) / (1024 * 1024)
        print(f"SUCCESS: GIF generated at {OUTPUT_GIF} ({file_size_mb:.2f} MB)")

    finally:
        driver.quit()

if __name__ == "__main__":
    capture_gif()
