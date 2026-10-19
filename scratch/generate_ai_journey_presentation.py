import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Output paths
OUT_DIR = "scratch/presentation_assets"
os.makedirs(OUT_DIR, exist_ok=True)
PPTX_PATH = "C:/Users/richa/Downloads/AI_Journey_Single_Agent_to_Ambient_Enterprise.pptx"
PPTX_LOCAL_PATH = "AI_Journey_Single_Agent_to_Ambient_Enterprise.pptx"

# Modern Color Palette
C_NAVY = "#0F172A"
C_SLATE = "#334155"
C_BLUE = "#0284C7"
C_PURPLE = "#7C3AED"
C_GREEN = "#059669"
C_AMBER = "#D97706"
C_RED = "#DC2626"
C_BG_CARD = "#F8FAFC"
C_BORDER = "#E2E8F0"

print("Generating high-res diagram graphics without emoji font warnings...")

# ==============================================================================
# DIAGRAM 1: THE 6-STAGE EVOLUTIONARY ROADMAP
# ==============================================================================
def create_roadmap_diagram():
    fig, ax = plt.subplots(figsize=(10.5, 4.4), dpi=240)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 12.2)
    ax.set_ylim(0, 5)
    ax.axis('off')

    stages = [
        ("1. Single Agent", "Lone Wolf\nMonolithic Prompt\nLinear Context", "#64748B", "01"),
        ("2. Multi-Agent", "Specialized Squad\nPeer Review & QA\nTask Delegation", "#0284C7", "02"),
        ("3. 3-Layer Brain", "Cognitive Architecture\nFast Reflex + Thinking\nMeta-Executive L3", "#7C3AED", "03"),
        ("4. AI Factory", "Assembly Line\nDeterministic CI Matrix\nKMS Artifact Store", "#D97706", "04"),
        ("5. S&OP Org", "Enterprise Division\nSupply & Demand AI\nAutonomous Protocol", "#EA580C", "05"),
        ("6. Ambient AI", "Zero Cognitive Load\nContext DAG + Skills\nSelf-Healing Loop", "#059669", "06"),
    ]

    # Connecting curve
    xs = np.linspace(1, 11, 200)
    ys = 2.5 + 0.35 * np.sin(np.linspace(0, 3 * np.pi, 200))
    ax.plot(xs, ys, color='#CBD5E1', lw=5, zorder=1)

    for i, (title, sub, col, num) in enumerate(stages):
        x = 1.0 + i * 2.0
        y = 2.5 + 0.35 * np.sin(i * 0.6 * np.pi)

        # Pulse circle
        circle = patches.Circle((x, y), 0.52, facecolor=col, edgecolor='#FFFFFF', lw=3.5, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y - 0.02, num, fontsize=11, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=4)

        # Stage label box
        box_y = y + 0.85 if i % 2 == 0 else y - 1.35
        card = patches.FancyBboxPatch((x - 0.9, box_y), 1.8, 0.95,
                                      boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor='#F8FAFC', edgecolor=col, lw=2.0, zorder=2)
        ax.add_patch(card)
        ax.text(x, box_y + 0.66, title, fontsize=9.5, fontweight='bold', color=col, ha='center', va='center', zorder=4)
        ax.text(x, box_y + 0.30, sub, fontsize=7.2, color='#334155', ha='center', va='center', zorder=4)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "diag_roadmap.png")
    plt.savefig(path, bbox_inches='tight', dpi=240)
    plt.close()
    return path

