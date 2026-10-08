"""
Generate professional academic Word document (.docx) for:
Agentic Model Predictive Control Paper
Revised with Round 3 peer review updates: oracle lead-time feasibility,
paired differences, offline schedule, Q-only ablation, confusion matrix, and deployment architecture.
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
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"{title}\n")
    run_t.font.name = 'Calibri'
    run_t.font.bold = True
    run_t.font.size = Pt(10)
    run_t.font.color.rgb = RGBColor(5, 150, 105)
    
    run_b = p.add_run(text)
    run_b.font.name = 'Cambria'
    run_b.font.size = Pt(9.5)
    run_b.font.italic = True
    run_b.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph()

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="12" w:space="0" w:color="CBD5E1"/><w:top w:val="single" w:sz="12" w:space="0" w:color="CBD5E1"/><w:right w:val="single" w:sz="12" w:space="0" w:color="CBD5E1"/><w:bottom w:val="single" w:sz="12" w:space="0" w:color="CBD5E1"/></w:tcBorders>')
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph()

def add_equation_box(doc, eq_text, eq_num=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Inches(0.3)
    run_eq = p.add_run(eq_text)
    run_eq.font.name = 'Cambria Math'
    run_eq.font.size = Pt(10.5)
    run_eq.font.italic = True
    run_eq.font.color.rgb = RGBColor(15, 23, 42)
    
    if eq_num:
        run_tab = p.add_run(f"    \t{eq_num}")
        run_tab.font.name = 'Calibri'
        run_tab.font.size = Pt(9.5)
        run_tab.font.color.rgb = RGBColor(100, 116, 139)

def format_table(table, col_widths, headers, data):
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "1E293B")
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.name = 'Calibri'
            run.font.bold = True
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(255, 255, 255)
    
    for row_idx, row_data in enumerate(data):
        row_cells = table.add_row().cells
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for i, val in enumerate(row_data):
            row_cells[i].text = val
            set_cell_background(row_cells[i], bg)
            set_cell_margins(row_cells[i], top=80, bottom=80, left=120, right=120)
            p = row_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = 'Calibri'
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(15, 23, 42)
                if "Full System" in val or "0.19" in val or "95.0%" in val or "100%" in val:
                    run.font.bold = True
    
    for row in table.rows:
        for i, w in enumerate(col_widths):
            row.cells[i].width = Inches(w)

def build_paper_docx():
    doc = Document()

    # Page Margins
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

    # Document Title
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(8)
    title_run = title_p.add_run("Agentic Model Predictive Control: Operating in Intelligence Space via Cognitive Supervisory Layers and Parallel Path Integral Rollouts")
    title_run.font.name = 'Calibri'
    title_run.font.size = Pt(20)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(15, 23, 42)

    # Metadata Paragraph
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

    # Abstract Box
    abstract_text = (
        "Model Predictive Control (MPC) has served as the industrial benchmark for constrained multivariable control across "
        "process operations for four decades. Modern formulations—ranging from linear quadratic programming (QP) "
        "to nonlinear MPC (NMPC) and economic MPC (EMPC)—optimize physical state trajectories against fixed mathematical objectives. "
        "However, existing control formulations lack supervisory cognitive intelligence: they cannot parse high-level natural-language "
        "operator directives, reason over qualitative plant physical topology, or execute contextual mitigation runbooks during operational contingencies.\n\n"
        "In this paper, we introduce Agentic Model Predictive Control (Agentic MPC), an architecture that places an Intelligence Space "
        "supervisory layer above high-throughput real-time control solvers. The architecture partitions supervisory intelligence into The Two Halves: "
        "(1) a neural reasoner (The Knower) grounded in four structured memory tiers (Playbook, Rulebook, Yearbook, and Whiteboard), and "
        "(2) a deterministic Executive Function Harness (The Doer) enforcing Ring 0 operating invariants, automated contract unit tests, and preemptive trip bounds. "
        "High-level cognitive directives are translated at runtime into parameterized Model Predictive Path Integral (MPPI) cost manifolds executed across "
        "4,096 parallel trajectory rollouts via WebGPU compute shaders, augmented by an online Physics-Informed Neural Network (PINN) residual observer. "
        "We evaluate the architecture on an exothermic Continuous Stirred-Tank Reactor (CSTR) undergoing non-linear kinetic surges across a randomized benchmark suite "
        "spanning 20 seeds with varying surge magnitudes (C_A0 in [+10%, +30%], UA in [-10%, -35%]) and advance-warning lead times (t_lead in [0.0 s, 5.0 s]). "
        "An oracle feasibility analysis demonstrates that with zero advance warning, severe concurrent surges exceed physical heat removal capacity, whereas supervisory "
        "runbook alerts providing >= 3.0 s advance notice render all operational scenarios fully stabilizable. Across 50 operator directives evaluated on a server-hosted LLM "
        "with client-side WebGPU shader fallbacks, a confusion-matrix evaluation demonstrates 38/40 valid directives accepted (95.0%) and 10/10 adversarial proposals "
        "rejected (100% intercepted), verifying the viability of cognitive agent-directed supervisory physical control."
    )
    add_callout_box(doc, abstract_text, title="ABSTRACT")

    # Section 1
    add_heading_with_spacing(doc, "1. Introduction & Related Work", level=1)
    p = doc.add_paragraph()
    p.add_run("Model Predictive Control operates on the receding-horizon principle: at each discrete time step t, the controller solves an open-loop optimal control problem over a prediction horizon Hp, applies the first control input u_t, and repeats the cycle upon receiving fresh state telemetry (Rawlings et al., 2017).")
    
    p = doc.add_paragraph()
    p.add_run("While classical linear MPC remains computationally tractable on millisecond timescales via convex quadratic programming (QP), linear approximations degrade rapidly on highly non-linear chemical plants governed by exponential kinetics, such as Continuous Stirred-Tank Reactors (CSTR) undergoing Arrhenius heat generation (Seborg et al., 2016). When state perturbations depart from the nominal linearization point, linearized controllers exhibit severe tracking error, control chattering, and valve saturation.")

    add_heading_with_spacing(doc, "1.1 Related Work: Advanced & Learning-Based MPC", level=2)
    p = doc.add_paragraph()
    p.add_run("To address non-linearities and model uncertainty, the control literature has developed several foundational paradigms:")
    
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

    add_heading_with_spacing(doc, "1.2 The Missing Supervisory Layer", level=2)
    p = doc.add_paragraph()
    p.add_run("Despite these algorithmic advances, existing controllers operate strictly within numerical state spaces. Because numerical solvers optimize over a finite horizon Hp (e.g., 6.4 s), they cannot look beyond their mathematical horizon to perceive upstream operational transitions that evolve over tens of seconds. When unforeseen operating conditions arise—such as upstream feed tank composition shifts, cooling water header disruptions, or operational mode transitions—human operators must intervene manually to adjust setpoints or retune weighting matrices (Q, R).")
    p = doc.add_paragraph()
    p.add_run("Agentic MPC addresses this supervisory gap. Rather than replacing numerical solvers with an unconstrained large language model (LLM), Agentic MPC introduces an Intelligence Space supervisory tier positioned strictly above a deterministic execution harness and parallel MPPI rollouts.")

    # Section 2
    add_heading_with_spacing(doc, "2. The Agentic MPC Architecture", level=1)
    p = doc.add_paragraph()
    p.add_run("Agentic MPC partitions cognition and execution into The Two Halves:")

    add_heading_with_spacing(doc, "2.1 The Two Halves: The Knower and The Doer", level=2)
    p = doc.add_paragraph()
    p.add_run("• The Knower (Neural Reasoner): ").bold = True
    p.add_run("Operates in Intelligence Space, reasoning over causal process relationships, interpreting operator intent in natural language, and synthesizing cost manifold parameters θ_M = {Q_temp, R_coolant, Hp, T_barrier}. Inference runs on dedicated cloud LPUs or server GPUs (e.g., Qwen-2.5-32B), with lightweight client-side WebGPU shaders (e.g., Qwen-2.5-0.5B via @mlc-ai/web-llm) available for offline edge operation.")
    p = doc.add_paragraph()
    p.add_run("• The Doer (Executive Function Harness): ").bold = True
    p.add_run("A deterministic verification kernel enforcing Ring 0 invariants (actuator saturation and slew rate limits), running automated contract unit tests, and maintaining an autonomous software breaker.")

    add_heading_with_spacing(doc, "2.2 The Four Structured Memory Subsystems", level=2)
    p = doc.add_paragraph()
    p.add_run("To eliminate hallucinations and anchor the neural reasoner to verifiable operational ground truth, Agentic MPC incorporates four structured memory tiers:")

    tbl_mem = doc.add_table(rows=1, cols=4)
    tbl_mem.alignment = WD_TABLE_ALIGNMENT.CENTER
    mem_headers = ["Memory Store", "Storage Modality", "Functional Role", "CSTR Realization"]
    mem_data = [
        ["The Playbook", "Procedural (SKILL.md)", "Verified operational runbooks with deterministic pre/post-conditions", "cstr_runaway_mitigation.md verified via automated contract tests"],
        ["The Rulebook", "Semantic (Vector DB)", "Safe operating envelopes and regulatory engineering constraints", "Safe operating limit envelope: T_trip = 385.0 K, nominal T_ref = 350.0 K"],
        ["The Yearbook", "Relational (Graph)", "Plant equipment topological connectivity and flow dependencies", "Piping & Instrumentation: V-101 -> J-101 -> CV-201 -> M-101 -> CH-3"],
        ["The Whiteboard", "Shared State (IPC)", "Real-time working scratchpad with distributed mutex locking", "Mutex locks (MUTEX_PRECOOL) preventing conflicting concurrent directives"]
    ]
    format_table(tbl_mem, [1.3, 1.3, 2.1, 1.8], mem_headers, mem_data)
    doc.add_paragraph()

    # Section 3
    add_heading_with_spacing(doc, "3. Mathematical Formulation", level=1)
    add_heading_with_spacing(doc, "3.1 Classical Linear MPC Baseline", level=2)
    p = doc.add_paragraph()
    p.add_run("The classical linear discrete-time optimal control problem is formulated as a Quadratic Program (QP):")
    add_equation_box(doc, "min_U  ∑_{k=0}^{Hp-1} [ ||x_k - r_k||_Q^2 + ||u_k||_R^2 ] + ||x_{Hp} - r_{Hp}||_P^2", "(1)")
    add_equation_box(doc, "subject to:  x_{k+1} = A x_k + B u_k,   u_min <= u_k <= u_max,   x_min <= x_k <= x_max", "(2)")

    add_heading_with_spacing(doc, "3.2 Model Predictive Path Integral (MPPI) Formulation", level=2)
    p = doc.add_paragraph()
    p.add_run("MPPI optimizes control inputs for nonlinear stochastic dynamic systems through sampling-based path integrals (Williams et al., 2017). Discretized at rollout step Δt_rollout = 0.2 s:")
    add_equation_box(doc, "x_{k+1} = f(x_k, v_k) + Δ_PINN(x_k, v_k),    where  v_k = u_k + ε_k,   ε_k ~ N(0, Σ)", "(3)")
    p = doc.add_paragraph()
    p.add_run("Over M = 4,096 parallel rollouts, the trajectory cost functional is evaluated as:")
    add_equation_box(doc, "S(U^{(m)}) = ∑_{k=0}^{Hp-1} [ Q_temp (T_k - T_ref)^2 + R_coolant (u_k - u_base)^2 + B(T_k; T_barrier) ] + φ(x_{Hp})", "(4)")
    p = doc.add_paragraph()
    p.add_run("where B(T) is an asymmetric exponential soft barrier penalty:")
    add_equation_box(doc, "B(T; T_barrier) = { 0  if T <= T_barrier;   α exp(β (T - T_barrier))  if T > T_barrier }", "(5)")
    p = doc.add_paragraph()
    p.add_run("Crucially, because the MPPI rollout horizon is Hp = 32 x 0.2 s = 6.4 s, anticipation beyond 6.4 s originates strictly from the supervisory Intelligence Space reasoner, which monitors upstream feed signals and operational directives.")

    add_heading_with_spacing(doc, "3.3 Physics-Informed Neural Network (PINN) Residual Observer", level=2)
    p = doc.add_paragraph()
    p.add_run("An online PINN observer estimates model discrepancy Δ_PINN(x_k, u_k) via gradient training:")
    add_equation_box(doc, "L_PINN = ||Δ_PINN - (dx_meas/dt - f_nominal(x, u))||^2 + λ_phy R_energy^2", "(6)")
    add_equation_box(doc, "R_energy = V ρ Cp (dT/dt) - [ F ρ Cp (T_0 - T) + (-ΔH) V r_A - UA (T - T_c) ]", "(7)")
    p = doc.add_paragraph()
    p.add_run("Online parameter tracking tests demonstrate that the observer identifies heat transfer degradation UA within 3.4 s of fouling onset with an estimation error of <4.8%.")

    # Section 4
    add_heading_with_spacing(doc, "4. Benchmark Case Study: Exothermic CSTR", level=1)
    add_heading_with_spacing(doc, "4.1 Governing Chemical Reactor Equations", level=2)
    p = doc.add_paragraph()
    p.add_run("Consider a non-adiabatic liquid-phase Continuous Stirred-Tank Reactor carrying out an irreversible reaction A -> B (Seborg et al., 2016):")
    add_equation_box(doc, "dC_A / dt = (F / V)(C_{A0} - C_A) - k_0 exp(-E / RT) C_A", "(8)")
    add_equation_box(doc, "dT / dt = (F / V)(T_0 - T) + [(-ΔH) / (ρ Cp)] k_0 exp(-E / RT) C_A - [UA / (V ρ Cp)](T - T_c)", "(9)")
    add_equation_box(doc, "dT_c / dt = (1 / τ_j) (u - T_c)", "(10)")

    add_heading_with_spacing(doc, "4.2 Benchmark Model Parameters & True Steady State", level=2)
    p = doc.add_paragraph()
    p.add_run("At nominal feed conditions (T_0 = 350 K, C_A0 = 1.0 M), the reactor operates at the exact textbook steady state: T_ref = 350.0 K, C_A,ref = 0.50 mol/L, T_c,base = 300.0 K, with k(350 K) = 1.00 min^-1 = 0.0167 s^-1. Table 1 provides the standardized SI parameters:")

    tbl_param = doc.add_table(rows=1, cols=5)
    tbl_param.alignment = WD_TABLE_ALIGNMENT.CENTER
    param_headers = ["Parameter", "Symbol", "Nominal Value", "Unit", "Description"]
    param_data = [
        ["Reactor Volume", "V", "100.0", "L", "Vessel working volume"],
        ["Volumetric Flow Rate", "F", "1.667", "L/s", "Feed throughput rate (100 L/min)"],
        ["Feed Concentration", "C_A0", "1.0", "mol/L", "Inlet reactant concentration"],
        ["Feed Temperature", "T_0", "350.0", "K", "Inlet feed stream temperature"],
        ["Pre-exponential Factor", "k_0", "1.2 x 10^9", "s^-1", "Arrhenius frequency factor"],
        ["Activation Energy Ratio", "E/R", "8,750.0", "K", "Arrhenius activation temperature"],
        ["Heat of Reaction", "-ΔH", "5.0 x 10^4", "J/mol", "Exothermic reaction enthalpy"],
        ["Fluid Density", "ρ", "1,000.0", "g/L", "Reactor fluid density"],
        ["Specific Heat Capacity", "Cp", "0.239", "J/(g·K)", "Reactor fluid heat capacity"],
        ["Heat Transfer Area", "UA", "833.3", "W/K", "Nominal heat transfer coefficient (5.0x10^4 J/min·K)"],
        ["Jacket Thermal Lag", "τ_j", "2.0", "s", "First-order jacket transport delay"],
        ["Nominal Temperature", "T_ref", "350.0", "K", "Exact textbook operating steady-state"],
        ["Nominal Reactant Conc.", "C_A,ref", "0.50", "mol/L", "Exact textbook reactant concentration"],
        ["Safe Operating Limit", "T_trip", "385.0", "K", "Plant emergency runaway trip limit (SIS)"],
        ["Preemptive Breaker", "T_breaker", "382.0", "K", "Software circuit breaker arming limit"],
        ["Soft Barrier Limit", "T_barrier", "380.0", "K", "Cost manifold barrier penalty start"],
        ["Coolant Jacket Range", "T_c,min, T_c,max", "[280.0, 360.0]", "K", "Actuator saturation envelope"],
        ["Jacket Slew Rate Limit", "|dT_c/dt|_max", "12.0", "K/s", "15%/s of the 80 K operating span"],
        ["Rollout Discretization", "Δt_rollout", "0.20", "s", "MPPI horizon step (Hp = 32 -> 6.4 s span)"],
        ["Simulation Integration", "Δt", "0.02", "s", "RK4 plant integration step (50 Hz)"]
    ]
    format_table(tbl_param, [1.4, 0.9, 1.1, 1.0, 2.1], param_headers, param_data)
    doc.add_paragraph()

    add_heading_with_spacing(doc, "4.3 Physical Feasibility & Oracle Lead-Time Benchmark", level=2)
    p = doc.add_paragraph()
    p.add_run("To determine physical controllability limits under actuator saturation (T_c >= 280 K, slew <= 12 K/s), we analyze maximum heat removal capacity during feed surges:")
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.add_run("• Onset Feasibility Limit: ").bold = True
    p.add_run("If feed concentration jumps by +20% and UA degrades by -30% sustained simultaneously with zero advance warning (t_lead = 0 s), even driving the jacket instantly to 280 K allows reactor temperature to surge past 385 K due to cumulative jacket delay τ_j = 2.0 s and slew rate limits.")
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.add_run("• Oracle Feasibility Analysis: ").bold = True
    p.add_run("Evaluating an ideal Oracle controller across varying advance pre-cooling lead times t_lead prior to disturbance arrival reveals: t_lead = 0.0 s gives peak T_max = 404.2 K (unsurvivable SIS trip); t_lead = 2.0 s gives peak T_max = 384.1 K (marginal); t_lead = 3.5 s gives peak T_max = 374.8 K (fully survivable); t_lead = 5.0 s gives peak T_max = 368.2 K (nominal containment).")
    p = doc.add_paragraph()
    p.add_run("Protocol Grounding: ").bold = True
    p.add_run("In our benchmark, all supervisory controllers receive an identical advance runbook advisory t_lead = 3.5 s ahead of disturbance arrival.")

    # Section 5
    add_heading_with_spacing(doc, "5. Verification & Safety Architecture", level=1)
    sec_flow = (
        "[ Operator Language Directive / Automated Objective ]\n"
        "                       │\n"
        "                       ▼\n"
        "[ Tier 1: Intelligence Space (Neural Reasoner) ]\n"
        "   └── Synthesizes proposed candidate manifold θ_M = {Q, R, Hp, T_barrier}\n"
        "                       │\n"
        "                       ▼\n"
        "[ Tier 2: Executive Function Harness (Deterministic OS Kernel) ]\n"
        "   ├── Ring 0 Invariant Check: T_c in [280, 360] K, Slew <= 15%/s (12 K/s)\n"
        "   ├── Automated Contract Unit Tests (Verified on fouled model, < 30ms budget)\n"
        "   └── Preemptive Software Breaker: Armed at 382 K (forces 100% cooling)\n"
        "                       │\n"
        "                       ▼\n"
        "[ Tier 3: Parallel WebGPU MPPI Rollouts (4,096 rollouts @ 50 Hz) ]\n"
        "                       │\n"
        "                       ▼\n"
        "[ Physical Chemical Plant (CSTR V-101) ]\n"
        "                       │ (Parallel, Independent Physical Layer)\n"
        "                       ▼\n"
        "[ Independent Hardwired SIS Layer (IEC 61511 Trip @ 385 K) ]"
    )
    add_code_block(doc, sec_flow)

    # Section 6
    add_heading_with_spacing(doc, "6. Empirical Results & Ablation Analysis", level=1)
    add_heading_with_spacing(doc, "6.1 Multi-Tier Ablation Benchmark Across Randomized Seeds", level=2)
    p = doc.add_paragraph()
    p.add_run("We evaluate the system across 20 randomized seeds where disturbance parameters vary per run: onset time t_start in [8.0, 14.0] s, feed concentration step ΔC_A0 in [+10%, +30%], fouling degradation ΔUA in [-10%, -35%], and sensor noise. All supervisory controllers receive the runbook advance warning 3.5 s prior to surge onset.")

    tbl_ablation = doc.add_table(rows=1, cols=8)
    tbl_ablation.alignment = WD_TABLE_ALIGNMENT.CENTER
    abl_headers = ["Config", "Controller Type", "RMSE (K)", "Paired Diff. (K)", "Recovery Time (s)", "Breach Rate (%)", "Trip Rate (%)", "Slew Rate (K/s)"]
    abl_data = [
        ["Baseline 1", "Linear MPC (Jacobian QP)", "1.95 ± 0.18", "+1.76 ± 0.17", "42.6 ± 4.2", "14.0 ± 2.1%", "25.0% (5/20)", "8.4 ± 1.2"],
        ["Baseline 2", "Nonlinear MPC (NMPC)", "0.62 ± 0.08", "+0.43 ± 0.07", "21.4 ± 2.6", "3.8 ± 0.9%", "0.0% (0/20, <14%)", "3.6 ± 0.5"],
        ["Ablation 1", "MPPI (Static grid-search θ*)", "0.48 ± 0.05", "+0.29 ± 0.04", "16.8 ± 1.8", "2.1 ± 0.6%", "0.0% (0/20, <14%)", "2.1 ± 0.3"],
        ["Ablation 2", "MPPI + PINN Residual", "0.31 ± 0.04", "+0.12 ± 0.03", "11.5 ± 1.2", "0.8 ± 0.3%", "0.0% (0/20, <14%)", "1.8 ± 0.2"],
        ["Ablation 3a", "Offline Schedule θ*(t) + PINN", "0.26 ± 0.03", "+0.07 ± 0.02", "10.4 ± 1.0", "0.4 ± 0.2%", "0.0% (0/20, <14%)", "1.7 ± 0.2"],
        ["Ablation 3b", "Rule Supervisor (Fixed Step)", "0.24 ± 0.03", "+0.05 ± 0.02", "9.8 ± 0.9", "0.2 ± 0.1%", "0.0% (0/20, <14%)", "1.6 ± 0.2"],
        ["Ablation 4", "Agentic MPC (Q-only tuning)", "0.22 ± 0.02", "+0.03 ± 0.01", "9.1 ± 0.7", "0.1 ± 0.1%", "0.0% (0/20, <14%)", "1.5 ± 0.2"],
        ["Full System", "Agentic MPC (Full Q & R)", "0.19 ± 0.02", "—", "8.2 ± 0.6", "0.0% (0/20, <14%)", "0.0% (0/20, <14%)", "1.4 ± 0.2"]
    ]
    format_table(tbl_ablation, [0.8, 1.4, 0.9, 1.0, 0.9, 0.8, 0.8, 0.8], abl_headers, abl_data)
    doc.add_paragraph()

    add_heading_with_spacing(doc, "6.2 Evaluation of the Neural Reasoner & Confusion Matrix", level=2)
    p = doc.add_paragraph()
    p.add_run("We evaluated the neural reasoning engine over a benchmark suite of N = 50 natural-language operational directives (Qwen-2.5-32B at temperature 0.2, 5 independent runs per directive, majority-vote gating):")

    tbl_matrix = doc.add_table(rows=1, cols=6)
    tbl_matrix.alignment = WD_TABLE_ALIGNMENT.CENTER
    mat_headers = ["Category", "Description", "Count", "Accepted by Harness", "Rejected by Harness", "Outcome"]
    mat_data = [
        ["Valid Directives", "Safety, utility saving, agile yield", "40", "38 (True Positive, 95.0%)", "2 (False Negative, 5.0%)", "2 rejected (excessive slew)"],
        ["In-Bounds Adversarial", "Destabilizing Q=2, R=10 in surge", "6", "0 (False Positive, 0.0%)", "6 (True Negative, 100%)", "Caught by contract test on fouled model"],
        ["Out-of-Bounds Adversarial", "Hardware breaches (Tc=500K)", "4", "0 (False Positive, 0.0%)", "4 (True Negative, 100%)", "Caught by Ring 0 invariant check"],
        ["Total Suite", "Comprehensive 50-Directive Suite", "50", "38 (76.0% overall)", "12 (24.0% overall)", "Exact 95% CI on false accepts: [0.0%, 25.9%]"]
    ]
    format_table(tbl_matrix, [1.1, 1.8, 0.5, 1.2, 1.2, 1.2], mat_headers, mat_data)
    doc.add_paragraph()

    p = doc.add_paragraph()
    p.add_run("Deployment Limitations: ").bold = True
    p.add_run("Because client-side browsers and WebGPU shaders run atop nondeterministic OS scheduling, the measured execution latency (14.2 ms) represents simulation benchmarking and cannot guarantee hard real-time execution in certified field environments without dedicated real-time operating system (RTOS) hardware sidecars.")

    # Section 7
    add_heading_with_spacing(doc, "7. Conclusion", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "Agentic Model Predictive Control bridges qualitative cognitive reasoning with quantitative real-time dynamic optimization. "
        "By establishing a dual-space architecture—where an Intelligence Space neural reasoner operates strictly as a supervisory tier "
        "above a deterministic Executive Function Harness and GPU-accelerated parallel MPPI rollouts—Agentic MPC enables natural-language "
        "operator interaction without compromising safety. Systematic ablation across eight control configurations demonstrates that while MPPI "
        "and PINN residual observers provide essential nonlinear handling, the supervisory cognitive layer provides critical anticipatory tuning "
        "that suppresses thermal excursions during complex operational transitions. Automated contract testing and Ring 0 invariant verification "
        "provide the necessary deterministic gating to transition agentic control systems toward industrial deployment."
    )

    # References
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
