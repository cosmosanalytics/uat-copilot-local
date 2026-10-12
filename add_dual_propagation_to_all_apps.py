# -*- coding: utf-8 -*-
"""
add_dual_propagation_to_all_apps.py
Adds the 2 types of active propagation to all 6 post-S&OP applications:
  1. Multi-Agent Swarm Small-World Propagation (Peer-to-Peer Watts-Strogatz inter-agent pulse & O(N) Whiteboard)
  2. Vertical 3-Tier Recursive Stack Propagation (Tier 0 AWS Base -> Tier 1 Agent Kernel -> Tier 2 Swarm Consensus)

The 6 Target Apps:
  1. network_optimization_multi_agent_app.html
  2. optimal_menu_pricing_app.html
  3. business_war_room_multi_agent_app.html
  4. multi_agent_brain_app.html
  5. multi_agent_game_app.html
  6. multi_agent_chess_app.html & multi_agent_go_app.html
"""

import os
import re

APPS = [
    {
        "file": "network_optimization_multi_agent_app.html",
        "name": "Hub & Spoke Network Optimization",
        "tab_id": "tab-propagation",
        "btn_id": "tabBtnProp",
        "t0_title": "Tier 0: AWS Primitives (DynamoDB MSEG Routing Mutex, S3 WORM Vault, Bedrock Lane Solver)",
        "t0_items": [
            ("🔒 DynamoDB Mutex", "LOCKED (Exclusive Route)", "Prevents concurrent lane over-allocation"),
            ("🧠 Amazon Bedrock", "Lane Bundles (FTL/LTL)", "Heuristic routing candidate proposals"),
            ("📦 S3 WORM Vault", "SHA-256 MSEG Receipts", "Immutable freight expenditure baseline")
        ],
        "t1_title": "Tier 1: Individual Agent OS Kernel (Prefrontal Ring 0 Cedar & Capacity Memory Pager)",
        "t1_items": [
            ("🛡️ Cedar Guardrail Gate", "PERMIT (Work Center 1000)", "Enforces 400hr blend & 150hr pack limits"),
            ("💾 Context Pager", "RAM 4,200 / 8,192 Tok", "Pages cold BOM bill-of-materials to S3"),
            ("⛓️ Episodic Ledger", "Block #891 Sealed", "Appends verified transport movements")
        ],
        "t2_title": "Tier 2: Multi-Agent Swarm Lattice (Watts-Strogatz Topology & O(N) Whiteboard)",
        "t2_items": [
            ("🌉 Liaison Router", "Max Hops: ≤ 3", "Connects Procurement to Hub Router via EventBridge"),
            ("📋 O(N) Shared Whiteboard", "Cost Breakdown Synced", "Live landed costs updated under CAS leases"),
            ("⚖️ Consensus Arbiter", "S&OP Plan Reconciled", "Cedar gate seals purchase ledger")
        ],
        "agents": [
            ("📦 Procurement", "procure"),
            ("🏭 Production", "produce"),
            ("🌐 Hub Router", "routing"),
            ("⚖️ Batching", "batch"),
            ("🏛️ Arbiter", "arbiter")
        ]
    },
    {
        "file": "optimal_menu_pricing_app.html",
        "name": "Optimal Menu Pricing",
        "tab_id": "tab-propagation",
        "btn_id": "tabBtnProp",
        "t0_title": "Tier 0: AWS Primitives (HiGHS MILP Lambda MicroVM, S3 WORM WTP Ledger, Bedrock)",
        "t0_items": [
            ("🔒 DynamoDB Mutex", "LOCKED (Tier State)", "Guarantees atomic K-tier menu selection"),
            ("🧠 Amazon Bedrock", "WTP Candidate Menus", "Generates reservation price structures"),
            ("📦 S3 WORM Vault", "SHA-256 Deal Audit", "Immutable 10-deal worked example receipts")
        ],
        "t1_title": "Tier 1: Individual Agent OS Kernel (Incentive Compatibility Ring 0 & Volatility Pager)",
        "t1_items": [
            ("🛡️ IC Sentinel Gate", "ENFORCED (Zero Cannibalization)", "Guarantees S_{i,k} ≥ S_{i,j} for all customer tiers"),
            ("💾 Context Pager", "RAM 3,600 / 8,192 Tok", "Pages 500 Monte Carlo draws to S3"),
            ("⛓️ Episodic Ledger", "Block #614 Sealed", "Append-only record of surplus & information rent")
        ],
        "t2_title": "Tier 2: Multi-Agent Swarm Lattice (Pricing Committee & O(N) Whiteboard)",
        "t2_items": [
            ("🌉 Liaison Router", "Max Hops: ≤ 2", "EventBridge links Demand Modeler to MILP Optimizer"),
            ("📋 O(N) Shared Whiteboard", "Surplus Matrix Synced", "All 5 agents read single customer surplus table"),
            ("⚖️ Commercial Arbiter", "Consensus Ratified", "Supermajority seals executive pricing playbook")
        ],
        "agents": [
            ("📊 Demand Modeler", "demand"),
            ("🛡️ IC Sentinel", "ic"),
            ("⚡ MILP Optimizer", "milp"),
            ("🎲 Stress Tester", "stress"),
            ("🏛️ Commercial Arbiter", "exec")
        ]
    },
    {
        "file": "business_war_room_multi_agent_app.html",
        "name": "Enterprise Strategic War Room",
        "tab_id": "tab-propagation",
        "btn_id": "tabBtnProp",
        "t0_title": "Tier 0: AWS Primitives (DynamoDB CapEx Mutex, S3 WORM Resolution Vault, Bedrock DCF)",
        "t0_items": [
            ("🔒 DynamoDB Mutex", "LOCKED (CapEx Budget)", "Guarantees single balance-sheet allocation"),
            ("🧠 Amazon Bedrock", "M&A Strategic Scenarios", "Proposes valuation & expansion schemas"),
            ("📦 S3 WORM Vault", "SHA-256 Board Records", "Immutable SEC & compliance disclosure receipts")
        ],
        "t1_title": "Tier 1: Individual Agent OS Kernel (WACC Hurdle Ring 0 & DCF Cash Flow Pager)",
        "t1_items": [
            ("🛡️ Cedar Hurdle Gate", "PASSED (IRR ≥ WACC)", "Enforces 10.5% minimum cost of capital threshold"),
            ("💾 Context Pager", "RAM 5,100 / 8,192 Tok", "Pages 5-year free cash flow projections to S3"),
            ("⛓️ Episodic Ledger", "Block #902 Sealed", "Append-only audit trail connecting IRR to approval")
        ],
        "t2_title": "Tier 2: Multi-Agent Swarm Lattice (C-Suite Boardroom & O(N) Whiteboard)",
        "t2_items": [
            ("🌉 Liaison Router", "Max Hops: ≤ 3", "Connects CEO, CFO, and CLO across EventBridge bus"),
            ("📋 O(N) Shared Whiteboard", "CapEx Ledger Synced", "Central milestone drawdowns updated under CAS leases"),
            ("⚖️ Board Consensus", "UNANIMOUS MANDATE", "Supermajority seals $45M capital allocation")
        ],
        "agents": [
            ("👔 CEO", "ceo"),
            ("💵 CFO", "cfo"),
            ("📢 CMO", "cmo"),
            ("⚙️ COO", "coo"),
            ("⚖️ CLO", "clo")
        ]
    },
    {
        "file": "multi_agent_brain_app.html",
        "name": "Cognitive Brain Connectome",
        "tab_id": "tab-propagation",
        "btn_id": "tabBtnProp",
        "t0_title": "Tier 0: AWS Primitives (OpenSearch Vector Vault, S3 WORM Episodic Buffer, Bedrock)",
        "t0_items": [
            ("🔒 DynamoDB Mutex", "LOCKED (Synaptic Firing)", "Serializes neurotransmitter state transitions"),
            ("🧠 Amazon Bedrock", "Broca Linguistic Tokens", "High-throughput token generation via Groq/LPU"),
            ("📦 S3 WORM Vault", "SHA-256 Episodic Hash", "Consolidated associative memory traces")
        ],
        "t1_title": "Tier 1: Individual Agent OS Kernel (Prefrontal Goal Decomposer & Amygdala Circuit Breaker)",
        "t1_items": [
            ("🛡️ Amygdala Safety Gate", "92% SHIELD (Zero Breaches)", "Enforces prompt injection & jailbreak circuit breaker"),
            ("💾 Context Pager", "RAM 8,192 Tok Synced", "Hippocampal attention buffer compaction"),
            ("⛓️ Episodic Ledger", "Block #389 Sealed", "Cosine similarity (Δ > 0.91) associative log")
        ],
        "t2_title": "Tier 2: Multi-Agent Swarm Lattice (Biomimetic Neural Connectome & O(N) Whiteboard)",
        "t2_items": [
            ("🌉 Liaison Router", "Max Hops: ≤ 2", "Synaptic action potentials cross thalamic switch"),
            ("📋 O(N) Shared Whiteboard", "Working Memory Loop", "PFC, Hippocampus, and Broca share active tensor"),
            ("⚖️ Connectome Arbiter", "SYNCHRONIZED (100%)", "Whole-brain coherent consensus state achieved")
        ],
        "agents": [
            ("🧠 Frontal Executive", "frontal"),
            ("🗄️ Hippocampus", "hippo"),
            ("⚡ Broca's Area", "broca"),
            ("🛡️ Amygdala", "amygdala"),
            ("👁️ Sensory Cortex", "sensory")
        ]
    },
    {
        "file": "multi_agent_game_app.html",
        "name": "AetherGrid Strategy Game",
        "tab_id": "tab-propagation",
        "btn_id": "tabBtnProp",
        "t0_title": "Tier 0: AWS Primitives (DynamoDB Territory Grid Mutex, S3 Treaty Vault, Bedrock)",
        "t0_items": [
            ("🔒 DynamoDB Mutex", "LOCKED (Turn Turnstile)", "Atomic CAS lock prevents simultaneous move race conditions"),
            ("🧠 Amazon Bedrock", "Faction Strategy Schemas", "Proposes diplomatic treaties & tactical strikes"),
            ("📦 S3 WORM Vault", "SHA-256 Treaty Ledger", "Immutable non-aggression pact & ceasefire receipts")
        ],
        "t1_title": "Tier 1: Individual Agent OS Kernel (Turn Validation Gate & Fog-of-War Memory Pager)",
        "t1_items": [
            ("🛡️ Rule Validation Gate", "VERIFIED (Zero Cheats)", "Enforces energy balance, movement ranges, and ranges"),
            ("💾 Context Pager", "RAM 3,200 / 8,192 Tok", "Pages diplomatic history and defection risks to S3"),
            ("⛓️ Episodic Ledger", "Block #512 Sealed", "Append-only battle log of skirmishes and strikes")
        ],
        "t2_title": "Tier 2: Multi-Agent Swarm Lattice (Faction Diplomacy Swarm & O(N) Whiteboard)",
        "t2_items": [
            ("🌉 Liaison Router", "Max Hops: ≤ 2", "EventBridge bus routes covert espionage and treaties"),
            ("📋 O(N) Shared Whiteboard", "Battlefield State Synced", "All 5 factions read single grid territory ledger"),
            ("⚖️ Hegemony Arbiter", "TREATY RATIFIED", "Bilateral peace pact sealed under CAS lease")
        ],
        "agents": [
            ("⚔️ Warlord", "warlord"),
            ("🕊️ Diplomat", "diplomat"),
            ("⚡ Technologist", "techno"),
            ("💰 Merchant", "merchant"),
            ("🗡️ Shadow", "shadow")
        ]
    },
    {
        "file": "multi_agent_chess_app.html",
        "name": "Grandmaster AI Chess",
        "tab_id": "tab-propagation",
        "btn_id": "tabBtnProp",
        "t0_title": "Tier 0: AWS Primitives (DynamoDB Board FEN Mutex, S3 WORM PGN Vault, Bedrock Engine)",
        "t0_items": [
            ("🔒 DynamoDB Mutex", "LOCKED (Ply Turnstile)", "Atomic CAS lock guarantees sequential White/Black turns"),
            ("🧠 Amazon Bedrock", "Grandmaster Candidates", "Generates tactical variations via Groq/LPU"),
            ("📦 S3 WORM Vault", "SHA-256 PGN Ledger", "Immutable move history & tournament record receipts")
        ],
        "t1_title": "Tier 1: Individual Agent OS Kernel (Chess.js Legal Move Ring 0 & ECO Memory Pager)",
        "t1_items": [
            ("🛡️ Chess Rule Gate", "VERIFIED (Legal SAN)", "Rejects illegal moves, pins, and checks at Ring 0"),
            ("💾 Context Pager", "RAM 2,400 / 8,192 Tok", "Pages opening book tree to S3 to save context"),
            ("⛓️ Episodic Ledger", "Block #108 Sealed", "Centipawn evaluation curve logged into hash chain")
        ],
        "t2_title": "Tier 2: Multi-Agent Swarm Lattice (Grandmaster Council & O(N) Move Whiteboard)",
        "t2_items": [
            ("🌉 Liaison Router", "Max Hops: ≤ 2", "EventBridge links Theorist, Attacker, and Defender"),
            ("📋 O(N) Shared Whiteboard", "Candidate Tree Synced", "All 5 agents inspect single shared board evaluation"),
            ("⚖️ Chief Arbiter", "CONSENSUS VOTE", "Grandmaster supermajority selects optimal move")
        ],
        "agents": [
            ("📖 Theorist", "theorist"),
            ("⚔️ Tactical", "tactical"),
            ("🛡️ Positional", "positional"),
            ("📊 Evaluator", "evaluator"),
            ("🏆 Arbiter", "arbiter")
        ]
    },
    {
        "file": "multi_agent_go_app.html",
        "name": "9-Dan AI Weiqi / Go",
        "tab_id": "tab-propagation",
        "btn_id": "tabBtnProp",
        "t0_title": "Tier 0: AWS Primitives (DynamoDB Goban State Mutex, S3 SGF Vault, Bedrock MCTS)",
        "t0_items": [
            ("🔒 DynamoDB Mutex", "LOCKED (Intersection CAS)", "Atomic lease prevents simultaneous stone placements"),
            ("🧠 Amazon Bedrock", "MCTS Policy Proposer", "Generates whole-board territorial policy priors"),
            ("📦 S3 WORM Vault", "SHA-256 SGF Ledger", "Immutable 9-Dan match move receipts")
        ],
        "t1_title": "Tier 1: Individual Agent OS Kernel (Liberty Tracking Ring 0 & Joseki Memory Pager)",
        "t1_items": [
            ("🛡️ Suicide & Ko Gate", "PERMIT (Liberties ≥ 1)", "Ring 0 flood-fill rejects suicide & repeated Ko positions"),
            ("💾 Context Pager", "RAM 3,900 / 8,192 Tok", "Pages corner joseki dictionary to S3"),
            ("⛓️ Episodic Ledger", "Block #245 Sealed", "Logs stone group captures and territory count")
        ],
        "t2_title": "Tier 2: Multi-Agent Swarm Lattice (9-Dan Sages Council & O(N) Whiteboard)",
        "t2_items": [
            ("🌉 Liaison Router", "Max Hops: ≤ 2", "EventBridge links Alpha MCTS, Combat, and Honte"),
            ("📋 O(N) Shared Whiteboard", "Goban Influence Grid", "All 5 sages debate over single shared board matrix"),
            ("⚖️ Grand Arbiter Meijin", "KOMI BALANCED", "7.5 Komi consensus yields master move recommendation")
        ],
        "agents": [
            ("🌀 Alpha MCTS", "mcts"),
            ("📐 Joseki", "joseki"),
            ("⚔️ Combat", "combat"),
            ("🛡️ Honte", "honte"),
            ("🏆 Meijin", "meijin")
        ]
    }
]

