# -*- coding: utf-8 -*-
"""
build_spec_and_intuitive_skills_pdf.py
Definitive script generating:
'20_Agentic_Skills_Spec_And_Intuitive_Guide.pdf'
Features:
- LEFT SIDE: Production SKILL.md Document & Engineering Specification.
- RIGHT SIDE: Simple, Intuitive, Graphical & Fun Explanation (Professional architecture audience).
- Pure LIGHT MODE throughout.
- 22 Landscape Pages (Cover + 20 Skills + Master Architecture Blueprint).
- Zero text clipping; smart multiline wrapping for YAML and architectural rules.
"""

import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import fitz

from build_side_by_side_skills_pdf import PROD_DETAILS, wrap_text
from intuitive_data import INTUITIVE_DATA

PDF_OUTPUT = "20_Agentic_Skills_Spec_And_Intuitive_Guide.pdf"
GRAPH_PNG = "three_tier_skill_dependency_graph.png"

# Professional titles and badges
PRO_METADATA = [
    {"num": 1, "tier": "Tier 0: Cloud Primitives", "color": colors.HexColor("#059669"), "badge": "BEDROCK", "title": "Amazon Bedrock: Foundation Proposal Engine"},
    {"num": 2, "tier": "Tier 0: Cloud Primitives", "color": colors.HexColor("#059669"), "badge": "AGENTCORE", "title": "AgentCore: Cedar Guardrail & AST Gate"},
    {"num": 3, "tier": "Tier 0: Cloud Primitives", "color": colors.HexColor("#059669"), "badge": "S3 VAULT", "title": "Amazon S3 Vault: Cryptographic WORM Storage"},
    {"num": 4, "tier": "Tier 0: Cloud Primitives", "color": colors.HexColor("#059669"), "badge": "DATABASE", "title": "AWS Database: CAS Mutex, Vector & Graph Store"},
    {"num": 5, "tier": "Tier 0: Cloud Primitives", "color": colors.HexColor("#059669"), "badge": "LAMBDA", "title": "AWS Lambda: Ephemeral MicroVM Sandbox"},
    {"num": 6, "tier": "Tier 0: Cloud Primitives", "color": colors.HexColor("#059669"), "badge": "STATE DAG", "title": "AWS Step Functions: Deterministic State Machine DAG"},
    {"num": 7, "tier": "Tier 0: Cloud Primitives", "color": colors.HexColor("#059669"), "badge": "EVENT BUS", "title": "Amazon EventBridge: Pub/Sub Event Mesh"},
    {"num": 8, "tier": "Tier 1: Agent OS Kernel", "color": colors.HexColor("#2563eb"), "badge": "ARBITER", "title": "Kernel Propose-Decide: Prefrontal Executive Arbiter"},
    {"num": 9, "tier": "Tier 1: Agent OS Kernel", "color": colors.HexColor("#2563eb"), "badge": "RUNBOOK", "title": "Kernel Runbook Engine: Procedural DAG Orchestrator"},
    {"num": 10, "tier": "Tier 1: Agent OS Kernel", "color": colors.HexColor("#2563eb"), "badge": "SUPERVISOR", "title": "Kernel Supervisor: Execution Watchdog & Circuit"},
    {"num": 11, "tier": "Tier 1: Agent OS Kernel", "color": colors.HexColor("#2563eb"), "badge": "MUTEX", "title": "Kernel Mutex Lease: Distributed CAS Concurrency Lock"},
    {"num": 12, "tier": "Tier 1: Agent OS Kernel", "color": colors.HexColor("#2563eb"), "badge": "MEMORY", "title": "Kernel Context Pager: Virtual Working Memory Manager"},
    {"num": 13, "tier": "Tier 1: Agent OS Kernel", "color": colors.HexColor("#2563eb"), "badge": "LEDGER", "title": "Kernel Episodic Ledger: SHA-256 Hash-Chained Audit"},
    {"num": 14, "tier": "Tier 1: Agent OS Kernel", "color": colors.HexColor("#2563eb"), "badge": "GROUNDING", "title": "Kernel Grounding Certifier: Tri-Store Fact Verification"},
    {"num": 15, "tier": "Tier 2: Multi-Agent Swarm", "color": colors.HexColor("#7c3aed"), "badge": "TOPOLOGY", "title": "Swarm Topology Builder: Watts-Strogatz Small World"},
    {"num": 16, "tier": "Tier 2: Multi-Agent Swarm", "color": colors.HexColor("#7c3aed"), "badge": "LIAISON", "title": "Swarm Liaison Router: Cross-Pod Ambassador Network"},
    {"num": 17, "tier": "Tier 2: Multi-Agent Swarm", "color": colors.HexColor("#7c3aed"), "badge": "HOP LIMIT", "title": "Swarm Hop Limiter: Bounded Delegation TTL & Loop Filter"},
    {"num": 18, "tier": "Tier 2: Multi-Agent Swarm", "color": colors.HexColor("#7c3aed"), "badge": "BLACKBOARD", "title": "Swarm Shared Whiteboard: O(N) Blackboard Memory"},
    {"num": 19, "tier": "Tier 2: Multi-Agent Swarm", "color": colors.HexColor("#7c3aed"), "badge": "QUORUM", "title": "Swarm Consensus Arbiter: Byzantine Fault-Tolerant Quorum"},
    {"num": 20, "tier": "Tier 2: Multi-Agent Swarm", "color": colors.HexColor("#7c3aed"), "badge": "BREAKER", "title": "Swarm Circuit Breaker: Cascade Quarantine & Lock Revocation"}
]