# ==============================================================================
# DIAGRAM 2: BRAIN-INSPIRED 3-LAYER COGNITIVE SYSTEM
# ==============================================================================
def create_brain_3layer_diagram():
    fig, ax = plt.subplots(figsize=(8.8, 5.5), dpi=240)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    layers = [
        ("Layer 3: Meta-Cognitive / Executive Control",
         "Executive Brain (Prefrontal Cortex)\n- Goal formulation, self-reflection & safety guardrails\n- Long-term Knowledge Graph memory & Cypher path traversal\n- Audits System 1 & 2 for syntax drift and hallucinations",
         "#7C3AED", "#F5F3FF", 5.2, "L3"),
        ("Layer 2: Deliberative Reasoning (System 2)",
         "Deep Deliberative Reasoning\n- High-capacity reasoning models (Claude Sonnet 4.6, DeepSeek)\n- Complex code refactoring, mathematical proofs, multi-turn plans\n- Activated ONLY when Layer 1 identifies non-trivial ambiguity",
         "#0284C7", "#F0F9FF", 2.9, "L2"),
        ("Layer 1: Sensory Reflex & Fast Filter (System 1)",
         "Intuitive Reflex / Spinal Cord\n- Sub-second local execution (WebGPU in-browser + Groq LPU)\n- Regex pattern matching, AST syntax validation, quick probes\n- 100% free / ultra-low latency; absorbs 80% of daily reflexes",
         "#059669", "#F0FDF4", 0.6, "L1")
    ]

    for title, desc, col, bg, y, tag in layers:
        card = patches.FancyBboxPatch((0.5, y), 9.0, 1.8,
                                      boxstyle="round,pad=0.15,rounding_size=0.2",
                                      facecolor=bg, edgecolor=col, lw=2.2, zorder=2)
        ax.add_patch(card)
        
        # Tag badge
        tag_box = patches.FancyBboxPatch((0.7, y + 1.25), 0.75, 0.4,
                                         boxstyle="round,pad=0.05,rounding_size=0.1",
                                         facecolor=col, edgecolor=col, lw=1, zorder=3)
        ax.add_patch(tag_box)
        ax.text(1.075, y + 1.45, tag, fontsize=9.5, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=4)

        ax.text(1.65, y + 1.45, title, fontsize=11, fontweight='bold', color=col, va='center', zorder=3)
        ax.text(0.8, y + 0.68, desc, fontsize=8.2, color='#1E293B', zorder=3, linespacing=1.35)

    # Connecting bi-directional arrows
    ax.annotate('', xy=(5.0, 2.7), xytext=(5.0, 2.5),
                arrowprops=dict(arrowstyle="<->", color="#64748B", lw=2.5))
    ax.annotate('', xy=(5.0, 5.0), xytext=(5.0, 4.8),
                arrowprops=dict(arrowstyle="<->", color="#64748B", lw=2.5))

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "diag_brain.png")
    plt.savefig(path, bbox_inches='tight', dpi=240)
    plt.close()
    return path

# ==============================================================================
# DIAGRAM 3: AI FACTORY & S&OP ORGANIZATIONAL ARCHITECTURE
# ==============================================================================
def create_factory_sop_diagram():
    fig, ax = plt.subplots(figsize=(8.8, 5.4), dpi=240)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Assembly line banner
    ax.text(5.0, 5.6, "THE DETERMINISTIC AI ASSEMBLY LINE", fontsize=10.5, fontweight='bold', color="#0F172A", ha='center')

    stations = [
        ("Station 1", "AST Ingestion\n& Code Parse", "#0284C7"),
        ("Station 2", "Secret Shield\n401 Gate Check", "#D97706"),
        ("Station 3", "48/48 CI Matrix\nGitHub VM Test", "#7C3AED"),
        ("Station 4", "KMS S3 Store\n& Signed Receipt", "#059669"),
    ]

    for i, (st, desc, col) in enumerate(stations):
        x = 0.5 + i * 2.35
        card = patches.FancyBboxPatch((x, 3.8), 2.05, 1.3,
                                      boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor='#FFFFFF', edgecolor=col, lw=2, zorder=2)
        ax.add_patch(card)
        ax.text(x + 1.025, 4.75, st, fontsize=9.5, fontweight='bold', color=col, ha='center', zorder=3)
        ax.text(x + 1.025, 4.25, desc, fontsize=7.8, color='#334155', ha='center', zorder=3)

        if i < 3:
            ax.annotate('', xy=(x + 2.3, 4.45), xytext=(x + 2.05, 4.45),
                        arrowprops=dict(arrowstyle="->", color="#94A3B8", lw=2))

    # S&OP Division Header
    ax.text(5.0, 3.1, "S&OP ENTERPRISE ORGANIZATIONAL MAPPING", fontsize=10.5, fontweight='bold', color="#0F172A", ha='center')

    org_units = [
        ("Demand & Forecast Agent", "Predicts token consumption, compute burst rates & team velocity.", "#0284C7", "DEMAND"),
        ("Operations & SFN Orchestrator", "Runs state machines, Step Functions, and multi-cloud workers.", "#7C3AED", "OPS"),
        ("Governance & Finance Gate", "Dual-tier cost shield ($0 visitor demo vs live project 966273137102).", "#059669", "FINANCE"),
    ]

    for i, (title, desc, col, tag) in enumerate(org_units):
        y = 1.9 - i * 0.9
        card = patches.FancyBboxPatch((0.5, y), 9.0, 0.75,
                                      boxstyle="round,pad=0.08,rounding_size=0.12",
                                      facecolor='#F8FAFC', edgecolor=col, lw=1.6, zorder=2)
        ax.add_patch(card)

        # Tag
        tag_b = patches.FancyBboxPatch((0.7, y + 0.18), 1.1, 0.38,
                                       boxstyle="round,pad=0.05,rounding_size=0.08",
                                       facecolor=col, edgecolor=col, lw=1, zorder=3)
        ax.add_patch(tag_b)
        ax.text(1.25, y + 0.37, tag, fontsize=7.5, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=4)

        ax.text(2.0, y + 0.50, title, fontsize=9, fontweight='bold', color=col, zorder=3)
        ax.text(2.0, y + 0.20, desc, fontsize=7.6, color='#475569', zorder=3)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "diag_factory_sop.png")
    plt.savefig(path, bbox_inches='tight', dpi=240)
    plt.close()
    return path