CSS_SNIPPET = """
  /* DUAL PROPAGATION MATRIX STYLES (SWARM & 3-TIER RECURSION) */
  .prop-unified-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin: 10px 0;
  }
  .prop-section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background: var(--panel-subtle);
    border: 1px solid var(--line);
    border-radius: 4px;
    font-family: var(--mono);
    font-size: 11.5px;
    font-weight: 700;
  }
  .swarm-mesh-visualizer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    padding: 14px;
    background: var(--panel);
    border: 1.5px solid var(--line-strong);
    border-radius: 6px;
    position: relative;
    overflow-x: auto;
  }
  .swarm-node-pill {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 8px 12px;
    background: var(--panel-subtle);
    border: 1.5px solid var(--line);
    border-radius: 6px;
    font-family: var(--mono);
    font-size: 11px;
    min-width: 110px;
    transition: all 0.3s ease;
  }
  .swarm-node-pill.active-pulse {
    border-color: var(--cyan);
    background: var(--cyan-bg);
    transform: translateY(-2px);
    box-shadow: 0 0 12px rgba(30, 92, 140, 0.3);
  }
  .swarm-node-pill.pulse-complete {
    border-color: var(--green);
    background: var(--green-bg);
  }
  .swarm-wire-arrow {
    font-size: 14px;
    color: var(--line-strong);
    font-weight: bold;
    transition: all 0.3s ease;
  }
  .swarm-wire-arrow.wire-lit {
    color: var(--cyan);
    text-shadow: 0 0 8px var(--cyan);
  }

  .tier-stack-card {
    background: var(--panel);
    border: 1.5px solid var(--line);
    border-radius: 6px;
    padding: 12px 16px;
    transition: all 0.35s ease;
    position: relative;
    overflow: hidden;
  }
  .tier-stack-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; bottom: 0;
    width: 5px;
    background: var(--line-strong);
  }
  .tier-stack-card.tier-0-card::before { background: var(--green); }
  .tier-stack-card.tier-1-card::before { background: var(--cyan); }
  .tier-stack-card.tier-2-card::before { background: var(--purple); }

  .tier-stack-card.active-propagating {
    transform: translateY(-2px);
    border-color: var(--cyan);
    box-shadow: 0 4px 14px rgba(30, 92, 140, 0.2);
  }
  .tier-stack-card.tier-0-card.active-propagating { background: var(--green-bg); border-color: var(--green); }
  .tier-stack-card.tier-1-card.active-propagating { background: var(--cyan-bg); border-color: var(--cyan); }
  .tier-stack-card.tier-2-card.active-propagating { background: var(--purple-bg); border-color: var(--purple); }
  .tier-stack-card.completed-tier { opacity: 0.95; }

  .tier-head-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }
  .tier-title-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    font-weight: 700;
  }
  .pill-tier {
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    color: #fff;
  }
  .pill-t0 { background: var(--green); }
  .pill-t1 { background: var(--cyan); }
  .pill-t2 { background: var(--purple); }

  .tier-items-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 10px;
  }
  .tier-item-box {
    background: var(--panel-subtle);
    border: 1px solid var(--line);
    border-radius: 4px;
    padding: 8px 10px;
  }
  .tier-item-title {
    display: flex;
    justify-content: space-between;
    font-size: 11.5px;
    font-weight: 700;
    margin-bottom: 2px;
  }
  .tier-item-val {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--cyan);
    font-weight: 600;
  }

  .prop-wire-row {
    text-align: center;
    font-family: var(--mono);
    font-size: 11px;
    color: var(--ink-soft);
    padding: 4px 0;
    position: relative;
  }
  .prop-wire-row.wire-active {
    color: var(--cyan);
    font-weight: 700;
  }
"""