def render_cover_page(c, width, height):
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.rect(0, 0, width, height, stroke=0, fill=1)

    c.setFillColor(colors.HexColor("#0284c7"))
    c.rect(0, height - 8, width, 8, stroke=0, fill=1)

    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#cbd5e1"))
    c.roundRect(30, height - 135, width - 60, 110, 10, stroke=1, fill=1)

    c.setFillColor(colors.HexColor("#0284c7"))
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(45, height - 48, "ENTERPRISE AI ARCHITECTURE • SPECIFICATION & INTUITION")

    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 22)
    c.drawString(45, height - 76, "The 3-Tier Enterprise Agent Stack")

    c.setFillColor(colors.HexColor("#475569"))
    c.setFont("Helvetica", 11)
    c.drawString(45, height - 98, "Side-by-Side Architectural Guide: Production SKILL.md Specs vs. Intuitive Mental Models")
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawString(45, height - 116, "Left: Formal Engineering Contract (SKILL.md)  |  Right: Simple, Intuitive, Graphical & Fun Architectural Models")

    # 3-Tier Summary Boxes
    box_w = (width - 60 - 30) / 3
    box_h = 75
    tiers = [
        ("TIER 0: CLOUD PRIMITIVES", "Skills #1 – #7", "Physical AWS foundation: DynamoDB CAS locks, S3 WORM compliance vaults, Firecracker microVMs & EventBridge buses.", "#ecfdf5", "#059669", "#065f46"),
        ("TIER 1: AGENT OS KERNEL", "Skills #8 – #14", "Individual agent governance: Prefrontal propose-decide gates, DAG runbooks, mutex leases, context pagers & fact detectives.", "#eff6ff", "#2563eb", "#1e40af"),
        ("TIER 2: MULTI-AGENT SWARMS", "Skills #15 – #20", "Social clubhouse governance: Watts-Strogatz small-world lattices, cross-pod liaisons, O(N) blackboards & Byzantine quorums.", "#faf5ff", "#7c3aed", "#5b21b6")
    ]
    for idx, (t_title, t_sub, t_desc, bg_color, border_color, text_color) in enumerate(tiers):
        bx = 30 + idx * (box_w + 15)
        by = height - 225
        c.setFillColor(colors.HexColor(bg_color))
        c.setStrokeColor(colors.HexColor(border_color))
        c.roundRect(bx, by, box_w, box_h, 8, stroke=1, fill=1)

        c.setFillColor(colors.HexColor(text_color))
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(bx + 12, by + box_h - 18, t_title)
        c.setFillColor(colors.HexColor("#0f172a"))
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(bx + 12, by + box_h - 32, t_sub)
        
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.HexColor("#334155"))
        lines = wrap_text(c, t_desc, "Helvetica", 7.5, box_w - 24)
        ly = by + box_h - 46
        for l in lines:
            c.drawString(bx + 12, ly, l)
            ly -= 9.5

    # ROSETTA STONE TRANSLATION TABLE (Spec to Intuition)
    ty = height - 245
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#cbd5e1"))
    c.roundRect(30, 36, width - 60, ty - 36, 10, stroke=1, fill=1)

    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(45, ty - 22, "THE ARCHITECTURAL TRANSLATION KEY: HOW FORMAL SPECIFICATIONS MAP TO INTUITION")

    th_y = ty - 42
    c.setFillColor(colors.HexColor("#f1f5f9"))
    c.rect(42, th_y - 8, width - 84, 22, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(50, th_y + 4, "LEFT: PRODUCTION SKILL.MD SPECIFICATION")
    c.drawString(290, th_y + 4, "ENGINEERING FUNCTION")
    c.drawString(490, th_y + 4, "RIGHT: INTUITIVE MENTAL MODEL (GRAPHICAL & FUN)")

    rows = [
        ("YAML Frontmatter (name, tier, ring)", "Identity, security privilege ring, IAM permissions", "Memorable Architectural Role & Operational Boundary"),
        ("1. Purpose & Architectural Boundary", "Strict operational boundary & separation of concerns", "The Core Mental Model (Analogy: Bouncer, Pager, Blackboard)"),
        ("2. Interface Contract (JSON Schema)", "Strict typed input/output validation schemas", "3-Stage Visual Pipeline Diagram"),
        ("3. Core System Invariants", "Non-negotiable invariants (CAS locks, zero IAM write)", "The Architectural Rule of Thumb (Golden Pro-Tip)"),
        ("4. Execution Protocol & Syscalls", "Deterministic state machine & downstream cloud calls", "Page 22 Master Blueprint Wire Connection"),
        ("5. Failure Modes & Self-Healing", "SLAs, timeout caps, fallback rollback handlers", "The Architectural Superpower & Recovery Mechanism")
    ]

    ry = th_y - 25
    for r_idx, (r1, r2, r3) in enumerate(rows):
        if r_idx % 2 == 1:
            c.setFillColor(colors.HexColor("#f8fafc"))
            c.rect(42, ry - 6, width - 84, 20, stroke=0, fill=1)
        c.setFont("Courier-Bold", 7.5)
        c.setFillColor(colors.HexColor("#0369a1"))
        c.drawString(50, ry + 2, r1)
        c.setFont("Helvetica", 7.2)
        c.setFillColor(colors.HexColor("#475569"))
        c.drawString(290, ry + 2, r2)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor("#0f172a"))
        c.drawString(490, ry + 2, r3)
        ry -= 23

    c.setFillColor(colors.HexColor("#64748b"))
    c.setFont("Helvetica", 8)
    c.drawString(45, 18, "Generated by Antigravity AI Engineering • Specification & Intuitive Guide (Light Mode)")
    c.drawRightString(width - 45, 18, "Page 1 of 22 • Methodology & Rosetta Stone")
    c.showPage()

