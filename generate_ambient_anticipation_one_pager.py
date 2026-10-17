import os
import pymupdf
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 1. Generate high-quality hero comparison infographic using Matplotlib
def generate_hero_diagram(output_path="scratch/ambient_vs_chatbot.png"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, ax = plt.subplots(figsize=(10.5, 3.8), dpi=300)
    fig.patch.set_facecolor('#0b0f19')
    ax.set_facecolor('#0b0f19')
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 3.8)
    ax.axis('off')

    # Left Side: The Chatbot Tennis Trap
    box_left = patches.FancyBboxPatch(
        (0.2, 0.2), 4.8, 3.4,
        boxstyle="round,pad=0.1,rounding_size=0.18",
        linewidth=1.5, edgecolor='#f43f5e', facecolor='#131b2e'
    )
    ax.add_patch(box_left)
    
    # Red pill badge
    pill_left = patches.FancyBboxPatch(
        (0.5, 3.1), 3.2, 0.35,
        boxstyle="round,pad=0.04,rounding_size=0.1",
        facecolor='#e11d48', edgecolor='none'
    )
    ax.add_patch(pill_left)
    ax.text(2.1, 3.27, "THE CHATBOT TENNIS TRAP", fontsize=9, fontweight='bold', color='#ffffff', ha='center', va='center')
    ax.text(0.5, 2.85, "High Cognitive Load  |  Excessive Prompt Ping-Pong", fontsize=7.5, color='#fda4af')

    steps_bad = [
        ("User", "Make an ambient AI app...", "#38bdf8"),
        ("Bot",  "Which CSS framework? Which API? Confirm?", "#fb7185"),
        ("User", "Now summarize & push to LinkedIn.", "#38bdf8"),
        ("Bot",  "Please provide credentials and repo name...", "#fb7185"),
        ("User", "'Go' -> Bot: 'What do you mean by Go?'", "#f43f5e")
    ]
    y_pos = 2.45
    for role, text, col in steps_bad:
        ax.text(0.55, y_pos, f"[{role}]", fontsize=7.8, fontweight='bold', color=col)
        ax.text(1.25, y_pos, text, fontsize=7.6, color='#cbd5e1')
        y_pos -= 0.38

    # Right Side: The Ambient AI Exoskeleton
    box_right = patches.FancyBboxPatch(
        (5.5, 0.2), 4.8, 3.4,
        boxstyle="round,pad=0.1,rounding_size=0.18",
        linewidth=1.5, edgecolor='#10b981', facecolor='#131b2e'
    )
    ax.add_patch(box_right)

    # Green pill badge
    pill_right = patches.FancyBboxPatch(
        (5.8, 3.1), 3.4, 0.35,
        boxstyle="round,pad=0.04,rounding_size=0.1",
        facecolor='#059669', edgecolor='none'
    )
    ax.add_patch(pill_right)
    ax.text(7.5, 3.27, "THE AMBIENT EXOSKELETON", fontsize=9, fontweight='bold', color='#ffffff', ha='center', va='center')
    ax.text(5.8, 2.85, "95% Friction Absorbed  |  Zero-Tennis Flow State", fontsize=7.5, color='#6ee7b7')

    steps_good = [
        ("User", "Specifies intent across turns (App + LinkedIn)", "#38bdf8"),
        ("User", "Types: 'Go' (2 keystrokes of executive intent)", "#fbbf24"),
        ("AI",   "Traverses Intent DAG (Prerequisites resolved)", "#34d399"),
        ("AI",   "Runs Headless Browser Test (0 errors verified)", "#34d399"),
        ("AI",   "Pushes Git, deploys, posts, arms 1-click Undo", "#10b981")
    ]
    y_pos = 2.45
    for role, text, col in steps_good:
        ax.text(5.85, y_pos, f"[{role}]", fontsize=7.8, fontweight='bold', color=col)
        ax.text(6.55, y_pos, text, fontsize=7.6, color='#cbd5e1')
        y_pos -= 0.38

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0.04, facecolor=fig.get_facecolor())
    plt.close()
    return output_path

# 2. Generate Flowchart pipeline diagram
def generate_flow_diagram(output_path="scratch/pipeline_flow.png"):
    fig, ax = plt.subplots(figsize=(10.5, 1.4), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 1.4)
    ax.axis('off')

    stages = [
        ("EXECUTIVE INTENT", "User types 'Go'", "#0284c7", "#e0f2fe"),
        ("DAG RESOLUTION", "Unfulfilled turns linked", "#6366f1", "#ede9fe"),
        ("CONTRACT TEST", "Headless verify (0 err)", "#d97706", "#fef3c7"),
        ("DEPLOY & SYNC", "Git push & CI green", "#059669", "#d1fae5"),
        ("SAFETY NET", "Armed 1-click Rollback", "#0d9488", "#ccfbf1"),
    ]

    box_w = 1.75
    box_h = 1.05
    start_x = 0.35
    gap = 0.35

    for i, (title, sub, stroke, bg) in enumerate(stages):
        x = start_x + i * (box_w + gap)
        bbox = patches.FancyBboxPatch(
            (x, 0.15), box_w, box_h,
            boxstyle="round,pad=0.06,rounding_size=0.12",
            edgecolor=stroke, facecolor=bg, linewidth=1.4
        )
        ax.add_patch(bbox)
        ax.text(x + box_w/2, 0.8, title, fontsize=7.5, fontweight='bold', color=stroke, ha='center', va='center')
        ax.text(x + box_w/2, 0.45, sub, fontsize=6.8, color='#334155', ha='center', va='center')

        # Arrow
        if i < len(stages) - 1:
            arr_x = x + box_w + 0.05
            ax.annotate(
                "", xy=(arr_x + 0.22, 0.67), xytext=(arr_x, 0.67),
                arrowprops=dict(arrowstyle="->", color="#94a3b8", lw=2, mutation_scale=12)
            )

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0.02, facecolor=fig.get_facecolor())
    plt.close()
    return output_path

