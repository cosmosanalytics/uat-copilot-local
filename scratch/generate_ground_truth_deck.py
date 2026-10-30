# -*- coding: utf-8 -*-
"""
Builds an executive-grade, graphical, simple, intuitive, and fun PowerPoint deck:
"Capturing World Invariants: The Foundation of Ground Truth"
Featuring 4 detailed real-world examples with embedded high-resolution screenshots.
"""
import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

sys.stdout.reconfigure(encoding='utf-8')

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette (Crisp Light Theme)
BG_COLOR = RGBColor(255, 255, 255)
NAVY_PRIMARY = RGBColor(15, 23, 42)       # Slate 900
BLUE_ACCENT = RGBColor(2, 132, 199)       # Sky 600
TEXT_MUTED = RGBColor(100, 116, 139)      # Slate 500
BORDER_LIGHT = RGBColor(226, 232, 240)    # Slate 200
CARD_BG = RGBColor(248, 250, 252)         # Slate 50
GREEN_EMERALD = RGBColor(16, 185, 129)    # Emerald 500
AMBER_WARM = RGBColor(245, 158, 11)       # Amber 500
RED_TRIPWIRE = RGBColor(239, 68, 68)      # Red 500
PURPLE_LIT = RGBColor(139, 92, 246)       # Purple 500

def set_slide_background(slide, color=BG_COLOR):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, category="GROUNDTRUTH ARCHITECTURE PRINCIPLES", subtitle=None):
    # Category Pill
    pill_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8), Inches(0.35))
    tf_p = pill_box.text_frame
    tf_p.word_wrap = True
    p_cat = tf_p.paragraphs[0]
    p_cat.text = f"📘 {category.upper()}"
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = BLUE_ACCENT
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11), Inches(0.65))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_title = tf_t.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY_PRIMARY

    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.5), Inches(0.35))
        tf_s = sub_box.text_frame
        tf_s.word_wrap = True
        p_sub = tf_s.paragraphs[0]
        p_sub.text = subtitle
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = TEXT_MUTED

# ==========================================
# SLIDE 1: TITLE SLIDE
# ==========================================
slide1 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide1)

# Main Title Card
card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.0), Inches(11.733), Inches(5.5))
card1.fill.solid()
card1.fill.fore_color.rgb = RGBColor(248, 250, 252)
card1.line.color.rgb = RGBColor(203, 213, 225)
card1.line.width = Pt(1.5)

tf1 = card1.text_frame
tf1.word_wrap = True
tf1.vertical_anchor = MSO_ANCHOR.MIDDLE

p = tf1.paragraphs[0]
p.text = "📘 GROUNDTRUTH AI ENGINEERING"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = BLUE_ACCENT
p.alignment = PP_ALIGN.CENTER

p2 = tf1.add_paragraph()
p2.text = "Capturing World Invariants:"
p2.font.size = Pt(38)
p2.font.bold = True
p2.font.color.rgb = NAVY_PRIMARY
p2.alignment = PP_ALIGN.CENTER

p3 = tf1.add_paragraph()
p3.text = "The Foundation of True Ground Truth"
p3.font.size = Pt(34)
p3.font.bold = True
p3.font.color.rgb = BLUE_ACCENT
p3.alignment = PP_ALIGN.CENTER

p4 = tf1.add_paragraph()
p4.text = "\nWhy AI Agents Fail in the Real World — and How Root Invariants Turn Hallucination into Deterministic Reliability."
p4.font.size = Pt(15)
p4.font.color.rgb = TEXT_MUTED
p4.alignment = PP_ALIGN.CENTER

p5 = tf1.add_paragraph()
p5.text = "\n4 Real-World Case Studies: Enterprise Security • FinTech AML • Cloud DevOps • Narrative Literature"
p5.font.size = Pt(12)
p5.font.bold = True
p5.font.color.rgb = RGBColor(71, 85, 105)
p5.alignment = PP_ALIGN.CENTER

# ==========================================
# SLIDE 2: THE CORE PRINCIPLES
# ==========================================
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide2)
add_header(slide2, "The Core Principle: What is a World Invariant?", 
           subtitle="Understanding why traditional prompting hallucinates and how ground truth anchors agent execution.")

cols_data = [
    ("🚫 Rule 1: Never Hallucinate Constants", 
     "If a source (like Wikipedia) defines an optimization formula algebraically as J = sum(w*(r-x)^2), DO NOT invent a fake 42.0 kPa ceiling.\n\nGround truth means exact fidelity: keep unspecified bounds algebraic and extract ONLY what exists.",
     RED_TRIPWIRE, RGBColor(254, 242, 242)),
    ("⚖️ Rule 2: World Physics != Agent Strategy", 
     "World Invariants are what the ENVIRONMENT enforces (gravity, token expiration, barren soil).\n\nAgent Policies are choices the actor makes. Policies can bend; world physics never bend for any prompt.",
     BLUE_ACCENT, RGBColor(240, 249, 255)),
    ("🛑 Rule 3: Every Invariant Needs a Tripwire", 
     "An invariant is useless as passive prose. It must be wired into the Directed Acyclic Graph (DAG) as a hard circuit breaker.\n\nIf state telemetry crosses the boundary, execution freezes instantly into safe fallback.",
     GREEN_EMERALD, RGBColor(236, 253, 245))
]

