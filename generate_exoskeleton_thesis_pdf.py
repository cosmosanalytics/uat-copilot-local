# -*- coding: utf-8 -*-
"""
generate_exoskeleton_thesis_pdf.py
Builds an executive one-pager PDF thesis:
"The Exoskeleton of Mind: Architectural Foundations for Frictionless Human-AI Symbiosis"
Focusing on solving the human working memory bottleneck and achieving zero-resistance cognitive symbiosis.
Strictly 1-page Letter layout with high-resolution PNG rendering.
"""

import os
import sys
import pymupdf
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

sys.stdout.reconfigure(encoding='utf-8')

def build_pdf(filename="exoskeleton_of_mind_thesis.pdf"):
    # Letter dimensions: 612 x 792 pt
    # Printable height: 792 - 48 = 744 pt
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=34,
        rightMargin=34,
        topMargin=26,
        bottomMargin=24
    )

    styles = getSampleStyleSheet()

    # Premium Color Palette: Neuro-Cognitive High-Tech
    c_primary = colors.HexColor("#0F172A")      # Deep Slate / Navy
    c_accent = colors.HexColor("#0284C7")       # Electric Sky Blue
    c_accent_dark = colors.HexColor("#0369A1")  # Deep Sky
    c_teal = colors.HexColor("#0D9488")         # Neuro Teal
    c_teal_dark = colors.HexColor("#0F766E")    # Deep Teal
    c_hero_bg = colors.HexColor("#F0FDF4")      # Soft Mint / Sage Tint
    c_hero_border = colors.HexColor("#86EFAC")  # Mint Green Accent
    c_card_bg = colors.HexColor("#F8FAFC")      # Slate 50
    c_card_border = colors.HexColor("#E2E8F0")  # Slate 200
    c_muted = colors.HexColor("#475569")        # Slate 600
    c_text = colors.HexColor("#1E293B")         # Charcoal 800
    c_gold = colors.HexColor("#D97706")         # Amber Highlight

    # Typography Styles
    top_badge_style = ParagraphStyle(
        'TopBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=c_accent_dark,
        alignment=1,
        spaceAfter=3
    )

    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=23,
        textColor=c_primary,
        alignment=1,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=12,
        textColor=c_muted,
        alignment=1,
        spaceAfter=6
    )

    meta_bar_style = ParagraphStyle(
        'MetaBar',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9,
        textColor=colors.HexColor("#64748B"),
        alignment=1,
        spaceAfter=6
    )

    hero_title_style = ParagraphStyle(
        'HeroTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11.5,
        textColor=colors.HexColor("#065F46"),
        spaceAfter=3
    )

    hero_body_style = ParagraphStyle(
        'HeroBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.2,
        textColor=colors.HexColor("#064E3B")
    )

    sec_hdr_style = ParagraphStyle(
        'SecHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10.5,
        textColor=c_primary,
        spaceAfter=3
    )

    card_title_style = ParagraphStyle(
        'CardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=c_accent_dark,
        spaceAfter=2
    )

    card_body_style = ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=10.4,
        textColor=c_text
    )

    tbl_hdr_style = ParagraphStyle(
        'TblHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=0
    )

    tbl_cell_bold = ParagraphStyle(
        'TblCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.5,
        textColor=c_primary
    )

    tbl_cell_text = ParagraphStyle(
        'TblCellText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.1,
        leading=9.2,
        textColor=c_text
    )

    synthesis_style = ParagraphStyle(
        'SynthesisStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11.5,
        textColor=c_primary,
        alignment=1
    )

    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.5,
        textColor=colors.HexColor("#94A3B8"),
        alignment=1
    )

    elements = []

    # 1. TOP HEADER & METADATA
    elements.append(Paragraph("COGNITIVE SYSTEMS &amp; HUMAN-AI SYMBIOSIS THESIS &bull; FIELD MONOGRAPH", top_badge_style))
    elements.append(Paragraph("The Exoskeleton of Mind: Overcoming the Working Memory Bottleneck", title_style))
    elements.append(Paragraph("Architectural Principles for Zero-Resistance, Direct-Coupled Human-AI Symbiosis", subtitle_style))
    elements.append(Paragraph("APPLIED INTELLIGENCE LAB &bull; COGNITIVE LOAD THEORY &bull; INTERACTIVE SYSTEMS ARCHITECTURE &bull; OCTOBER 2026", meta_bar_style))
    elements.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#CBD5E1"), spaceAfter=5, spaceBefore=0))

    # 2. CORE THESIS CALLOUT (HERO BOX)
    hero_content = [
        Paragraph("THE EXOSKELETON PARADOX &amp; CENTRAL THESIS", hero_title_style),
        Paragraph(
            "<b>The Paradox:</b> A mechanical exoskeleton generating 10,000 ft-lbs of torque is lethal or useless if its joint linkages oppose biological human gait. "
            "Similarly, superintelligent AI boasting infinite semantic depth is useless if human biological wetware cannot load its intelligence into working memory. "
            "Human conscious cognition is fundamentally bounded by <b>Miller's Law (~4 to 7 cognitive chunks)</b> and a sensory input rate of barely ~50 bits/second for serialized text. "
            "<br/><br/>"
            "<b>The Thesis:</b> True intellectual symbiosis cannot occur through the serialized 'drinking-from-a-firehose' straw of text-based chat. "
            "To achieve genuine cognitive symbiosis, the communication impedance between human and AI must approach <b>zero friction</b>: "
            "transforming the AI from an external advisor across a glass screen into an <b>ambient, ready-to-hand cognitive prosthetic</b> that matches biological bandwidth, anticipates mental states, and operates directly within human working memory limits.",
            hero_body_style
        )
    ]
    hero_table = Table([[hero_content]], colWidths=[544])
    hero_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_hero_bg),
        ('BOX', (0,0), (-1,-1), 1, c_hero_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(hero_table)
    elements.append(Spacer(1, 6))

    # 3. THREE-COLUMN ARCHITECTURAL FOUNDATIONS
    col_w = 176
    spacing_w = 8

    # Col 1: The Bottlenecks
    col1_content = [
        Paragraph("1. THE FRICTION SOURCES", card_title_style),
        Spacer(1, 1),
        Paragraph("<b>&bull; Serialization Tax:</b> Forcing multi-dimensional thoughts into sequential ASCII prompts discards 95% of intuitive human intent.", card_body_style),
        Spacer(1, 2),
        Paragraph("<b>&bull; Context Thrashing:</b> Paragraph-heavy AI responses instantly overflow the 4-chunk working memory stack, forcing mental resets.", card_body_style),
        Spacer(1, 2),
        Paragraph("<b>&bull; Epistemic Distance:</b> Constant prompt calibration and verification creates high extraneous cognitive load, halting deep flow.", card_body_style)
    ]

    # Col 2: The Symbiotic Solutions
    col2_content = [
        Paragraph("2. ZERO-RESISTANCE PILLARS", card_title_style),
        Spacer(1, 1),
        Paragraph("<b>&bull; Perceptual Chunking:</b> Bypassing verbal memory by projecting high-dimensional state into spatial graphs &amp; visual diffs.", card_body_style),
        Spacer(1, 2),
        Paragraph("<b>&bull; Delta-Signaling:</b> The AI transmits only the semantic delta between its model and the human's verified mental state.", card_body_style),
        Spacer(1, 2),
        Paragraph("<b>&bull; Latent Intent Coupling:</b> Continuous ambient steering via eye gaze, cursor kinematics, and 1-click decision forks.", card_body_style)
    ]

    # Col 3: The System State
    col3_content = [
        Paragraph("3. THE COGNITIVE PROSTHETIC", card_title_style),
        Spacer(1, 1),
        Paragraph("<b>&bull; Ready-to-Hand (Heidegger):</b> The tool becomes transparent. The user thinks <i>through</i> the AI rather than talking <i>to</i> it.", card_body_style),
        Spacer(1, 2),
        Paragraph("<b>&bull; Shared Working Memory:</b> AI acts as an active L1 cache, holding ephemeral branches and surfacing only the critical decision node.", card_body_style),
        Spacer(1, 2),
        Paragraph("<b>&bull; Invariant Bounds:</b> Autonomous background execution with guardrails, preventing human cognitive babysitting.", card_body_style)
    ]

    table_data = [[col1_content, col2_content, col3_content]]
    cards_table = Table(table_data, colWidths=[col_w, col_w, col_w])
    cards_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (0,0), 0.8, c_card_border),
        ('BOX', (1,0), (1,0), 0.8, c_card_border),
        ('BOX', (2,0), (2,0), 0.8, c_card_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(cards_table)
    elements.append(Spacer(1, 6))

    # 4. COMPARISON MATRIX: CHAT INTERACTION VS. EXOSKELETON SYMBIOSIS
    elements.append(Paragraph("THE PARADIGM SHIFT: CONVERSATIONAL CHATBOT VS. INTELLIGENCE EXOSKELETON", sec_hdr_style))
    matrix_data = [
        [
            Paragraph("Cognitive Dimension", tbl_hdr_style),
            Paragraph("Conversational AI (High Friction / Brittle)", tbl_hdr_style),
            Paragraph("Exoskeletal Symbiosis (Zero Resistance / Seamless)", tbl_hdr_style)
        ],
        [
            Paragraph("Bandwidth Medium", tbl_cell_bold),
            Paragraph("Sequential text paragraphs (~50 bps conscious verbal limit)", tbl_cell_text),
            Paragraph("Spatial state trees, visual diffs, and compressed mental chunks (Megabits visual cortex)", tbl_cell_text)
        ],
        [
            Paragraph("Working Memory Load", tbl_cell_bold),
            Paragraph("Saturated: Human must digest, filter, and hold raw token streams", tbl_cell_text),
            Paragraph("Zero Extraneous Load: Pre-chunked into human's 4-chunk capacity; AI acts as L1 buffer", tbl_cell_text)
        ],
        [
            Paragraph("Initiative &amp; Sync", tbl_cell_bold),
            Paragraph("Reactive / Turn-taking: User must frame explicit prompt prompts", tbl_cell_text),
            Paragraph("Anticipatory / Co-State: AI tracks attentional context &amp; delivers proactive forks", tbl_cell_text)
        ],
        [
            Paragraph("Mental Relationship", tbl_cell_bold),
            Paragraph("External conversational stranger across a browser window", tbl_cell_text),
            Paragraph("Integrated neural exoskeleton: Invisible tool dissolved into human intent", tbl_cell_text)
        ]
    ]

    matrix_table = Table(matrix_data, colWidths=[114, 215, 215])
    matrix_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOTTOMPADDING', (0,0), (-1,0), 4),
        ('TOPPADDING', (0,0), (-1,0), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,1), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,1), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(matrix_table)
    elements.append(Spacer(1, 6))

    # 5. THE FOUR OPERATIONAL LAWS FOR BUILDERS
    laws_content = [
        Paragraph("THE 4 OPERATIONAL LAWS OF SEAMLESS COGNITIVE COUPLING", ParagraphStyle('LawHdr', parent=sec_hdr_style, fontSize=7.8, textColor=c_teal_dark)),
        Paragraph("<b>Law 1 (The Chunking Invariant):</b> Never emit raw multi-paragraph prose when a structural hierarchy, state diagram, or interactive decision card can convey the same entropy in a single saccade.", card_body_style),
        Spacer(1, 1.5),
        Paragraph("<b>Law 2 (The Cognitive Delta Rule):</b> Never force the human to re-read what they already know. Transmit strictly the semantic delta required for the next executive decision.", card_body_style),
        Spacer(1, 1.5),
        Paragraph("<b>Law 3 (The Ergonomic Readiness Rule):</b> If the human must consciously ponder 'how to prompt the model', the exoskeleton has failed. Steering must occur at the speed of subconscious thought via micro-interactions.", card_body_style),
        Spacer(1, 1.5),
        Paragraph("<b>Law 4 (The Autonomy Trust Boundary):</b> Agents must execute routine tactical paths autonomously, escalating to the human working memory stack only when architectural ambiguity exceeds safety thresholds.", card_body_style)
    ]
    laws_table = Table([[laws_content]], colWidths=[544])
    laws_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(laws_table)
    elements.append(Spacer(1, 5))

    # 6. FINAL SYNTHESIS
    synthesis_box = [
        Paragraph(
            "<font color='#0284C7'><b>THE GOLDEN COUPLING THEOREM:</b></font> "
            "<i>The velocity of human-machine intelligence is inversely proportional to the friction of mental translation. "
            "When cognitive impedance reaches zero, the interface vanishes &mdash; and artificial intelligence ceases to be software you consult; "
            "it becomes the neuromuscular fabric through which you perceive, reason, and create.</i>",
            synthesis_style
        )
    ]
    syn_table = Table([[synthesis_box]], colWidths=[544])
    syn_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(syn_table)
    elements.append(Spacer(1, 4))

    # 7. FOOTER
    elements.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#E2E8F0"), spaceAfter=3, spaceBefore=0))
    elements.append(Paragraph("THE EXOSKELETON OF MIND &bull; APPLIED THESIS &bull; PUBLISHED FOR ARCHITECTS, COGNITIVE SCIENTISTS &amp; SYSTEM BUILDERS &bull; PAGE 1 OF 1", footer_style))

    doc.build(elements)
    print(f"[SUCCESS] Built PDF: {filename}")

    # Verify Page Count
    doc_fitz = pymupdf.open(filename)
    page_count = doc_fitz.page_count
    print(f"[VERIFY] Total Pages: {page_count}")
    assert page_count == 1, f"Expected strictly 1 page, but got {page_count} pages!"

    # Render High-Resolution PNG Preview
    page = doc_fitz[0]
    pix = page.get_pixmap(dpi=200)
    preview_img = "exoskeleton_thesis_preview.png"
    pix.save(preview_img)
    print(f"[SUCCESS] Generated 200 DPI PNG preview: {preview_img}")
    doc_fitz.close()
    return filename, preview_img

if __name__ == "__main__":
    build_pdf()
