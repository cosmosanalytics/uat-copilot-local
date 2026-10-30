# -*- coding: utf-8 -*-
"""
Builds an executive-grade, graphical, simple, intuitive, and fun PowerPoint deck:
"Capturing World Invariants: The Foundation of Ground Truth"
Featuring BOTH Original Inputs (Step 1 Ingestion) and Ground Truth Outputs (Step 2 Flowcharts)
across 4 detailed real-world examples with embedded high-resolution screenshots.
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
DOC_BG = RGBColor(241, 245, 249)          # Slate 100

def set_slide_background(slide, color=BG_COLOR):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, category="GROUNDTRUTH ARCHITECTURE PRINCIPLES", subtitle=None):
    # Category Pill
    pill_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(8), Inches(0.32))
    tf_p = pill_box.text_frame
    tf_p.word_wrap = True
    p_cat = tf_p.paragraphs[0]
    p_cat.text = f"📘 {category.upper()}"
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = BLUE_ACCENT
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.5), Inches(0.55))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_title = tf_t.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY_PRIMARY

    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.18), Inches(11.5), Inches(0.32))
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

card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.9), Inches(11.733), Inches(5.7))
card1.fill.solid()
card1.fill.fore_color.rgb = CARD_BG
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
p2.font.size = Pt(36)
p2.font.bold = True
p2.font.color.rgb = NAVY_PRIMARY
p2.alignment = PP_ALIGN.CENTER

p3 = tf1.add_paragraph()
p3.text = "The Foundation of True Ground Truth"
p3.font.size = Pt(32)
p3.font.bold = True
p3.font.color.rgb = BLUE_ACCENT
p3.alignment = PP_ALIGN.CENTER

p_axiom = tf1.add_paragraph()
p_axiom.text = "\n⭐ “The principle is to capture the essentials of the text so that interpretation will never deviate away from the ground truth.”"
p_axiom.font.size = Pt(15)
p_axiom.font.bold = True
p_axiom.font.color.rgb = AMBER_WARM
p_axiom.alignment = PP_ALIGN.CENTER

p4 = tf1.add_paragraph()
p4.text = "Why AI Agents Fail in the Real World — and How Root Invariants Turn Hallucination into Deterministic Reliability."
p4.font.size = Pt(13)
p4.font.color.rgb = TEXT_MUTED
p4.alignment = PP_ALIGN.CENTER

p5 = tf1.add_paragraph()
p5.text = "\nFull Pipeline Walkthrough: Original Input Ingestion (Step 1) ➔ Ground Truth Compilation ➔ Flowchart DAGs (Step 2)\nEnterprise IT Security • FinTech AML • Cloud DevOps • Narrative Literature"
p5.font.size = Pt(11.5)
p5.font.bold = True
p5.font.color.rgb = RGBColor(71, 85, 105)
p5.alignment = PP_ALIGN.CENTER

# ==========================================
# SLIDE 2: THE CORE PRINCIPLES
# ==========================================
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide2)
add_header(slide2, "The Golden Principle: Anchoring Interpretation to Ground Truth", 
           subtitle="Capturing the irreducible essentials so that downstream agent interpretation never drifts or hallucinates.")

# Top Golden Axiom Banner
banner2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(1.05))
banner2.fill.solid()
banner2.fill.fore_color.rgb = RGBColor(254, 249, 195)  # Amber 50
banner2.line.color.rgb = AMBER_WARM
banner2.line.width = Pt(1.5)

tf_b2 = banner2.text_frame
tf_b2.word_wrap = True
pb1 = tf_b2.paragraphs[0]
pb1.text = "⭐ THE GOLDEN AXIOM OF GROUND TRUTH"
pb1.font.size = Pt(10)
pb1.font.bold = True
pb1.font.color.rgb = RGBColor(180, 83, 9)

pb2 = tf_b2.add_paragraph()
pb2.text = "“The principle is to capture the essentials of the text so that interpretation will never deviate away from the ground truth.”"
pb2.font.size = Pt(13)
pb2.font.bold = True
pb2.font.color.rgb = NAVY_PRIMARY

pb3 = tf_b2.add_paragraph()
pb3.text = "Downstream interpretation naturally drifts when unconstrained. Extracting the invariant core creates an unbreakable tether."
pb3.font.size = Pt(9.5)
pb3.font.color.rgb = RGBColor(100, 116, 139)

cols_data = [
    ("🚫 Rule 1: Never Hallucinate Constants", 
     "If a source defines an optimization formula algebraically as J = sum(w*(r-x)^2), DO NOT invent a fake 42.0 kPa ceiling.\n\nKeep unspecified bounds algebraic and extract ONLY what exists in the input.",
     RED_TRIPWIRE, RGBColor(254, 242, 242)),
    ("⚖️ Rule 2: World Physics != Agent Strategy", 
     "World Invariants are what the ENVIRONMENT enforces (gravity, token expiration, barren soil, federal laws).\n\nAgent Strategy can adapt; world invariants never bend for any prompt.",
     BLUE_ACCENT, RGBColor(240, 249, 255)),
    ("🛑 Rule 3: Every Invariant Needs a Tripwire", 
     "An invariant is useless as passive prose. It must be wired into the Directed Acyclic Graph (DAG) as a hard circuit breaker.\n\nIf telemetry crosses the boundary, execution freezes instantly into safe fallback.",
     GREEN_EMERALD, RGBColor(236, 253, 245))
]

for idx, (title, desc, b_color, bg_color) in enumerate(cols_data):
    left = Inches(0.8 + idx * 4.0)
    card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.72), Inches(3.75), Inches(4.25))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = b_color
    card.line.width = Pt(1.5)
    
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = b_color
    
    p_body = tf.add_paragraph()
    p_body.text = f"\n{desc}"
    p_body.font.size = Pt(10.5)
    p_body.font.color.rgb = NAVY_PRIMARY

# ==========================================
# SLIDE 3: THE DUAL-INPUT ARCHITECTURE
# ==========================================
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide3)
add_header(slide3, "The Dual-Input Architecture: Two Sources of Truth", 
           subtitle="How the GroundTruth engine combines static policy contracts with dynamic live web interfaces.")

dual_cards = [
    ("📄 Input 1: Custom Document / Policy / SOP / Excerpt",
     "The Normative & Contractual Reality",
     "The user provides raw human prose: corporate SOPs, regulatory statutes, runbooks, or literary narratives.\n\n• Defines root axioms, permission bounds, and hard prohibitions.\n• Contains the world invariants that must NEVER be violated.\n• Unstructured and messy in raw form — requires structured parsing.",
     RGBColor(240, 249, 255), BLUE_ACCENT),
    ("🌐 Input 2: Web Address / Internal Portal URL",
     "The Empirical & Operational Environment",
     "The live target interface where actions execute: an internal SSO portal, dispute microservice, canary router, or external URL.\n\n• Supplies real-time observation telemetry.\n• Validates preconditions before dispatching mutations.\n• Exposes operational gates (APIs, routes, telemetry feeds).",
     RGBColor(245, 243, 255), PURPLE_LIT)
]

for idx, (head, subhead, body, bg_col, border_col) in enumerate(dual_cards):
    left = Inches(0.8 + idx * 5.95)
    card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.6), Inches(5.75), Inches(3.4))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_col
    card.line.color.rgb = border_col
    card.line.width = Pt(1.5)

    tf = card.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = head
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = border_col

    p_sub = tf.add_paragraph()
    p_sub.text = subhead
    p_sub.font.size = Pt(10)
    p_sub.font.bold = True
    p_sub.font.color.rgb = TEXT_MUTED

    p_b = tf.add_paragraph()
    p_b.text = f"\n{body}"
    p_b.font.size = Pt(10.5)
    p_b.font.color.rgb = NAVY_PRIMARY

# Bottom Banner: The Synthesis
syn_card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.2), Inches(11.733), Inches(1.6))
syn_card.fill.solid()
syn_card.fill.fore_color.rgb = CARD_BG
syn_card.line.color.rgb = GREEN_EMERALD
syn_card.line.width = Pt(1.5)

tf_syn = syn_card.text_frame
tf_syn.word_wrap = True
ps1 = tf_syn.paragraphs[0]
ps1.text = "⚡ DUAL GOVERNANCE COMPILATION: FROM INTAKE TO EXECUTABLE DAG"
ps1.font.size = Pt(11.5)
ps1.font.bold = True
ps1.font.color.rgb = GREEN_EMERALD

ps2 = tf_syn.add_paragraph()
ps2.text = "When both inputs are ingested, the GroundTruth compiler synthesizes:\n1. Cascading Policy Tree (Text Contract): 5 Tiers of verified invariants, directives, and dead ends.\n2. Interactive Flowchart DAG (Executable Topology): Branching decision diamonds with automated circuit-breaker tripwires."
ps2.font.size = Pt(10.5)
ps2.font.color.rgb = NAVY_PRIMARY

# ==========================================
# HELPER: BUILD ORIGINAL INPUT SLIDE (STEP 1)
# ==========================================
def build_input_slide(slide_num, title, domain_badge, image_path, doc_title, verbatim_text, url_text, challenge_text, color_theme):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, title, category=f"EXAMPLE {slide_num} (PART 1): {domain_badge} — ORIGINAL INPUT INTAKE")

    # Left: Original Input Details Card
    card_left = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.2), Inches(5.5))
    card_left.fill.solid()
    card_left.fill.fore_color.rgb = CARD_BG
    card_left.line.color.rgb = BORDER_LIGHT
    card_left.line.width = Pt(1.5)

    tf = card_left.text_frame
    tf.word_wrap = True

    # Section 1: Raw Input 1
    p1 = tf.paragraphs[0]
    p1.text = "📥 INPUT 1: RAW SOURCE DOCUMENT / SOP"
    p1.font.size = Pt(10.5)
    p1.font.bold = True
    p1.font.color.rgb = color_theme

    p1_title = tf.add_paragraph()
    p1_title.text = f"Title: {doc_title}"
    p1_title.font.size = Pt(9.5)
    p1_title.font.bold = True
    p1_title.font.color.rgb = NAVY_PRIMARY

    p1_quote = tf.add_paragraph()
    p1_quote.text = f'"{verbatim_text}"'
    p1_quote.font.size = Pt(9.0)
    p1_quote.font.italic = True
    p1_quote.font.color.rgb = RGBColor(51, 65, 85)

    # Section 2: Raw Input 2
    p2 = tf.add_paragraph()
    p2.text = "\n🌐 INPUT 2: WEB ADDRESS / TARGET ENDPOINT"
    p2.font.size = Pt(10.5)
    p2.font.bold = True
    p2.font.color.rgb = BLUE_ACCENT

    p2_url = tf.add_paragraph()
    p2_url.text = f"URL: {url_text}"
    p2_url.font.size = Pt(9.5)
    p2_url.font.bold = True
    p2_url.font.color.rgb = NAVY_PRIMARY

    # Section 3: The Challenge
    p3 = tf.add_paragraph()
    p3.text = "\n⚠️ WHY NAIVE LLMS FAIL ON THIS INPUT"
    p3.font.size = Pt(10.5)
    p3.font.bold = True
    p3.font.color.rgb = RED_TRIPWIRE

    p3_body = tf.add_paragraph()
    p3_body.text = challenge_text
    p3_body.font.size = Pt(9.2)
    p3_body.font.color.rgb = NAVY_PRIMARY

    # Right: High-Res Screenshot of Step 1 Intake Inspector
    if os.path.exists(image_path):
        slide.shapes.add_picture(image_path, Inches(6.2), Inches(1.5), Inches(6.33), Inches(5.5))
    else:
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.2), Inches(1.5), Inches(6.33), Inches(5.5))
        box.text = f"Step 1 Screenshot: {os.path.basename(image_path)}"

# ==========================================
# HELPER: BUILD GROUND TRUTH OUTPUT SLIDE (STEP 2)
# ==========================================
def build_output_slide(slide_num, title, domain_badge, image_path, invariant_text, parameter_bounds, dag_explanation, color_theme):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, title, category=f"EXAMPLE {slide_num} (PART 2): {domain_badge} — GROUND TRUTH OUTPUT & DAG")

    # Left: Explanation Card
    card_left = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.2), Inches(5.5))
    card_left.fill.solid()
    card_left.fill.fore_color.rgb = CARD_BG
    card_left.line.color.rgb = BORDER_LIGHT
    card_left.line.width = Pt(1.5)

    tf = card_left.text_frame
    tf.word_wrap = True

    # 1. World Invariant
    p1 = tf.paragraphs[0]
    p1.text = "🏛️ DERIVED WORLD INVARIANT (TIER 0)"
    p1.font.size = Pt(10.5)
    p1.font.bold = True
    p1.font.color.rgb = color_theme

    p1_b = tf.add_paragraph()
    p1_b.text = invariant_text
    p1_b.font.size = Pt(9.3)
    p1_b.font.color.rgb = NAVY_PRIMARY

    # 2. Parameter Bounds
    p2 = tf.add_paragraph()
    p2.text = "\n📏 GROUND TRUTH BOUNDS (EXACT LIMITS)"
    p2.font.size = Pt(10.5)
    p2.font.bold = True
    p2.font.color.rgb = BLUE_ACCENT

    p2_b = tf.add_paragraph()
    p2_b.text = parameter_bounds
    p2_b.font.size = Pt(9.3)
    p2_b.font.color.rgb = NAVY_PRIMARY

    # 3. DAG Tripwire
    p3 = tf.add_paragraph()
    p3.text = "\n⚡ EXECUTABLE DAG & CIRCUIT BREAKER"
    p3.font.size = Pt(10.5)
    p3.font.bold = True
    p3.font.color.rgb = RED_TRIPWIRE

    p3_b = tf.add_paragraph()
    p3_b.text = dag_explanation
    p3_b.font.size = Pt(9.3)
    p3_b.font.color.rgb = NAVY_PRIMARY

    # Right: High-Res Screenshot of Step 2 Flowchart DAG
    if os.path.exists(image_path):
        slide.shapes.add_picture(image_path, Inches(6.2), Inches(1.5), Inches(6.33), Inches(5.5))
    else:
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.2), Inches(1.5), Inches(6.33), Inches(5.5))
        box.text = f"Step 2 Flowchart: {os.path.basename(image_path)}"

# ==========================================
# SLIDES 4 & 5: EXAMPLE 1 - ENTERPRISE IT SECURITY
# ==========================================
# Part 1: Original Input
build_input_slide(
    slide_num="01",
    title="IT Security: Original Ingestion & Policy Document",
    domain_badge="ENTERPRISE IDENTITY & SOC2",
    image_path="scratch/app8_it_security_step1.png",
    doc_title="SEC-POL-402_Rev4: Enterprise IT SSO & Privilege Escalation Policy",
    verbatim_text="§ 1.0 Multi-Factor Authentication (MFA) Mandate: All engineers, contractor personnel, and automated system accounts accessing production VPCs... must authenticate using physical, hardware-backed FIDO2 WebAuthn cryptographic keys (e.g. YubiKey 5 Series). Legacy SMS OTP and voice-call telephone verifications are STRICTLY PROHIBITED.\n§ 2.0 Elevated Database Write Leases: Elevated access leases are strictly ephemeral: TTL SHALL NOT EXCEED 4 HOURS (240 minutes).\n§ 3.0 Emergency Break-Glass: Break-Glass tokens are hard-capped at 2 HOURS (7,200 SECONDS). A non-dismissible audit event is dispatched instantly to SIRT.",
    url_text="https://internal.corp.local/overview",
    challenge_text="Without strict invariant extraction, an LLM easily falls back to 'helpful' user options like sending an SMS code during login friction, directly violating SOC2 hardware token requirements. It also tends to round lease timers or fail to trigger immediate SIRT alerts.",
    color_theme=BLUE_ACCENT
)

# Part 2: Ground Truth Flowchart Output
build_output_slide(
    slide_num="01",
    title="IT Security: Compiled Ground Truth & Flowchart DAG",
    domain_badge="ENTERPRISE IDENTITY & SOC2",
    image_path="scratch/app8_it_security_flowchart.png",
    invariant_text="Hardware FIDO2 WebAuthn cryptographic keys are mandatory across production VPCs. Legacy SMS OTP and voice telephone MFA are STRICTLY PROHIBITED due to SIM-swapping vulnerabilities.",
    parameter_bounds="Direct database write lease TTL: capped at exactly 4 HOURS (240 minutes).\nEmergency Break-Glass tokens: hard-capped at exactly 2 HOURS (7,200 seconds).",
    dag_explanation="The DAG intercepts unauthorized escalations: if Break-Glass token expires at 2 hours, it instantly terminates DB leases, reverts credentials, and dispatches an immutable SOC2 audit incident to SIRT.",
    color_theme=BLUE_ACCENT
)

# ==========================================
# SLIDES 6 & 7: EXAMPLE 2 - FINTECH AML DISPUTE INTAKE
# ==========================================
# Part 1: Original Input
build_input_slide(
    slide_num="02",
    title="FinTech AML Dispute: Original Ingestion & Policy Document",
    domain_badge="FINANCIAL CRIME & REGULATION",
    image_path="scratch/app8_fintech_dispute_step1.png",
    doc_title="POL-OPS-AML-2026-015: FinTech Dispute Intake & AML Hold",
    verbatim_text="§ 1.0 Tier-1 Instant Provisional Refund Guidelines: Cardholder disputes for unauthorized transactions with an aggregate claim amount EQUAL TO OR LESS THAN $150.00 and a machine risk score under 25 may be provisionally credited within 60 seconds without supervisor override.\n§ 2.0 AML Velocity & SAR Filing Mandatory Freeze: Automated rule processors detecting transaction velocities exceeding $5,000.00 within a 24-hour window on newly provisioned cards MUST IMMEDIATELY PLACE A 72-HOUR RESTRICTIVE HOLD. Under Federal Non-Tipping Invariants (31 U.S.C. § 5318(g)), agents and customer support are STRICTLY PROHIBITED from disclosing SAR investigations.\n§ 3.0 Merchant Evidence: Merchants have strictly 5 business days to submit signed carrier proof of delivery.",
    url_text="https://internal.corp.local/disputes",
    challenge_text="An empathetic chatbot will naturally try to answer a customer's question: 'Why is my money frozen?'. Under 31 U.S.C. § 5318(g), tipping off a customer that an AML/SAR hold is in place is a federal crime punishable by fines and imprisonment!",
    color_theme=GREEN_EMERALD
)

# Part 2: Ground Truth Flowchart Output
build_output_slide(
    slide_num="02",
    title="FinTech AML Dispute: Compiled Ground Truth & Flowchart DAG",
    domain_badge="FINANCIAL CRIME & REGULATION",
    image_path="scratch/app8_fintech_dispute_flowchart.png",
    invariant_text="Federal Non-Tipping Invariant (31 U.S.C. § 5318(g)): Agents and customer support are STRICTLY PROHIBITED from tipping off customers about Suspicious Activity Report (SAR) filings or AML freezes.",
    parameter_bounds="Instant Tier-1 Provisional Credit: EQUAL TO OR LESS THAN $150.00.\nHigh-Velocity AML Hold Window: exactly 72 HOURS.\nMerchant Delivery Proof Rebuttal: strictly 5 business days.",
    dag_explanation="The DAG routes claims < $150 to automated reversal. If 24h card velocity exceeds $5,000, it instantly routes into a 72-hour frozen gate. Missing tracking proof triggers automatic merchant forfeiture.",
    color_theme=GREEN_EMERALD
)

# ==========================================
# SLIDES 8 & 9: EXAMPLE 3 - CLOUD CANARY RELEASE & DB LOCK
# ==========================================
# Part 1: Original Input
build_input_slide(
    slide_num="03",
    title="Cloud DevOps: Original Ingestion & SRE Runbook",
    domain_badge="SITE RELIABILITY ENGINEERING (SRE)",
    image_path="scratch/app8_cloud_devops_step1.png",
    doc_title="SRE-RUN-DB-MIG-2026: Cloud Canary Release & DB Lock Runbook",
    verbatim_text="§ 1.0 Production Canary Deployment Gate: New microservice artifact builds MUST FIRST route strictly 5% of live production traffic to isolated canary container pods. Canary evaluation duration MUST NOT BE LESS THAN 15 MINUTES (900 seconds) prior to promotion.\n§ 2.0 Database Schema Lock Mitigation: DDL migrations (ALTER TABLE, CREATE INDEX) executing against primary transactional relational tables MUST ACQUIRE EXCLUSIVE METADATA LOCKS IN LESS THAN 200 MILLISECONDS. If lock acquisition exceeds 200ms, the migration script MUST IMMEDIATELY ABORT and yield lock queues.\n§ 3.0 Automated SRE Rollback Tripwires: If Canary 5xx HTTP error rates exceed 0.05% or P99 request latency degrades by > 20%, automated deployment orchestrators MUST TRIGGER AN INSTANT ROLLBACK.",
    url_text="https://internal.corp.local/release-console",
    challenge_text="During an outage or high-load migration, an LLM might decide to 'retry for 10 seconds' to let the DDL lock acquire. In high-throughput PostgreSQL/Aurora clusters, a 10s metadata lock queues thousands of transactions, cascading into site-wide connection pool collapse.",
    color_theme=AMBER_WARM
)

# Part 2: Ground Truth Flowchart Output
build_output_slide(
    slide_num="03",
    title="Cloud DevOps: Compiled Ground Truth & Flowchart DAG",
    domain_badge="SITE RELIABILITY ENGINEERING (SRE)",
    image_path="scratch/app8_cloud_devops_flowchart.png",
    invariant_text="Production Availability Invariant: 99.99% service uptime supersedes manual operator overrides. Automated rollbacks trigger instantly whenever error budgets or lock latency thresholds drain.",
    parameter_bounds="Canary Traffic Proportion: strictly 5% for not less than 15 MINUTES (900s).\nDatabase Migration Metadata Lock: MUST NOT EXCEED 200 MILLISECONDS.",
    dag_explanation="The DAG mounts automated tripwires: if DDL migration metadata lock wait exceeds 200ms or Canary 5xx error rate exceeds 0.05%, it immediately aborts migration and triggers an automated instant rollback.",
    color_theme=AMBER_WARM
)

# ==========================================
# SLIDES 10 & 11: EXAMPLE 4 - LITERATURE (WHERE THE MOUNTAIN MEETS THE MOON)
# ==========================================
# Part 1: Original Input
build_input_slide(
    slide_num="04",
    title="Literature: Original Novel Excerpt & Web Intake",
    domain_badge="NARRATIVE PHYSICS & FOLKLORE MODELING",
    image_path="scratch/verified_today_com_step1.png",
    doc_title="Where Mountain Meets Moon Wbna33436633 (TODAY.com Excerpt)",
    verbatim_text="Far away from here, following the Jade River, there was once a black mountain that cut into the sky like a jagged piece of rough metal. The villagers called it Fruitless Mountain because nothing grew on it and birds and animals did not rest there.\nCrowded in the corner of where Fruitless Mountain and the Jade River met was a village that was a shade of faded brown... One of the houses in this village was so small that its wood boards, held together by the roof, made one think of a bunch of matches tied with a piece of twine. Inside, there was barely enough room for three people to sit around the table — which was lucky because only three people lived there. One of them was a young girl called Minli.\nMinli was not brown and dull like the rest of the village. She had glossy black hair with pink cheeks, shining eyes always eager for adventure, and a fast smile... habit of quick acting.",
    url_text="https://www.today.com/popculture/where-mountain-meets-moon-wbna33436633",
    challenge_text="Standard AI toolchains blindly force corporate telemetry boilerplate ('Enforce cryptographic SSO token interface') onto children's folklore! Ground truth requires adapting to the domain's real 'physics': barren terrain, poverty constraints, and the protagonist's impulsive nature.",
    color_theme=PURPLE_LIT
)

# Part 2: Ground Truth Flowchart Output
build_output_slide(
    slide_num="04",
    title="Literature: Narrative Physics & Hero's Journey DAG",
    domain_badge="NARRATIVE PHYSICS & FOLKLORE MODELING",
    image_path="scratch/verified_flowchart_expanded_big.png",
    invariant_text="World Invariant: Fruitless Mountain is completely barren; nothing grows on it and birds/animals do not rest there. The mud village land is stubbornly poor. Minli has an impulsive, quick-acting nature.",
    parameter_bounds="Exact Family Bounds: only 3 people live in the house (Minli, Father, Mother).\nHouse Bound: tiny boards tied with twine.\nGeography: the corner where Fruitless Mountain and Jade River meet.",
    dag_explanation="Instead of IT jargon, the DAG maps the real dramatic dilemma: Accept Poverty & Stagnate vs. Follow Impulsive Spirit and embark on the quest to find the Old Man of the Moon to change her family's fortune.",
    color_theme=PURPLE_LIT
)

# ==========================================
# SLIDE 12: TAKEAWAYS & THE GROUNDTRUTH FORMULA
# ==========================================
slide12 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide12)
add_header(slide12, "The GroundTruth Formula: From Raw Input to Reliable Agent", 
           subtitle="How the 5-Tier Policy Tree and DAG Circuit Breakers eliminate hallucination across any domain.")

summary_card = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2))
summary_card.fill.solid()
summary_card.fill.fore_color.rgb = CARD_BG
summary_card.line.color.rgb = RGBColor(203, 213, 225)
summary_card.line.width = Pt(1.5)

tf12 = summary_card.text_frame
tf12.word_wrap = True

p_sum = tf12.paragraphs[0]
p_sum.text = "🎯 4 KEY TAKEAWAYS FOR ENTERPRISE AI ARCHITECTS"
p_sum.font.size = Pt(13)
p_sum.font.bold = True
p_sum.font.color.rgb = BLUE_ACCENT

items = [
    ("1. The Core Principle: Capture Essentials to Prevent Deviation", 
     "The fundamental principle is to capture the essentials of the text so that downstream interpretation will never deviate away from the ground truth. Anchoring root invariants eliminates prompt drift across any domain."),
    ("2. Zero Hallucinated Numbers — Respect Algebraic Bounds", 
     "If a source doesn't specify physical constants, keep them algebraic. Inventing 42 kPa or $1.5% from thin air is a catastrophic failure of ground truth."),
    ("3. The 5-Tier Policy Hierarchy Bridges Any Domain", 
     "Root Invariants ➔ Scoped Directives ➔ Execution Rules ➔ Parameter Bounds ➔ Dead Ends provides an immutable contract layer for both engineering runbooks and story plots."),
    ("4. Circuit-Breaker DAGs Enforce Deterministic Safety", 
     "By compiling invariants directly into LangGraph decision nodes and tripwire terminals, agents are evaluated and constrained by a deterministic hidden answer key.")
]

for title, body in items:
    p_t = tf12.add_paragraph()
    p_t.text = f"\n• {title}"
    p_t.font.size = Pt(11)
    p_t.font.bold = True
    p_t.font.color.rgb = NAVY_PRIMARY

    p_b = tf12.add_paragraph()
    p_b.text = f"   {body}"
    p_b.font.size = Pt(10)
    p_b.font.color.rgb = RGBColor(71, 85, 105)

output_pptx = "Capturing_World_Invariants_Ground_Truth.pptx"
prs.save(output_pptx)
print(f"Successfully generated PowerPoint presentation: {output_pptx} with {len(prs.slides)} slides!")
