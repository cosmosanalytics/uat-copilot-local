# -*- coding: utf-8 -*-
"""
Rebuild PowerPoint Presentation (.pptx) with:
  1. SOP Policy Reference Cards placed directly next to / above the graph screenshots
  2. Pure graph screenshots (unstretched, aspect-ratio locked)
  3. Clear citations linking benefits (LOAD 1 & LOAD 2) to specific SOP clauses
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    C_BG_CARD = RGBColor(255, 255, 255)
    C_TEXT_DARK = RGBColor(15, 23, 42)
    C_TEXT_MUTED = RGBColor(100, 116, 139)
    C_INDIGO = RGBColor(67, 56, 202)
    C_INDIGO_LIGHT = RGBColor(238, 242, 255)
    C_EMERALD = RGBColor(5, 150, 105)
    C_EMERALD_LIGHT = RGBColor(236, 253, 245)
    C_AMBER = RGBColor(217, 119, 6)
    C_AMBER_LIGHT = RGBColor(254, 243, 199)
    C_PINK = RGBColor(219, 39, 119)
    C_PINK_LIGHT = RGBColor(253, 242, 248)
    C_SLATE_BORDER = RGBColor(203, 213, 225)

    assets_dir = os.path.abspath("docs/presentation_assets")

    def add_header(slide, title, category, subtitle=""):
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.35), Inches(3.2), Inches(0.3))
        pill.fill.solid()
        pill.fill.fore_color.rgb = C_INDIGO_LIGHT
        pill.line.color.rgb = C_INDIGO
        pill.line.width = Pt(1)
        tf_pill = pill.text_frame
        p_p = tf_pill.paragraphs[0]
        p_p.text = category.upper()
        p_p.font.size = Pt(8.5)
        p_p.font.bold = True
        p_p.font.color.rgb = C_INDIGO
        p_p.alignment = PP_ALIGN.CENTER

        tx_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.75))
        tf_t = tx_title.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(21)
        p_t.font.bold = True
        p_t.font.color.rgb = C_TEXT_DARK

        if subtitle:
            p_sub = tf_t.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = C_TEXT_MUTED
            p_sub.space_before = Pt(2)

    def add_unstretched_picture(slide, img_path, left_in, top_in, max_width_in, max_height_in):
        """Calculates exact dimensions to fit bounding box with ZERO stretching."""
        if not os.path.exists(img_path):
            print(f"Warning: {img_path} not found!")
            return None
        with Image.open(img_path) as im:
            orig_w, orig_h = im.size
        aspect = orig_w / orig_h

        if (max_width_in / max_height_in) > aspect:
            final_h = max_height_in
            final_w = max_height_in * aspect
        else:
            final_w = max_width_in
            final_h = max_width_in / aspect

        final_top = top_in + (max_height_in - final_h) / 2.0
        final_left = left_in + (max_width_in - final_w) / 2.0
        return slide.shapes.add_picture(img_path, Inches(final_left), Inches(final_top), width=Inches(final_w), height=Inches(final_h))

    def add_sop_reference_card(slide, left_in, top_in, width_in, height_in, sop_code, sop_title, base_rule, exception_clause):
        """Adds a clean, official SOP Reference Document Card."""
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(248, 250, 252) # Slate 50
        card.line.color.rgb = C_INDIGO
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.12)

        # Header with SOP badge
        p_head = tf.paragraphs[0]
        p_head.text = f"📄 SOP REFERENCE: {sop_code} — {sop_title}"
        p_head.font.size = Pt(10)
        p_head.font.bold = True
        p_head.font.color.rgb = C_INDIGO
        p_head.space_after = Pt(4)

        # Base rule
        p_base = tf.add_paragraph()
        p_base.text = f"• Baseline Rule: {base_rule}"
        p_base.font.size = Pt(9)
        p_base.font.color.rgb = RGBColor(71, 85, 105)
        p_base.space_after = Pt(3)

        # Exception rule
        p_exc = tf.add_paragraph()
        p_exc.text = f"• Exception Authority: {exception_clause}"
        p_exc.font.size = Pt(9.5)
        p_exc.font.bold = True
        p_exc.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = RGBColor(15, 23, 42)
    bg1.line.fill.background()

    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.5))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "ENTERPRISE CALL CENTER AI ARCHITECTURE"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(52, 211, 153)
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "Call Center AI Voice Agents Studio"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    p1.space_after = Pt(14)

    p2 = tf1.add_paragraph()
    p2.text = "Three linked graphs let agents decide with more freedom within limits,\nand let policies learn continuously from real calls."
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_after = Pt(28)

    p3 = tf1.add_paragraph()
    p3.text = "KG: Knowledge Graph (What SHOULD happen)  •  CG: Context Graph (What ACTUALLY happened)  •  BG: Business Graph (Reconciliation)"
    p3.font.size = Pt(11.5)
    p3.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: THE PROPOSAL (REDUCING TWO HUMAN COGNITIVE LOADS)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Linking to the Business Graph Reduces Two Human Cognitive Loads", "The Proposal", "Humans keep setting the limits. The graphs take over the repetitive judgment.")

    load_cols = [
        {
            "tag": "1 LOAD 1",
            "title": "Forming and Updating SOPs",
            "today": "Today: People write the rulebook and learn it has drifted only during lagging quarterly financial audits.",
            "with_bg": "With the Business Graph: The drift feedback loop automatically flags rules that real calls keep bending, accompanied by live empirical evidence.",
            "color": C_PINK,
            "bg": C_PINK_LIGHT
        },
        {
            "tag": "2 LOAD 2",
            "title": "Maximizing Business Benefit",
            "today": "Today: Every exception requires human judgment to evaluate if it is worth the cost, forcing customer calls into supervisor queues.",
            "with_bg": "With the Business Graph: The autonomous voice agent weighs net customer value within the KG's limits and decides decisively on the live call.",
            "color": C_EMERALD,
            "bg": C_EMERALD_LIGHT
        }
    ]

    for i, c in enumerate(load_cols):
        x = Inches(0.8 + i * 5.95)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(5.75), Inches(4.9))
        card.fill.solid()
        card.fill.fore_color.rgb = c["bg"]
        card.line.color.rgb = c["color"]
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.4)
        tf.margin_right = Inches(0.4)
        tf.margin_top = Inches(0.4)

        pn = tf.paragraphs[0]
        pn.text = c["tag"]
        pn.font.size = Pt(16)
        pn.font.bold = True
        pn.font.color.rgb = c["color"]
        pn.space_after = Pt(8)

        pt = tf.add_paragraph()
        pt.text = c["title"]
        pt.font.size = Pt(20)
        pt.font.bold = True
        pt.font.color.rgb = C_TEXT_DARK
        pt.space_after = Pt(18)

        p_tod = tf.add_paragraph()
        p_tod.text = c["today"]
        p_tod.font.size = Pt(13)
        p_tod.font.color.rgb = RGBColor(71, 85, 105)
        p_tod.space_after = Pt(16)
        p_tod.line_spacing = 1.25

        p_bg = tf.add_paragraph()
        p_bg.text = c["with_bg"]
        p_bg.font.size = Pt(13.5)
        p_bg.font.bold = True
        p_bg.font.color.rgb = C_TEXT_DARK
        p_bg.line_spacing = 1.25

    # =========================================================================
    # SLIDE 3: CORE ARCHITECTURE (THE SPATIAL TRIAD)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "The Core Architecture: The Spatial Triad Framework", "System Core", "Grounding voice autonomy across Knowledge Graph, Context Graph, and Business Graph.")

    diag_path = os.path.join(assets_dir, "architecture_spatial_triad.png")
    add_unstretched_picture(s3, diag_path, left_in=0.8, top_in=1.8, max_width_in=6.8, max_height_in=4.9)

    right_x = Inches(7.9)
    cards_data = [
        ("Knowledge Graph (KG) — Upper Left", "What SHOULD Happen (SOPs)", "Encodes approved business policies, authority limits, and exception thresholds into formal RDF/OWL triples.", C_INDIGO),
        ("Context Graph (CG) — Upper Right", "What ACTUALLY Happened (Calls)", "Captures real-time caller facts, tenure LTV, streaming audio intent, and agent decisions.", C_EMERALD),
        ("Business Graph (BG) — Center Middle", "Reconciliation Engine", "Reconciles SHOULD vs ACTUALLY in real time. Weighs net customer value, verifies compliance, and flags policy drift.", C_AMBER),
        ("Policy Drift Loop — Closed Loop", "Continuous SOP Self-Healing", "Dashed feedback arrow signals management when frontline calls repeatedly deviate, updating the baseline SOPs.", C_PINK)
    ]

    for j, (title, tag, desc, col) in enumerate(cards_data):
        y = Inches(1.8 + j * 1.25)
        cd = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, y, Inches(4.6), Inches(1.15))
        cd.fill.solid()
        cd.fill.fore_color.rgb = C_BG_CARD
        cd.line.color.rgb = col
        cd.line.width = Pt(1.5)

        tf = cd.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.12)

        p = tf.paragraphs[0]
        p.text = f"{title} • {tag}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 4: END-TO-END FLOW
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "End-to-End Operational Flow: Document to Decision to Loop", "Execution Flow", "How unstructured text documents become computable graphs and real-time voice intelligence.")

    flow_steps = [
        ("1. Ingestion", "Raw SOP manuals & exception clauses ingested via Groq LPU (Llama 3.3 70B) & AWS Bedrock.", C_INDIGO),
        ("2. Graph Build", "Constructs formal Knowledge Graph: SOP-04, $50 Base Cap, Clause 4.2 VIP exception ($250).", C_INDIGO),
        ("3. Inbound Call", "Customer dials in; streaming ASR transcribes voice into real-time Context Graph (CG).", C_EMERALD),
        ("4. Reconciliation", "Business Graph (BG) checks: Base $50 exceeded? Yes. Customer LTV > $1,500? Yes. Concession Validated.", C_AMBER),
        ("5. Agent Speech", "Autonomous AI speaks grounded answer via Web Speech API; balance zeroed in 42 seconds.", C_EMERALD),
        ("6. Drift Loop", "Policy Drift logged (67% exception frequency) & triggers feedback arrow to update SOP-04.", C_PINK)
    ]

    for k, (step_t, step_d, step_c) in enumerate(flow_steps):
        col_idx = k % 3
        row_idx = k // 3
        x = Inches(0.8 + col_idx * 4.0)
        y = Inches(1.8 + row_idx * 2.5)

        fcard = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.7), Inches(2.2))
        fcard.fill.solid()
        fcard.fill.fore_color.rgb = C_BG_CARD
        fcard.line.color.rgb = step_c
        fcard.line.width = Pt(1.5)

        tf = fcard.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = step_t
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = step_c
        p.space_after = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = step_d
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_TEXT_DARK
        p2.line_spacing = 1.2

    # =========================================================================
    # SLIDE 5: VALUE STORY 1 - BILLING (SOP REFERENCE + UNSTRETCHED GRAPH)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Story 1: Billing Dispute ($150 International Roaming)", "Use Case 1 · Customer Retention", "Sarah Jenkins · LTV $2,400 · threatens to churn over a $150 roaming fee")

    # 1. SOP Reference Card (Above Graph on the Left)
    add_sop_reference_card(
        slide=s5,
        left_in=0.8,
        top_in=1.65,
        width_in=7.5,
        height_in=1.3,
        sop_code="SOP-04 (REV. 8.2)",
        sop_title="Telecom Billing Disputes & Roaming Waivers",
        base_rule="§2.1: Tier-1 Customer Care CSR ceiling is strictly capped at $50.00 USD per billing cycle.",
        exception_clause="§4.2 VIP Hardship Clause: Authorizes up to $250.00 USD waiver without supervisor escalation if Account LTV > $1,500 and 0 prior concessions in 12 months."
    )

    # 2. Pure Graph Screenshot (Below SOP card, completely unstretched)
    g1_path = os.path.join(assets_dir, "graph_only_billing.png")
    add_unstretched_picture(s5, g1_path, left_in=0.8, top_in=3.05, max_width_in=7.5, max_height_in=3.9)

    # 3. Right Side: Benefits with direct SOP citations
    rx = Inches(8.6)
    
    # Top Value Badge
    vbox1 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, Inches(1.65), Inches(3.9), Inches(0.95))
    vbox1.fill.solid()
    vbox1.fill.fore_color.rgb = C_EMERALD_LIGHT
    vbox1.line.color.rgb = C_EMERALD
    vbox1.line.width = Pt(1.5)
    tf_v1 = vbox1.text_frame
    tf_v1.word_wrap = True
    pv1 = tf_v1.paragraphs[0]
    pv1.text = "+$2,250"
    pv1.font.size = Pt(22)
    pv1.font.bold = True
    pv1.font.color.rgb = C_EMERALD
    pv1_sub = tf_v1.add_paragraph()
    pv1_sub.text = "Net value: $2,400 LTV protected vs $150 concession"
    pv1_sub.font.size = Pt(10)
    pv1_sub.font.color.rgb = C_TEXT_DARK

    # Card: LOAD 2 (Direct citation to SOP-04 §4.2)
    c_l2_1 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, Inches(2.72), Inches(3.9), Inches(2.05))
    c_l2_1.fill.solid()
    c_l2_1.fill.fore_color.rgb = C_BG_CARD
    c_l2_1.line.color.rgb = C_INDIGO
    c_l2_1.line.width = Pt(1.5)
    tf_l2_1 = c_l2_1.text_frame
    tf_l2_1.word_wrap = True
    tf_l2_1.margin_left = Inches(0.2)
    tf_l2_1.margin_top = Inches(0.12)
    p = tf_l2_1.paragraphs[0]
    p.text = "2 LOAD 2: Maximizes Business Benefit"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_INDIGO
    p.space_after = Pt(5)
    p2 = tf_l2_1.add_paragraph()
    p2.text = "Direct Reference: SOP-04 §4.2 (VIP Exception)\nThe Business Graph reconciles Sarah Jenkins' $2,400 LTV against the $1,500 qualification threshold. The voice agent executes the $150 waiver instantly on the live call, eliminating supervisor queue latency."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_TEXT_DARK
    p2.line_spacing = 1.2

    # Card: LOAD 1 (Direct citation to SOP-04 §2.1 policy drift)
    c_l1_1 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, Inches(4.88), Inches(3.9), Inches(2.05))
    c_l1_1.fill.solid()
    c_l1_1.fill.fore_color.rgb = C_BG_CARD
    c_l1_1.line.color.rgb = C_PINK
    c_l1_1.line.width = Pt(1.5)
    tf_l1_1 = c_l1_1.text_frame
    tf_l1_1.word_wrap = True
    tf_l1_1.margin_left = Inches(0.2)
    tf_l1_1.margin_top = Inches(0.12)
    p = tf_l1_1.paragraphs[0]
    p.text = "1 LOAD 1: Updates the SOP for Us"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_PINK
    p.space_after = Pt(5)
    p2 = tf_l1_1.add_paragraph()
    p2.text = "Policy Drift Feedback: SOP-04 §2.1 Base Limit\nBecause 67% of billing disputes exceed the standard $50 limit and trigger Clause 4.2, the BG feedback loop automatically flags SOP-04 to raise its base ceiling to $150, eliminating repetitive exception processing."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_TEXT_DARK
    p2.line_spacing = 1.2

    # =========================================================================
    # SLIDE 6: VALUE STORY 2 - BROADBAND OUTAGE (SOP REFERENCE + GRAPH)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Story 2: Broadband Outage & Telemetry Preemption", "Use Case 2 · Technical Operations", "Marcus Vance · 1Gbps Fiber · red optical alarm, 3 reboots already tried")

    # 1. SOP Reference Card
    add_sop_reference_card(
        slide=s6,
        left_in=0.8,
        top_in=1.65,
        width_in=7.5,
        height_in=1.3,
        sop_code="SOP-12 (REV. 5.1)",
        sop_title="Broadband Outage Triage & Truck Roll Protocol",
        base_rule="§2.1 Mandatory Diagnostic: Telemetry must be queried. If upstream optical loss (LOS) is detected, remote rebooting is counter-indicated.",
        exception_clause="§6.1 Hardware Defect Waiver: Standard $120.00 truck roll fee is 100% waived, and an urgent field technician slot is scheduled within 4 hours."
    )

    # 2. Pure Graph Screenshot (unstretched)
    g2_path = os.path.join(assets_dir, "graph_only_outage.png")
    add_unstretched_picture(s6, g2_path, left_in=0.8, top_in=3.05, max_width_in=7.5, max_height_in=3.9)

    # 3. Right Side Cards
    vbox2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, Inches(1.65), Inches(3.9), Inches(0.95))
    vbox2.fill.solid()
    vbox2.fill.fore_color.rgb = C_EMERALD_LIGHT
    vbox2.line.color.rgb = C_EMERALD
    vbox2.line.width = Pt(1.5)
    tf_v2 = vbox2.text_frame
    tf_v2.word_wrap = True
    pv2 = tf_v2.paragraphs[0]
    pv2.text = "+$340"
    pv2.font.size = Pt(22)
    pv2.font.bold = True
    pv2.font.color.rgb = C_EMERALD
    pv2_sub = tf_v2.add_paragraph()
    pv2_sub.text = "Avoided cost: no false dispatch, 18 minutes saved"
    pv2_sub.font.size = Pt(10)
    pv2_sub.font.color.rgb = C_TEXT_DARK

    c_l2_2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, Inches(2.72), Inches(3.9), Inches(2.05))
    c_l2_2.fill.solid()
    c_l2_2.fill.fore_color.rgb = C_BG_CARD
    c_l2_2.line.color.rgb = C_INDIGO
    c_l2_2.line.width = Pt(1.5)
    tf_l2_2 = c_l2_2.text_frame
    tf_l2_2.word_wrap = True
    tf_l2_2.margin_left = Inches(0.2)
    tf_l2_2.margin_top = Inches(0.12)
    p = tf_l2_2.paragraphs[0]
    p.text = "2 LOAD 2: Maximizes Business Benefit"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_INDIGO
    p.space_after = Pt(5)
    p2 = tf_l2_2.add_paragraph()
    p2.text = "Direct Reference: SOP-12 §6.1 (Hardware Defect Waiver)\nThe agent verifies upstream LOS telemetry (31.4dB line loss), bypasses the standard 180s modem reset checklist, waives the $120 dispatch fee, and dispatches field engineering in 2 hours."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_TEXT_DARK
    p2.line_spacing = 1.2

    c_l1_2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, Inches(4.88), Inches(3.9), Inches(2.05))
    c_l1_2.fill.solid()
    c_l1_2.fill.fore_color.rgb = C_BG_CARD
    c_l1_2.line.color.rgb = C_PINK
    c_l1_2.line.width = Pt(1.5)
    tf_l1_2 = c_l1_2.text_frame
    tf_l1_2.word_wrap = True
    tf_l1_2.margin_left = Inches(0.2)
    tf_l1_2.margin_top = Inches(0.12)
    p = tf_l1_2.paragraphs[0]
    p.text = "1 LOAD 1: Updates the SOP for Us"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_PINK
    p.space_after = Pt(5)
    p2 = tf_l1_2.add_paragraph()
    p2.text = "Policy Drift Feedback: SOP-12 §2.1 Triage Trees\n84% of loss-of-signal calls skip remote troubleshooting. The Business Graph flags SOP-12 to mandate automated upstream telemetry verification prior to any customer-facing diagnostic questions."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_TEXT_DARK
    p2.line_spacing = 1.2

    # =========================================================================
    # SLIDE 7: VALUE STORY 3 - VIP RETENTION (SOP REFERENCE + GRAPH)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Story 3: VIP Enterprise Retention ($18k Contract Churn)", "Use Case 3 · Revenue Protection", "Elena Rostova (Apex Global Logistics) · $18,000 ARR · competitor offers 15% less")

    # 1. SOP Reference Card
    add_sop_reference_card(
        slide=s7,
        left_in=0.8,
        top_in=1.65,
        width_in=7.5,
        height_in=1.3,
        sop_code="SOP-28 (REV. 4.0)",
        sop_title="Enterprise & High-LTV Retention Governance",
        base_rule="§2.1 Discretionary Ceiling: Standard account representative renewal concession is capped at 5.0% without director sign-off.",
        exception_clause="§3.1 High-Value Allowance: For enterprise accounts with ARR > $15,000.00 USD, specialists are authorized to grant up to 15.0% discount on 24-month contract lock."
    )

    # 2. Pure Graph Screenshot (unstretched)
    g3_path = os.path.join(assets_dir, "graph_only_retention.png")
    add_unstretched_picture(s7, g3_path, left_in=0.8, top_in=3.05, max_width_in=7.5, max_height_in=3.9)

    # 3. Right Side Cards
    vbox3 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, Inches(1.65), Inches(3.9), Inches(0.95))
    vbox3.fill.solid()
    vbox3.fill.fore_color.rgb = C_EMERALD_LIGHT
    vbox3.line.color.rgb = C_EMERALD
    vbox3.line.width = Pt(1.5)
    tf_v3 = vbox3.text_frame
    tf_v3.word_wrap = True
    pv3 = tf_v3.paragraphs[0]
    pv3.text = "+$15,300"
    pv3.font.size = Pt(22)
    pv3.font.bold = True
    pv3.font.color.rgb = C_EMERALD
    pv3_sub = tf_v3.add_paragraph()
    pv3_sub.text = "Net retained ARR: $18k saved, $2.7k discount"
    pv3_sub.font.size = Pt(10)
    pv3_sub.font.color.rgb = C_TEXT_DARK

    c_l2_3 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, Inches(2.72), Inches(3.9), Inches(2.05))
    c_l2_3.fill.solid()
    c_l2_3.fill.fore_color.rgb = C_BG_CARD
    c_l2_3.line.color.rgb = C_INDIGO
    c_l2_3.line.width = Pt(1.5)
    tf_l2_3 = c_l2_3.text_frame
    tf_l2_3.word_wrap = True
    tf_l2_3.margin_left = Inches(0.2)
    tf_l2_3.margin_top = Inches(0.12)
    p = tf_l2_3.paragraphs[0]
    p.text = "2 LOAD 2: Maximizes Business Benefit"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_INDIGO
    p.space_after = Pt(5)
    p2 = tf_l2_3.add_paragraph()
    p2.text = "Direct Reference: SOP-28 §3.1 (High-Value Retention)\nThe agent confirms Elena's $18k ARR qualifies for Clause 3.1. Approves the 15% rate match ($15,300) contingent on a 24-month lock, protecting $30.6k multi-year revenue with 0 days approval delay."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_TEXT_DARK
    p2.line_spacing = 1.2

    c_l1_3 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, Inches(4.88), Inches(3.9), Inches(2.05))
    c_l1_3.fill.solid()
    c_l1_3.fill.fore_color.rgb = C_BG_CARD
    c_l1_3.line.color.rgb = C_PINK
    c_l1_3.line.width = Pt(1.5)
    tf_l1_3 = c_l1_3.text_frame
    tf_l1_3.word_wrap = True
    tf_l1_3.margin_left = Inches(0.2)
    tf_l1_3.margin_top = Inches(0.12)
    p = tf_l1_3.paragraphs[0]
    p.text = "1 LOAD 1: Updates the SOP for Us"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_PINK
    p.space_after = Pt(5)
    p2 = tf_l1_3.add_paragraph()
    p2.text = "Policy Drift Feedback: SOP-28 §2.1 Discount Cap\nThe Business Graph logs that enterprise renewals routinely trigger the 15% exception, flagging SOP-28 to permanently delegate competitive matching authority to Tier-1 enterprise specialists."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_TEXT_DARK
    p2.line_spacing = 1.2

    # =========================================================================
    # SLIDE 8: DOCUMENT-TO-GRAPH EXTRACTION PIPELINE (GROQ LPU)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Document-to-Graph Extraction Pipeline: Groq LPU Engine", "Technical Ingestion", "Extracting Knowledge Graphs and Context Graphs from raw text documents with sub-second inference.")

    img_ext = os.path.join(assets_dir, "extractor_pipeline.png")
    add_unstretched_picture(s8, img_ext, left_in=0.8, top_in=1.8, max_width_in=7.5, max_height_in=4.9)

    ext_notes = [
        ("Raw Text Ingestion", "Ingests 3 unformatted SOP policy manuals and 3 real-world timestamped call transcripts directly from the repository.", C_TEXT_DARK),
        ("Default Groq Cloud LPU", "Powered by Llama-3.3-70B running on Groq LPUs at 340+ tokens/sec with sub-400ms round-trip latency.", C_AMBER),
        ("Knowledge Graph Triples", "Extracts explicit policy nodes and predicates: (SOP-04) -[:governs]-> ($50 Cap), (SOP-04) -[:allows_exception]-> (Clause 4.2).", C_INDIGO),
        ("Context Graph Triples", "Extracts runtime event nodes and customer states: (Sarah Jenkins) -[:disputed]-> ($150 Roaming), (Sarah) -[:LTV]-> ($2,400).", C_EMERALD),
        ("Real-Time Synchronization", "One click on 'Apply Extracted Graph' maps the LLM-derived triples straight onto the live Vis.js canvas.", C_PINK)
    ]

    for m, (atitle, adesc, acol) in enumerate(ext_notes):
        y = Inches(1.8 + m * 1.0)
        box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, y, Inches(3.9), Inches(0.92))
        box.fill.solid()
        box.fill.fore_color.rgb = C_BG_CARD
        box.line.color.rgb = acol
        box.line.width = Pt(1.2)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_top = Inches(0.08)

        p = tf.paragraphs[0]
        p.text = atitle
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = acol

        p2 = tf.add_paragraph()
        p2.text = adesc
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 9: BUSINESS IMPACT & ROI SCORECARD
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Enterprise Business Impact & Operational Scorecard", "Business Value & ROI", "Quantified business results across compliance, handle time, and net revenue.")

    metrics = [
        {"metric": "92%", "label": "First Contact Resolution", "sub": "Up from 61% baseline; eliminates repetitive escalations", "col": C_EMERALD},
        {"metric": "42 sec", "label": "Average Handle Time (AHT)", "sub": "Down from 4.8 min average; zero supervisor transfer wait", "col": C_INDIGO},
        {"metric": "100%", "label": "Audit Compliance", "sub": "Every concession mapped directly to verified SOP exception clauses", "col": C_AMBER},
        {"metric": "+$2,250", "label": "Net Value Per Dispute", "sub": "High-LTV customer accounts preserved at fractional concession cost", "col": C_PINK}
    ]

    for idx, m in enumerate(metrics):
        x = Inches(0.8 + idx * 2.95)
        mcard = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(2.8), Inches(4.8))
        mcard.fill.solid()
        mcard.fill.fore_color.rgb = C_BG_CARD
        mcard.line.color.rgb = m["col"]
        mcard.line.width = Pt(1.5)

        tf = mcard.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.4)

        pm = tf.paragraphs[0]
        pm.text = m["metric"]
        pm.font.size = Pt(36)
        pm.font.bold = True
        pm.font.color.rgb = m["col"]
        pm.space_after = Pt(14)

        pl = tf.add_paragraph()
        pl.text = m["label"]
        pl.font.size = Pt(15)
        pl.font.bold = True
        pl.font.color.rgb = C_TEXT_DARK
        pl.space_after = Pt(14)

        ps = tf.add_paragraph()
        ps.text = m["sub"]
        ps.font.size = Pt(11)
        ps.font.color.rgb = C_TEXT_MUTED
        ps.line_spacing = 1.25

    # Save presentation
    output_pptx = os.path.abspath("Call_Center_AI_Voice_Agents_Presentation.pptx")
    prs.save(output_pptx)
    print(f"Successfully generated PowerPoint presentation (9 slides with SOP Reference Cards) at: {output_pptx}")

if __name__ == "__main__":
    create_deck()