# 3. Build the ReportLab 1-Pager
def build_one_pager_pdf(pdf_path="ambient_anticipation_one_pager.pdf"):
    hero_img = generate_hero_diagram()
    flow_img = generate_flow_diagram()

    # Exact Letter size: 612 x 792 pt
    margin = 26
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=21,
        leading=23,
        textColor=colors.HexColor('#0f172a'),
        alignment=1
    )

    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#475569'),
        alignment=1
    )

    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9,
        textColor=colors.HexColor('#0369a1'),
        alignment=1
    )

    card_header_style = ParagraphStyle(
        'CardH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#0f172a')
    )

    card_text_style = ParagraphStyle(
        'CardT',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=9.8,
        textColor=colors.HexColor('#334155')
    )

    formula_style = ParagraphStyle(
        'Formula',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#065f46'),
        alignment=1
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("THE ANATOMY OF \"GO\"", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("How Ambient AI Anticipates What You Need Without Prompt Ping-Pong", subtitle_style))
    story.append(Spacer(1, 5))

    # Top Feature Badges
    badges_data = [[
        Paragraph("<b>[ Miller's Law Shield ]</b><br/>Protects ~4 Working Memory Slots", badge_style),
        Paragraph("<b>[ Zero Prompt Tennis ]</b><br/>Intent Traversed Across Turns", badge_style),
        Paragraph("<b>[ Reversible Safety Net ]</b><br/>1-Click Automated Rollback", badge_style)
    ]]
    badges_table = Table(badges_data, colWidths=[186, 186, 186])
    badges_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#e0f2fe')),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(badges_table)
    story.append(Spacer(1, 6))

    # Hero Comparison Graphic
    story.append(Image(hero_img, width=560, height=198))
    story.append(Spacer(1, 5))

    # Visual Flow Diagram
    story.append(Image(flow_img, width=560, height=74))
    story.append(Spacer(1, 6))

    # 5 Strategic Pillars Grid
    # Row 1: 3 cards
    w3 = 184
    row1 = [
        [
            Paragraph("<b>1. Topological Intent Graph</b>", card_header_style),
            Paragraph("<b>2. Low-Entropy 'Go' Trigger</b>", card_header_style),
            Paragraph("<b>3. Silent Sub-Goal Expansion</b>", card_header_style)
        ],
        [
            Paragraph("Maintains a Directed Acyclic Graph (DAG) across turns. It knew Request #9 (LinkedIn) strictly depended on Request #10 (App build).", card_text_style),
            Paragraph("'Go' has near-zero token entropy. The AI sees it as an <b>Executive Greenlight</b>, not missing info. No stalling with trivial questions.", card_text_style),
            Paragraph("Silently spawned a headless browser, checked console for 0 errors, formatted XOR tokens, and queried CI—without being asked.", card_text_style)
        ]
    ]
    t1 = Table(row1, colWidths=[w3, w3, w3])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (0,-1), 1, colors.HexColor('#cbd5e1')),
        ('BOX', (1,0), (1,-1), 1, colors.HexColor('#cbd5e1')),
        ('BOX', (2,0), (2,-1), 1, colors.HexColor('#cbd5e1')),
        ('ROUNDEDCORNERS', [5, 5, 5, 5]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t1)
    story.append(Spacer(1, 5))

    # Row 2: 2 cards
    w2 = 278
    row2 = [
        [
            Paragraph("<b>4. Asymmetric Reversibility Calculus</b>", card_header_style),
            Paragraph("<b>5. Active Thread vs Dormant Pruning</b>", card_header_style)
        ],
        [
            Paragraph("<b>Heuristic: Cost of Stalling &gt; Cost of Undoable Action</b><br/>Git pushes and LinkedIn shares are 100% reversible. Proactive execution with an armed rollback switch beats human interruption.", card_text_style),
            Paragraph("The conversation had earlier discussions about AWS setup. The AI recognized AWS was dormant (waiting on accounts) while the Ambient App pipeline was active and executable.", card_text_style)
        ]
    ]
    t2 = Table(row2, colWidths=[w2, w2])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (0,-1), 1, colors.HexColor('#cbd5e1')),
        ('BOX', (1,0), (1,-1), 1, colors.HexColor('#cbd5e1')),
        ('ROUNDEDCORNERS', [5, 5, 5, 5]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t2)
    story.append(Spacer(1, 6))

    # Bottom Formula Banner
    formula_data = [[
        Paragraph("<b>THE AMBIENT PRINCIPLE:</b> Human Bandwidth (Pure Intent) + Ambient Exoskeleton (Silent Execution) = <b>10x Flow State</b>", formula_style)
    ]]
    tf = Table(formula_data, colWidths=[560])
    tf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#dcfce7')),
        ('BOX', (0,0), (-1,-1), 1.4, colors.HexColor('#16a34a')),
        ('ROUNDEDCORNERS', [5, 5, 5, 5]),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tf)

    doc.build(story)
    print("PDF build complete:", pdf_path)

if __name__ == "__main__":
    build_one_pager_pdf()