def generate_tab_html(app_info):
    agents_html = ""
    for idx, (ag_name, ag_class) in enumerate(app_info["agents"]):
        wire = f'<span class="swarm-wire-arrow" id="sWire_{idx}">➔</span>' if idx < len(app_info["agents"]) - 1 else ""
        agents_html += f"""
          <div class="swarm-node-pill" id="sNode_{idx}">
            <span style="font-weight:700;">{ag_name}</span>
            <span style="font-size:9.5px; color:var(--ink-soft);" id="sNodeStatus_{idx}">STANDBY</span>
          </div>
          {wire}
        """

    t0_boxes = "".join([f"""
              <div class="tier-item-box" id="pBoxT0_{i}">
                <div class="tier-item-title"><span>{item[0]}</span></div>
                <div class="tier-item-val" id="pValT0_{i}">{item[1]}</div>
                <div style="font-size:10.5px; color:var(--ink-soft);">{item[2]}</div>
              </div>""" for i, item in enumerate(app_info["t0_items"])])

    t1_boxes = "".join([f"""
              <div class="tier-item-box" id="pBoxT1_{i}">
                <div class="tier-item-title"><span>{item[0]}</span></div>
                <div class="tier-item-val" id="pValT1_{i}">{item[1]}</div>
                <div style="font-size:10.5px; color:var(--ink-soft);">{item[2]}</div>
              </div>""" for i, item in enumerate(app_info["t1_items"])])

    t2_boxes = "".join([f"""
              <div class="tier-item-box" id="pBoxT2_{i}">
                <div class="tier-item-title"><span>{item[0]}</span></div>
                <div class="tier-item-val" id="pValT2_{i}">{item[1]}</div>
                <div style="font-size:10.5px; color:var(--ink-soft);">{item[2]}</div>
              </div>""" for i, item in enumerate(app_info["t2_items"])])

    html = f"""
  <!-- DUAL PROPAGATION MATRIX TAB (SWARM & 3-TIER RECURSIVE STACK) -->
  <div class="tabpage" id="{app_info["tab_id"]}">
    <section class="panel">
      <div class="panel-head">
        <div>
          <div class="tag">RELIABILITY &amp; RECURSIVE REASONING ENGINE</div>
          <h2>⚡ Dual Propagation: Watts-Strogatz Swarm &amp; 3-Tier Stack (0 ➔ 1 ➔ 2)</h2>
        </div>
        <button class="btn-theme" onclick="runDualPropagationWave()" style="background:var(--cyan); color:#fff; border-color:var(--cyan);">🚀 Trigger Dual Propagation Wave</button>
      </div>

      <div class="panel-body">
        <div class="prop-unified-container">

          <!-- TYPE 1: MULTI-AGENT SWARM SMALL-WORLD PROPAGATION -->
          <div class="prop-section-header">
            <span>🌐 PROPAGATION TYPE 1: WATTS-STROGATZ SWARM PEER PROPAGATION &bull; O(N) WHITEBOARD</span>
            <span id="swarmPropStatusBadge" style="color:var(--cyan);">IDLE &bull; READY</span>
          </div>

          <div class="swarm-mesh-visualizer">
            {agents_html}
          </div>

          <!-- TYPE 2: 3-TIER VERTICAL PROPAGATION STACK -->
          <div class="prop-section-header" style="margin-top:10px;">
            <span>🏛️ PROPAGATION TYPE 2: 3-TIER RECURSIVE REASONING (TIER 0 ➔ TIER 1 ➔ TIER 2)</span>
            <span id="tierPropStatusBadge" style="color:var(--green);">STACK SYNCHRONIZED</span>
          </div>

          <!-- TIER 0 CARD (AWS BASE PRIMITIVES) -->
          <div class="tier-stack-card tier-0-card" id="cardTier0">
            <div class="tier-head-row">
              <div class="tier-title-badge">
                <span class="pill-tier pill-t0">TIER 0</span>
                <span>{app_info["t0_title"]}</span>
              </div>
              <span class="ag-status" id="badgeTier0">READY</span>
            </div>
            <div class="tier-items-grid">
              {t0_boxes}
            </div>
          </div>

          <!-- PROPAGATION WIRE 0 -> 1 -->
          <div class="prop-wire-row" id="wire0to1">
            ▲ Step 1: AWS physical CAS leases &amp; Bedrock proposals feed into Prefrontal OS Kernel ▲
          </div>

          <!-- TIER 1 CARD (INDIVIDUAL AGENT OS KERNEL) -->
          <div class="tier-stack-card tier-1-card" id="cardTier1">
            <div class="tier-head-row">
              <div class="tier-title-badge">
                <span class="pill-tier pill-t1">TIER 1</span>
                <span>{app_info["t1_title"]}</span>
              </div>
              <span class="ag-status" id="badgeTier1">RING 0 READY</span>
            </div>
            <div class="tier-items-grid">
              {t1_boxes}
            </div>
          </div>

          <!-- PROPAGATION WIRE 1 -> 2 -->
          <div class="prop-wire-row" id="wire1to2">
            ▲ Step 2: Vetted kernel decisions &amp; episodic context propagate up to Multi-Agent Swarm ▲
          </div>

          <!-- TIER 2 CARD (MULTI-AGENT SWARM LATTICE) -->
          <div class="tier-stack-card tier-2-card" id="cardTier2">
            <div class="tier-head-row">
              <div class="tier-title-badge">
                <span class="pill-tier pill-t2">TIER 2</span>
                <span>{app_info["t2_title"]}</span>
              </div>
              <span class="ag-status" id="badgeTier2">LATTICE ONLINE</span>
            </div>
            <div class="tier-items-grid">
              {t2_boxes}
            </div>
          </div>

        </div>
      </div>
    </section>
  </div>
"""
    return html

