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
        ("3. 3-Layer Brain", "Cognitive Hierarchy\nFast Reflex + Thinking\nMeta-Executive L3", "#7C3AED", "03"),
        ("4. AI Factory", "Assembly Line\nDeterministic CI Matrix\nCertified Artifacts", "#D97706", "04"),
        ("5. Ambient AI", "Invisible Autonomy\nContext DAG + Skills\nOne-Button Reverse", "#059669", "05"),
        ("6. Zero Mental Load", "Ambient Ergonomics\n-88% Cognitive Burden\n1-Click Execution", "#4338CA", "06"),
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
         "Intuitive Reflex / Spinal Cord\n- Sub-second local execution (fast AST parsers & regex gates)\n- Pattern matching, syntax validation, pre-flight environment probes\n- Absorbs 80% of daily reflexes with zero delay",
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
# DIAGRAM 3: THE AI FACTORY & ASSEMBLY WORKERS
# ==============================================================================
def create_factory_workers_diagram():
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
        ("Station 2", "Secret Shield\nSecurity Audit", "#D97706"),
        ("Station 3", "48/48 CI Matrix\nAutomated Test", "#7C3AED"),
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

    # Assembly Workers Division Header
    ax.text(5.0, 3.1, "AI FACTORY ASSEMBLY WORKER SPECIALIZATION", fontsize=10.5, fontweight='bold', color="#0F172A", ha='center')

    worker_units = [
        ("Architecture & Contract Worker", "Decomposes high-level requirements into atomic component specifications and AST schemas.", "#0284C7", "ARCH"),
        ("Synthesis & Code Worker", "Constructs clean, modular code units with live self-correcting unit test validation.", "#7C3AED", "CODE"),
        ("Verification & Packaging Worker", "Executes automated test matrix, validates security constraints, and seals verified artifacts.", "#059669", "VERIFY"),
    ]

    for i, (title, desc, col, tag) in enumerate(worker_units):
        y = 1.9 - i * 0.9
        card = patches.FancyBboxPatch((0.5, y), 9.0, 0.75,
                                      boxstyle="round,pad=0.08,rounding_size=0.12",
                                      facecolor='#F8FAFC', edgecolor=col, lw=1.6, zorder=2)
        ax.add_patch(card)

        # Tag
        tag_b = patches.FancyBboxPatch((0.7, y + 0.18), 1.15, 0.38,
                                       boxstyle="round,pad=0.05,rounding_size=0.08",
                                       facecolor=col, edgecolor=col, lw=1, zorder=3)
        ax.add_patch(tag_b)
        ax.text(1.275, y + 0.37, tag, fontsize=7.5, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=4)

        ax.text(2.1, y + 0.50, title, fontsize=9, fontweight='bold', color=col, zorder=3)
        ax.text(2.1, y + 0.20, desc, fontsize=7.6, color='#475569', zorder=3)

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
        ("1. CHUNKING", "Deconstruct large intents into atomic verifiable micro-tasks (<50 lines).", "#0284C7", "P1"),
        ("2. CONTEXT DAG", "Directed Acyclic Graph routes only prerequisite state node-to-node without context bloat.", "#7C3AED", "P2"),
        ("3. SKILL TRANSITION", "Proven execution sequences crystalize into permanent, reusable SKILL.md modules.", "#059669", "P3"),
        ("4. ONE-BUTTON REVERSE", "Instant rollback safety net via isolated Git branches & atomic commits.", "#DC2626", "P4"),
        ("5. MULTI-ROUTING", "Dynamic dispatch: Fast Local Reflex -> Specialized LPUs -> Deep Frontier Models.", "#D97706", "P5"),
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
    fig, ax = plt.subplots(figsize=(8.8, 5.2), dpi=240)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    stages = ['Single\nAgent', 'Multi\nAgent', '3-Layer\nBrain', 'AI Factory\nAssembly', 'Ambient AI\nErgonomics']
    traditional_load = [95, 110, 80, 50, 12]  # Multi-agent initially caused coordination overhead!
    human_leverage =   [10,  30, 55, 82, 98]

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

    # Highlight 88% reduction tag
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

