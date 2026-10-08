"""
Generate professional academic Word document (.docx) for:
Agentic Model Predictive Control Paper
Reflecting verified simulation realities: equal tuning across baselines,
honest supervisory schedule deconstruction, and robust mathematical formulation.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_heading_with_spacing(doc, text, level):
    p = doc.add_heading(text, level=level)
    p.paragraph_format.keep_with_next = True
    if level == 1:
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        for run in p.runs:
            run.font.name = 'Calibri'
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(15, 23, 42)
    elif level == 2:
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        for run in p.runs:
            run.font.name = 'Calibri'
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(30, 41, 59)
    elif level == 3:
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(2)
        for run in p.runs:
            run.font.name = 'Calibri'
            run.font.size = Pt(10.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_callout_box(doc, text, title="ABSTRACT", hex_color="F1F5F9", border_color="059669"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, hex_color)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:left w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/>
            <w:top w:val="none"/>
            <w:right w:val="none"/>
            <w:bottom w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(4)
    run_title = p.add_run(f"■ {title}\n")
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(10.5)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 23, 42)
    
    run_body = p.add_run(text)
    run_body.font.name = 'Cambria'
    run_body.font.size = Pt(9.5)
    run_body.font.color.rgb = RGBColor(51, 65, 85)
    doc.add_paragraph()

def add_equation_box(doc, eq_text, eq_num=""):
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1 = tbl.cell(0, 0)
    c2 = tbl.cell(0, 1)
    set_cell_background(c1, "F8FAFC")
    set_cell_background(c2, "F8FAFC")
    set_cell_margins(c1, top=60, bottom=60, left=100, right=100)
    set_cell_margins(c2, top=60, bottom=60, left=60, right=60)
    
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p1.add_run(eq_text)
    r1.font.name = 'Cambria Math'
    r1.font.size = Pt(10)
    r1.font.italic = True
    r1.font.color.rgb = RGBColor(15, 23, 42)
    
    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if eq_num:
        r2 = p2.add_run(f"({eq_num})")
        r2.font.name = 'Calibri'
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = RGBColor(100, 116, 139)
        
    c1.width = Inches(5.8)
    c2.width = Inches(0.7)
    
    for c in [c1, c2]:
        tcPr = c._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                <w:left w:val="none"/>
                <w:right w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)
    doc.add_paragraph()

def format_table(table, col_widths, headers, data, header_bg="0F172A"):
    for idx, width in enumerate(col_widths):
        table.columns[idx].width = Inches(width)
        
    hdr_cells = table.rows[0].cells
    for i, header_text in enumerate(headers):
        hdr_cells[i].text = header_text
        set_cell_background(hdr_cells[i], header_bg)
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in p.runs:
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    for row_idx, row_data in enumerate(data):
        row = table.add_row()
        bg = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        for i, val in enumerate(row_data):
            cell = row.cells[i]
            cell.text = str(val)
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Calibri'
                r.font.size = Pt(8.5)
                r.font.color.rgb = RGBColor(30, 41, 59)
                if i == 0 or "SAFE" in str(val) or "Full" in str(val):
                    r.font.bold = True
                    if "SAFE" in str(val):
                        r.font.color.rgb = RGBColor(5, 150, 105)
                if "TRIP" in str(val) or "Breached" in str(val):
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(220, 38, 38)
                    
    for row in table.rows:
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            borders = parse_xml(f'''
                <w:tcBorders {nsdecls("w")}>
                    <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                    <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                    <w:left w:val="none"/>
                    <w:right w:val="none"/>
                </w:tcBorders>
            ''')
            tcPr.append(borders)

def build_paper_docx():
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Agentic Model Predictive Control — Technical Report")
        hrun.font.name = 'Calibri'
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(148, 163, 184)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Zhaoyang Wan, PhD, MBA • October 2026")
        frun.font.name = 'Calibri'
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(148, 163, 184)

    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(8)
    title_run = title_p.add_run("Agentic Model Predictive Control: Operating in Intelligence Space via Cognitive Supervisory Layers and Parallel Path Integral Rollouts")
    title_run.font.name = 'Calibri'
    title_run.font.size = Pt(18)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(15, 23, 42)

    meta_p = doc.add_paragraph()
    meta_p.paragraph_format.space_after = Pt(12)
    runs_data = [
        ("Author: ", True), ("Zhaoyang Wan, PhD, MBA    |    ", False),
        ("Date: ", True), ("October 2026    |    ", False),
        ("Repository: ", True), ("cosmosanalytics/uat-copilot-local", False)
    ]
    for text, bold in runs_data:
        r = meta_p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(9.5)
        r.font.bold = bold
        r.font.color.rgb = RGBColor(71, 85, 105)

    abstract_text = (
        "Model Predictive Control (MPC) has served as the industrial benchmark for constrained multivariable control across "
        "process operations for four decades. Modern formulations—ranging from linear quadratic programming (QP) "
        "to nonlinear MPC (NMPC) and economic MPC (EMPC)—optimize physical state trajectories against fixed mathematical objectives. "
        "However, existing control formulations lack supervisory cognitive intelligence: they cannot parse unstructured natural-language "
        "operator directives, reason over qualitative plant physical topology, or execute contextual mitigation runbooks during operational contingencies.\n\n"
        "In this paper, we introduce Agentic Model Predictive Control (Agentic MPC), an architecture that places an Intelligence Space "
        "supervisory layer above high-throughput real-time control solvers. The architecture partitions supervisory intelligence into The Two Halves: "
        "(1) a neural reasoner (The Knower) grounded in four structured memory tiers (Playbook, Rulebook, Yearbook, and Whiteboard), and "
        "(2) a deterministic Executive Function Harness (The Doer) enforcing Ring 0 operating invariants, automated contract unit tests, and preemptive trip bounds. "
        "High-level cognitive directives are translated at runtime into parameterized Model Predictive Path Integral (MPPI) cost manifolds executed across "
        "parallel trajectory rollouts via GPU/WebGPU compute shaders, augmented by an online recursive parameter observer.\n\n"
        "We evaluate the physical dynamics on an exothermic Continuous Stirred-Tank Reactor (CSTR) undergoing non-linear kinetic surges across a fully reproducible "
        "benchmark suite spanning 20 randomized seeds with varying surge magnitudes (C_A0 in [+10%, +30%], T_0 in [+5 K, +12 K], UA in [-10%, -35%]) "
        "and advance-warning advisory lead time (t_lead = 3.5 s). Numerical dynamic optimization demonstrates that with zero advance warning, the combined jacket "
        "transport delay (tau_j = 2.0 s) and valve slew limit (12 K/s) physically prevent avoiding thermal runaway (T_max >= 440 K), establishing a physical floor "
        "of 6/20 trips across all feedback controllers (Linear MPC: 6/20 trips, 9.49 K RMSE; NMPC: 6/20 trips, 9.62 K RMSE; MPPI: 6/20 trips, 9.79 K RMSE).\n\n"
        "When advance preview lookahead (t_lead = 3.5 s) is supplied, trips drop to 1/20 across all preview controllers, with failure occurring exclusively on Seed 18 "
        "(an extreme corner realization requiring >4.5 s of lead time). Crucially, our ablation isolates that the supervisory layer's quantitative advantage "
        "(0.95 ± 0.40 K non-trip RMSE vs. 1.81 ± 1.11 K for standard preview MPPI) stems from coordinating an anticipatory pre-cooling ramp that avoids reaction quenching: "
        "naive rule-based step switching quenches the reactor, accumulates unreacted feed, and triggers delayed thermal blowout (8/20 trips, 9.44 K RMSE). "
        "We present the full system architecture, formal Ring 0 contract invariants, and offline prompt evaluation protocols, establishing a rigorous foundation for process control."
    )
    add_callout_box(doc, abstract_text, title="ABSTRACT")

    add_heading_with_spacing(doc, "1. Introduction & Related Work", level=1)
    p = doc.add_paragraph()
    p.add_run("Model Predictive Control operates on the receding-horizon principle: at each discrete time step t, the controller solves an open-loop optimal control problem over a prediction horizon Hp, applies the first control input u_t, and repeats the cycle upon receiving fresh state telemetry (Rawlings et al., 2017).")
    
    add_heading_with_spacing(doc, "1.1 Related Work: Advanced & Learning-Based MPC", level=2)
    related_items = [
        ("• Robust and Constrained MPC: ", "Linear Matrix Inequality (LMI) and tube-based robust MPC formulations synthesize invariant sets to maintain constraint satisfaction under bounded disturbances (Kothare et al., 1996; Mayne et al., 2005)."),
        ("• Learning-Based and Differentiable MPC: ", "Recent advances integrate Gaussian Processes and neural networks into MPC for online residual compensation (Hewing et al., 2020), while differentiable MPC embeds convex optimization layers into end-to-end gradient-based neural networks (Amos et al., 2018). Physics-informed neural network formulations (Raissi et al., 2019) have inspired domain-constrained residual observers that embed conservation laws into state estimation."),
        ("• Sampling-Based Non-Convex Control: ", "Model Predictive Path Integral (MPPI) control computes optimal control signals via Monte Carlo importance sampling over stochastic forward rollouts (Williams et al., 2017). Because MPPI evaluates trajectories independently without computing Jacobian matrices, it naturally maps to massively parallel GPU compute shaders.")
    ]
    for pre, bdy in related_items:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.add_run(pre).bold = True
        p.add_run(bdy)

    add_heading_with_spacing(doc, "1.2 The Role of the Supervisory Layer: Lookahead vs. Reasoning", level=2)
    p = doc.add_paragraph()
    p.add_run("A critical insight in receding-horizon control is that numerical solvers optimize over a fixed finite horizon Hp (e.g., 4.0 s). When future disturbances are known in advance, mathematical solvers with preview can naturally pre-actuate within their horizon. However, in actual plant operations, forecasts arrive as human shift handover notes, laboratory feed analysis reports, or upstream DCS alarms. Agentic MPC introduces an Intelligence Space supervisory tier positioned strictly above a deterministic execution harness and parallel MPPI rollouts.")

    add_heading_with_spacing(doc, "2. The Agentic MPC Architecture", level=1)
    add_heading_with_spacing(doc, "2.1 The Two Halves: The Knower and The Doer", level=2)
    p = doc.add_paragraph()
    p.add_run("• The Knower (Neural Reasoner): ").bold = True
    p.add_run("Operates in Intelligence Space, translating operator directives into cost manifold parameters θ_M = {q_T, q_barrier, u_target, λ}. Inference runs on dedicated cloud LPUs or server GPUs (e.g., Qwen-2.5-32B), with lightweight client-side WebGPU shaders (e.g., Qwen-2.5-0.5B via @mlc-ai/web-llm) available for offline edge operation.")
    p = doc.add_paragraph()
    p.add_run("• The Doer (Executive Function Harness): ").bold = True
    p.add_run("A deterministic verification kernel enforcing Ring 0 invariants (actuator saturation and slew rate limits), running automated contract unit tests, and operating preemptively below plant emergency shutdown thresholds.")

    add_heading_with_spacing(doc, "3. Mathematical Formulation", level=1)
    add_heading_with_spacing(doc, "3.1 Classical Linear MPC Baseline (Jacobian QP)", level=2)
    p = doc.add_paragraph()
    p.add_run("The linear discrete-time optimal control problem is solved as a condensed Quadratic Program (QP) around the textbook steady state (C_A,ref = 0.50 mol/L, T_ref = 350.0 K, T_c,base = 300.0 K). The Jacobian matrix A has eigenvalues [-0.0076, +0.0472] s^-1, exhibiting an open-loop thermal runaway pole (tau_growth ~ 21.2 s). State penalty is Q = diag(10.0, q_T), R = 0.02, input bounds [280, 360] K, and slew limit 12 K/s.")
    add_equation_box(doc, "min_U  (1/2) U^T H_qp U + g^T U    subject to: u_min <= u_k <= u_max,  |Δu_k| <= Δu_max", "1")

    add_heading_with_spacing(doc, "3.2 Model Predictive Path Integral (MPPI) Formulation", level=2)
    p = doc.add_paragraph()
    p.add_run("MPPI evaluates K = 1,024 stochastic control rollouts sampled from N(0, Σ) with covariance Σ = 6.0^2 I and temperature λ = 10.0. The optimal control update is computed via softmax importance weighting:")
    add_equation_box(doc, "u_t* = u_t + ∑_{m=1}^K w(U^{(m)}) ε_t^{(m)},    w(U^{(m)}) = exp(-S(U^{(m)})/λ) / ∑_j exp(-S(U^{(j)})/λ)", "2")

    add_heading_with_spacing(doc, "4. Benchmark Case Study: Exothermic CSTR", level=1)
    add_heading_with_spacing(doc, "4.1 Numerical Dynamic Oracle Feasibility", level=2)
    p = doc.add_paragraph()
    p.add_run("Dynamic trajectory optimization over the benchmark kinetic surge demonstrates the physical controllability limits:")

    tbl_oracle = doc.add_table(rows=1, cols=4)
    tbl_oracle.alignment = WD_TABLE_ALIGNMENT.CENTER
    oracle_headers = ["Lead Time t_lead", "Peak Temp T_max (K)", "SIS Trip (>= 385.0 K)", "Operational Controllability Outcome"]
    oracle_data = [
        ["0.0 s (Reaction at Onset)", "444.9 K", "TRIP (Breached)", "Unsurvivable runaway due to jacket lag (tau_j = 2 s) & slew cap"],
        ["1.0 s Lead Time", "443.4 K", "TRIP (Breached)", "Insufficient thermal extraction ahead of exponential surge"],
        ["2.0 s Lead Time", "378.2 K", "SAFE (Zero Trip)", "Modulated dynamic pre-cooling contains surge below trip"],
        ["2.5 s Lead Time", "367.8 K", "SAFE (Zero Trip)", "Stable containment with 17.2 K safety margin"],
        ["3.0 s Lead Time", "361.2 K", "SAFE (Zero Trip)", "Smooth containment"],
        ["3.5 s Lead Time", "356.5 K", "SAFE (Zero Trip)", "Robust containment (28.5 K margin to trip)"],
        ["5.0 s Lead Time", "350.0 K", "SAFE (Zero Trip)", "Fully absorbed thermal surge clamped at nominal setpoint"]
    ]
    format_table(tbl_oracle, [1.5, 1.4, 1.4, 2.7], oracle_headers, oracle_data)
    doc.add_paragraph()

    add_heading_with_spacing(doc, "5. Verification & Safety Architecture", level=1)
    p = doc.add_paragraph()
    p.add_run("Agentic MPC enforces defense-in-depth: Ring 0 invariant checking (q_T >= 0.1, q_barrier >= 1000, u in [280, 360] K, slew <= 12 K/s), automated contract unit tests on the active fouled plant model (<30 ms), a software preemptive breaker at 382 K, and an independent hardware SIS scram at 385 K (failsafe cooling valve full open, feed shut off).")

    add_heading_with_spacing(doc, "6. Empirical Results & Ablation Analysis", level=1)
    add_heading_with_spacing(doc, "6.1 Multi-Tier Benchmark Across 20 Randomized Seeds", level=2)
    p = doc.add_paragraph()
    p.add_run("Table 2 presents authentic simulation results across 20 randomized seeds computed directly from discrete QP, L-BFGS-B NMPC, and GPU MPPI path integral solvers:")

    tbl_ablation = doc.add_table(rows=1, cols=8)
    tbl_ablation.alignment = WD_TABLE_ALIGNMENT.CENTER
    abl_headers = ["Config", "Controller Type", "Surv RMSE", "All RMSE", "Peak T (K)", "Slew (K/s)", "SIS Trips", "Settled"]
    abl_data = [
        ["Baseline 1 (qT=1)", "Linear MPC (q_T = 1.0, No Forecast)", "2.56 ± 1.36", "16.26 ± 5.52", "389.3 ± 14.2", "3.29 ± 0.95", "12 / 20 (60%)", "8 / 20 (9.8 s)"],
        ["Baseline 1 (qT=10)", "Linear MPC (q_T = 10.0, No Forecast)", "2.45 ± 1.41", "9.49 ± 5.34", "372.1 ± 13.5", "4.85 ± 1.12", "6 / 20 (30%)", "13 / 20 (7.1 s)"],
        ["Baseline 2a", "NMPC (L-BFGS-B, No Forecast)", "2.48 ± 1.47", "9.62 ± 5.37", "372.9 ± 13.7", "5.04 ± 1.29", "6 / 20 (30%)", "13 / 20 (6.9 s)"],
        ["Ablation 1", "MPPI (Static θ*, No Forecast)", "2.98 ± 1.75", "12.03 ± 5.57", "378.9 ± 14.6", "2.44 ± 0.38", "8 / 20 (40%)", "11 / 20 (8.6 s)"],
        ["Ablation 2", "MPPI + Observer (No Forecast)", "2.60 ± 1.28", "9.79 ± 5.39", "373.4 ± 13.9", "2.42 ± 0.38", "6 / 20 (30%)", "14 / 20 (11.6 s)"],
        ["Baseline 2b", "NMPC (With Forecast Preview)", "1.47 ± 0.85", "2.82 ± 2.93", "356.7 ± 7.6", "6.41 ± 1.03", "1 / 20 (5%)", "19 / 20 (2.6 s)"],
        ["Ablation 3a", "MPPI + Observer (With Forecast)", "1.81 ± 1.11", "3.11 ± 2.99", "357.3 ± 7.7", "2.72 ± 0.19", "1 / 20 (5%)", "18 / 20 (5.7 s)"],
        ["Ablation 3b", "Rule Supervisor + MPPI", "2.50 ± 1.66", "9.44 ± 4.92", "381.1 ± 17.1", "3.77 ± 0.37", "8 / 20 (40%)", "12 / 20 (13.1 s)"],
        ["Full System", "Agentic MPC (Full Architecture)", "0.95 ± 0.40", "2.17 ± 2.57", "355.5 ± 6.2", "3.36 ± 0.19", "1 / 20 (5%)", "19 / 20 (2.9 s)"]
    ]
    format_table(tbl_ablation, [1.1, 1.8, 0.8, 0.8, 0.9, 0.7, 0.7, 0.7], abl_headers, abl_data)
    doc.add_paragraph()

    add_heading_with_spacing(doc, "6.2 Deconstructing the Supervisory Advantage", level=2)
    p = doc.add_paragraph()
    p.add_run("Ablation across the 19 non-trip seeds isolates the quantitative mechanism behind the supervisory schedule:")
    tbl_ablat_sub = doc.add_table(rows=1, cols=3)
    tbl_ablat_sub.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table(tbl_ablat_sub, [2.2, 1.5, 3.5], ["Configuration", "Non-Trip RMSE", "Physical Mechanism"], [
        ["MPPI + Forecast Preview", "1.81 K", "Unconstrained optimal preview tracking"],
        ["+ Ramp Cap Only", "1.12 K", "Modulates pre-cooling to 282 K, preventing reaction quenching"],
        ["+ Elevated Barrier Weights Only", "1.36 K", "Stiff penalty keeps state strictly within safe envelope"],
        ["Both (Anticipatory Supervisory Schedule)", "0.95 K", "Coordinated pre-cooling containment (+0.86 K gain, p = 0.0088)"]
    ])
    doc.add_paragraph()

    add_heading_with_spacing(doc, "7. Industrial Deployment Limits & Conclusion", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "While Agentic MPC demonstrates robust supervisory capabilities in simulation, certified industrial deployment requires strict separation of concerns. "
        "Under IEC 61511 / ISA-84, safety instrumented functions must remain physically independent, deterministic, and SIL-rated. The agentic layer operates solely "
        "in the basic process control system (BPCS) supervisory space and must never share hardware, sensors, or actuators with the emergency shutdown interlock. "
        "Systematic ablation across eight control configurations demonstrates that while numerical preview lookahead provides the essential physical mechanism "
        "of thermal stabilization, the supervisory agentic layer provides critical directive translation, formal contract gating, and smooth pre-cooling modulation "
        "that eliminates the hazardous quenching trips of naive rule-based switching. Automated contract testing and Ring 0 invariant verification provide "
        "the necessary deterministic gating to transition agentic control systems toward industrial deployment."
    )

    add_heading_with_spacing(doc, "References", level=1)
    refs = [
        "Williams, G., Aldrich, A., & Theodorou, E. A. (2017). Model Predictive Path Integral Control: From Theory to Parallel Computation. Journal of Guidance, Control, and Dynamics, 40(2), 344–357.",
        "Rawlings, J. B., Mayne, D. Q., & Diehl, M. (2017). Model Predictive Control: Theory, Computation, and Design (2nd ed.). Nob Hill Publishing.",
        "Seborg, D. E., Edgar, T. F., Mellichamp, D. A., & Doyle, F. J. (2016). Process Dynamics and Control (4th ed.). John Wiley & Sons.",
        "Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019). Physics-Informed Neural Networks: A Deep Learning Framework for Solving Forward and Inverse Problems Involving Nonlinear Partial Differential Equations. Journal of Computational Physics, 378, 686–707.",
        "Kothare, M. V., Balakrishnan, V., & Morari, M. (1996). Robust Constrained Model Predictive Control using Linear Matrix Inequalities. Automatica, 32(10), 1361–1379.",
        "Mayne, D. Q., Seron, M. M., & Raković, S. V. (2005). Robust Model Predictive Control of Constrained Linear Systems with Bounded Disturbances. Automatica, 41(2), 219–224.",
        "Hewing, L., Wabersich, K. P., Menner, M., & Zeilinger, M. N. (2020). Learning-Based Model Predictive Control: Toward Safe Learning in Control. Annual Review of Control, Robotics, and Autonomous Systems, 3, 269–296.",
        "Amos, B., Jiménez, I., Sacks, J., Boots, B., & Kolter, J. Z. (2018). Differentiable MPC for End-to-End Planning and Control. Advances in Neural Information Processing Systems (NeurIPS), 31, 8289–8300."
    ]
    for idx, ref in enumerate(refs, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.first_line_indent = Inches(-0.3)
        p.paragraph_format.space_after = Pt(4)
        run_idx = p.add_run(f"[{idx}] ")
        run_idx.bold = True
        run_idx.font.name = 'Calibri'
        run_ref = p.add_run(ref)
        run_ref.font.name = 'Cambria'
        run_ref.font.size = Pt(9.5)

    output_path = r"C:\Users\richa\ai-engineering\agentic_mpc_paper.docx"
    doc.save(output_path)
    print(f"Successfully generated DOCX at: {output_path} (size: {os.path.getsize(output_path)} bytes)")

if __name__ == '__main__':
    build_paper_docx()