# ==============================================================================
# DIAGRAM 4: THE 5 AMBIENT AI PILLARS
# ==============================================================================
def create_ambient_pillars_diagram():
    fig, ax = plt.subplots(figsize=(8.8, 5.4), dpi=240)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    pillars = [
        ("1. CHUNKING", "Deconstruct large intents into atomic verifiable micro-tasks.", "#0284C7", "P1"),
        ("2. CONTEXT DAG", "Directed Acyclic Graph routes only prerequisite state node-to-node.", "#7C3AED", "P2"),
        ("3. SKILL TRANSITION", "Proven sequences crystalize into reusable SKILL.md modules.", "#059669", "P3"),
        ("4. ONE-BUTTON REVERSE", "Instant rollback safety net via isolated Git branches & atomic commits.", "#DC2626", "P4"),
        ("5. MULTI-ROUTING", "Dynamic dispatch: Local WebGPU ($0) -> Fast Groq LPU -> Deep Bedrock.", "#D97706", "P5"),
    ]

    for i, (title, desc, col, badge) in enumerate(pillars):
        y = 4.8 - i * 1.15
        card = patches.FancyBboxPatch((0.5, y), 9.0, 0.95,
                                      boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor='#F8FAFC', edgecolor=col, lw=1.8, zorder=2)
        ax.add_patch(card)
        
        # Badge circle
        circ = patches.Circle((1.1, y + 0.48), 0.32, facecolor=col, edgecolor='#FFFFFF', lw=2.0, zorder=3)
        ax.add_patch(circ)
        ax.text(1.1, y + 0.48, badge, fontsize=9.5, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=4)

        ax.text(1.65, y + 0.62, title, fontsize=10, fontweight='bold', color=col, zorder=3)
        ax.text(1.65, y + 0.28, desc, fontsize=8.2, color='#334155', zorder=3)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "diag_ambient_pillars.png")
    plt.savefig(path, bbox_inches='tight', dpi=240)
    plt.close()
    return path

# ==============================================================================
# DIAGRAM 5: HUMAN COGNITIVE LOAD REDUCTION CURVE
# ==============================================================================
def create_cognitive_load_diagram():
    fig, ax = plt.subplots(figsize=(8.8, 5.0), dpi=240)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    stages = ['Single\nAgent', 'Multi\nAgent', '3-Layer\nBrain', 'AI Factory\nPipeline', 'Ambient AI\nErgonomics']
    traditional_load = [95, 110, 80, 55, 12]  # Multi-agent initially caused coordination overhead!
    human_leverage =   [10,  30, 55, 80, 98]

    x = np.arange(len(stages))
    width = 0.35

    rects1 = ax.bar(x - width/2, traditional_load, width, label='Human Cognitive Fatigue (%)', color='#EF4444', alpha=0.88, edgecolor='#DC2626', lw=1.5)
    rects2 = ax.bar(x + width/2, human_leverage, width, label='Autonomous Leverage (%)', color='#10B981', alpha=0.88, edgecolor='#059669', lw=1.5)

    ax.set_ylabel('Percentage (%)', fontsize=10, fontweight='bold', color='#334155')
    ax.set_title('Evolution of Human Cognitive Load vs. Autonomous Leverage', fontsize=11.5, fontweight='bold', color='#0F172A', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(stages, fontsize=9.5, fontweight='bold', color='#334155')
    ax.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=9)
    ax.set_ylim(0, 125)
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # Highlight 90% reduction tag
    ax.annotate('-88% Mental Fatigue\n("Ship it" in 1 click)',
                xy=(4 - width/2, 14), xytext=(3.1, 45),
                arrowprops=dict(facecolor='#059669', shrink=0.08, width=2, headwidth=8),
                fontsize=8.5, fontweight='bold', color='#047857',
                bbox=dict(boxstyle="round,pad=0.4", fc="#ECFDF5", ec="#10B981", lw=1.5))

    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color('#CBD5E1')

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "diag_cognitive_load.png")
    plt.savefig(path, bbox_inches='tight', dpi=240)
    plt.close()
    return path