# ==============================================================================
# DIAGRAM 6: GRAPHICAL PRODUCTION TECH STACK SHOWCASE
# ==============================================================================
def create_tech_stack_diagram():
    fig, ax = plt.subplots(figsize=(10.8, 5.6), dpi=240)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7)
    ax.axis('off')

    tiers = [
        ('TIER 1: CLIENT REFLEX & SENSORY FILTER', '#0284C7', '#F0F9FF', 5.35, [
            ('Sub-Second AST Parser', 'Parses syntax & validates structure locally'),
            ('Regex Pre-Flight Gate', 'Scans for secrets & unauthorized patterns'),
            ('Live Telemetry Stream', 'Real-time packet telemetry & state monitor')
        ]),
        ('TIER 2: CI/CD AUTOMATED FACTORY PIPELINE', '#7C3AED', '#F5F3FF', 3.65, [
            ('CI Isolated Runner', 'Ephemeral clean-room virtual test environments'),
            ('48/48 CI Test Matrix', 'Rigid automated pass/fail assertion suite'),
            ('Ed25519 Signer & Git', 'Cryptographic commit & artifact attestation')
        ]),
        ('TIER 3: AWS PRODUCTION CLOUD (us-east-2)', '#D97706', '#FFFBEB', 1.95, [
            ('Lambda HTTPS Gate', 'SHA-256 header check & secure ingress'),
            ('Step Functions & Bedrock', 'Multi-agent state machines + Claude Sonnet'),
            ('Amazon KMS Encrypted S3', 'Tamper-proof storage with signed receipts')
        ]),
        ('TIER 4: COGNITIVE MEMORY & DEPENDENCY ENGINE', '#059669', '#F0FDF4', 0.25, [
            ('Vector DB Semantic RAG', 'Cosine similarity embeddings & fast search'),
            ('Knowledge Graph DB', 'Cypher multi-hop relational path traversal'),
            ('Context DAG Cache', 'Prerequisite node routing with zero bloat')
        ])
    ]

    for title, col, bg, y, subs in tiers:
        card = patches.FancyBboxPatch((0.4, y), 10.2, 1.45,
                                      boxstyle='round,pad=0.08,rounding_size=0.12',
                                      facecolor=bg, edgecolor=col, lw=1.8, zorder=2)
        ax.add_patch(card)
        
        # Title badge
        tb = patches.FancyBboxPatch((0.6, y + 1.1), 3.4, 0.28,
                                    boxstyle='round,pad=0.04,rounding_size=0.06',
                                    facecolor=col, edgecolor=col, lw=1, zorder=3)
        ax.add_patch(tb)
        ax.text(2.3, y + 1.24, title, fontsize=8.2, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=4)

        # 3 sub-boxes
        for j, (st, sd) in enumerate(subs):
            sx = 0.6 + j * 3.3
            sub_card = patches.FancyBboxPatch((sx, y + 0.12), 3.15, 0.88,
                                              boxstyle='round,pad=0.05,rounding_size=0.08',
                                              facecolor='#FFFFFF', edgecolor=col, lw=1.0, zorder=3)
            ax.add_patch(sub_card)
            ax.text(sx + 1.575, y + 0.72, st, fontsize=8.5, fontweight='bold', color=col, ha='center', va='center', zorder=4)
            ax.text(sx + 1.575, y + 0.38, sd, fontsize=7.2, color='#334155', ha='center', va='center', zorder=4)

    # Connecting vertical flow arrows on the right
    for y_arr in [5.3, 3.6, 1.9]:
        ax.annotate('', xy=(10.7, y_arr - 0.25), xytext=(10.7, y_arr + 0.25),
                    arrowprops=dict(arrowstyle='->', color='#64748B', lw=2.5))
    ax.text(10.7, 3.5, 'DATA & EXECUTION FLOW', fontsize=7.5, fontweight='bold', color='#64748B', rotation=270, ha='center', va='center')

    plt.tight_layout()
    p = os.path.join(OUT_DIR, 'diag_tech_stack.png')
    plt.savefig(p, bbox_inches='tight', dpi=240)
    plt.close()
    return p

# Generate all diagrams
d_roadmap = create_roadmap_diagram()
d_brain = create_brain_3layer_diagram()
d_factory = create_factory_workers_diagram()
d_ambient = create_ambient_pillars_diagram()
d_load = create_cognitive_load_diagram()
d_stack = create_tech_stack_diagram()

print("All diagrams generated cleanly without any font warnings!")

