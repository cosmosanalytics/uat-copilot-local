# -*- coding: utf-8 -*-
"""
Captures Ultra-High-Resolution (device_scale_factor=2.5) screenshots for all 4 examples.
"""
import sys
import os
from playwright.sync_api import sync_playwright
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

def capture_all_hi_res():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome')
        context = browser.new_context(
            viewport={'width': 1680, 'height': 950},
            device_scale_factor=2.5
        )
        page = context.new_page()

        abs_path = os.path.abspath('truth_policy_flowchart_studio.html').replace('\\', '/')
        page.goto(f'file:///{abs_path}')
        page.wait_for_timeout(1500)

        # -------------------------------------------------------------------
        # EXAMPLE 1: ENTERPRISE IT SSO
        # -------------------------------------------------------------------
        print("\n--- Capturing Example 1: Enterprise IT SSO (Hi-Res) ---")
        page.locator("#tabBtn1").click()
        page.wait_for_timeout(300)
        page.locator("button:has-text('Enterprise IT SSO')").click()
        page.wait_for_timeout(800)
        page.locator("#stepPanel1").screenshot(path="scratch/app8_it_security_step1.png")
        print("  -> Captured scratch/app8_it_security_step1.png")

        page.locator("#tabBtn2").click()
        page.wait_for_timeout(800)
        page.locator("#stepPanel2").screenshot(path="scratch/app8_it_security_flowchart.png")
        print("  -> Captured scratch/app8_it_security_flowchart.png")

        # -------------------------------------------------------------------
        # EXAMPLE 2: FINTECH DISPUTE INTAKE
        # -------------------------------------------------------------------
        print("\n--- Capturing Example 2: FinTech Dispute Intake (Hi-Res) ---")
        page.locator("#tabBtn1").click()
        page.wait_for_timeout(300)
        page.locator("button:has-text('FinTech Dispute Intake')").click()
        page.wait_for_timeout(800)
        page.locator("#stepPanel1").screenshot(path="scratch/app8_fintech_dispute_step1.png")
        print("  -> Captured scratch/app8_fintech_dispute_step1.png")

        page.locator("#tabBtn2").click()
        page.wait_for_timeout(800)
        page.locator("#stepPanel2").screenshot(path="scratch/app8_fintech_dispute_flowchart.png")
        print("  -> Captured scratch/app8_fintech_dispute_flowchart.png")

        # -------------------------------------------------------------------
        # EXAMPLE 3: CLOUD DEVOPS CANARY RELEASE
        # -------------------------------------------------------------------
        print("\n--- Capturing Example 3: Cloud DevOps Canary Release (Hi-Res) ---")
        page.locator("#tabBtn1").click()
        page.wait_for_timeout(300)
        page.locator("button:has-text('Cloud Canary Release')").click()
        page.wait_for_timeout(800)
        page.locator("#stepPanel1").screenshot(path="scratch/app8_cloud_devops_step1.png")
        print("  -> Captured scratch/app8_cloud_devops_step1.png")

        page.locator("#tabBtn2").click()
        page.wait_for_timeout(800)
        page.locator("#stepPanel2").screenshot(path="scratch/app8_cloud_devops_flowchart.png")
        print("  -> Captured scratch/app8_cloud_devops_flowchart.png")

        # -------------------------------------------------------------------
        # EXAMPLE 4: NARRATIVE LITERATURE (WHERE THE MOUNTAIN MEETS THE MOON)
        # -------------------------------------------------------------------
        print("\n--- Capturing Example 4: Literature Where the Mountain Meets the Moon (Hi-Res) ---")
        page.locator("#tabBtn1").click()
        page.wait_for_timeout(300)
        
        # Populate input fields
        page.locator("#customDocTitleInput").fill("Where Mountain Meets Moon Wbna33436633")
        page.locator("#customWebAddressInput").fill("https://www.today.com/popculture/where-mountain-meets-moon-wbna33436633")
        page.locator("#customDocTextInput").fill("""Far away from here, following the Jade River, there was once a black mountain that cut into the sky like a jagged piece of rough metal. The villagers called it Fruitless Mountain because nothing grew on it and birds and animals did not rest there.

Crowded in the corner of where Fruitless Mountain and the Jade River met was a village that was a shade of faded brown. This was because the land around the village was hard and poor. To coax rice out of the stubborn land, the fields had to be flooded with water. The villagers had to tramp in the mud, bending and stooping and planting day after day. Working in the mud so much made it spread everywhere and the hot sun dried it onto their clothes and hair and homes. Over time, everything in the village had become the dull color of dried mud.

One of the houses in this village was so small that its wood boards, held together by the roof, made one think of a bunch of matches tied with a piece of twine. Inside, there was barely enough room for three people to sit around the table — which was lucky because only three people lived there. One of them was a young girl called Minli.

Minli was not brown and dull like the rest of the village. She had glossy black hair with pink cheeks, shining eyes always eager for adventure, and a fast smile that flashed from her face. When people saw her lively and impulsive spirit, they thought her name, which meant quick thinking, suited her well. "Too well," her mother sighed, as Minli had a habit of quick acting as well.""")
        page.wait_for_timeout(300)
        
        # Click Synthesize button
        page.locator("button[onclick*='synthesizeFromCustomInputs']").click()
        page.wait_for_timeout(1000)

        # Step 1: Populated Intake (active right now)
        page.locator("#stepPanel1").screenshot(path="scratch/verified_today_com_step1.png")
        print("  -> Captured scratch/verified_today_com_step1.png")

        # Transition to Step 2
        page.locator("#tabBtn2").click()
        page.wait_for_timeout(1000)

        # Step 2: High-res Flowchart DAG
        page.locator("#stepPanel2").screenshot(path="scratch/verified_flowchart_expanded_big.png")
        print("  -> Captured scratch/verified_flowchart_expanded_big.png")

        browser.close()
        print("\nAll 8 screenshots successfully captured at 2.5x Retina resolution!")

if __name__ == '__main__':
    capture_all_hi_res()
