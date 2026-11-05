# -*- coding: utf-8 -*-
"""
apply_order_123.py
Implements:
1. Unified Triad Cross-Graph View (Tab 6) with explicit cross-graph edges.
2. Domain Subgraph Navigation (Billing, Telecom, Enterprise, Macro All-Domains).
3. Real-Time Animated Graph Growth stepper in the Live Call Simulator.
"""

import sys
import re

def build_app():
    # Let's read the current callcenter_ai_voice_agents.html
    with open('callcenter_ai_voice_agents.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean out the misplaced script block from <head> if present
    # Look for "// REAL-TIME CALL SIMULATOR (GROUNDED IN KG & CG)" in <head>
    head_match = re.search(r'(<script>\s*tailwind\.config = \{.*?\};\s*)(// =========================================================================\s*// REAL-TIME CALL SIMULATOR.*?)(</script>\s*<style>)', content, re.DOTALL)
    if head_match:
        print("Cleaning up misplaced script in head...")
        clean_head = head_match.group(1) + head_match.group(3)
        content = content[:head_match.start()] + clean_head + content[head_match.end():]

    # 1. Update Navigation to have 6 Tabs:
    # 1. Agent Hierarchical Structure
    # 2. SOP Knowledge Graph (Rulebook)
    # 3. Call Records Context Graph (Diary)
    # 4. Business Goals & ROI Graph
    # 5. 📞 Real-Time Live Call
    # 6. 🌐 Cross-Graph Triad (Unified)
    nav_pattern = r'<nav class="bg-white dark:bg-slate-900 border-b border-slate-200.*?<!-- Active Preset Pill -->'
    new_nav = '''<nav class="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-4 sm:px-6 py-2.5 flex items-center justify-between shrink-0 text-xs sticky top-[61px] z-30 shadow-2xs">
    <div class="flex items-center space-x-1.5 sm:space-x-2 overflow-x-auto">
      <button onclick="switchTab('hierarchy')" id="tab-hierarchy" class="tab-btn px-3 py-1.5 rounded-lg font-bold bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 transition flex items-center space-x-1.5">
        <i class="fa-solid fa-sitemap"></i>
        <span>1. Agent Hierarchical Structure</span>
      </button>
      <button onclick="switchTab('kg')" id="tab-kg" class="tab-btn px-3 py-1.5 rounded-lg font-bold text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 transition flex items-center space-x-1.5">
        <i class="fa-solid fa-book-open text-indigo-500"></i>
        <span>2. SOP Knowledge Graph</span>
      </button>
      <button onclick="switchTab('cg')" id="tab-cg" class="tab-btn px-3 py-1.5 rounded-lg font-bold text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 transition flex items-center space-x-1.5">
        <i class="fa-solid fa-phone-volume text-amber-500"></i>
        <span>3. Call Records Context Graph</span>
      </button>
      <button onclick="switchTab('bg')" id="tab-bg" class="tab-btn px-3 py-1.5 rounded-lg font-bold text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 transition flex items-center space-x-1.5">
        <i class="fa-solid fa-chart-line text-emerald-500"></i>
        <span>4. Business Goals &amp; ROI Graph</span>
      </button>
      <button onclick="switchTab('call')" id="tab-call" class="tab-btn px-3 py-1.5 rounded-lg font-bold text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 transition flex items-center space-x-1.5">
        <i class="fa-solid fa-phone-arrow-down-left text-emerald-500"></i>
        <span>5. 📞 Real-Time Live Call</span>
      </button>
      <button onclick="switchTab('triad')" id="tab-triad" class="tab-btn px-3 py-1.5 rounded-lg font-bold text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 transition flex items-center space-x-1.5 bg-gradient-to-r hover:from-indigo-50 hover:to-emerald-50 dark:hover:from-indigo-950/40 dark:hover:to-emerald-950/40">
        <i class="fa-solid fa-diagram-project text-indigo-500"></i>
        <span>6. 🌐 Cross-Graph Triad (Unified)</span>
      </button>
    </div>

    <!-- Active Preset Pill -->'''

    content = re.sub(nav_pattern, new_nav, content, flags=re.DOTALL)

    # 2. Update Domain selector options to include Macro Enterprise All-Domains
    preset_pattern = r'<select id="preset-select" onchange="loadScenarioPreset\(this\.value\)".*?</select>'
    new_preset_select = '''<select id="preset-select" onchange="loadScenarioPreset(this.value)" class="bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1 text-xs font-bold text-slate-800 dark:text-slate-200 focus:outline-none">
        <option value="billing_dispute" selected>💳 1. Billing Dispute &amp; Fee Waiver (SOP-04)</option>
        <option value="tech_outage">🌐 2. Broadband Hardware Outage (SOP-12)</option>
        <option value="vip_retention">💼 3. Enterprise Churn &amp; Renewal (SOP-28)</option>
        <option value="all_domains">🌍 4. Macro Enterprise (All 3 Domains Unified)</option>
      </select>'''
    content = re.sub(preset_pattern, new_preset_select, content, flags=re.DOTALL)

    # 3. Add view-triad right after view-call and before closing main view wrapper
    view_triad_html = '''
      <!-- ================================================================= -->
      <!-- VIEW 6: UNIFIED TRIAD CROSS-GRAPH VIEW (KG + CG + BG SYNTHESIS)   -->
      <!-- ================================================================= -->
      <div id="view-triad" class="view-panel flex-1 flex flex-col hidden overflow-hidden">
        <!-- TOP CONTROL & DOMAIN FILTER STRIP -->
        <div class="p-3 bg-slate-50 dark:bg-slate-850 border-b border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs shrink-0">
          <div class="flex items-center space-x-2">
            <span class="w-2.5 h-2.5 rounded-full bg-gradient-to-r from-indigo-500 via-amber-500 to-emerald-500"></span>
            <strong class="text-slate-900 dark:text-white">Unified Triad Cross-Graph Engine</strong>
            <span class="text-slate-400 hidden md:inline">&bull; Co-locates SOP Rulebook, Live Call Diary &amp; Business ROI with Cross-Graph Edges</span>
          </div>

          <!-- Domain Subgraph Filter Pills -->
          <div class="flex items-center space-x-1.5 bg-slate-200/70 dark:bg-slate-800 p-1 rounded-xl">
            <button onclick="filterTriadDomain('billing')" id="triad-filter-billing" class="px-2.5 py-1 rounded-lg text-[11px] font-bold bg-white dark:bg-slate-700 text-indigo-700 dark:text-indigo-300 shadow-2xs transition">
              💳 Billing (SOP-04)
            </button>
            <button onclick="filterTriadDomain('outage')" id="triad-filter-outage" class="px-2.5 py-1 rounded-lg text-[11px] font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">
              🌐 Telecom (SOP-12)
            </button>
            <button onclick="filterTriadDomain('retention')" id="triad-filter-retention" class="px-2.5 py-1 rounded-lg text-[11px] font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">
              💼 Enterprise (SOP-28)
            </button>
            <button onclick="filterTriadDomain('all')" id="triad-filter-all" class="px-2.5 py-1 rounded-lg text-[11px] font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition">
              🌍 All Domains Unified
            </button>
          </div>

          <div class="flex items-center space-x-2">
            <button onclick="resetGraphView('triad-network')" class="px-2.5 py-1 rounded bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-semibold hover:bg-slate-100 dark:hover:bg-slate-700">
              <i class="fa-solid fa-arrows-to-dot mr-1"></i> Center Triad
            </button>
          </div>
        </div>

        <!-- TRIAD VIS.JS CANVAS -->
        <div class="flex-1 relative bg-slate-950" id="triad-canvas-container">
          <div id="triad-network" class="w-full h-full"></div>

          <!-- Unified Legend Overlay -->
          <div class="absolute bottom-3 left-3 bg-slate-900/95 border border-slate-800 rounded-xl p-3 text-[11px] text-white shadow-lg pointer-events-none max-w-xs space-y-2">
            <div class="font-extrabold text-slate-400 uppercase text-[9px] tracking-wider">Unified Triad Layers &amp; Cross-Edges</div>
            <div class="grid grid-cols-2 gap-x-3 gap-y-1 text-[10px]">
              <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded bg-indigo-500"></span><span>KG: SOP Rulebook</span></div>
              <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span><span>CG: Call Diary / Event</span></div>
              <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-sm bg-emerald-500"></span><span>BG: Financial / ROI</span></div>
              <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-sm bg-purple-500 rotate-45"></span><span>BG: Policy Drift Signal</span></div>
            </div>
            <div class="pt-1.5 border-t border-slate-800 text-[10px] space-y-0.5 text-slate-300">
              <div class="flex items-center justify-between"><span class="text-red-400 font-mono">-- evaluates_against &rarr;</span><span class="text-[9px] text-slate-400">CG &rarr; KG</span></div>
              <div class="flex items-center justify-between"><span class="text-indigo-400 font-mono">&mdash; conforms_to &rarr;</span><span class="text-[9px] text-slate-400">CG &rarr; KG</span></div>
              <div class="flex items-center justify-between"><span class="text-emerald-400 font-mono">&mdash; measures_into &rarr;</span><span class="text-[9px] text-slate-400">CG &rarr; BG</span></div>
              <div class="flex items-center justify-between"><span class="text-pink-400 font-mono">-- updates_rule &rarr;</span><span class="text-[9px] text-slate-400">BG &rarr; KG (Loop)</span></div>
            </div>
          </div>

          <!-- Node Inspection Pill (Updated on node click) -->
          <div id="triad-inspector-card" class="absolute top-3 right-3 bg-slate-900/90 border border-slate-700/80 rounded-xl p-3 text-xs text-white shadow-xl max-w-sm hidden">
            <div class="flex items-center justify-between mb-1">
              <span id="inspect-tier-badge" class="px-2 py-0.5 rounded text-[9px] font-extrabold uppercase bg-indigo-500 text-white">Knowledge Graph</span>
              <button onclick="document.getElementById('triad-inspector-card').classList.add('hidden')" class="text-slate-400 hover:text-white">&times;</button>
            </div>
            <h5 id="inspect-title" class="font-bold text-white text-xs">SOP-04: Billing &amp; Roaming Disputes</h5>
            <p id="inspect-desc" class="text-slate-300 text-[11px] mt-1 leading-relaxed">Canonical policy governing fee waivers, agent discretionary limits, and VIP exception escalations.</p>
            <div class="mt-2 pt-2 border-t border-slate-800 text-[10px] text-slate-400 flex items-center justify-between">
              <span id="inspect-conn-count">Connected to 3 nodes</span>
              <span class="text-emerald-400 font-mono font-bold">Cross-Graph Active</span>
            </div>
          </div>
        </div>
      </div>
'''

    # Insert view-triad before the bottom run panel
    bottom_run_marker = '    <!-- BOTTOM RUN & RAW RECORD VIEWER -->'
    if 'id="view-triad"' not in content:
        content = content.replace(bottom_run_marker, view_triad_html + '\n    ' + bottom_run_marker, 1)

    # 4. In Live Call Simulator (view-call), add the Real-Time Animated Graph Growth Stepper widget!
    stepper_html = '''
        <!-- REAL-TIME GRAPH GROWTH TIMELINE (ORDER 3 ANIMATION ENGINE) -->
        <div class="bg-gradient-to-r from-slate-900 via-indigo-950/70 to-slate-900 border border-indigo-900/60 rounded-2xl p-4 shadow-sm text-white">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
            <div class="flex items-center space-x-2">
              <span class="flex h-2.5 w-2.5 relative">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-indigo-500"></span>
              </span>
              <h4 class="text-xs font-black uppercase tracking-wider text-white">Real-Time Graph Growth &bull; Step-by-Step Propagation</h4>
            </div>

            <div class="flex items-center space-x-3 text-[11px]">
              <div class="flex items-center space-x-1.5 font-mono text-[10px]">
                <span class="px-2 py-0.5 rounded bg-indigo-900/80 border border-indigo-700/60 text-indigo-300" id="badge-kg-count">KG: 6 Rules</span>
                <span class="px-2 py-0.5 rounded bg-amber-900/80 border border-amber-700/60 text-amber-300" id="badge-cg-count">CG: 3 Events (+2)</span>
                <span class="px-2 py-0.5 rounded bg-emerald-900/80 border border-emerald-700/60 text-emerald-300" id="badge-bg-count">BG: 3 Metrics (+2)</span>
              </div>
              <button onclick="replayGraphGrowthAnimation()" class="px-2.5 py-1 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-[10px] transition flex items-center space-x-1">
                <i class="fa-solid fa-play"></i>
                <span>Replay Graph Growth</span>
              </button>
            </div>
          </div>

          <!-- 4 Sequential Stage Indicators -->
          <div class="grid grid-cols-1 sm:grid-cols-4 gap-2.5">
            <!-- Stage 1 -->
            <div id="step-growth-1" class="growth-step-card p-2.5 rounded-xl border border-indigo-500/80 bg-indigo-950/60 transition-all duration-300">
              <div class="flex items-center justify-between text-[10px] font-mono text-indigo-400 font-bold mb-1">
                <span>STAGE 1 &bull; 0.0s</span>
                <i class="fa-solid fa-circle-check text-emerald-400"></i>
              </div>
              <div class="font-bold text-xs text-white">1. Ingest Inbound Call</div>
              <div class="text-[10px] text-slate-300 mt-0.5">Transcribes caller utterance &rarr; Appends Customer &amp; Dispute nodes to CG.</div>
            </div>

            <!-- Stage 2 -->
            <div id="step-growth-2" class="growth-step-card p-2.5 rounded-xl border border-indigo-500/80 bg-indigo-950/60 transition-all duration-300">
              <div class="flex items-center justify-between text-[10px] font-mono text-indigo-400 font-bold mb-1">
                <span>STAGE 2 &bull; 0.8s</span>
                <i class="fa-solid fa-circle-check text-emerald-400"></i>
              </div>
              <div class="font-bold text-xs text-white">2. Query SOP Rulebook</div>
              <div class="text-[10px] text-slate-300 mt-0.5">Cross-examines SOP-04 limits &rarr; Evaluates VIP Hardship Clause 4.2 in KG.</div>
            </div>

            <!-- Stage 3 -->
            <div id="step-growth-3" class="growth-step-card p-2.5 rounded-xl border border-indigo-500/80 bg-indigo-950/60 transition-all duration-300">
              <div class="flex items-center justify-between text-[10px] font-mono text-indigo-400 font-bold mb-1">
                <span>STAGE 3 &bull; 1.6s</span>
                <i class="fa-solid fa-circle-check text-emerald-400"></i>
              </div>
              <div class="font-bold text-xs text-white">3. Synthesize &amp; Speak</div>
              <div class="text-[10px] text-slate-300 mt-0.5">Authorizes $150 credit &rarr; Voice agent speaks &amp; appends Decision to CG.</div>
            </div>

            <!-- Stage 4 -->
            <div id="step-growth-4" class="growth-step-card p-2.5 rounded-xl border border-indigo-500/80 bg-indigo-950/60 transition-all duration-300">
              <div class="flex items-center justify-between text-[10px] font-mono text-indigo-400 font-bold mb-1">
                <span>STAGE 4 &bull; 2.4s</span>
                <i class="fa-solid fa-arrows-spin text-pink-400 animate-spin"></i>
              </div>
              <div class="font-bold text-xs text-white">4. Settle ROI &amp; Drift</div>
              <div class="text-[10px] text-slate-300 mt-0.5">Reconciles +$2,250 Net Value &rarr; Emits policy drift feedback loop to KG!</div>
            </div>
          </div>
        </div>
'''

        # Place stepper above the 2-column console in view-call
    target_call_console = '        <!-- MAIN REAL-TIME CALL CONSOLE (2 COLUMNS) -->'
    if 'id="step-growth-1"' not in content:
        content = content.replace(target_call_console, stepper_html + '\n' + target_call_console, 1)

    # 5. Add the complete Unified Triad data, domain filtering, and real-time animation JS
    # Replace the JS logic at the bottom of the file
    js_triad_full_logic = '''
    // =========================================================================
    // UNIFIED TRIAD ENGINE (KG + CG + BG + CROSS-GRAPH EDGES)
    // =========================================================================
    const TRIAD_DATA = {
      billing: {
        domainName: "Billing Dispute & Roaming Concession",
        nodes: [
          // KG Layer (Indigo)
          { id: "kg_sop_bill", label: "SOP-04: Billing & Roaming", group: "kg", color: "#4f46e5", shape: "box", font: { color: "#ffffff", face: "Plus Jakarta Sans", size: 12 } },
          { id: "kg_rule_50", label: "Tier-1 Limit: $50", group: "kg", color: "#6366f1", shape: "ellipse", font: { color: "#ffffff", size: 11 } },
          { id: "kg_rule_250", label: "VIP Clause 4.2: $250", group: "kg", color: "#6366f1", shape: "ellipse", font: { color: "#ffffff", size: 11 } },
          { id: "kg_role_agent", label: "Tier-1 Voice Agent", group: "kg", color: "#818cf8", shape: "dot", size: 14, font: { color: "#ffffff", size: 10 } },

          // CG Layer (Amber)
          { id: "cg_cust_sarah", label: "Customer: Sarah Jenkins (LTV $2.4k)", group: "cg", color: "#f59e0b", shape: "dot", size: 16, font: { color: "#ffffff", size: 11 } },
          { id: "cg_event_bill", label: "Event: Disputed $150 Roaming Fee", group: "cg", color: "#d97706", shape: "box", font: { color: "#ffffff", size: 11 } },
          { id: "cg_dec_waiver", label: "Decision: Waived $150 (Clause 4.2)", group: "cg", color: "#b45309", shape: "box", font: { color: "#ffffff", size: 11 } },

          // BG Layer (Emerald & Purple)
          { id: "bg_goal_ret", label: "Goal: Protect Customer LTV", group: "bg", color: "#10b981", shape: "box", font: { color: "#ffffff", size: 11 } },
          { id: "bg_kpi_fcr", label: "KPI: 100% First Call Resolution", group: "bg", color: "#059669", shape: "ellipse", font: { color: "#ffffff", size: 10 } },
          { id: "bg_roi_val", label: "Net Value: +$2,250", group: "bg", color: "#047857", shape: "box", font: { color: "#ffffff", size: 12, bold: true } },
          { id: "bg_drift_48", label: "Policy Drift: 48 Exceptions", group: "bg", color: "#8b5cf6", shape: "diamond", size: 18, font: { color: "#ffffff", size: 11 } }
        ],
        edges: [
          // Internal KG
          { from: "kg_sop_bill", to: "kg_rule_50", label: "governs", color: { color: "#818cf8" } },
          { from: "kg_sop_bill", to: "kg_rule_250", label: "governs", color: { color: "#818cf8" } },
          { from: "kg_role_agent", to: "kg_rule_50", label: "authorized_for", color: { color: "#818cf8" } },

          // Internal CG
          { from: "cg_cust_sarah", to: "cg_event_bill", label: "incurred", color: { color: "#f59e0b" } },
          { from: "cg_event_bill", to: "cg_dec_waiver", label: "resolved_by", color: { color: "#f59e0b" } },

          // Cross-Graph CG -> KG
          { from: "cg_event_bill", to: "kg_rule_50", label: "evaluates_against ($150 > $50)", dashes: true, color: { color: "#ef4444" }, width: 2 },
          { from: "cg_dec_waiver", to: "kg_rule_250", label: "conforms_to (Clause 4.2)", color: { color: "#6366f1" }, width: 2.5 },

          // Cross-Graph CG -> BG
          { from: "cg_dec_waiver", to: "bg_roi_val", label: "measures_into (+$2,250)", color: { color: "#10b981" }, width: 2.5 },
          { from: "cg_dec_waiver", to: "bg_kpi_fcr", label: "achieves", color: { color: "#10b981" } },

          // Internal BG
          { from: "bg_goal_ret", to: "bg_roi_val", label: "measures", color: { color: "#059669" } },
          { from: "bg_roi_val", to: "bg_drift_48", label: "logs_exception", color: { color: "#8b5cf6" } },

          // Cross-Graph BG -> KG (The Policy Drift Feedback Loop!)
          { from: "bg_drift_48", to: "kg_sop_bill", label: "updates_rule (Feedback Loop)", dashes: [6, 4], width: 3.5, color: { color: "#ec4899" } }
        ]
      },
      outage: {
        domainName: "Broadband Hardware & Field Dispatch",
        nodes: [
          // KG Layer
          { id: "kg_sop_12", label: "SOP-12: Broadband Attenuation", group: "kg", color: "#4f46e5", shape: "box", font: { color: "#ffffff" } },
          { id: "kg_rule_restart", label: "Standard: 180s Reboot Checklist", group: "kg", color: "#6366f1", shape: "ellipse", font: { color: "#ffffff" } },
          { id: "kg_rule_opt", label: "Telemetry Rule: Optical Loss > 28dB", group: "kg", color: "#6366f1", shape: "ellipse", font: { color: "#ffffff" } },
          { id: "kg_role_dispatch", label: "Field Technician Dispatcher", group: "kg", color: "#818cf8", shape: "dot", size: 14, font: { color: "#ffffff" } },

          // CG Layer
          { id: "cg_cust_marcus", label: "Customer: Marcus Vance (Gigabit)", group: "cg", color: "#0284c7", shape: "dot", size: 16, font: { color: "#ffffff" } },
          { id: "cg_event_los", label: "Event: Red Optical LOS Alarm", group: "cg", color: "#0369a1", shape: "box", font: { color: "#ffffff" } },
          { id: "cg_event_loss31", label: "Telemetry: 31.4dB Line Loss", group: "cg", color: "#0284c7", shape: "box", font: { color: "#ffffff" } },
          { id: "cg_dec_truck", label: "Decision: Instant Truck Roll #TX-9041", group: "cg", color: "#075985", shape: "box", font: { color: "#ffffff" } },

          // BG Layer
          { id: "bg_goal_uptime", label: "Goal: SLA 99.9% Uptime", group: "bg", color: "#10b981", shape: "box", font: { color: "#ffffff" } },
          { id: "bg_kpi_aht12", label: "KPI: 12s AHT (Saves 168s)", group: "bg", color: "#059669", shape: "ellipse", font: { color: "#ffffff" } },
          { id: "bg_val_cost", label: "Cost Avoidance: +$450 Saved", group: "bg", color: "#047857", shape: "box", font: { color: "#ffffff" } },
          { id: "bg_drift_auto", label: "Bottleneck Fixed: Auto-Triage", group: "bg", color: "#8b5cf6", shape: "diamond", size: 18, font: { color: "#ffffff" } }
        ],
        edges: [
          { from: "kg_sop_12", to: "kg_rule_restart", label: "governs", color: { color: "#818cf8" } },
          { from: "kg_sop_12", to: "kg_rule_opt", label: "governs", color: { color: "#818cf8" } },
          { from: "kg_role_dispatch", to: "kg_rule_opt", label: "authorized_for", color: { color: "#818cf8" } },

          { from: "cg_cust_marcus", to: "cg_event_los", label: "reported", color: { color: "#0284c7" } },
          { from: "cg_event_los", to: "cg_event_loss31", label: "measured", color: { color: "#0284c7" } },
          { from: "cg_event_loss31", to: "cg_dec_truck", label: "triggers", color: { color: "#0284c7" } },

          // Cross-Graph
          { from: "cg_event_los", to: "kg_rule_restart", label: "bypasses (180s hold)", dashes: true, color: { color: "#ef4444" } },
          { from: "cg_event_loss31", to: "kg_rule_opt", label: "conforms_to (31.4dB > 28dB)", color: { color: "#6366f1" }, width: 2.5 },
          { from: "cg_dec_truck", to: "bg_kpi_aht12", label: "slashes_hold_time", color: { color: "#10b981" }, width: 2.5 },
          { from: "cg_dec_truck", to: "bg_val_cost", label: "measures_into", color: { color: "#10b981" } },

          { from: "bg_goal_uptime", to: "bg_kpi_aht12", label: "monitors", color: { color: "#059669" } },
          { from: "bg_kpi_aht12", to: "bg_drift_auto", label: "proves_efficiency", color: { color: "#8b5cf6" } },
          { from: "bg_drift_auto", to: "kg_sop_12", label: "updates_rule (Standardize Auto-Triage)", dashes: [6, 4], width: 3.5, color: { color: "#ec4899" } }
        ]
      },
      retention: {
        domainName: "Enterprise Churn & Contract Retention",
        nodes: [
          // KG Layer
          { id: "kg_sop_28", label: "SOP-28: Enterprise Retention", group: "kg", color: "#4f46e5", shape: "box", font: { color: "#ffffff" } },
          { id: "kg_rule_5pct", label: "Tier-1 Discretion: 5% Max", group: "kg", color: "#6366f1", shape: "ellipse", font: { color: "#ffffff" } },
          { id: "kg_rule_15pct", label: "Clause 2.4: 15% VIP 2-Yr Lock", group: "kg", color: "#6366f1", shape: "ellipse", font: { color: "#ffffff" } },
          { id: "kg_role_exec", label: "Executive Account Director", group: "kg", color: "#818cf8", shape: "dot", size: 14, font: { color: "#ffffff" } },

          // CG Layer
          { id: "cg_cust_elena", label: "Customer: Apex Logistics (ARR $18k)", group: "cg", color: "#059669", shape: "dot", size: 16, font: { color: "#ffffff" } },
          { id: "cg_event_churn", label: "Event: Cancellation Demand (Price)", group: "cg", color: "#047857", shape: "box", font: { color: "#ffffff" } },
          { id: "cg_dec_lock", label: "Decision: 15% Renewal ($15.3k/yr)", group: "cg", color: "#065f46", shape: "box", font: { color: "#ffffff" } },

          // BG Layer
          { id: "bg_goal_arr", label: "Goal: Enterprise Net Retention", group: "bg", color: "#10b981", shape: "box", font: { color: "#ffffff" } },
          { id: "bg_kpi_tenure", label: "KPI: 2-Year Contract Locked", group: "bg", color: "#059669", shape: "ellipse", font: { color: "#ffffff" } },
          { id: "bg_val_arr", label: "Net Preserved: +$27,900 ARR", group: "bg", color: "#047857", shape: "box", font: { color: "#ffffff" } },
          { id: "bg_drift_pricing", label: "Policy Drift: Tier-1 Quota Audit", group: "bg", color: "#8b5cf6", shape: "diamond", size: 18, font: { color: "#ffffff" } }
        ],
        edges: [
          { from: "kg_sop_28", to: "kg_rule_5pct", label: "governs", color: { color: "#818cf8" } },
          { from: "kg_sop_28", to: "kg_rule_15pct", label: "governs", color: { color: "#818cf8" } },
          { from: "kg_role_exec", to: "kg_rule_15pct", label: "authorized_for", color: { color: "#818cf8" } },

          { from: "cg_cust_elena", to: "cg_event_churn", label: "threatened", color: { color: "#059669" } },
          { from: "cg_event_churn", to: "cg_dec_lock", label: "mitigated_by", color: { color: "#059669" } },

          // Cross-Graph
          { from: "cg_event_churn", to: "kg_rule_5pct", label: "evaluates_against (5% Insufficient)", dashes: true, color: { color: "#ef4444" } },
          { from: "cg_dec_lock", to: "kg_rule_15pct", label: "conforms_to (Clause 2.4)", color: { color: "#6366f1" }, width: 2.5 },
          { from: "cg_dec_lock", to: "bg_val_arr", label: "measures_into (+$27,900)", color: { color: "#10b981" }, width: 2.5 },
          { from: "cg_dec_lock", to: "bg_kpi_tenure", label: "achieves", color: { color: "#10b981" } },

          { from: "bg_goal_arr", to: "bg_val_arr", label: "measures", color: { color: "#059669" } },
          { from: "bg_val_arr", to: "bg_drift_pricing", label: "audits", color: { color: "#8b5cf6" } },
          { from: "bg_drift_pricing", to: "kg_sop_28", label: "updates_rule (Feedback Loop)", dashes: [6, 4], width: 3.5, color: { color: "#ec4899" } }
        ]
      }
    };

    // Macro Enterprise: Merges all 3 domains into one unified graph connected to a central corporate enterprise hub!
    TRIAD_DATA.all = {
      domainName: "Macro Enterprise (All 3 Domains Unified)",
      nodes: [
        { id: "corp_hub", label: "ENTERPRISE CALL CENTER AI CORE", group: "bg", color: "#1e1b4b", shape: "star", size: 24, font: { color: "#ffffff", size: 14, bold: true } },
        ...TRIAD_DATA.billing.nodes,
        ...TRIAD_DATA.outage.nodes,
        ...TRIAD_DATA.retention.nodes
      ],
      edges: [
        { from: "corp_hub", to: "kg_sop_bill", label: "orchestrates", color: { color: "#6366f1" } },
        { from: "corp_hub", to: "kg_sop_12", label: "orchestrates", color: { color: "#6366f1" } },
        { from: "corp_hub", to: "kg_sop_28", label: "orchestrates", color: { color: "#6366f1" } },
        ...TRIAD_DATA.billing.edges,
        ...TRIAD_DATA.outage.edges,
        ...TRIAD_DATA.retention.edges
      ]
    };

    let activeTriadDomain = "billing";

    function renderTriadGraph() {
      const container = document.getElementById('triad-network');
      if (!container) return;

      const data = TRIAD_DATA[activeTriadDomain] || TRIAD_DATA.billing;
      const options = {
        nodes: {
          font: { face: 'Plus Jakarta Sans', size: 11 },
          borderWidth: 2,
          shadow: true
        },
        edges: {
          arrows: { to: { enabled: true, scaleFactor: 0.8 } },
          font: { color: '#94a3b8', size: 9, face: 'JetBrains Mono', strokeWidth: 0 },
          smooth: { type: 'cubicBezier', forceDirection: 'none', roundness: 0.15 }
        },
        physics: {
          stabilization: { iterations: 120 },
          forceAtlas2Based: {
            gravitationalConstant: -70,
            centralGravity: 0.015,
            springLength: 120,
            springStrength: 0.08
          },
          solver: 'forceAtlas2Based'
        }
      };

      if (networks.triad) networks.triad.destroy();
      networks.triad = new vis.Network(container, data, options);

      // Node selection click inspector
      networks.triad.on("selectNode", function(params) {
        if (params.nodes.length > 0) {
          const nodeId = params.nodes[0];
          const node = data.nodes.find(n => n.id === nodeId);
          if (node) {
            const card = document.getElementById('triad-inspector-card');
            const titleEl = document.getElementById('inspect-title');
            const descEl = document.getElementById('inspect-desc');
            const badgeEl = document.getElementById('inspect-tier-badge');
            const connEl = document.getElementById('inspect-conn-count');

            if (card && titleEl && descEl && badgeEl) {
              card.classList.remove('hidden');
              titleEl.textContent = node.label;
              if (node.id.startsWith('kg')) {
                badgeEl.textContent = "Knowledge Graph (SOP)";
                badgeEl.className = "px-2 py-0.5 rounded text-[9px] font-extrabold uppercase bg-indigo-600 text-white";
                descEl.textContent = "Normative policy rulebook defining authoritative thresholds, role requirements, and automated exception conditions.";
              } else if (node.id.startsWith('cg')) {
                badgeEl.textContent = "Context Graph (Call Record)";
                badgeEl.className = "px-2 py-0.5 rounded text-[9px] font-extrabold uppercase bg-amber-600 text-white";
                descEl.textContent = "Episodic runtime event recorded in the live customer conversation, linking audio inputs to operational decisions.";
              } else {
                badgeEl.textContent = "Business Graph (ROI & Drift)";
                badgeEl.className = "px-2 py-0.5 rounded text-[9px] font-extrabold uppercase bg-emerald-600 text-white";
                descEl.textContent = "Reconciliation metric computing the financial dollar value, handle time efficiency, and policy drift feedback loop.";
              }
              const edgeCount = data.edges.filter(e => e.from === nodeId || e.to === nodeId).length;
              if (connEl) connEl.textContent = `Connected to ${edgeCount} cross-graph paths`;
            }
          }
        }
      });
    }

    function filterTriadDomain(domainKey) {
      activeTriadDomain = domainKey;

      ['billing', 'outage', 'retention', 'all'].forEach(k => {
        const btn = document.getElementById(`triad-filter-${k}`);
        if (btn) {
          if (k === domainKey) {
            btn.className = "px-2.5 py-1 rounded-lg text-[11px] font-bold bg-white dark:bg-slate-700 text-indigo-700 dark:text-indigo-300 shadow-2xs transition";
          } else {
            btn.className = "px-2.5 py-1 rounded-lg text-[11px] font-bold text-slate-600 dark:text-slate-300 hover:text-slate-900 transition";
          }
        }
      });

      // Synchronize with the preset selector if not all
      if (domainKey === 'billing') loadScenarioPreset('billing_dispute');
      else if (domainKey === 'outage') loadScenarioPreset('tech_outage');
      else if (domainKey === 'retention') loadScenarioPreset('vip_retention');

      renderTriadGraph();
    }

    // =========================================================================
    // ORDER 3: REAL-TIME GRAPH GROWTH ANIMATION ENGINE
    // =========================================================================
    let growthAnimationTimeout = null;

    function replayGraphGrowthAnimation() {
      if (growthAnimationTimeout) clearTimeout(growthAnimationTimeout);

      const step1 = document.getElementById('step-growth-1');
      const step2 = document.getElementById('step-growth-2');
      const step3 = document.getElementById('step-growth-3');
      const step4 = document.getElementById('step-growth-4');

      const cgBadge = document.getElementById('badge-cg-count');
      const bgBadge = document.getElementById('badge-bg-count');

      // Reset all steps to inactive
      [step1, step2, step3, step4].forEach(s => {
        if (s) {
          s.className = "growth-step-card p-2.5 rounded-xl border border-slate-700/60 bg-slate-900/60 opacity-50 transition-all duration-300";
        }
      });

      if (cgBadge) cgBadge.textContent = "CG: 1 Event (Waiting...)";
      if (bgBadge) bgBadge.textContent = "BG: 0 Metrics";

      // Stage 1 (0ms): Inbound Call & Ingest
      step1.className = "growth-step-card p-2.5 rounded-xl border-2 border-amber-500 bg-amber-950/60 shadow-lg scale-102 transition-all duration-300";
      if (cgBadge) cgBadge.textContent = "CG: +2 Nodes Ingested";

      // Stage 2 (800ms): SOP Rulebook Retrieval
      growthAnimationTimeout = setTimeout(() => {
        step1.className = "growth-step-card p-2.5 rounded-xl border border-indigo-500/80 bg-indigo-950/40 transition-all duration-300";
        step2.className = "growth-step-card p-2.5 rounded-xl border-2 border-indigo-500 bg-indigo-950/70 shadow-lg scale-102 transition-all duration-300";
      }, 800);

      // Stage 3 (1600ms): Decision & Voice Output
      setTimeout(() => {
        step2.className = "growth-step-card p-2.5 rounded-xl border border-indigo-500/80 bg-indigo-950/40 transition-all duration-300";
        step3.className = "growth-step-card p-2.5 rounded-xl border-2 border-emerald-500 bg-emerald-950/70 shadow-lg scale-102 transition-all duration-300";
        if (cgBadge) cgBadge.textContent = "CG: +3 Nodes (Decision Live)";
      }, 1600);

      // Stage 4 (2400ms): ROI Settle & Policy Drift Feedback
      setTimeout(() => {
        step3.className = "growth-step-card p-2.5 rounded-xl border border-indigo-500/80 bg-indigo-950/40 transition-all duration-300";
        step4.className = "growth-step-card p-2.5 rounded-xl border-2 border-purple-500 bg-purple-950/80 shadow-lg scale-102 transition-all duration-300";
        if (bgBadge) bgBadge.textContent = "BG: +2 Nodes & Drift Loop Fired!";
      }, 2400);

      // Return all to clean active state
      setTimeout(() => {
        [step1, step2, step3, step4].forEach(s => {
          if (s) s.className = "growth-step-card p-2.5 rounded-xl border border-indigo-500/80 bg-indigo-950/60 transition-all duration-300";
        });
        if (cgBadge) cgBadge.textContent = "CG: 3 Events (+2 Live)";
        if (bgBadge) bgBadge.textContent = "BG: 3 Metrics (+2 Live)";
      }, 3600);
    }
'''

    # Update switchTab to support 'triad'
    # Find `const tabs = ['hierarchy', 'kg', 'cg', 'bg', 'call'];`
    tabs_pattern = r"const tabs = \['hierarchy', 'kg', 'cg', 'bg', 'call'\];"
    new_tabs = "const tabs = ['hierarchy', 'kg', 'cg', 'bg', 'call', 'triad'];"
    content = re.sub(tabs_pattern, new_tabs, content)

    # In switchTab, render triad when tabId === 'triad'
    render_timeout_pattern = r"(if \(tabId === 'kg'\) renderKG\(\);.*?else if \(tabId === 'call'\) startCallTimer\(\);)"
    new_render_timeout = r"\1\n        else if (tabId === 'triad') renderTriadGraph();"
    content = re.sub(render_timeout_pattern, new_render_timeout, content, flags=re.DOTALL)

    # In simulateSampleCall, trigger replayGraphGrowthAnimation()
    sim_pattern = r"(function simulateSampleCall\(type\) \{.*?speakCurrentResponse\(\);)"
    new_sim = r"\1\n      replayGraphGrowthAnimation();"
    content = re.sub(sim_pattern, new_sim, content, flags=re.DOTALL)

    # Append js_triad_full_logic to the bottom script
    script_end = '</script>\n</body>'
    if js_triad_full_logic not in content:
        content = content.replace(script_end, js_triad_full_logic + '\n' + script_end)

    with open('callcenter_ai_voice_agents.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: Unified Triad View (1), Domain Subgraph Navigation (2), and Real-Time Graph Growth (3) implemented successfully!")

if __name__ == '__main__':
    build_app()