# Generate all diagrams
d_roadmap = create_roadmap_diagram()
d_brain = create_brain_3layer_diagram()
d_factory = create_factory_sop_diagram()
d_ambient = create_ambient_pillars_diagram()
d_load = create_cognitive_load_diagram()

print("All diagrams generated cleanly without any font warnings!")

# ==============================================================================
# POWERPOINT SLIDES ASSEMBLY
# ==============================================================================
prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return RGBColor(*(int(hex_str[i:i+2], 16) for i in (0, 2, 4)))

def add_header(slide, title_text, category_badge, subtitle_text):
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = hex_to_rgb("#FFFFFF")
    top_bar.line.color.rgb = hex_to_rgb("#E2E8F0")
    top_bar.line.width = Pt(1)

    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.18), Inches(2.2), Inches(0.32))
    pill.fill.solid()
    pill.fill.fore_color.rgb = hex_to_rgb("#0284C7")
    pill.line.fill.background()
    tf_p = pill.text_frame
    tf_p.text = category_badge.upper()
    tf_p.paragraphs[0].font.size = Pt(9.5)
    tf_p.paragraphs[0].font.bold = True
    tf_p.paragraphs[0].font.color.rgb = hex_to_rgb("#FFFFFF")
    tf_p.paragraphs[0].alignment = PP_ALIGN.CENTER

    tx_box = slide.shapes.add_textbox(Inches(3.2), Inches(0.1), Inches(9.5), Inches(0.5))
    tf = tx_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = hex_to_rgb("#0F172A")

    tx_sub = slide.shapes.add_textbox(Inches(0.8), Inches(0.58), Inches(11.8), Inches(0.45))
    tf_s = tx_sub.text_frame
    p_s = tf_s.paragraphs[0]
    p_s.text = subtitle_text
    p_s.font.size = Pt(11)
    p_s.font.color.rgb = hex_to_rgb("#64748B")

def add_card(slide, left, top, width, height, bg_color="#FFFFFF", border_color="#CBD5E1"):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = hex_to_rgb(bg_color)
    card.line.color.rgb = hex_to_rgb(border_color)
    card.line.width = Pt(1.5)
    return card

# ------------------------------------------------------------------------------
# SLIDE 1: COVER
# ------------------------------------------------------------------------------
s1 = prs.slides.add_slide(blank_layout)

hero = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
hero.fill.solid()
hero.fill.fore_color.rgb = hex_to_rgb("#0F172A")
hero.line.fill.background()

cover_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1))
cover_card.fill.solid()
cover_card.fill.fore_color.rgb = hex_to_rgb("#1E293B")
cover_card.line.color.rgb = hex_to_rgb("#38BDF8")
cover_card.line.width = Pt(2)

c_tf = cover_card.text_frame
c_tf.vertical_anchor = MSO_ANCHOR.MIDDLE

p1 = c_tf.paragraphs[0]
p1.text = "THE AUTONOMOUS ODYSSEY"
p1.font.size = Pt(14)
p1.font.bold = True
p1.font.color.rgb = hex_to_rgb("#38BDF8")
p1.alignment = PP_ALIGN.CENTER

p2 = c_tf.add_paragraph()
p2.text = "From Single Agent to Ambient AI Enterprise"
p2.font.size = Pt(32)
p2.font.bold = True
p2.font.color.rgb = hex_to_rgb("#FFFFFF")
p2.alignment = PP_ALIGN.CENTER

p3 = c_tf.add_paragraph()
p3.text = "A Journey Through 3-Layer Cognitive Brains, Factory Assembly Lines, S&OP Organizations, and Zero-Cognitive-Load Ambient AI"
p3.font.size = Pt(13)
p3.font.color.rgb = hex_to_rgb("#94A3B8")
p3.alignment = PP_ALIGN.CENTER