for idx, (title, desc, b_color, bg_color) in enumerate(cols_data):
    left = Inches(0.8 + idx * 4.0)
    card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.8), Inches(3.75), Inches(4.8))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = b_color
    card.line.width = Pt(1.5)
    
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = b_color
    
    p_body = tf.add_paragraph()
    p_body.text = f"\n{desc}"
    p_body.font.size = Pt(11.5)
    p_body.font.color.rgb = NAVY_PRIMARY

# ==========================================
# HELPER FOR EXAMPLE SLIDES (SCREENSHOT + BREAKDOWN)
# ==========================================
def build_example_slide(slide_num, title, domain_badge, image_path, invariant_text, parameter_bounds, dag_explanation, color_theme):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, title, category=f"EXAMPLE {slide_num}: {domain_badge}")

    # Left: Explanation Card
    card_left = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.3))
    card_left.fill.solid()
    card_left.fill.fore_color.rgb = CARD_BG
    card_left.line.color.rgb = BORDER_LIGHT
    card_left.line.width = Pt(1.5)

    tf = card_left.text_frame
    tf.word_wrap = True

    # 1. World Invariant
    p1 = tf.paragraphs[0]
    p1.text = "🏛️ THE WORLD INVARIANT"
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = color_theme

    p1_b = tf.add_paragraph()
    p1_b.text = invariant_text
    p1_b.font.size = Pt(10)
    p1_b.font.color.rgb = NAVY_PRIMARY

    # 2. Parameter Bounds
    p2 = tf.add_paragraph()
    p2.text = "\n📏 GROUND TRUTH BOUNDS"
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = BLUE_ACCENT

    p2_b = tf.add_paragraph()
    p2_b.text = parameter_bounds
    p2_b.font.size = Pt(10)
    p2_b.font.color.rgb = NAVY_PRIMARY

    # 3. DAG Tripwire
    p3 = tf.add_paragraph()
    p3.text = "\n⚡ DAG CIRCUIT BREAKER"
    p3.font.size = Pt(11)
    p3.font.bold = True
    p3.font.color.rgb = RED_TRIPWIRE

    p3_b = tf.add_paragraph()
    p3_b.text = dag_explanation
    p3_b.font.size = Pt(10)
    p3_b.font.color.rgb = NAVY_PRIMARY

    # Right: High-Res Screenshot
    if os.path.exists(image_path):
        slide.shapes.add_picture(image_path, Inches(5.8), Inches(1.6), Inches(6.7), Inches(5.3))
    else:
        # Fallback placeholder
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.8), Inches(1.6), Inches(6.7), Inches(5.3))
        box.text = f"Screenshot: {os.path.basename(image_path)}"

# ==========================================
# SLIDE 3: EXAMPLE 1 - ENTERPRISE IT SECURITY
# ==========================================
build_example_slide(
    slide_num="01",
    title="Enterprise IT Security: FIDO2 & Break-Glass Governance",
    domain_badge="ENTERPRISE IDENTITY & SOC2 COMPLIANCE",
    image_path="scratch/app8_it_security_flowchart.png",
    invariant_text="Hardware FIDO2 WebAuthn cryptographic keys are strictly mandatory across production VPCs. Legacy SMS OTP and voice telephone MFA are STRICTLY PROHIBITED due to SIM-swapping vulnerabilities.",
    parameter_bounds="Direct database write lease TTL: capped at exactly 4 HOURS (240 minutes).\nEmergency Break-Glass tokens: hard-capped at exactly 2 HOURS (7,200 seconds).",
    dag_explanation="The DAG intercepts unauthorized escalations: if Break-Glass token expires at 2 hours, it instantly terminates DB leases, reverts credentials, and dispatches an immutable SOC2 audit incident to SIRT.",
    color_theme=BLUE_ACCENT
)

# ==========================================
# SLIDE 4: EXAMPLE 2 - FINTECH DISPUTE INTAKE & AML
# ==========================================
build_example_slide(
    slide_num="02",
    title="FinTech Dispute Intake: AML Velocity & Federal Non-Tipping",
    domain_badge="FINANCIAL CRIME & REGULATORY COMPLIANCE",
    image_path="scratch/app8_fintech_dispute_flowchart.png",
    invariant_text="Federal Non-Tipping Invariant (31 U.S.C. 5318(g)): Agents and customer support are STRICTLY PROHIBITED from tipping off customers about Suspicious Activity Report (SAR) filings or AML freezes.",
    parameter_bounds="Instant Tier-1 Provisional Credit: EQUAL TO OR LESS THAN $150.00.\nHigh-Velocity AML Hold Window: exactly 72 HOURS.\nMerchant Delivery Proof Rebuttal: strictly 5 business days.",
    dag_explanation="The DAG routes claims < $150 to automated reversal. If 24h card velocity exceeds $5,000, it instantly routes into a 72-hour frozen gate. Missing tracking proof triggers automatic merchant forfeiture.",
    color_theme=GREEN_EMERALD
)