# ==============================================================================
# POWERPOINT SLIDES ASSEMBLY (9 TIGHT, HIGH-IMPACT SLIDES)
# ==============================================================================
prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return RGBColor(*(int(hex_str[i:i+2], 16) for i in (0, 2, 4)))

def setup_text_frame(tf):
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    tf.margin_bottom = Inches(0.2)

def add_header(slide, title_text, category_badge, subtitle_text):
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = hex_to_rgb("#FFFFFF")
    top_bar.line.color.rgb = hex_to_rgb("#E2E8F0")
    top_bar.line.width = Pt(1)

    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.18), Inches(2.3), Inches(0.32))
    pill.fill.solid()
    pill.fill.fore_color.rgb = hex_to_rgb("#0284C7")
    pill.line.fill.background()
    tf_p = pill.text_frame
    setup_text_frame(tf_p)
    tf_p.text = category_badge.upper()
    tf_p.paragraphs[0].font.size = Pt(9.5)
    tf_p.paragraphs[0].font.bold = True
    tf_p.paragraphs[0].font.color.rgb = hex_to_rgb("#FFFFFF")
    tf_p.paragraphs[0].alignment = PP_ALIGN.CENTER

    tx_box = slide.shapes.add_textbox(Inches(3.3), Inches(0.1), Inches(9.5), Inches(0.5))
    tf = tx_box.text_frame
    setup_text_frame(tf)
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = hex_to_rgb("#0F172A")

    tx_sub = slide.shapes.add_textbox(Inches(0.8), Inches(0.58), Inches(11.8), Inches(0.45))
    tf_s = tx_sub.text_frame
    setup_text_frame(tf_s)
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
    setup_text_frame(card.text_frame)
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
setup_text_frame(c_tf)
c_tf.vertical_anchor = MSO_ANCHOR.MIDDLE

p1 = c_tf.paragraphs[0]
p1.text = "THE AUTONOMOUS ODYSSEY"
p1.font.size = Pt(14)
p1.font.bold = True
p1.font.color.rgb = hex_to_rgb("#38BDF8")
p1.alignment = PP_ALIGN.CENTER

p2 = c_tf.add_paragraph()
p2.text = "From Single Agent to Ambient AI"
p2.font.size = Pt(32)
p2.font.bold = True
p2.font.color.rgb = hex_to_rgb("#FFFFFF")
p2.alignment = PP_ALIGN.CENTER

p3 = c_tf.add_paragraph()
p3.text = "A Journey Through 3-Layer Cognitive Brains, Factory Assembly Workers, and Zero-Cognitive-Load Ambient AI"
p3.font.size = Pt(13)
p3.font.color.rgb = hex_to_rgb("#94A3B8")
p3.alignment = PP_ALIGN.CENTER

# ------------------------------------------------------------------------------
# SLIDE 2: ROADMAP OVERVIEW
# ------------------------------------------------------------------------------
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "The Evolutionary Path of Autonomous AI", "Evolution Map", "Visualizing how our architecture matured from brute-force prompts to an intelligent autonomous ecosystem")
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
p.text = "Brain-inspired 3-tier cognition + AI Factory assembly workers with deterministic verification gates."
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
    ("Key Analogy", "Asking a single intern to build a skyscraper, draft legal contracts, and inspect plumbing alone.")
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
    ("The Emerging Challenge", "Coordination tax: Agents chatting endlessly in loops ('After you!' 'No, after you!') consuming massive context."),
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
    ("Layer 1 (Reflex)", "Fast local/edge filter. Handles AST syntax, regex gates, and pre-flight probes with sub-second latency."),
    ("Layer 2 (Deliberation)", "Heavyweight deliberative LLMs (Claude Sonnet 4.6). Engaged only for complex synthesis, algorithmic proofs, and code diffs."),
    ("Layer 3 (Meta-Cognitive)", "The Executive Monitor. Maintains long-term Knowledge Graph memory, verifies goal alignment, and halts runaways."),
    ("Core Takeaway", "Stop waking heavy frontier models to verify if a semicolon exists!")
]
for title, desc in b_items:
    p = tbl.add_paragraph()
    p.text = f"- {title}: {desc}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = hex_to_rgb("#334155")

s4.shapes.add_picture(d_brain, Inches(5.2), Inches(1.35), width=Inches(7.333))

