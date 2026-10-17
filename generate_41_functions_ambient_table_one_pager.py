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

# 1. Build an illustrated mini-flowchart banner showing Subconscious vs Conscious HUD
def generate_subconscious_banner(output_path="scratch/subconscious_banner.png"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, ax = plt.subplots(figsize=(10.5, 1.3), dpi=300)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 1.3)
    ax.axis('off')

    # Background panel
    panel = patches.FancyBboxPatch(
        (0.2, 0.1), 10.1, 1.1,
        boxstyle="round,pad=0.05,rounding_size=0.15",
        edgecolor='#334155', facecolor='#1e293b', linewidth=1.2
    )
    ax.add_patch(panel)

    # Left: Subconscious Engine (41 Functions)
    ax.text(0.5, 0.85, "SUBCONSCIOUS MACHINE ENGINE", fontsize=8.5, fontweight='bold', color='#38bdf8')
    ax.text(0.5, 0.45, "41 Brain Functions running in parallel on AWS / local execution mesh (Pillars 1 to 5)", fontsize=7, color='#94a3b8')

    # Arrow & Gating
    ax.annotate(
        "Filtered 95%", xy=(6.5, 0.65), xytext=(5.1, 0.65),
        arrowprops=dict(arrowstyle="->", color="#34d399", lw=2, mutation_scale=12),
        fontsize=7, fontweight='bold', color='#34d399', va='bottom', ha='center'
    )

    # Right: Conscious Human HUD (Miller's Law)
    hud_box = patches.FancyBboxPatch(
        (6.7, 0.22), 3.4, 0.85,
        boxstyle="round,pad=0.05,rounding_size=0.12",
        edgecolor='#10b981', facecolor='#064e3b', linewidth=1.2
    )
    ax.add_patch(hud_box)
    ax.text(8.4, 0.75, "CONSCIOUS HUMAN HUD", fontsize=8, fontweight='bold', color='#a7f3d0', ha='center')
    ax.text(8.4, 0.42, "Single-card summary | 1-Click Rollback | ~4 Working Slots", fontsize=6.8, color='#ecfdf5', ha='center')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0.02, facecolor=fig.get_facecolor())
    plt.close()
    return output_path