p4 = c_tf.add_paragraph()
p4.text = "\nSimple  *  Intuitive  *  Graphical  *  Fun  *  Autonomous"
p4.font.size = Pt(13)
p4.font.bold = True
p4.font.color.rgb = hex_to_rgb("#34D399")
p4.alignment = PP_ALIGN.CENTER

# ------------------------------------------------------------------------------
# SLIDE 2: ROADMAP OVERVIEW
# ------------------------------------------------------------------------------
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "The 6 Eras of the Autonomous Evolution", "Evolution Map", "Visualizing how our architecture matured from brute-force prompts to an intelligent autonomous organization")
s2.shapes.add_picture(d_roadmap, Inches(0.8), Inches(1.35), width=Inches(11.733))

c1 = add_card(s2, 0.8, 5.7, 3.6, 1.45, "#F0F9FF", "#0284C7")
t1 = c1.text_frame
t1.paragraphs[0].text = "Phase 1: Tool Execution"
t1.paragraphs[0].font.bold = True
t1.paragraphs[0].font.size = Pt(11)
t1.paragraphs[0].font.color.rgb = hex_to_rgb("#0369A1")
p = t1.add_paragraph()
p.text = "Early single/multi-agent scripts acting as simple task runners. Required high human babysitting and constant prompt tweaking."
p.font.size = Pt(9)
p.font.color.rgb = hex_to_rgb("#334155")

c2 = add_card(s2, 4.85, 5.7, 3.6, 1.45, "#F5F3FF", "#7C3AED")
t2 = c2.text_frame
t2.paragraphs[0].text = "Phase 2: Cognitive Factories"
t2.paragraphs[0].font.bold = True
t2.paragraphs[0].font.size = Pt(11)
t2.paragraphs[0].font.color.rgb = hex_to_rgb("#6D28D9")
p = t2.add_paragraph()
p.text = "Brain-inspired 3-tier cognition + standardized assembly lines. S&OP role division and deterministic verification gates."
p.font.size = Pt(9)
p.font.color.rgb = hex_to_rgb("#334155")

c3 = add_card(s2, 8.9, 5.7, 3.6, 1.45, "#F0FDF4", "#059669")
t3 = c3.text_frame
t3.paragraphs[0].text = "Phase 3: Ambient Intelligence"
t3.paragraphs[0].font.bold = True
t3.paragraphs[0].font.size = Pt(11)
t3.paragraphs[0].font.color.rgb = hex_to_rgb("#047857")
p = t3.add_paragraph()
p.text = "Context DAGs, self-healing skills, one-button rollbacks. AI runs quietly in the ambient background with near-zero human fatigue."
p.font.size = Pt(9)
p.font.color.rgb = hex_to_rgb("#334155")

# ------------------------------------------------------------------------------
# SLIDE 3: MILESTONES 1 & 2
# ------------------------------------------------------------------------------
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "From Lone Wolf to the Specialized Squad", "Milestones 1 & 2", "Breaking out of the single-prompt trap by assembling cooperative specialized agents")

c_left = add_card(s3, 0.8, 1.4, 5.6, 5.6, "#FFFFFF", "#94A3B8")
tl = c_left.text_frame
p = tl.paragraphs[0]
p.text = "MILESTONE 1: The Lone Wolf (Single Agent)"
p.font.bold = True
p.font.size = Pt(13)
p.font.color.rgb = hex_to_rgb("#0F172A")

bullets_l = [
    ("Concept", "One giant prompt attempting to be architect, coder, tester, and deployer simultaneously."),
    ("The Pain Point", "Context rot: as conversations grew past 50 turns, the lone agent forgot previous constraints and hallucinated."),
    ("Bottleneck", "Linear thinking with 0 peer review. If the model made a false assumption at step 1, the entire codebase broke."),
    ("Fun Analogy", "Asking a single intern to build a skyscraper, draft legal contracts, and inspect plumbing alone.")
]
for title, desc in bullets_l:
    p = tl.add_paragraph()
    p.text = f"- {title}: {desc}"
    p.font.size = Pt(10)
    p.font.color.rgb = hex_to_rgb("#334155")

c_right = add_card(s3, 6.9, 1.4, 5.6, 5.6, "#FFFFFF", "#0284C7")
tr = c_right.text_frame
p = tr.paragraphs[0]
p.text = "MILESTONE 2: The Squad (Multi-Agent Systems)"
p.font.bold = True
p.font.size = Pt(13)
p.font.color.rgb = hex_to_rgb("#0369A1")