# ==========================================
# SLIDE 5: EXAMPLE 3 - CLOUD CANARY RELEASE & DB LOCK
# ==========================================
build_example_slide(
    slide_num="03",
    title="Cloud DevOps: Canary Rollouts & Zero-Downtime DDL Locks",
    domain_badge="SITE RELIABILITY ENGINEERING (SRE)",
    image_path="scratch/app8_cloud_devops_flowchart.png",
    invariant_text="Production Availability Invariant: 99.99% service uptime supersedes manual operator overrides. Automated rollbacks trigger instantly whenever error budgets or lock latency thresholds drain.",
    parameter_bounds="Canary Traffic Proportion: strictly 5% for not less than 15 MINUTES (900s).\nDatabase Migration Metadata Lock: MUST NOT EXCEED 200 MILLISECONDS.",
    dag_explanation="The DAG mounts automated tripwires: if DDL migration metadata lock wait exceeds 200ms or Canary 5xx error rate exceeds 0.05%, it immediately aborts migration and triggers an automated instant rollback.",
    color_theme=AMBER_WARM
)

# ==========================================
# SLIDE 6: EXAMPLE 4 - LITERATURE (WHERE THE MOUNTAIN MEETS THE MOON)
# ==========================================
build_example_slide(
    slide_num="04",
    title="Literature & Narrative: Story Invariants & The Hero's Journey",
    domain_badge="NARRATIVE PHYSICS & FOLKLORE MODELING",
    image_path="scratch/verified_flowchart_expanded_big.png",
    invariant_text="World Invariant: Fruitless Mountain is completely barren; nothing grows on it and birds/animals do not rest there. The mud village land is stubbornly poor. Minli has an impulsive, quick-acting nature.",
    parameter_bounds="Exact Family Bounds: only 3 people live in the house (Minli, Father, Mother).\nHouse Bound: tiny boards tied with twine.\nGeography: the corner where Fruitless Mountain and Jade River meet.",
    dag_explanation="Instead of IT jargon ('cryptographic telemetry'), the DAG maps the real dramatic dilemma: Accept Poverty & Stagnate vs. Follow Impulsive Spirit and embark on the quest to find the Old Man of the Moon.",
    color_theme=PURPLE_LIT
)

# ==========================================
# SLIDE 7: TAKEAWAYS & THE GROUNDTRUTH FORMULA
# ==========================================
slide7 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide7)
add_header(slide7, "The GroundTruth Formula: From Raw Input to Reliable Agent", 
           subtitle="How the 5-Tier Policy Tree and DAG Circuit Breakers eliminate hallucination across any domain.")

summary_card = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0))
summary_card.fill.solid()
summary_card.fill.fore_color.rgb = RGBColor(248, 250, 252)
summary_card.line.color.rgb = RGBColor(203, 213, 225)
summary_card.line.width = Pt(1.5)

tf7 = summary_card.text_frame
tf7.word_wrap = True

p_sum = tf7.paragraphs[0]
p_sum.text = "🎯 KEY TAKEAWAYS FOR AI SYSTEMS ARCHITECTS"
p_sum.font.size = Pt(13)
p_sum.font.bold = True
p_sum.font.color.rgb = BLUE_ACCENT

items = [
    ("1. True Ground Truth Means No Hallucinated Numbers", 
     "If a source (novel, Wikipedia, whitepaper) doesn't specify physical constants, leave them algebraic. Inventing 42 kPa or $1.5% from thin air is a catastrophic failure of ground truth."),
    ("2. World Invariants Govern the Reality of the Environment", 
     "Whether it's the physics of Fruitless Mountain, SOC2 4-hour lease timers, or mass-conservation laws, world invariants never bend to an LLM's prompt persuasion."),
    ("3. The 5-Tier Policy Hierarchy Bridges Any Domain", 
     "Root Invariants ➔ Scoped Directives ➔ Execution Rules ➔ Parameter Bounds ➔ Dead Ends provides a universal contract layer for both engineering runbooks and story plots."),
    ("4. Circuit-Breaker DAGs Enforce Deterministic Safety", 
     "By compiling invariants directly into LangGraph decision nodes and tripwire terminals, agents are evaluated and constrained by a deterministic hidden answer key.")
]

for title, body in items:
    p_t = tf7.add_paragraph()
    p_t.text = f"\n• {title}"
    p_t.font.size = Pt(11.5)
    p_t.font.bold = True
    p_t.font.color.rgb = NAVY_PRIMARY

    p_b = tf7.add_paragraph()
    p_b.text = f"   {body}"
    p_b.font.size = Pt(10.5)
    p_b.font.color.rgb = RGBColor(71, 85, 105)

output_pptx = "Capturing_World_Invariants_Ground_Truth.pptx"
prs.save(output_pptx)
print(f"Successfully generated PowerPoint presentation: {output_pptx}")
