# -*- coding: utf-8 -*-
import sys
import time
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'
URL = "https://api.linkedin.com/v2/ugcPosts"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0"
}

POSTS = [
    {
        "skill": "Skill #2: algorithmic-art",
        "text": """Excited to share the Algorithmic Art Studio: a standalone, HTML-only web app demonstrating Skill #2 — algorithmic-art (Apache 2.0)! 🌀🎨

Following Anthropic's open-source agent skills runbook, this app implements seeded generative p5.js art with real-time AI synthesis:

• 📜 Algorithmic Philosophy Manifesto: Synthesizes computational theory, emergent behavioral laws, and mathematical noise field dynamics.
• 🎨 Live p5.js Canvas Stage: Vector flow fields, quantum wave harmonics, and recursive phyllotaxis with seed exploration (prev/next/random) and parameter tuning.
• ⚡ Dual In-Browser Inference: Runs on Groq LPU (500+ tok/s) with pre-provisioned free token or local WebGPU (WebLLM).
• 💡 Freeform Input: Prompt chips and custom brief input in clean Light Mode.

👉 Live GitHub Pages App:
https://cosmosanalytics.github.io/uat-copilot-local/algorithmic_art_app.html

#AIAgents #GenerativeArt #p5js #WebGPU #Groq #OpenSource #CreativeCoding"""
    },
    {
        "skill": "Skill #3: theme-factory",
        "text": """Excited to share the Theme Factory Studio: a standalone, HTML-only web app demonstrating Skill #3 — theme-factory (Apache 2.0)! 🎨🏷️

Following Anthropic's open-source agent skills runbook, this app provides curated design system palettes, typography pairings, and dynamic theme synthesis:

• 🎨 10 Verified Pre-Set Themes: Ocean Depths, Sunset Boulevard, Forest Canopy, Modern Minimalist, Golden Hour, Arctic Frost, Desert Rose, Tech Innovation, Botanical Garden, Midnight Galaxy.
• 📊 Multi-Artifact Stager: Live previews across Executive Slide Decks, KPI Dashboards, and Strategic Documents.
• ⚡ On-The-Fly Theme Synthesis: Groq LPU (500+ tok/s) & WebGPU generate cohesive color palettes, Google Font pairings, and semantic tokens from freeform briefs.
• 🏷️ Design Token Export: One-click export for CSS Custom Properties (:root), Tailwind CSS, and W3C JSON tokens.

👉 Live GitHub Pages App:
https://cosmosanalytics.github.io/uat-copilot-local/theme_factory_app.html

#AIAgents #DesignSystems #WebDevelopment #TailwindCSS #WebGPU #Groq #OpenSource"""
    }
]

def publish(post):
    payload = {
        "author": MEMBER_URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post["text"]
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    print(f"\nPublishing post for {post['skill']}...")
    res = requests.post(URL, headers=HEADERS, json=payload)
    print(f"Status: {res.status_code}")
    if res.status_code == 201:
        post_id = res.json().get('id')
        print(f"SUCCESS: Post ID = {post_id}")
        return post_id
    else:
        print(f"FAILED: {res.text}")
        return None

def main():
    results = []
    for idx, post in enumerate(POSTS):
        pid = publish(post)
        results.append({"skill": post["skill"], "id": pid})
        if idx < len(POSTS) - 1:
            time.sleep(3)

    print("\n================ SUMMARY ================")
    for r in results:
        print(f"• {r['skill']}: {r['id']}")

if __name__ == "__main__":
    main()