# ------------------------------------------------------------------------------
# SLIDE 5: THE AI FACTORY & ASSEMBLY WORKERS (ONE COMPLETE SLIDE)
# ------------------------------------------------------------------------------
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "The AI Factory & Assembly Workers", "Milestone 4", "Replacing artisanal prompt crafting with standardized assembly lines and specialized worker roles")

c_fac_l = add_card(s5, 0.8, 1.35, 4.2, 5.7, "#F8FAFC", "#D97706")
tfl = c_fac_l.text_frame
p = tfl.paragraphs[0]
p.text = "The Industrial AI Paradigm"
p.font.bold = True
p.font.size = Pt(13)
p.font.color.rgb = hex_to_rgb("#B45309")

f_items = [
    ("The Assembly Metaphor", "Henry Ford didn't build cars by shouting vague verbal orders. He built a conveyor belt with specialized stations and strict tollgates."),
    ("Assembly Workers", "Specialized agents (Architect, Coder, Verifier) execute discrete tasks with clean contracts (<50 lines)."),
    ("Deterministic Gates", "AI is probabilistic; code execution is deterministic. The factory wraps LLMs in rigid 48/48 CI matrix tests."),
    ("Automated Testing VM", "GitHub Actions runners act as robotic inspectors, auditing diffs for secrets and syntax drift before commit."),
    ("Certified Storage", "Verified artifacts are sealed into Amazon S3 with KMS encryption and verifiable attestation receipts."),
    ("Core Takeaway", "Treat prompts like machine tooling, not creative writing!")
]
for title, desc in f_items:
    p = tfl.add_paragraph()
    p.text = f"- {title}: {desc}"
    p.font.size = Pt(9.2)
    p.font.color.rgb = hex_to_rgb("#334155")

s5.shapes.add_picture(d_factory, Inches(5.2), Inches(1.35), width=Inches(7.333))

# ------------------------------------------------------------------------------
# SLIDE 6: AMBIENT AI & THE 5 PILLARS
# ------------------------------------------------------------------------------
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "Ambient AI: The 5 Pillars of Invisible Ergonomics", "Milestone 5", "Moving from active prompt manipulation to quiet, ambient background autonomy")

c_amb_l = add_card(s6, 0.8, 1.35, 4.2, 5.7, "#F8FAFC", "#059669")
tal = c_amb_l.text_frame
p = tal.paragraphs[0]
p.text = "What is Ambient AI?"
p.font.bold = True
p.font.size = Pt(13)
p.font.color.rgb = hex_to_rgb("#047857")

amb_items = [
    ("Invisible Autonomy", "AI shouldn't demand your constant attention. It should operate like electricity: always on, reliable, invisible until called."),
    ("Zero Context Bloat", "Instead of dumping 100,000 tokens into every turn, context is managed as an active Directed Acyclic Graph (DAG)."),
    ("Evolution to Skills", "When an agent discovers a reliable workflow, it packages it into a permanent SKILL.md so it never has to re-learn it."),
    ("Reversible Safety", "Total psychological safety: any change can be rolled back in one click via atomic Git branches."),
    ("Core Takeaway", "The ultimate luxury in AI is not a chatbox - it's not having to chat at all!")
]
for title, desc in amb_items:
    p = tal.add_paragraph()
    p.text = f"- {title}: {desc}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = hex_to_rgb("#334155")

s6.shapes.add_picture(d_ambient, Inches(5.2), Inches(1.35), width=Inches(7.333))

# ------------------------------------------------------------------------------
# SLIDE 7: MINIMIZING HUMAN COGNITIVE LOAD (FIXED VISUAL COMPARISON)
# ------------------------------------------------------------------------------
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "The North Star: Minimizing Human Cognitive Load", "Milestone 6", "Transforming human operators from stressed micromanagers into confident directors")

# Card 1: Top Left (The Micromanager Trap - Red)
c_old = add_card(s7, 0.8, 1.35, 4.2, 2.75, "#FEF2F2", "#EF4444")
to = c_old.text_frame
p = to.paragraphs[0]
p.text = "OLD WAY: The Babysitting Trap"
p.font.bold = True
p.font.size = Pt(11.5)
p.font.color.rgb = hex_to_rgb("#DC2626")

old_bullets = [
    ("Context Exhaustion", "Paste stack traces, re-read code diffs, re-prompt."),
    ("Manual Babysitting", "Anxiously inspect every single line & syntax output."),
    ("Mental Burnout", "40+ context switches/hour causing extreme fatigue.")
]
for title, desc in old_bullets:
    p = to.add_paragraph()
    p.text = f"- {title}: {desc}"
    p.font.size = Pt(9.2)
    p.font.color.rgb = hex_to_rgb("#991B1B")