# 2. Build the ReportLab 1-Pager PDF
def build_ambient_mapping_pdf(pdf_path="ambient_41_brain_functions_mapping.pdf"):
    banner_img = generate_subconscious_banner()

    # Exact Letter: 612 x 792 pt
    margin = 24
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=22,
        bottomMargin=22
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=20,
        textColor=colors.HexColor('#0f172a'),
        alignment=1
    )

    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#475569'),
        alignment=1
    )

    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=8.5,
        textColor=colors.HexColor('#0369a1'),
        alignment=1
    )

    th_style = ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=9.5,
        textColor=colors.HexColor('#ffffff')
    )

    col_pillar_style = ParagraphStyle(
        'ColPillar',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#0f172a')
    )

    col_bio_style = ParagraphStyle(
        'ColBio',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.5,
        textColor=colors.HexColor('#475569')
    )

    col_aws_style = ParagraphStyle(
        'ColAws',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=6.8,
        leading=8.5,
        textColor=colors.HexColor('#b45309')
    )

    col_ambient_style = ParagraphStyle(
        'ColAmbient',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.0,
        leading=8.8,
        textColor=colors.HexColor('#0f172a')
    )

    formula_style = ParagraphStyle(
        'Formula',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.6,
        leading=10,
        textColor=colors.HexColor('#065f46'),
        alignment=1
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("THE 41 BRAIN FUNCTIONS OF AMBIENT AI", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Mapping Cognitive Neuroscience Pillars to Cloud Primitives & Ergonomic Human Interfaces", subtitle_style))
    story.append(Spacer(1, 4))

    # Badges bar
    badges_data = [[
        Paragraph("<b>[ 41 Brain Functions ]</b><br/>Spanning 6 Cognitive Pillars", badge_style),
        Paragraph("<b>[ 95% Friction Absorbed ]</b><br/>Machine shoulders execution load", badge_style),
        Paragraph("<b>[ Miller's Law Shield ]</b><br/>Protects ~4 human working slots", badge_style),
        Paragraph("<b>[ 100% Reversible ]</b><br/>Proactive action + armed rollback", badge_style)
    ]]
    badges_table = Table(badges_data, colWidths=[141, 141, 141, 141])
    badges_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#e0f2fe')),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(badges_table)
    story.append(Spacer(1, 5))

    # Subconscious vs Conscious Infographic Banner
    story.append(Image(banner_img, width=564, height=70))
    story.append(Spacer(1, 5))

    # The Master Mapping Table (6 Pillars)
    headers = [
        Paragraph("Cognitive Pillar & Brain Region", th_style),
        Paragraph("Key Functions (Total 41)", th_style),
        Paragraph("Cloud / OS Primitives", th_style),
        Paragraph("Ambient AI Ergonomic Role (What the Human Experiences)", th_style)
    ]

    table_rows = [headers]

    pillars_content = [
        (
            "<b>PILLAR 1: PERCEIVE & ATTEND</b><br/><font color='#0284c7'>Thalamus, Salience Network</font>",
            "Sensory Gating, Salience Allocation, Prediction Error, Multimodal Fusion, Spatial Mapping (7 funcs)",
            "EventBridge, CloudWatch Logs, OpenSearch, File Watchers",
            "<b>Noise Filter & Triage HUD</b>: Ingests 87 unread emails, terminal logs, and system alerts; suppresses 95% background noise and surfaces only the 1 critical action card."
        ),
        (
            "<b>PILLAR 2: REMEMBER</b><br/><font color='#0284c7'>Hippocampus, Prefrontal Cortex</font>",
            "Working Memory Buffer, Episodic Retrieval, Semantic Index, Consolidation, Principled Forgetting (7 funcs)",
            "DynamoDB, Redis ElastiCache, S3 Vector, Bedrock Knowledge Bases",
            "<b>Topological Intent Graph</b>: Retains intent dependencies across turns (Turn N-1 'Post link' -> Turn N 'Build app'). Relieves human working memory from keeping mental checklists."
        ),
        (
            "<b>PILLAR 3: THINK & DECIDE</b><br/><font color='#0284c7'>DLPFC, Basal Ganglia, ACC</font>",
            "Executive Planning, Response Inhibition, Error Monitoring, Reality Monitoring, Counterfactual Logic (8 funcs)",
            "AWS Step Functions, Bedrock Agentic Loop, Circuit Breakers",
            "<b>Low-Entropy 'Go' & Inhibition Gate</b>: Decomposes 'Go' into an executable DAG. <i>Inhibits</i> the chatbot impulse to ask trivial questions on safe, reversible tasks."
        ),
        (
            "<b>PILLAR 4: LEARN & FEEL</b><br/><font color='#0284c7'>Amygdala, Insula, VTA Dopamine</font>",
            "Reward Prediction Error, Somatic Markers, Metacognition, Insight Synthesis, Homeostatic Alarms (6 funcs)",
            "Composite CloudWatch Alarms, Bedrock Guardrails, Feedback Ledgers",
            "<b>Confidence & Risk Gate</b>: Evaluates execution safety. High confidence + low risk = silent execution. If a somatic safety threshold is breached, triggers a 1-click human veto."
        ),
        (
            "<b>PILLAR 5: ACT & REGULATE</b><br/><font color='#0284c7'>Motor Cortex, Hypothalamus</font>",
            "Motor Tool Execution, Token Streaming, Lateral Inhibition, Homeostatic Reversibility, Rate Limits (5 funcs)",
            "AWS Lambda, Local Subshells, WAF Quotas, Transaction URNs",
            "<b>Silent Motor Execution & Armed Undo</b>: Runs headless browser tests (0 console errors), compiles code, pushes Git, dispatches APIs, and automatically arms 1-click rollback scripts."
        ),
        (
            "<b>PILLAR 6: CONNECT & AWARE</b><br/><font color='#0284c7'>Global Workspace (GWT), Callosum</font>",
            "Global Workspace Broadcast, Hemisphere Transfer, Multi-Agent Voting, Ambient Vigilance Daemons (8 funcs)",
            "SNS Fanout, EventBridge Pipes, Cron Schedules, Subagent Mesh",
            "<b>Global Workspace HUD & Vigilance</b>: Broadcasts the finished product into a single peripheral card. Keeps silent background vigilance over CI/CD pipelines until green."
        )
    ]

    for p_name, p_funcs, p_prims, p_amb in pillars_content:
        table_rows.append([
            Paragraph(p_name, col_pillar_style),
            Paragraph(p_funcs, col_bio_style),
            Paragraph(p_prims, col_aws_style),
            Paragraph(p_amb, col_ambient_style)
        ])

    col_widths = [118, 126, 114, 206]
    main_table = Table(table_rows, colWidths=col_widths)
    main_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('ROUNDEDCORNERS', [5, 5, 5, 5]),
        ('ALIGN', (0,0), (-1,0), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
    ]))
    story.append(main_table)
    story.append(Spacer(1, 5))

    # Bottom Cognitive Ergonomics Rule Banner
    rule_data = [[
        Paragraph(
            "<b>THE GOLDEN ERGONOMIC RULE:</b> All 41 brain functions execute continuously in the subconscious machine layer; "
            "only <b>one unified, actionable decision card</b> surfaces into the conscious human HUD (~4 slots protected).",
            formula_style
        )
    ]]
    t_rule = Table(rule_data, colWidths=[564])
    t_rule.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#dcfce7')),
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor('#16a34a')),
        ('ROUNDEDCORNERS', [5, 5, 5, 5]),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_rule)

    doc.build(story)
    print("PDF build complete:", pdf_path)

if __name__ == "__main__":
    build_ambient_mapping_pdf()