def render_spec_left_and_intuitive_right(c, width, height, meta, p_detail, i_data, page_num):
    tier_color = meta["color"]
    col_w = 368
    col_h = 504
    left_x = 20
    right_x = 404
    col_y = 28

    # Background
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.rect(0, 0, width, height, stroke=0, fill=1)

    # 1. TOP HEADER BAR (height 50)
    c.setFillColor(tier_color)
    c.rect(0, height - 50, width, 50, stroke=0, fill=1)

    # Symbol Badge
    c.setFillColor(colors.white)
    c.roundRect(20, height - 40, 80, 30, 6, stroke=0, fill=1)
    c.setFillColor(tier_color)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(60, height - 30, meta["badge"])

    # Title & Subtitle
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13.5)
    c.drawString(112, height - 28, meta["title"])
    c.setFont("Helvetica", 8.5)
    c.drawString(112, height - 42, "Architectural Study: Left = Production SKILL.md Contract  |  Right = Intuitive Graphical Explanation")

    # Tier Tag on Top Right
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(width - 20, height - 26, meta["tier"].upper())
    c.setFont("Helvetica", 8)
    c.drawRightString(width - 20, height - 40, f"Skill #{meta['num']} of 20")

    # 2. FOOTER
    c.setFillColor(colors.HexColor("#64748b"))
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(20, 14, "THE 3-TIER ENTERPRISE AGENT STACK — SPECIFICATION & INTUITIVE ARCHITECTURE GUIDE")
    c.drawRightString(width - 20, 14, f"Skill #{meta['num']} of 20 | Page {page_num} of 22")

    # ==========================================================
    # 3. LEFT COLUMN: PRODUCTION SKILL.MD SPECIFICATION (CONTRACT)
    # ==========================================================
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#cbd5e1"))
    c.roundRect(left_x, col_y, col_w, col_h, 8, stroke=1, fill=1)

    # Left Header (Sky Blue)
    c.setFillColor(colors.HexColor("#f0f9ff"))
    c.roundRect(left_x + 6, col_y + col_h - 32, col_w - 12, 26, 6, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#0369a1"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_x + 14, col_y + col_h - 22, "PRODUCTION SKILL.MD SPECIFICATION (ENGINEERING CONTRACT)")

    # YAML Frontmatter Box (GitHub Light Style)
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.setStrokeColor(colors.HexColor("#e2e8f0"))
    c.roundRect(left_x + 12, col_y + col_h - 130, col_w - 24, 92, 6, stroke=1, fill=1)

    c.setFont("Courier-Bold", 7)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawString(left_x + 20, col_y + col_h - 46, "---")

    yy = col_y + col_h - 56
    for key, val in p_detail["yaml"][:6]:
        c.setFont("Courier-Bold", 6.8)
        c.setFillColor(colors.HexColor("#be123c")) # Crimson key
        c.drawString(left_x + 20, yy, key)
        c.setFillColor(colors.HexColor("#0369a1")) # Sky blue value
        c.setFont("Courier", 6.8)
        kw = c.stringWidth(key, "Courier-Bold", 6.8)
        
        # Check if value needs wrapping
        avail_w = col_w - 48 - kw
        val_lines = wrap_text(c, val, "Courier", 6.8, avail_w)
        c.drawString(left_x + 20 + kw + 4, yy, val_lines[0])
        if len(val_lines) > 1 and key == "description:":
            yy -= 8.5
            c.drawString(left_x + 24 + kw, yy, val_lines[1])
        yy -= 9.5
    c.setFont("Courier-Bold", 7)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawString(left_x + 20, yy, "---")

    # Specification Sections on Left
    my = col_y + col_h - 142

    # 1. Purpose & Axiom
    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(left_x + 14, my, "1. Purpose & Architectural Boundary")
    my -= 10
    c.setFont("Helvetica", 7.2)
    c.setFillColor(colors.HexColor("#334155"))
    ax_lines = wrap_text(c, p_detail["axiom"], "Helvetica", 7.2, col_w - 28)
    for al in ax_lines[:2]:
        c.drawString(left_x + 14, my, al)
        my -= 9.5
    my -= 4

    # 2. Invariants
    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(left_x + 14, my, "2. Core System Invariants (Non-Negotiable)")
    my -= 10
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#1e293b"))
    for inv in p_detail["invariants"][:3]:
        c.drawString(left_x + 14, my, inv[:75])
        my -= 9.5
    my -= 4

    # 3. Execution Pipeline
    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(left_x + 14, my, "3. Execution Protocol & Syscalls")
    my -= 10
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#334155"))
    for stp in p_detail["pipeline"][:4]:
        c.drawString(left_x + 14, my, stp[:75])
        my -= 9.5
    my -= 4

    # 4. Failure Modes
    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(left_x + 14, my, "4. Failure Modes & Self-Healing")
    my -= 10
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#b91c1c")) # Crimson
    for fl in p_detail["failures"][:2]:
        c.drawString(left_x + 14, my, fl[:75])
        my -= 9.5

    # ==========================================================
    # 4. RIGHT COLUMN: INTUITIVE, GRAPHICAL & FUN EXPLANATION
    # ==========================================================
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#cbd5e1"))
    c.roundRect(right_x, col_y, col_w, col_h, 8, stroke=1, fill=1)

    # Right Header (Clean Emerald)
    c.setFillColor(colors.HexColor("#f0fdf4"))
    c.roundRect(right_x + 6, col_y + col_h - 32, col_w - 12, 26, 6, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#15803d"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(right_x + 14, col_y + col_h - 22, "INTUITIVE ARCHITECTURAL MODEL (SIMPLE & GRAPHICAL)")

    # Hook & Title
    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 11.5)
    c.drawString(right_x + 14, col_y + col_h - 50, f"Mental Model: {i_data['hook']}")

    # One sentence architectural concept box
    c.setFillColor(colors.HexColor("#eff6ff"))
    c.setStrokeColor(colors.HexColor("#93c5fd"))
    c.roundRect(right_x + 12, col_y + col_h - 100, col_w - 24, 42, 6, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#1e40af"))
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(right_x + 20, col_y + col_h - 68, "THE CORE INTUITION IN ONE SENTENCE:")
    c.setFont("Helvetica", 7.8)
    c.setFillColor(colors.HexColor("#1e3a8a"))
    c_lines = wrap_text(c, i_data["concept"], "Helvetica", 7.8, col_w - 40)
    cy_text = col_y + col_h - 80
    for cl in c_lines[:2]:
        c.drawString(right_x + 20, cy_text, cl)
        cy_text -= 10

    # Intuitive Metaphor Story
    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(right_x + 14, col_y + col_h - 116, "How It Works (The Intuitive Analogy):")
    c.setFont("Helvetica", 7.6)
    c.setFillColor(colors.HexColor("#334155"))
    meta_lines = wrap_text(c, i_data["metaphor"], "Helvetica", 7.6, col_w - 28)
    sy = col_y + col_h - 128
    for ml in meta_lines[:6]:
        c.drawString(right_x + 14, sy, ml)
        sy -= 10.5

    # Visual Workflow Diagram Box
    dy_box = sy - 8
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.setStrokeColor(colors.HexColor("#e2e8f0"))
    c.roundRect(right_x + 12, dy_box - 54, col_w - 24, 56, 6, stroke=1, fill=1)

    step_w = 92
    step_h = 36
    d1_title, d1_sub = i_data["diagram"][0]
    d2_title, d2_sub = i_data["diagram"][1]
    d3_title, d3_sub = i_data["diagram"][2]

    # Diagram Step 1
    c.setFillColor(colors.HexColor("#fef3c7"))
    c.setStrokeColor(colors.HexColor("#f59e0b"))
    c.roundRect(right_x + 18, dy_box - 46, step_w, step_h, 4, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#92400e"))
    c.setFont("Helvetica-Bold", 7.2)
    c.drawCentredString(right_x + 18 + step_w/2, dy_box - 24, d1_title[:18])
    c.setFont("Helvetica", 6.6)
    c.drawCentredString(right_x + 18 + step_w/2, dy_box - 36, d1_sub[:20])

    c.setStrokeColor(colors.HexColor("#64748b"))
    c.line(right_x + 18 + step_w + 3, dy_box - 28, right_x + 18 + step_w + 22, dy_box - 28)

    # Diagram Step 2
    c.setFillColor(colors.HexColor("#dbeafe"))
    c.setStrokeColor(colors.HexColor("#3b82f6"))
    c.roundRect(right_x + 18 + step_w + 26, dy_box - 46, step_w + 8, step_h, 4, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#1e40af"))
    c.setFont("Helvetica-Bold", 7.2)
    c.drawCentredString(right_x + 18 + step_w + 26 + (step_w+8)/2, dy_box - 24, d2_title[:18])
    c.setFont("Helvetica", 6.6)
    c.drawCentredString(right_x + 18 + step_w + 26 + (step_w+8)/2, dy_box - 36, d2_sub[:22])

    c.setStrokeColor(colors.HexColor("#64748b"))
    c.line(right_x + 18 + step_w*2 + 38, dy_box - 28, right_x + 18 + step_w*2 + 57, dy_box - 28)

    # Diagram Step 3
    c.setFillColor(colors.HexColor("#dcfce7"))
    c.setStrokeColor(colors.HexColor("#22c55e"))
    c.roundRect(right_x + 18 + step_w*2 + 61, dy_box - 46, step_w, step_h, 4, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#166534"))
    c.setFont("Helvetica-Bold", 7.2)
    c.drawCentredString(right_x + 18 + step_w*2 + 61 + step_w/2, dy_box - 24, d3_title[:18])
    c.setFont("Helvetica", 6.6)
    c.drawCentredString(right_x + 18 + step_w*2 + 61 + step_w/2, dy_box - 36, d3_sub[:20])

    # Wire connection box
    wy = dy_box - 64
    c.setFillColor(colors.HexColor("#faf5ff"))
    c.setStrokeColor(colors.HexColor("#d8b4fe"))
    c.roundRect(right_x + 12, wy - 48, col_w - 24, 48, 6, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#6b21a8"))
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(right_x + 20, wy - 14, f"PAGE 22 BLUEPRINT WIRING: Plugs into {i_data['wire_target']}")
    c.setFont("Helvetica", 7.2)
    c.setFillColor(colors.HexColor("#581c87"))
    w_lines = wrap_text(c, i_data["wire_expl"], "Helvetica", 7.2, col_w - 40)
    w_y = wy - 26
    for wl in w_lines[:2]:
        c.drawString(right_x + 20, w_y, wl)
        w_y -= 10

    # Superpower & Rule of Thumb Box (Clean Multiline)
    gy = wy - 58
    c.setFillColor(colors.HexColor("#ecfdf5"))
    c.setStrokeColor(colors.HexColor("#a7f3d0"))
    c.roundRect(right_x + 12, gy - 54, col_w - 24, 54, 6, stroke=1, fill=1)
    
    c.setFillColor(colors.HexColor("#065f46"))
    c.setFont("Helvetica-Bold", 7.2)
    sp_lines = wrap_text(c, f"Architectural Superpower: {i_data['superpower']}", "Helvetica-Bold", 7.2, col_w - 40)
    c.drawString(right_x + 20, gy - 12, sp_lines[0])
    if len(sp_lines) > 1:
        c.drawString(right_x + 20, gy - 21, sp_lines[1])

    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(right_x + 20, gy - 32, "Architectural Rule of Thumb:")
    c.setFont("Helvetica-Oblique", 7.2)
    rot_lines = wrap_text(c, f"\"{i_data['rule_of_thumb']}\"", "Helvetica-Oblique", 7.2, col_w - 40)
    c.drawString(right_x + 20, gy - 43, rot_lines[0])
    if len(rot_lines) > 1:
        c.drawString(right_x + 20, gy - 51, rot_lines[1])

    c.showPage()

def render_blueprint_page(c, width, height):
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.rect(0, 0, width, height, stroke=0, fill=1)

    c.setFillColor(colors.HexColor("#7c3aed"))
    c.rect(0, height - 52, width, 52, stroke=0, fill=1)

    c.setFillColor(colors.white)
    c.roundRect(24, height - 42, 60, 30, 6, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#7c3aed"))
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(54, height - 32, "MAP")

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(96, height - 32, "The Master Blueprint: All 20 Skills & Specifications Connect!")

    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(width - 24, height - 26, "THE COMPLETE 3-TIER STACK")
    c.setFont("Helvetica", 8)
    c.drawRightString(width - 24, height - 40, "Summary Page • Page 22 of 22")

    c.setFillColor(colors.HexColor("#f1f5f9"))
    c.rect(0, height - 76, width, 24, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#334155"))
    c.setFont("Helvetica-Bold", 8)
    sub = "Look at the colorful wires! Purple wires connect Swarm Coordination (#15-20) to Agent Kernel OS (#8-14). Blue wires connect Kernel OS down to Physical Cloud Safes (#1-7)!"
    c.drawCentredString(width / 2, height - 68, sub)

    if os.path.exists(GRAPH_PNG):
        dw = width - 40
        dh = height - 100
        dx = 20
        dy = 22
        c.drawImage(GRAPH_PNG, dx, dy, width=dw, height=dh, preserveAspectRatio=True, anchor='c')

    c.setFillColor(colors.HexColor("#64748b"))
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(20, 10, "THE 3-TIER ENTERPRISE AGENT STACK — 20 SKILLS COMPLETE DEPENDENCY BLUEPRINT (LIGHT MODE)")
    c.drawRightString(width - 20, 10, "Page 22 of 22 (Final Master Map)")
    c.showPage()

def build_pdf():
    c = canvas.Canvas(PDF_OUTPUT, pagesize=landscape(letter))
    width, height = landscape(letter)

    print("Building Page 1: Cover & Methodology Translation Key...")
    render_cover_page(c, width, height)

    print("Building Pages 2 to 21: 20 Skills (Left: SKILL.md Spec | Right: Intuitive Architecture)...")
    for idx in range(20):
        meta = PRO_METADATA[idx]
        p_d = PROD_DETAILS[idx]
        i_d = INTUITIVE_DATA[idx]
        page_num = idx + 2
        print(f"  Rendering Skill #{idx+1:02d}: {meta['title'][:32]} (Page {page_num}/22)...")
        render_spec_left_and_intuitive_right(c, width, height, meta, p_d, i_d, page_num)

    print("Building Page 22: Master Blueprint Landscape...")
    render_blueprint_page(c, width, height)

    c.save()
    print(f"Successfully generated {PDF_OUTPUT}!")

if __name__ == "__main__":
    build_pdf()
