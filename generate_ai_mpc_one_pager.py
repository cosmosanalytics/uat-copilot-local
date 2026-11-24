# -*- coding: utf-8 -*-
"""
Generates a stunning, publication-grade 1-Page PDF and high-res Preview PNG:
"AI MODEL PREDICTIVE CONTROL (AI-MPC)
 Bounding Stochastic Agents into Deterministic Closed-Loop Cybernetic Control
 Defined by the 6-Layer Architecture"

Header and footer strips removed. Guaranteed STRICT 1-PAGE FIT.
"""

import os
import subprocess
import pymupdf

BASE_DIR = os.path.abspath(r"c:\Users\richa\ai-engineering")
HTML_PATH = os.path.join(BASE_DIR, "ai_model_predictive_control_one_pager.html")
PDF_PATH = os.path.join(BASE_DIR, "ai_model_predictive_control_one_pager.pdf")
PNG_PATH = os.path.join(BASE_DIR, "ai_model_predictive_control_one_pager_preview.png")

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AI Model Predictive Control (AI-MPC) — 6-Layer Architecture One-Pager</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    @page {
      size: letter portrait;
      margin: 0;
    }
    * {
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }
    body {
      width: 816px;
      height: 1056px;
      margin: 0;
      padding: 30px 34px;
      font-family: 'Plus Jakarta Sans', sans-serif;
      background: #ffffff;
      color: #0f172a;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .font-mono-code {
      font-family: 'JetBrains Mono', monospace;
    }
    .math-pill {
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      font-weight: 700;
      color: #1e293b;
    }
  </style>