# Card 2: Bottom Left (The Ambient Director - Green)
c_new = add_card(s7, 0.8, 4.25, 4.2, 2.8, "#F0FDF4", "#10B981")
tn = c_new.text_frame
p = tn.paragraphs[0]
p.text = "NEW WAY: Ambient Autonomy"
p.font.bold = True
p.font.size = Pt(11.5)
p.font.color.rgb = hex_to_rgb("#059669")

new_bullets = [
    ("Executive Intent", "Human gives high-level directive: 'Ship it' or 'Proceed'."),
    ("Autonomous Execution", "Context DAG routes state, executes 48/48 CI matrix."),
    ("Reversible Safety", "One-button rollback safety net + signed receipts."),
    ("Proven Result", "-88% cognitive mental fatigue eliminated!")
]
for title, desc in new_bullets:
    p = tn.add_paragraph()
    p.text = f"- {title}: {desc}"
    p.font.size = Pt(9.2)
    p.font.color.rgb = hex_to_rgb("#065F46")

# Right Side Chart
s7.shapes.add_picture(d_load, Inches(5.2), Inches(1.35), width=Inches(7.333))

# ------------------------------------------------------------------------------
# SLIDE 8: ARCHITECTURAL BLUEPRINT (INTUITIVE & GRAPHICAL DIAGRAM)
# ------------------------------------------------------------------------------
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "Production Tech Stack & Cloud Architecture", "Tech Showcase", "Real-world infrastructure connecting client reflex, CI/CD factory, and AWS us-east-2 (966273137102)")

# Embed graphical tech stack diagram
s8.shapes.add_picture(d_stack, Inches(0.8), Inches(1.35), width=Inches(8.2))

# Right summary card highlighting the 4 core guarantees
c_stack_summary = add_card(s8, 9.2, 1.35, 3.333, 5.7, "#F8FAFC", "#0284C7")
tss = c_stack_summary.text_frame
p = tss.paragraphs[0]
p.text = "Architectural Guarantees"
p.font.bold = True
p.font.size = Pt(12)
p.font.color.rgb = hex_to_rgb("#0369A1")

stack_takeaways = [
    ("Tier 1: Sub-Second Reflex", "Local AST parsing & regex filters absorb routine syntax probes before cloud API invocation.", "#0284C7"),
    ("Tier 2: Deterministic CI", "48/48 automated assertions on clean-room virtual runners before merge.", "#7C3AED"),
    ("Tier 3: AWS us-east-2", "Lambda HTTPS gateway, Step Functions state machine, Bedrock Claude Sonnet, and KMS S3.", "#D97706"),
    ("Tier 4: Cognitive Memory", "Vector DB cosine embeddings + Knowledge Graph Cypher multi-hop traversal.", "#059669"),
]

for title, desc, col in stack_takeaways:
    p = tss.add_paragraph()
    p.text = f"\n{title}"
    p.font.bold = True
    p.font.size = Pt(9.5)
    p.font.color.rgb = hex_to_rgb(col)
    
    p2 = tss.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = hex_to_rgb("#334155")

# ------------------------------------------------------------------------------
# SLIDE 9: CONCLUSION & FUTURE VISION
# ------------------------------------------------------------------------------
s9 = prs.slides.add_slide(blank_layout)

end_card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
end_card.fill.solid()
end_card.fill.fore_color.rgb = hex_to_rgb("#0F172A")
end_card.line.color.rgb = hex_to_rgb("#10B981")
end_card.line.width = Pt(2.5)

tf_end = end_card.text_frame
setup_text_frame(tf_end)
tf_end.vertical_anchor = MSO_ANCHOR.MIDDLE

p = tf_end.paragraphs[0]
p.text = "THE FUTURE OF AUTONOMOUS SYSTEMS"
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
    "2. The AI Factory organizes assembly workers along a deterministic line to turn unpredictable LLM outputs into certified software.",
    "3. Ambient AI makes the entire apparatus invisible: you speak your intent, and the system executes with total safety.",
    "4. Minimizing human cognitive load is the ultimate north star: from anxious babysitting to high-leverage execution in 1 click."
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