bullets_r = [
    ("Concept", "Role specialization: Researcher, Architect, Coder, and QA Critic working in tandem."),
    ("The Breakthrough", "Cross-verification: The Coder cannot push until the QA Critic asserts exit code 0."),
    ("The Emerging Challenge", "Coordination tax: Agents chatting endlessly in loops ('After you!' 'No, after you!') consuming massive tokens."),
    ("Key Lesson", "Specialization is essential, but without hierarchical cognitive control, multi-agent teams drift into chaos.")
]
for title, desc in bullets_r:
    p = tr.add_paragraph()
    p.text = f"- {title}: {desc}"
    p.font.size = Pt(10)
    p.font.color.rgb = hex_to_rgb("#334155")

# ------------------------------------------------------------------------------
# SLIDE 4: BRAIN-INSPIRED 3-LAYER COGNITION
# ------------------------------------------------------------------------------
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "Brain-Inspired Cognitive Architecture (3 Layers)", "Milestone 3", "Mimicking biological cognitive hierarchy to balance instant reflexes with deep deliberative reason")

c_brain_l = add_card(s4, 0.8, 1.35, 4.2, 5.7, "#F8FAFC", "#7C3AED")
tbl = c_brain_l.text_frame
p = tbl.paragraphs[0]
p.text = "Biological Cognition in AI"
p.font.bold = True
p.font.size = Pt(13)
p.font.color.rgb = hex_to_rgb("#6D28D9")

b_items = [
    ("Why 3 Layers?", "The human brain doesn't fire millions of neurons to blink an eyelid. Fast tasks stay in the spinal cord; only novel dilemmas wake the prefrontal cortex."),
    ("Layer 1 (Reflex)", "WebGPU in-browser + Groq LPU. Handles AST syntax, regex gates, and pre-flight probes at 0ms cost."),
    ("Layer 2 (Deliberation)", "Heavyweight LLMs (Claude Sonnet 4.6). Engaged only for complex synthesis, algorithmic proofs, and code diffs."),
    ("Layer 3 (Meta-Cognitive)", "The Executive Monitor. Keeps long-term Knowledge Graph memory, verifies goal alignment, and halts runaways."),
    ("Fun Takeaway", "Stop burning $0.05 on cloud models to verify if a semicolon exists!")
]
for title, desc in b_items:
    p = tbl.add_paragraph()
    p.text = f"- {title}: {desc}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = hex_to_rgb("#334155")

s4.shapes.add_picture(d_brain, Inches(5.2), Inches(1.35), width=Inches(7.333))

# ------------------------------------------------------------------------------
# SLIDE 5: THE AI FACTORY
# ------------------------------------------------------------------------------
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "The AI Factory: Industrializing Software Construction", "Milestone 4", "Replacing artisanal prompt crafting with standardized assembly lines and deterministic quality gates")

c_fac_l = add_card(s5, 0.8, 1.35, 4.2, 5.7, "#F8FAFC", "#D97706")
tfl = c_fac_l.text_frame
p = tfl.paragraphs[0]
p.text = "Industrializing Intelligence"
p.font.bold = True
p.font.size = Pt(13)
p.font.color.rgb = hex_to_rgb("#B45309")

f_items = [
    ("The Factory Metaphor", "Henry Ford didn't build cars by giving 10 workers vague verbal instructions. He built a conveyor belt with specialized stations and rigorous tollgates."),
    ("Deterministic Gates", "AI is probabilistic; code execution is deterministic. The factory wraps LLMs in rigid CI assertion matrices (48/48 checks)."),
    ("Automated Testing VM", "GitHub Actions ubuntu-latest runners act as robotic inspectors, auditing builds for secrets and syntax drift."),
    ("Cryptographic Storage", "Verified artifacts are sealed into Amazon S3 with KMS encryption and return signed execution receipts."),
    ("Fun Takeaway", "Treat prompts like machine tooling, not creative writing!")
]
for title, desc in f_items:
    p = tfl.add_paragraph()
    p.text = f"- {title}: {desc}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = hex_to_rgb("#334155")

s5.shapes.add_picture(d_factory, Inches(5.2), Inches(1.35), width=Inches(7.333))

# ------------------------------------------------------------------------------
# SLIDE 6: S&OP & ORGANIZATION
# ------------------------------------------------------------------------------
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "Organization of Workers: S&OP Corporate Governance", "Milestone 5", "Structuring autonomous agents into cross-functional business departments with budgets and protocol")