JS_PROPAGATION_SCRIPT = """
/* =========================================================================
   DUAL PROPAGATION WAVE CONTROLLER (SWARM & 3-TIER RECURSIVE STACK)
   ========================================================================= */
async function runDualPropagationWave() {
  showToast("⚡ Initiating Dual Propagation Wave: Swarm + Tier 0->1->2...");

  // Reset visual states
  ['cardTier0', 'cardTier1', 'cardTier2'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.remove('active-propagating', 'completed-tier');
  });
  document.getElementById('wire0to1')?.classList.remove('wire-active');
  document.getElementById('wire1to2')?.classList.remove('wire-active');

  const nodeCount = 5;
  for (let i = 0; i < nodeCount; i++) {
    const n = document.getElementById(`sNode_${i}`);
    if (n) n.classList.remove('active-pulse', 'pulse-complete');
    const st = document.getElementById(`sNodeStatus_${i}`);
    if (st) st.textContent = "STANDBY";
    const w = document.getElementById(`sWire_${i}`);
    if (w) w.classList.remove('wire-lit');
  }

  // PHASE 1: TIER 0 AWS CLOUD GROUNDING
  const c0 = document.getElementById('cardTier0');
  if (c0) c0.classList.add('active-propagating');
  const b0 = document.getElementById('badgeTier0');
  if (b0) b0.textContent = "CAS LOCK ALLOCATED";
  document.getElementById('tierPropStatusBadge').textContent = "PHASE 1/3: [TIER 0 AWS BASE]";
  showToast("🔒 [Tier 0] Allocating DynamoDB CAS mutex lease & S3 WORM vault...");
  await new Promise(r => setTimeout(r, 600));

  if (c0) { c0.classList.remove('active-propagating'); c0.classList.add('completed-tier'); }
  if (b0) b0.textContent = "TIER 0 VERIFIED ✔";
  document.getElementById('wire0to1')?.classList.add('wire-active');
  await new Promise(r => setTimeout(r, 350));

  // PHASE 2: TIER 1 AGENT OS KERNEL RING 0 GATE
  const c1 = document.getElementById('cardTier1');
  if (c1) c1.classList.add('active-propagating');
  const b1 = document.getElementById('badgeTier1');
  if (b1) b1.textContent = "RING 0 VETTING";
  document.getElementById('tierPropStatusBadge').textContent = "PHASE 2/3: [TIER 1 KERNEL HARNESS]";
  showToast("🛡️ [Tier 1] Prefrontal Kernel validating Cedar schema invariants...");
  await new Promise(r => setTimeout(r, 650));

  if (c1) { c1.classList.remove('active-propagating'); c1.classList.add('completed-tier'); }
  if (b1) b1.textContent = "TIER 1 COMMITTED ✔";
  document.getElementById('wire1to2')?.classList.add('wire-active');
  await new Promise(r => setTimeout(r, 350));

  // PHASE 3: TIER 2 WATTS-STROGATZ SWARM PROPAGATION
  const c2 = document.getElementById('cardTier2');
  if (c2) c2.classList.add('active-propagating');
  const b2 = document.getElementById('badgeTier2');
  if (b2) b2.textContent = "SWARM CONSENSUS";
  document.getElementById('tierPropStatusBadge').textContent = "PHASE 3/3: [TIER 2 SWARM LATTICE]";
  document.getElementById('swarmPropStatusBadge').textContent = "PROPAGATING SWARM PACKETS...";
  showToast("🌐 [Tier 2] Multi-Agent Swarm propagating across small-world liaison bridges...");

  // Propagate sequentially through the 5 swarm nodes
  for (let i = 0; i < nodeCount; i++) {
    const node = document.getElementById(`sNode_${i}`);
    const status = document.getElementById(`sNodeStatus_${i}`);
    const wire = document.getElementById(`sWire_${i}`);

    if (node) node.classList.add('active-pulse');
    if (status) status.textContent = "PROCESSING...";
    await new Promise(r => setTimeout(r, 350));

    if (node) { node.classList.remove('active-pulse'); node.classList.add('pulse-complete'); }
    if (status) status.textContent = "COMMITTED ✔";
    if (wire) wire.classList.add('wire-lit');
  }

  if (c2) { c2.classList.remove('active-propagating'); c2.classList.add('completed-tier'); }
  if (b2) b2.textContent = "SUPERMAJORITY SEALED ✔";
  document.getElementById('swarmPropStatusBadge').textContent = "SWARM FULLY SYNCHRONIZED (100%)";
  document.getElementById('tierPropStatusBadge').textContent = "TIER 0 ➔ 1 ➔ 2 COMMITTED (100%)";
  showToast("✅ Dual Propagation Wave Complete! All 3 tiers & swarm nodes synchronized.");
}
"""

