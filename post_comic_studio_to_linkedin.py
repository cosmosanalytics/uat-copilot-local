# -*- coding: utf-8 -*-
import sys
import requests
import json

# Force stdout to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'
PREVIOUS_POST_URN = 'urn:li:share:7513925671245594624'

LIVE_PAGE_LINK = 'https://cosmosanalytics.github.io/uat-copilot-local/comic_webllm_studio.html'
TITLE = 'ComicCrafter AI: In-Browser Page-by-Page Comic Studio (WebLLM + WebGPU)'

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
    'X-Restli-Protocol-Version': '2.0.0',
    'LinkedIn-Version': '202609'
}

# 1. Delete previous post containing the file link
print(f"Deleting previous post {PREVIOUS_POST_URN}...")
del_url = f"https://api.linkedin.com/rest/posts/{requests.utils.quote(PREVIOUS_POST_URN)}"
del_res = requests.delete(del_url, headers=headers)
print(f"Delete status: {del_res.status_code}")

raw_text = """ComicCrafter AI: In-Browser Page-by-Page Comic Studio (WebGPU + WebLLM) 🎨📖⚡

Can you direct and generate an entire multi-page comic book right inside your browser without any server or cloud API costs?

I built ComicCrafter AI — a standalone, single-file web studio where you direct comics page-by-page using natural language prompts, powered 100% locally on your device GPU via WebGPU and @mlc-ai/web-llm.

Key Highlights:
• Page-by-Page Storytelling: Generate Page 1, Page 2, Page 3... with persistent character memory, ongoing plot continuity, and cliffhanger pacing.
• Procedural Comic Art Engine: Procedural SVG/Canvas rendering with authentic Ben-Day halftone dots, radial action speedlines, dramatic skylines, speech balloons with tails, narration boxes, and 3D onomatopoeia SFX (KRA-KOOM!, BZZZT!).
• Flexible Page Layouts: Classic 4-panel grid, dynamic 5-panel action splash, manga 6-panel flow, cinematic widescreen, and vertical webtoon.
• 100% Client-Side & Zero Cost: In-browser local LLM inference (Qwen2.5 / SmolLM2 / Llama 3.2) running in WebGPU compute shaders — zero data leaves your machine.
• Live Inspector & Export: Interactive panel editing, 1-click high-res PNG export, print/PDF layout, and full JSON project save/load.

🔗 Live Web App (GitHub Pages):
https://cosmosanalytics.github.io/uat-copilot-local/comic_webllm_studio.html

#WebGPU #WebLLM #GenerativeAI #OpenSource #CreativeTech #GameDev #JavaScript #AIArt #Comics"""

def escape_little_text(text: str) -> str:
    reserved = ['\\', '|', '{', '}', '@', '[', ']', '(', ')', '<', '>', '*', '_', '~']
    for ch in reserved:
        text = text.replace(ch, '\\' + ch)
    return text

escaped_text = escape_little_text(raw_text)

post_url = 'https://api.linkedin.com/rest/posts'
post_payload = {
    'author': MEMBER_URN,
    'commentary': escaped_text,
    'visibility': 'PUBLIC',
    'distribution': {
        'feedDistribution': 'MAIN_FEED',
        'targetEntities': [],
        'thirdPartyDistributionChannels': []
    },
    'content': {
        'article': {
            'source': LIVE_PAGE_LINK,
            'title': TITLE,
            'description': 'Create multi-page comic books page-by-page using natural language directives powered locally by WebLLM and WebGPU shaders.'
        }
    },
    'lifecycleState': 'PUBLISHED',
    'isReshareDisabledByAuthor': False
}

print(f"Publishing updated post with only the live link to LinkedIn...")
response = requests.post(post_url, headers=headers, json=post_payload)

print(f"Status Code: {response.status_code}")
if response.status_code in (201, 200):
    post_id = response.headers.get('x-restli-id', 'Created')
    print(f"Success! Post published.")
    print(f"Post ID: {post_id}")
    print(f"LinkedIn URL: https://www.linkedin.com/feed/update/{post_id}/")
else:
    print(f"Response Error: {response.text}")