deps = [
    ("Demand & Capacity Planning Agent",
     "- Anticipates upcoming project workload and calculates token quotas.\n- Forecasts compute burst needs across local vs cloud models.\n- Balances team velocity against API rate limits and quotas.",
     "#0284C7", "#F0F9FF", 0.8),
    ("Operational Assembly & Step Functions",
     "- Converts business objectives into state machines and workflow graphs.\n- Dispatches specialized subagents with isolated branch workspaces.\n- Aggregates telemetry across GitHub Actions and AWS us-east-2.",
     "#7C3AED", "#F5F3FF", 4.85),
    ("Finance, Security & Cost Shield",
     "- Dual-Tier Spending Governance: Enforces $0 visitor demo safety net.\n- Unlocks live AWS Bedrock & S3 only when Owner Passcode is verified.\n- Generates signed audit one-pagers for executive governance.",
     "#059669", "#F0FDF4", 8.9),
]

for title, desc, col, bg, left in deps:
    c = add_card(s6, left, 1.4, 3.6, 5.6, bg, col)
    tf = c.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = hex_to_rgb(col)
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = hex_to_rgb("#1E293B")
    p2.line_spacing = 1.3

# ------------------------------------------------------------------------------
# SLIDE 7: AMBIENT AI & THE 5 PILLARS
# ------------------------------------------------------------------------------
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "Ambient AI: The 5 Pillars of Invisible Ergonomics", "Milestone 6", "Moving from active prompt manipulation to quiet, ambient background autonomy")

c_amb_l = add_card(s7, 0.8, 1.35, 4.2, 5.7, "#F8FAFC", "#059669")
tal = c_amb_l.text_frame
p = tal.paragraphs[0]
p.text = "What is Ambient AI?"
p.font.bold = True
p.font.size = Pt(13)
p.font.color.rgb = hex_to_rgb("#047857")

amb_items = [
    ("Invisible Autonomy", "AI shouldn't demand your constant attention. It should operate like electricity in the wall: always on, reliable, invisible until called."),
    ("Zero Context Bloat", "Instead of dumping 100,000 tokens into every turn, context is managed as an active Directed Acyclic Graph (DAG)."),
    ("Evolution to Skills", "When an agent discovers a reliable workflow, it packages it into a permanent SKILL.md so it never has to re-learn it."),
    ("Reversible Safety", "Total psychological safety: any change can be rolled back in one click via atomic Git branches."),
    ("Fun Takeaway", "The ultimate luxury in AI is not a chatbox - it's not having to chat at all!")
]
for title, desc in amb_items:
    p = tal.add_paragraph()
    p.text = f"- {title}: {desc}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = hex_to_rgb("#334155")

s7.shapes.add_picture(d_ambient, Inches(5.2), Inches(1.35), width=Inches(7.333))

# ------------------------------------------------------------------------------
# SLIDE 8: MINIMIZING HUMAN COGNITIVE LOAD
# ------------------------------------------------------------------------------
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "The North Star: Minimizing Human Cognitive Load", "Human Ergonomics", "Transforming human operators from stressed micromanagers into confident directors")

c_cmp = add_card(s8, 0.8, 1.35, 4.2, 5.7, "#FFFFFF", "#DC2626")
tcmp = c_cmp.text_frame
p = tcmp.paragraphs[0]
p.text = "The Babysitting Trap vs. Ambient Ease"
p.font.bold = True
p.font.size = Pt(11)
p.font.color.rgb = hex_to_rgb("#DC2626")

p_old = tcmp.add_paragraph()
p_old.text = "\nOLD WAY: Human Micromanager\n- Paste stack trace -> read code -> ask model\n- Copy snippet -> test manually -> hit syntax bug\n- Repeat 40 times per hour -> Extreme mental fatigue"
p_old.font.size = Pt(9)
p_old.font.color.rgb = hex_to_rgb("#991B1B")

p_new = tcmp.add_paragraph()
p_new.text = "\nAMBIENT WAY: Executive Director\n- Human says: 'Proceed' or 'Ship it'\n- AI team evaluates DAG, runs CI matrix, pushes commit\n- Delivers signed receipt + PDF summary\n- 90% cognitive load eliminated!"
p_new.font.size = Pt(9)
p_new.font.color.rgb = hex_to_rgb("#065F46")

s8.shapes.add_picture(d_load, Inches(5.2), Inches(1.35), width=Inches(7.333))