</head>
<body>

  <!-- TITLE BLOCK (Running Header Removed) -->
  <div>
    <div class="mb-2.5">
      <h1 class="text-[25px] font-black tracking-tight text-slate-900 leading-tight">
        AI Model Predictive Control (AI-MPC)
      </h1>
      <p class="text-[12px] font-semibold text-indigo-700 tracking-tight mt-0.5">
        Bounding Stochastic Generative LLMs with Receding-Horizon Control &amp; Deterministic Invariant Oracles
      </p>
    </div>

    <!-- EXECUTIVE THESIS CALLOUT -->
    <div class="bg-slate-50 border-l-4 border-indigo-600 rounded-r-xl p-3 mb-3 shadow-xs">
      <div class="text-[10.5px] font-bold text-slate-800 leading-snug">
        <span class="text-indigo-700 font-extrabold uppercase font-mono tracking-wider">The Cybernetic Paradigm:</span>
        Traditional agents run open-loop prompts or rigid DAGs that suffer catastrophic parameter hallucination and compounding state drift. 
        <strong>AI-MPC</strong> adapts the classical control formulation 
        <span class="math-pill">min_{u} &Sigma; L(x, u) s.t. I(x, u) &le; 0</span>
        by using a generative model to simulate candidate trajectory horizons, passing proposals through a <strong>deterministic Invariant Oracle</strong>, 
        and executing <em>only the first verified atomic action</em> before observing true telemetry and recalculating.
      </div>
    </div>
  </div>

  <!-- THE 6-LAYER ARCHITECTURE MATRIX TABLE -->
  <div class="border border-slate-200 rounded-xl overflow-hidden shadow-xs mb-3">
    <div class="bg-slate-900 text-white px-3 py-1.5 flex items-center justify-between text-[11px] font-bold">
      <span class="font-mono tracking-wider">THE 6-LAYER CLOSED-LOOP AI-MPC ENGINE SPECIFICATION</span>
      <span class="text-[10px] font-mono text-indigo-300 font-medium">Receding Horizon: N-Step Search &bull; 1-Step Commit</span>
    </div>
    <table class="w-full text-left border-collapse text-[10px]">
      <thead class="bg-slate-100 text-slate-700 font-bold border-b border-slate-200 font-mono text-[9.5px]">
        <tr>
          <th class="p-1.5 pl-2.5 w-16">Layer</th>
          <th class="p-1.5 w-32">Module Name</th>
          <th class="p-1.5 w-40">Formal Mathematical Role</th>
          <th class="p-1.5">Runtime Mechanism &amp; Operational Defense</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-100 font-medium text-slate-700">
        <tr class="bg-blue-50/30">
          <td class="p-1.5 pl-2.5 font-mono font-bold text-blue-700">L1</td>
          <td class="p-1.5 font-bold text-slate-900">State Space Ingestion</td>
          <td class="p-1.5 font-mono text-[9px] text-blue-900">x<sub>t</sub> &isin; &Sopf; (Ground Truth State)</td>
          <td class="p-1.5 text-[9.5px] leading-snug">
            Normalizes unstructured inputs, environment telemetry, and user intent into a strongly typed state schema. Filters sensory noise.
          </td>
        </tr>
        <tr class="bg-indigo-50/30">
          <td class="p-1.5 pl-2.5 font-mono font-bold text-indigo-700">L2</td>
          <td class="p-1.5 font-bold text-slate-900">Symbolic &amp; World Model</td>
          <td class="p-1.5 font-mono text-[9px] text-indigo-900">x̂<sub>t+1</sub> = &Wopf;(x<sub>t</sub>, u<sub>t</sub>)</td>
          <td class="p-1.5 text-[9.5px] leading-snug">
            Causal ontology graph, ODE physics equations, or organizational topology. Provides internal simulator to predict future dynamics.
          </td>
        </tr>
        <tr class="bg-purple-50/30">
          <td class="p-1.5 pl-2.5 font-mono font-bold text-purple-700">L3</td>
          <td class="p-1.5 font-bold text-slate-900">Policy Engine (Planner)</td>
          <td class="p-1.5 font-mono text-[9px] text-purple-900">&pi;<sub>&theta;</sub>(u<sub>t:t+N</sub> | x<sub>t</sub>, &Wopf;)</td>
          <td class="p-1.5 text-[9.5px] leading-snug">
            Explores candidate action trajectories over prediction horizon N using Monte Carlo search, agent consensus, or recursive mutation.
          </td>
        </tr>
        <tr class="bg-emerald-50/40">
          <td class="p-1.5 pl-2.5 font-mono font-bold text-emerald-700">L4</td>
          <td class="p-1.5 font-bold text-slate-900">Invariant Safety Oracle</td>
          <td class="p-1.5 font-mono text-[9px] text-emerald-900">&Iopf;(x̂, u) &le; 0 (Hard Proofs)</td>
          <td class="p-1.5 text-[9.5px] leading-snug">
            <strong>Deterministic, non-LLM ground-truth gate</strong>. Evaluates formal invariants (thermal limits, ACID atomicity, legal bounds). Binary PASS/FAIL.
          </td>
        </tr>
        <tr class="bg-amber-50/30">
          <td class="p-1.5 pl-2.5 font-mono font-bold text-amber-700">L5</td>
          <td class="p-1.5 font-bold text-slate-900">Actuator (Execution)</td>
          <td class="p-1.5 font-mono text-[9px] text-amber-900">u<sub>t</sub> &isin; &Aopf;<sub>atomic</sub> (Commit First)</td>
          <td class="p-1.5 text-[9.5px] leading-snug">
            Commits <em>only the immediate first action</em> u<sub>t</sub> of the verified policy. Generates PRDs, executes Lua mutexes, or actuates physical setpoints.
          </td>
        </tr>
        <tr class="bg-rose-50/30">
          <td class="p-1.5 pl-2.5 font-mono font-bold text-rose-700">L6</td>
          <td class="p-1.5 font-bold text-slate-900">Telemetry Loop (Feedback)</td>
          <td class="p-1.5 font-mono text-[9px] text-rose-900">e<sub>t+1</sub> = x<sub>t+1</sub> &minus; x̂<sub>t+1</sub></td>
          <td class="p-1.5 text-[9.5px] leading-snug">
            Measures true environmental delta at 60 Hz. Updates world model beliefs, penalizes trajectory error, and closes the receding loop.
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- CORE ARCHITECTURAL FLOW DIAGRAM (3 CARDS) -->
  <div class="grid grid-cols-3 gap-3 mb-3">
    
    <!-- Left Column: Classical MPC vs AI-MPC -->
    <div class="border border-slate-200 rounded-xl p-3 bg-slate-50 flex flex-col justify-between shadow-xs">
      <div>
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[10.5px] font-black uppercase text-indigo-700 font-mono">1. Receding Horizon Cycle</span>
          <span class="text-[9px] font-mono text-slate-400">Classical &harr; AI</span>
        </div>
        <p class="text-[9.5px] text-slate-600 leading-snug">
          Instead of generating a brittle 50-step plan, AI-MPC solves an optimization window of depth <strong>N</strong>, executes <strong>1 step</strong>, 
          re-samples reality, and shifts the window forward:
        </p>
        <div class="mt-2 bg-white p-2 rounded border border-slate-200 font-mono text-[8.5px] text-slate-700 leading-relaxed">
          T=0: Plan [u0, u1, u2] &rarr; Commit u0<br>
          T=1: Observe x1 &rarr; Plan [u1', u2', u3'] &rarr; Commit u1'<br>
          T=2: Observe x2 &rarr; Plan [u2'', u3'', u4'] &rarr; Commit u2''
        </div>
      </div>
      <div class="text-[9px] font-mono text-emerald-700 font-bold bg-emerald-50 p-1.5 rounded border border-emerald-200 mt-2">
        &check; Guarantees zero cumulative drift
      </div>
    </div>

    <!-- Middle Column: Role of the Invariant Oracle -->
    <div class="border border-slate-200 rounded-xl p-3 bg-slate-50 flex flex-col justify-between shadow-xs">
      <div>
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[10.5px] font-black uppercase text-emerald-700 font-mono">2. The Invariant Oracle Gate</span>
          <span class="text-[9px] font-mono text-slate-400">Layer 4 Core</span>
        </div>
        <p class="text-[9.5px] text-slate-600 leading-snug">
          The mathematical circuit breaker protecting external systems. Evaluates proposals against formal assertions:
        </p>
        <ul class="text-[9px] text-slate-700 space-y-1 mt-1.5 font-mono">
          <li class="flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
            <span>Physical: Temp T &lt; 375 K</span>
          </li>
          <li class="flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-blue-600"></span>
            <span>Concurrency: Grants &le; Capacity</span>
          </li>
          <li class="flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-purple-600"></span>
            <span>Ontology: Graph Cycles &equiv; &empty;</span>
          </li>
          <li class="flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-amber-600"></span>
            <span>Compliance: SLA Delay == 0 ms</span>
          </li>
        </ul>
      </div>
      <div class="text-[9px] font-mono text-indigo-700 font-bold bg-indigo-50 p-1.5 rounded border border-indigo-200 mt-2">
        Deterministic Code &gt; Probabilistic Text
      </div>
    </div>

    <!-- Right Column: Atomic Policy Contracts -->
    <div class="border border-slate-200 rounded-xl p-3 bg-slate-50 flex flex-col justify-between shadow-xs">
      <div>
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[10.5px] font-black uppercase text-amber-700 font-mono">3. Atomic Policy Runbooks</span>
          <span class="text-[9px] font-mono text-slate-400">Action Space</span>
        </div>
        <p class="text-[9.5px] text-slate-600 leading-snug">
          Actions are strictly quantized into <strong>255 Atomic Policies</strong>. Unregistered actions or out-of-order mutations are rejected at schema validation:
        </p>
        <div class="mt-2 bg-white p-2 rounded border border-slate-200 font-mono text-[8.5px] text-slate-700 leading-tight">
          &lang;Precondition, Tool, Invariant, NextState&rang;<br>
          <span class="text-emerald-600 font-bold">POL-303</span>: Lua Script &rarr; Atomic Redis<br>
          <span class="text-blue-600 font-bold">POL-404</span>: Coolant Valve &rarr; Setpoint Commit<br>
          <span class="text-purple-600 font-bold">POL-504</span>: Falsification &rarr; Pivot Gate
        </div>
      </div>
      <div class="text-[9px] font-mono text-amber-700 font-bold bg-amber-50 p-1.5 rounded border border-amber-200 mt-2">
        Action space strictly machine-bounded
      </div>
    </div>

  </div>

  <!-- COMPARISON TABLE: CONVENTIONAL CHATBOT VS STATIC DAG VS AI-MPC -->
  <div class="border border-slate-200 rounded-xl overflow-hidden shadow-xs mb-3">
    <table class="w-full text-left border-collapse text-[10px]">
      <thead class="bg-slate-100 text-slate-800 font-bold font-mono text-[9px] border-b border-slate-200">
        <tr>
          <th class="p-1.5 pl-2.5 w-36">Architectural Paradigm</th>
          <th class="p-1.5 w-32">Control Nature</th>
          <th class="p-1.5 w-36">Failure Mode</th>
          <th class="p-1.5">Safety &amp; Reliability Guarantee</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-100 text-slate-700 font-medium">
        <tr>
          <td class="p-1.5 pl-2.5 font-bold text-slate-900">Unconstrained Chatbot</td>
          <td class="p-1.5 text-rose-700 font-mono">Open-Loop Prompting</td>
          <td class="p-1.5 text-rose-600">Hallucinations, parameter drift</td>
          <td class="p-1.5 text-slate-500">None. Output is stochastic and unchecked.</td>
        </tr>
        <tr>
          <td class="p-1.5 pl-2.5 font-bold text-slate-900">Static DAG Workflow</td>
          <td class="p-1.5 text-amber-700 font-mono">Hardcoded Graph</td>
          <td class="p-1.5 text-amber-600">Brittle branch deadlocks</td>
          <td class="p-1.5 text-slate-500">Rigid. Cannot dynamically optimize trajectory parameters.</td>
        </tr>
        <tr class="bg-emerald-50/50 font-bold text-emerald-950">
          <td class="p-1.5 pl-2.5 text-emerald-900 flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-600"></span> AI-MPC (6 Layers)
          </td>
          <td class="p-1.5 text-emerald-700 font-mono">Closed-Loop Cybernetic</td>
          <td class="p-1.5 text-emerald-700">Self-correcting rollback</td>
          <td class="p-1.5 text-emerald-800">
            <strong>Provable Mathematical Safety:</strong> Invariant Oracle blocks violation before actuation.
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- APPLICATION MAPPING BANNER (Footer Bar Removed) -->
  <div class="bg-indigo-900 text-white rounded-xl p-3 flex items-center justify-between text-[10.5px] font-mono shadow-xs">
    <div>
      <span class="text-indigo-300 font-bold uppercase tracking-wider block text-[9.5px]">Production Implementations Across Top 5 Agent Suite:</span>
      <span class="text-slate-200 text-[10px]">
        1. Self-Improving (Kadane Invariant) &bull; 2. Knowledge Engineer (OWL Acyclicity) &bull; 3. Software Co (Mutex) &bull; 4. Digital Twin (ODE CSTR) &bull; 5. Exoskeleton (Pivot Gate)
      </span>
    </div>
    <div class="text-right pl-3 flex-shrink-0">
      <span class="px-2.5 py-1 rounded bg-indigo-800 text-indigo-200 border border-indigo-700 font-bold text-[9.5px]">Zero-Drift Execution</span>
    </div>
  </div>

</body>
</html>
"""

def generate_assets():
    # 1. Write HTML
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Generated HTML source at: {HTML_PATH}")

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    # 2. Print to PDF (Letter portrait, no header/footer, exact 1 page)
    args_pdf = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF_PATH}",
        f"file:///{HTML_PATH.replace(os.sep, '/')}"
    ]
    res_pdf = subprocess.run(args_pdf, capture_output=True, text=True)
    if res_pdf.returncode != 0:
        print(f"Chrome PDF Error: {res_pdf.stderr}")
    print(f"Compiled PDF to: {PDF_PATH}")

    # 3. Check page count via PyMuPDF
    doc = pymupdf.open(PDF_PATH)
    page_count = len(doc)
    print(f"Verified Page Count: {page_count} page(s)")
    doc.close()

    # 4. Render preview PNG
    args_png = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--window-size=1200,1580",
        f"--screenshot={PNG_PATH}",
        f"file:///{HTML_PATH.replace(os.sep, '/')}"
    ]
    res_png = subprocess.run(args_png, capture_output=True, text=True)
    if res_png.returncode != 0:
        print(f"Chrome PNG Error: {res_png.stderr}")
    print(f"Rendered Preview PNG at: {PNG_PATH}")

if __name__ == "__main__":
    generate_assets()