def enhance_app(app_info):
    fname = app_info["file"]
    print(f"Enhancing {fname} with Dual Propagation Matrix...")
    if not os.path.exists(fname):
        print(f"Error: {fname} does not exist!")
        return

    with open(fname, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Inject CSS if not present
    if "/* DUAL PROPAGATION MATRIX STYLES" not in html:
        html = html.replace("</style>", CSS_SNIPPET + "\n</style>")

    # 2. Add Navigation Tab Button
    prop_tab_btn = f'<button onclick="switchTab(\'propagation\')" id="{app_info["btn_id"]}">⚡ Dual Propagation (Swarm &amp; 3-Tier)</button>'
    if app_info["btn_id"] not in html:
        # Insert before closing </div class="tabbar">
        html = re.sub(r'(<div class="tabbar"[^>]*>[\s\S]*?)(</div>)', r'\1  ' + prop_tab_btn + r'\n  \2', html, count=1)

    # 3. Add Tab Content
    tab_html = generate_tab_html(app_info)
    if app_info["tab_id"] not in html:
        # Insert before closing </div><!-- wrap --> or right before <div id="toast">
        if '<div id="toast">' in html:
            html = html.replace('<div id="toast">', tab_html + '\n<div id="toast">')
        else:
            html = html.replace('</body>', tab_html + '\n</body>')

    # 4. Update switchTab function in JS
    if "'propagation': '" + app_info["btn_id"] + "'" not in html:
        html = html.replace(
            "const btnMap = {",
            f"const btnMap = {{\n    'propagation': '{app_info['btn_id']}',"
        )

    # 5. Inject Propagation JS Controller
    if "function runDualPropagationWave" not in html:
        last_script_idx = html.rfind("</script>")
        if last_script_idx != -1:
            html = html[:last_script_idx] + "\n" + JS_PROPAGATION_SCRIPT + "\n" + html[last_script_idx:]

    with open(fname, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Successfully updated {fname}!")

def main():
    for app in APPS:
        enhance_app(app)

if __name__ == "__main__":
    main()