# ------------------------------------------------------------------------------
# SLIDE 9: ARCHITECTURAL BLUEPRINT
# ------------------------------------------------------------------------------
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "Production Tech Stack & Live Cloud Bridge", "Tech Showcase", "Real-world infrastructure proven across GitHub Actions and AWS Project us-east-2 (966273137102)")

tech_blocks = [
    ("Client & Reflex Layer", "- WebGPU in-browser shader acceleration\n- WebLLM local 360M inference ($0 cost)\n- Real-time Canvas telemetry packet visualizer", "#0284C7", 0.8, 1.4),
    ("GitHub CI/CD Automation", "- 4 Automated robot jobs (AST, Secrets, Matrix, 401)\n- ubuntu-latest free public cloud runners\n- Ed25519 SSH key signing for live Git pushes", "#7C3AED", 4.85, 1.4),
    ("AWS Cloud Core (us-east-2)", "- Lambda HTTPS Gateway with SHA-256 header gate\n- Bedrock Claude Sonnet 4.6 Mantle Converse API\n- Step Functions state machines & KMS S3 bucket", "#D97706", 8.9, 1.4),
    ("AI Knowledge & Database", "- Vector Database with cosine similarity search\n- Knowledge Graph with Cypher multi-hop traversals\n- Context DAG memory indexing & skill registry", "#059669", 0.8, 4.3),
    ("Dual-Mode Security Gate", "- Non-Owner Visitor Mode: 100% free $0 demo\n- Owner Passcode Mode: Real AWS us-east-2 access\n- Zero secret leakage guarantee via regex auditor", "#DC2626", 4.85, 4.3),
    ("Executive Synthesis", "- Automated 1-page visual PDF guides\n- Cryptographic telemetry receipts\n- Executive bullet point audit stream", "#475569", 8.9, 4.3),
]

for title, desc, col, left, top in tech_blocks:
    c = add_card(s9, left, top, 3.6, 2.65, "#FFFFFF", col)
    tf = c.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = hex_to_rgb(col)
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(8.8)
    p2.font.color.rgb = hex_to_rgb("#334155")
    p2.line_spacing = 1.25

# ------------------------------------------------------------------------------
# SLIDE 10: CONCLUSION & FUTURE VISION
# ------------------------------------------------------------------------------
s10 = prs.slides.add_slide(blank_layout)

end_card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
end_card.fill.solid()
end_card.fill.fore_color.rgb = hex_to_rgb("#0F172A")
end_card.line.color.rgb = hex_to_rgb("#10B981")
end_card.line.width = Pt(2.5)

tf_end = end_card.text_frame
tf_end.vertical_anchor = MSO_ANCHOR.MIDDLE

p = tf_end.paragraphs[0]
p.text = "THE FUTURE OF AI ORGANIZATIONS"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = hex_to_rgb("#34D399")
p.alignment = PP_ALIGN.CENTER

p = tf_end.add_paragraph()
p.text = "From Chatting with Models to Conducting Orchestras"
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = hex_to_rgb("#FFFFFF")
p.alignment = PP_ALIGN.CENTER

p = tf_end.add_paragraph()
p.text = "\nKey Takeaways from Our Journey:\n"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = hex_to_rgb("#94A3B8")
p.alignment = PP_ALIGN.CENTER

takeaways = [
    "1. Lone agents hit context ceilings; 3-Layer Brains distribute cognition from instant reflexes to deep deliberation.",
    "2. The AI Factory turns unpredictable hallucinations into certified 48/48 CI matrix software builds.",
    "3. S&OP organizational structures allow multi-agent teams to forecast, operate, and govern autonomously.",
    "4. Ambient AI makes the entire apparatus invisible: you speak your intent, and the organization executes with total safety."
]
for t in takeaways:
    p = tf_end.add_paragraph()
    p.text = t
    p.font.size = Pt(11)
    p.font.color.rgb = hex_to_rgb("#F1F5F9")
    p.alignment = PP_ALIGN.CENTER

p_quote = tf_end.add_paragraph()
p_quote.text = "\n\"The best AI system is the one you don't have to micromanage.\""
p_quote.font.size = Pt(14)
p_quote.font.bold = True
p_quote.font.color.rgb = hex_to_rgb("#38BDF8")
p_quote.alignment = PP_ALIGN.CENTER

# Save presentation
prs.save(PPTX_PATH)
prs.save(PPTX_LOCAL_PATH)
print(f"Presentation saved successfully to:\n1. {PPTX_PATH}\n2. {PPTX_LOCAL_PATH}")
