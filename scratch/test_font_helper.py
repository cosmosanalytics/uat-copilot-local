import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

FONT_BOLD_24 = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 24)
FONT_BOLD_18 = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 18)
FONT_BOLD_14 = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 14)
FONT_REG_14 = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 14)
FONT_REG_12 = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 12)

def annotate_image(im_path, step_tag, title, subtitle, callouts=[]):
    im = Image.open(im_path).convert('RGBA')
    w, h = im.size
    
    # Overlay for translucent elements
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    draw = ImageDraw.Draw(im)

    # 1. Top Banner (85px)
    banner_h = 85
    draw.rectangle([(0, 0), (w, banner_h)], fill=(15, 23, 42))
    # Accent color line
    draw.rectangle([(0, banner_h - 5), (w, banner_h)], fill=(16, 185, 129))

    # Badge Pill
    badge_w = 170
    draw.rounded_rectangle([(24, 14), (24 + badge_w, 38)], radius=6, fill=(30, 41, 59), outline=(99, 102, 241), width=1)
    draw.text((34, 17), step_tag, font=FONT_BOLD_12, fill=(129, 140, 248))

    # Title & Subtitle
    draw.text((24 + badge_w + 16, 12), title, font=FONT_BOLD_20, fill=(255, 255, 255))
    draw.text((24, 48), subtitle, font=FONT_REG_14, fill=(203, 213, 225))

    # 2. In-Scene Callout Overlays
    for c in callouts:
        cx, cy, cw, ch, c_title, c_text, c_color, c_border = c
        # Background box
        draw_overlay.rounded_rectangle([(cx, cy), (cx + cw, cy + ch)], radius=10, fill=c_color, outline=c_border, width=2)
        draw.text((cx + 14, cy + 10), c_title, font=FONT_BOLD_14, fill=(255, 255, 255))
        draw.text((cx + 14, cy + 32), c_text, font=FONT_REG_12, fill=(241, 245, 249))

    # Composite
    final_im = Image.alpha_composite(im, overlay).convert('RGB')
    return final_im

print("Helper ready")
