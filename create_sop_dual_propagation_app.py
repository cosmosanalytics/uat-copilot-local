# -*- coding: utf-8 -*-
"""
create_sop_dual_propagation_app.py
Creates `sop_agent_propagation_swarm_app.html`, a standalone HTML-only copy of the S&OP app
featuring comprehensive visualization of:
1. Agent-to-Agent Transition (as each agent propagates to the next in the 11-stage swarm)
2. Synchronized 3-Tier Recursive Stack Propagation (Tier 0 AWS Primitives -> Tier 1 Kernel -> Tier 2 Swarm Lattice)
3. Step-by-step playback, auto-play, speed control, scenario support, and live audit telemetry.
"""

import os
import re

SOURCE_HTML = "sop_multi_agent_swarm_app.html"
TARGET_HTML = "sop_agent_propagation_swarm_app.html"

def generate():
    with open(SOURCE_HTML, "r", encoding="utf-8") as f:
        src = f.read()

    # 1. Update Title and Header
    src = re.sub(r'<title>.*?</title>', '<title>S&OP Swarm Studio — Agent-to-Agent & 3-Tier Dual Propagation</title>', src)
    src = src.replace(
        "S&OP Swarm Studio</h1>",
        "S&OP Swarm Studio — Dual Propagation</h1>"
    )

    # 2. Add new CSS for the Agent-to-Agent & 3-Tier Propagation Visualizer
    dual_prop_css = """
    /* =========================================================================
       AGENT-TO-AGENT & 3-TIER DUAL PROPAGATION MATRIX STYLES
       ========================================================================= */
    .prop-engine-card {
      background: var(--bg-card);
      border: 1.5px solid var(--border-color);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: var(--shadow-sm);
    }
    .prop-engine-card:hover {
      border-color: var(--border-focus);
    }
    .prop-header-flex {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      margin-bottom: 20px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border-color);
    }
    .prop-header-title {
      font-size: 19px;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .prop-controls-toolbar {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    .prop-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 9px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
      border: 1px solid transparent;
      font-family: var(--font-sans);
    }
    .prop-btn-primary {
      background: var(--swarm-purple);
      color: #ffffff;
      box-shadow: 0 2px 6px rgba(124, 58, 237, 0.25);
    }
    .prop-btn-primary:hover {
      background: #6d28d9;
      transform: translateY(-1px);
    }
    .prop-btn-secondary {
      background: var(--bg-card-subtle);
      color: var(--text-main);
      border-color: var(--border-color);
    }
    .prop-btn-secondary:hover {
      background: var(--border-color);
    }
    .prop-btn-step {
      background: var(--kernel-blue);
      color: #ffffff;
    }
    .prop-btn-step:hover {
      background: #1d4ed8;
    }

    /* 11-Stage Agent Mesh Pipeline Visualizer */
    .agent-pipeline-mesh {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      padding: 18px 12px;
      background: var(--bg-card-subtle);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      overflow-x: auto;
      margin-bottom: 24px;
      position: relative;
    }
    .agent-mesh-node {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
      padding: 10px 8px;
      min-width: 82px;
      background: var(--bg-card);
      border: 1.5px solid var(--border-color);
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s ease;
      position: relative;
      text-align: center;
    }
    .agent-mesh-node:hover {
      border-color: var(--swarm-purple);
      transform: translateY(-2px);
    }
    .agent-mesh-node.source-active {
      border-color: #f59e0b;
      background: rgba(245, 158, 11, 0.08);
      box-shadow: 0 0 12px rgba(245, 158, 11, 0.4);
      transform: scale(1.05);
    }
    .agent-mesh-node.target-active {
      border-color: #10b981;
      background: rgba(16, 185, 129, 0.08);
      box-shadow: 0 0 12px rgba(16, 185, 129, 0.4);
      transform: scale(1.05);
    }
    .agent-mesh-node.passed {
      border-color: var(--swarm-purple);
      background: var(--swarm-purple-bg);
      opacity: 0.9;
    }
    .mesh-node-icon {
      font-size: 18px;
      line-height: 1;
    }
    .mesh-node-num {
      font-size: 10px;
      font-weight: 800;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }
    .mesh-node-name {
      font-size: 10.5px;
      font-weight: 700;
      color: var(--text-main);
      white-space: nowrap;
    }
    .mesh-node-role-badge {
      font-size: 9px;
      font-weight: 700;
      padding: 1px 5px;
      border-radius: 4px;
      text-transform: uppercase;
      font-family: var(--font-mono);
    }
    .badge-source {
      background: #fef3c7;
      color: #92400e;
      border: 1px solid #fde68a;
    }
    .badge-target {
      background: #d1fae5;
      color: #065f46;
      border: 1px solid #a7f3d0;
    }

    /* Handover connector wires */
    .mesh-wire-arrow {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: var(--text-muted);
      font-size: 14px;
      font-weight: 800;
      user-select: none;
      transition: all 0.3s ease;
      min-width: 16px;
    }
    .mesh-wire-arrow.wire-pulsing {
      color: #7c3aed;
      text-shadow: 0 0 8px rgba(124, 58, 237, 0.8);
      animation: wirePulseAnim 0.7s infinite alternate;
    }
    .mesh-wire-arrow.cross-pod {
      color: #f59e0b;
      font-size: 16px;
    }
    @keyframes wirePulseAnim {
      from { transform: scale(1); opacity: 0.6; }
      to { transform: scale(1.3); opacity: 1; }
    }

    /* Active Handover Showcase Box */
    .handover-showcase {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      gap: 16px;
      background: linear-gradient(135deg, rgba(124, 58, 237, 0.04) 0%, rgba(37, 99, 235, 0.04) 100%);
      border: 1.5px solid var(--border-color);
      border-radius: 12px;
      padding: 18px 24px;
      margin-bottom: 24px;
    }
    .handover-agent-card {
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 12px 16px;
      background: var(--bg-card);
      border: 1.5px solid var(--border-color);
      border-radius: 10px;
    }
    .handover-agent-card.source-card {
      border-color: #f59e0b;
      border-left: 5px solid #f59e0b;
    }
    .handover-agent-card.target-card {
      border-color: #10b981;
      border-left: 5px solid #10b981;
    }
    .handover-agent-avatar {
      font-size: 28px;
    }
    .handover-agent-title {
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      font-family: var(--font-mono);
    }
    .handover-agent-name {
      font-size: 15px;
      font-weight: 800;
      color: var(--text-main);
    }
    .handover-agent-detail {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 2px;
    }
    .handover-beam-center {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 4px;
      padding: 0 12px;
      text-align: center;
    }
    .handover-step-badge {
      font-size: 11px;
      font-weight: 800;
      font-family: var(--font-mono);
      padding: 3px 10px;
      border-radius: 9999px;
      background: var(--swarm-purple-bg);
      color: var(--swarm-purple);
      border: 1px solid var(--swarm-purple-border);
    }
    .handover-beam-graphic {
      font-size: 24px;
      color: var(--swarm-purple);
      line-height: 1;
      letter-spacing: -2px;
    }
    .handover-payload-text {
      font-size: 11.5px;
      font-weight: 600;
      color: var(--text-main);
      max-width: 260px;
      background: var(--bg-card);
      padding: 6px 10px;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      font-family: var(--font-mono);
      box-shadow: var(--shadow-sm);
    }

    /* 3-Tier Recursive Stack Grid (Tier 0 -> Tier 1 -> Tier 2) */
    .tier-stack-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
      margin-bottom: 24px;
    }
    @media (max-width: 1024px) {
      .tier-stack-grid {
        grid-template-columns: 1fr;
      }
    }
    .tier-card {
      background: var(--bg-card);
      border: 1.5px solid var(--border-color);
      border-radius: 12px;
      padding: 18px;
      transition: all 0.3s ease;
      position: relative;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .tier-card.tier-0-card {
      border-top: 4px solid var(--cloud-green);
    }
    .tier-card.tier-1-card {
      border-top: 4px solid var(--kernel-blue);
    }
    .tier-card.tier-2-card {
      border-top: 4px solid var(--swarm-purple);
    }
    .tier-card.pulse-active {
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }
    .tier-card.tier-0-card.pulse-active {
      border-color: var(--cloud-green);
      box-shadow: 0 0 16px rgba(5, 150, 105, 0.25);
    }
    .tier-card.tier-1-card.pulse-active {
      border-color: var(--kernel-blue);
      box-shadow: 0 0 16px rgba(37, 99, 235, 0.25);
    }
    .tier-card.tier-2-card.pulse-active {
      border-color: var(--swarm-purple);
      box-shadow: 0 0 16px rgba(124, 58, 237, 0.25);
    }

    .tier-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border-color);
    }
    .tier-title-group {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .tier-badge-pill {
      font-size: 10.5px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
      font-family: var(--font-mono);
      text-transform: uppercase;
    }
    .tier-0-badge {
      background: var(--cloud-green-bg);
      color: var(--cloud-green);
      border: 1px solid var(--cloud-green-border);
    }
    .tier-1-badge {
      background: var(--kernel-blue-bg);
      color: var(--kernel-blue);
      border: 1px solid var(--kernel-blue-border);
    }
    .tier-2-badge {
      background: var(--swarm-purple-bg);
      color: var(--swarm-purple);
      border: 1px solid var(--swarm-purple-border);
    }
    .tier-name-label {
      font-size: 14px;
      font-weight: 800;
      color: var(--text-main);
    }
    .tier-activity-indicator {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 700;
      font-family: var(--font-mono);
    }
    .indicator-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #94a3b8;
    }
    .indicator-dot.active-pulse {
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
      animation: dotPulse 1s infinite;
    }
    @keyframes dotPulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(1.3); }
    }

    /* Tier Primitive Rows */
    .tier-primitive-row {
      display: flex;
      flex-direction: column;
      gap: 3px;
      padding: 10px 12px;
      background: var(--bg-card-subtle);
      border: 1px solid var(--border-color);
      border-radius: 8px;
    }
    .primitive-label-flex {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .primitive-name {
      font-size: 11.5px;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .primitive-status-tag {
      font-size: 10px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: var(--font-mono);
    }
    .primitive-desc-text {
      font-size: 11px;
      color: var(--text-muted);
      line-height: 1.4;
      font-family: var(--font-mono);
    }

    /* Live Transition History Table */
    .trans-history-card {
      background: var(--bg-card);
      border: 1.5px solid var(--border-color);
      border-radius: 12px;
      padding: 20px;
      margin-top: 20px;
    }
    .trans-history-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      margin-top: 12px;
    }
    .trans-history-table th {
      text-align: left;
      padding: 10px 12px;
      background: var(--bg-card-subtle);
      color: var(--text-muted);
      font-weight: 700;
      font-size: 11px;
      text-transform: uppercase;
      font-family: var(--font-mono);
      border-bottom: 1px solid var(--border-color);
    }
    .trans-history-table td {
      padding: 10px 12px;
      border-bottom: 1px solid var(--border-color);
      color: var(--text-main);
      vertical-align: middle;
    }
    .trans-history-table tr:hover td {
      background: var(--bg-card-subtle);
    }
    .table-step-pill {
      font-size: 10px;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 9999px;
      background: var(--swarm-purple-bg);
      color: var(--swarm-purple);
      border: 1px solid var(--swarm-purple-border);
      font-family: var(--font-mono);
    }
    """

    # Inject CSS before </style>
    style_end = src.find("</style>")
    src = src[:style_end] + "\n" + dual_prop_css + "\n" + src[style_end:]

    # 3. Add the Dual Propagation tab button to .tab-bar
    tab_replacement = """<button class="tab-item active" onclick="switchTab('agentprop')" id="tabBtnAgentProp">⚡ Agent Step &amp; 3-Tier Propagation</button>
        <button class="tab-item" onclick="switchTab('pipeline')" id="tabBtnPipeline">🌐 11-Stage Swarm Pipeline</button>"""
    src = re.sub(
        r'<button class="tab-item active"\s+onclick="switchTab\(\'pipeline\'\)"\s+id="tabBtnPipeline">.*?</button>',
        tab_replacement,
        src
    )

    # 4. Create the Tab Content HTML for tabAgentProp
    tab_agent_prop_html = """
    <!-- TAB: AGENT-TO-AGENT & 3-TIER DUAL PROPAGATION MATRIX -->
    <div class="tab-content active" id="tabAgentProp">
      <div class="prop-engine-card">
        <div class="prop-header-flex">
          <div class="prop-header-title">
            <span>⚡ S&OP Multi-Agent Transition &amp; 3-Tier Dual Propagation</span>
            <span class="status-badge badge-ok" id="propStatusBadge">SYNCHRONIZED • READY</span>
          </div>
          <div class="prop-controls-toolbar">
            <button class="prop-btn prop-btn-primary" id="btnAutoPropWave" onclick="toggleAutoPropagationWave()">
              <span id="btnAutoPropIcon">▶</span> <span id="btnAutoPropText">Auto-Play All 10 Handovers</span>
            </button>
            <button class="prop-btn prop-btn-step" id="btnStepNextProp" onclick="stepNextPropagation()">
              <span>⏭ Next Agent Handover</span>
            </button>
            <button class="prop-btn prop-btn-secondary" id="btnStepPrevProp" onclick="stepPrevPropagation()">
              <span>⏮ Prev</span>
            </button>
            <button class="prop-btn prop-btn-secondary" onclick="resetPropagationMatrix()">
              <span>↺ Reset</span>
            </button>
            <div style="display:flex; align-items:center; gap:6px; font-size:12px; font-family:var(--font-mono); color:var(--text-muted); margin-left:8px;">
              <span>Speed:</span>
              <select id="propSpeedSelect" onchange="setPropSpeed(this.value)" style="padding:4px 8px; border-radius:6px; border:1px solid var(--border-color); background:var(--bg-card); color:var(--text-main); font-family:var(--font-mono); font-size:11px;">
                <option value="2200">0.5x Slow (2.2s)</option>
                <option value="1200" selected>1.0x Normal (1.2s)</option>
                <option value="600">2.0x Fast (0.6s)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 11-Stage Interactive Pipeline Mesh -->
        <div style="margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:11px; font-weight:700; color:var(--text-muted); text-transform:uppercase; font-family:var(--font-mono);">
            Horizontal Agent-to-Agent Transition Mesh (11 Nodes in 3 Pods)
          </span>
          <span style="font-size:11px; color:var(--text-muted); font-family:var(--font-mono);">
            Click any node or wire to inspect handover
          </span>
        </div>
        <div class="agent-pipeline-mesh" id="agentPipelineMeshContainer">
          <!-- Populated by JS -->
        </div>

        <!-- Active Handover Showcase Box -->
        <div class="handover-showcase" id="activeHandoverShowcase">
          <!-- Source Agent -->
          <div class="handover-agent-card source-card" id="sourceAgentCard">
            <div class="handover-agent-avatar" id="sourceAgentAvatar">📊</div>
            <div>
              <div class="handover-agent-title">Source Handover Agent</div>
              <div class="handover-agent-name" id="sourceAgentName">Stage 1: Aggregate Demand</div>
              <div class="handover-agent-detail" id="sourceAgentPod">Demand Pod • Propose Stage</div>
            </div>
          </div>

          <!-- Handover Beam & S&OP Payload -->
          <div class="handover-beam-center">
            <div class="handover-step-badge" id="handoverStepBadge">HANDOVER 1 OF 10</div>
            <div class="handover-beam-graphic" id="handoverBeamGraphic">➔➔➔</div>
            <div class="handover-payload-text" id="handoverPayloadText">
              Baseline Sales Demand: 12,500 units ($25.0M)
            </div>
          </div>

          <!-- Target Agent -->
          <div class="handover-agent-card target-card" id="targetAgentCard">
            <div class="handover-agent-avatar" id="targetAgentAvatar">📈</div>
            <div>
              <div class="handover-agent-title">Receiving Target Agent</div>
              <div class="handover-agent-name" id="targetAgentName">Stage 2: Baseline Forecast</div>
              <div class="handover-agent-detail" id="targetAgentPod">Demand Pod • ML ARIMA/Prophet</div>
            </div>
          </div>
        </div>

        <!-- 3-Tier Recursive Stack Grid (Tier 0 -> Tier 1 -> Tier 2) -->
        <div style="margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:11px; font-weight:700; color:var(--text-muted); text-transform:uppercase; font-family:var(--font-mono);">
            Vertical 3-Tier Stack Propagation for Current Handover
          </span>
          <span style="font-size:11px; font-weight:700; color:var(--swarm-purple); font-family:var(--font-mono);" id="tierWaveStatusText">
            TIER 0 CAS LOCK ➔ TIER 1 CEDAR GATE ➔ TIER 2 SWARM WHITEBOARD
          </span>
        </div>

        <div class="tier-stack-grid">
          <!-- TIER 0: AWS CLOUD PRIMITIVES -->
          <div class="tier-card tier-0-card" id="tier0Card">
            <div class="tier-card-header">
              <div class="tier-title-group">
                <span class="tier-badge-pill tier-0-badge">Tier 0</span>
                <span class="tier-name-label">Enterprise AWS Cloud Layer</span>
              </div>
              <div class="tier-activity-indicator">
                <span class="indicator-dot" id="tier0Dot"></span>
                <span id="tier0StateText">IDLE</span>
              </div>
            </div>

            <!-- AWS Bedrock -->
            <div class="tier-primitive-row">
              <div class="primitive-label-flex">
                <span class="primitive-name">🧠 AWS Bedrock / Nitro Enclave</span>
                <span class="primitive-status-tag" id="tier0BedrockTag" style="background:#ecfdf5; color:#065f46;">TOKEN VERIFIED</span>
              </div>
              <div class="primitive-desc-text" id="tier0BedrockDesc">
                Claude 3.5 Sonnet / Llama-3-70B signed inference token &amp; cryptographic attestation
              </div>
            </div>

            <!-- Amazon DynamoDB CAS Mutex -->
            <div class="tier-primitive-row">
              <div class="primitive-label-flex">
                <span class="primitive-name">🔒 Amazon DynamoDB CAS Mutex</span>
                <span class="primitive-status-tag" id="tier0MutexTag" style="background:#fef3c7; color:#92400e;">MUTEX LOCKED</span>
              </div>
              <div class="primitive-desc-text" id="tier0MutexDesc">
                Conditional PutItem row lock: Lease #lk-ddb-0102 on /sop/handover/stage-1 (15s lease expiry)
              </div>
            </div>

            <!-- Amazon S3 Object Lock (WORM) -->
            <div class="tier-primitive-row">
              <div class="primitive-label-flex">
                <span class="primitive-name">📦 Amazon S3 WORM Vault</span>
                <span class="primitive-status-tag" id="tier0WormTag" style="background:#ecfdf5; color:#065f46;">WORM IMMUTABLE</span>
              </div>
              <div class="primitive-desc-text" id="tier0WormDesc">
                SHA-256 Digest: s3://sop-vault-ledger/stage-1-handover.json (Retention: Compliance Mode)
              </div>
            </div>

            <!-- AWS CloudTrail & KMS -->
            <div class="tier-primitive-row">
              <div class="primitive-label-flex">
                <span class="primitive-name">🛡️ AWS CloudTrail &amp; KMS Key</span>
                <span class="primitive-status-tag" id="tier0KmsTag" style="background:#ecfdf5; color:#065f46;">HMAC SIGNED</span>
              </div>
              <div class="primitive-desc-text" id="tier0KmsDesc">
                arn:aws:kms:us-east-1:7829... / Event PutHandoverRecord verified in CloudTrail stream
              </div>
            </div>
          </div>

          <!-- TIER 1: INDIVIDUAL AGENT OS KERNEL -->
          <div class="tier-card tier-1-card" id="tier1Card">
            <div class="tier-card-header">
              <div class="tier-title-group">
                <span class="tier-badge-pill tier-1-badge">Tier 1</span>
                <span class="tier-name-label">Individual Agent OS Kernel</span>
              </div>
              <div class="tier-activity-indicator">
                <span class="indicator-dot" id="tier1Dot"></span>
                <span id="tier1StateText">IDLE</span>
              </div>
            </div>

            <!-- Ring 0 Cedar Deterministic Gate -->
            <div class="tier-primitive-row">
              <div class="primitive-label-flex">
                <span class="primitive-name">🛡️ Ring 0 Cedar Policy Gate</span>
                <span class="primitive-status-tag" id="tier1CedarTag" style="background:#eff6ff; color:#1e40af;">PERMIT (0.7ms)</span>
              </div>
              <div class="primitive-desc-text" id="tier1CedarDesc">
                permit(principal == Agent::Aggregate, action == Action::Handover, resource == Stage::Forecast)
              </div>
            </div>

            <!-- Ring 2 Context Pager -->
            <div class="tier-primitive-row">
              <div class="primitive-label-flex">
                <span class="primitive-name">📑 Ring 2 Context Pager (KV Memory)</span>
                <span class="primitive-status-tag" id="tier1PagerTag" style="background:#eff6ff; color:#1e40af;">CONTEXT PAGED</span>
              </div>
              <div class="primitive-desc-text" id="tier1PagerDesc">
                Evict raw 24-mo sales logs to S3 cold store; page statistical summary vectors into target working memory
              </div>
            </div>

            <!-- Ring 3 Epistemic Hash Chain -->
            <div class="tier-primitive-row">
              <div class="primitive-label-flex">
                <span class="primitive-name">📜 Ring 3 Epistemic Ledger</span>
                <span class="primitive-status-tag" id="tier1HashTag" style="background:#eff6ff; color:#1e40af;">CHAIN BLOCK #1</span>
              </div>
              <div class="primitive-desc-text" id="tier1HashDesc">
                Block #1 signed: Hash(prev + state_diff) = 8e17b3c2... (Tamper-evident per-agent chain)
              </div>
            </div>

            <!-- Ring 1 Supervisor Watchdog -->
            <div class="tier-primitive-row">
              <div class="primitive-label-flex">
                <span class="primitive-name">⏱️ Ring 1 Sandbox Watchdog</span>
                <span class="primitive-status-tag" id="tier1SandboxTag" style="background:#eff6ff; color:#1e40af;">15s LEASE OK</span>
              </div>
              <div class="primitive-desc-text" id="tier1SandboxDesc">
                Process isolated in Nitro cgroup; wall-clock budget 15.0s armed; zero socket leak detected
              </div>
            </div>
          </div>

          <!-- TIER 2: SWARM COORDINATION LATTICE -->
          <div class="tier-card tier-2-card" id="tier2Card">
            <div class="tier-card-header">
              <div class="tier-title-group">
                <span class="tier-badge-pill tier-2-badge">Tier 2</span>
                <span class="tier-name-label">Swarm Coordination Lattice</span>
              </div>
              <div class="tier-activity-indicator">
                <span class="indicator-dot" id="tier2Dot"></span>
                <span id="tier2StateText">IDLE</span>
              </div>
            </div>

            <!-- Swarm Liaison Bridge & Hop Limiter -->
            <div class="tier-primitive-row">
              <div class="primitive-label-flex">
                <span class="primitive-name">🌉 Liaison Bridge &amp; Hop Limiter</span>
                <span class="primitive-status-tag" id="tier2LiaisonTag" style="background:#f5f3ff; color:#5b21b6;">INTRA-POD LINK</span>
              </div>
              <div class="primitive-desc-text" id="tier2LiaisonDesc">
                Intra-Demand Pod direct mesh link (Hop count: 1 / 3, latency: 4ms). Watts-Strogatz small-world route.
              </div>
            </div>

            <!-- O(N) Distributed Whiteboard -->
            <div class="tier-primitive-row">
              <div class="primitive-label-flex">
                <span class="primitive-name">📋 O(N) Shared Whiteboard</span>
                <span class="primitive-status-tag" id="tier2WhiteboardTag" style="background:#f5f3ff; color:#5b21b6;">LANE WRITTEN</span>
              </div>
              <div class="primitive-desc-text" id="tier2WhiteboardDesc">
                Lane Demand: written 'Stage 1 Aggregated baseline 12.5k units' (VectorClock: [1,0,0])
              </div>
            </div>

            <!-- Byzantine Quorum Consensus Gate -->
            <div class="tier-primitive-row">
              <div class="primitive-label-flex">
                <span class="primitive-name">⚖️ Byzantine Quorum Consensus</span>
                <span class="primitive-status-tag" id="tier2QuorumTag" style="background:#f5f3ff; color:#5b21b6;">5/5 UNANIMOUS</span>
              </div>
              <div class="primitive-desc-text" id="tier2QuorumDesc">
                (2f + 1) Quorum satisfied. 5 peer verifier nodes confirmed baseline distribution validity.
              </div>
            </div>

            <!-- Circuit Breaker #20 Sentinel -->
            <div class="tier-primitive-row">
              <div class="primitive-label-flex">
                <span class="primitive-name">🚨 Circuit Breaker Sentinel</span>
                <span class="primitive-status-tag" id="tier2BreakerTag" style="background:#ecfdf5; color:#065f46;">ARMED • NORMAL</span>
              </div>
              <div class="primitive-desc-text" id="tier2BreakerDesc">
                Dual-key authorization intact; duplicate PO &amp; budget leak traps monitoring state
              </div>
            </div>
          </div>
        </div>

        <!-- Live Step-by-Step Transition Audit Ledger -->
        <div class="trans-history-card">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div style="font-size:14px; font-weight:800; color:var(--text-main); display:flex; align-items:center; gap:8px;">
              <span>📜 Real-Time Dual Propagation Handover Ledger</span>
              <span class="table-step-pill" id="historyCounterPill">0 Handovers Executed</span>
            </div>
            <button class="prop-btn prop-btn-secondary" style="padding:4px 10px; font-size:11px;" onclick="clearPropagationHistory()">
              <span>Clear Ledger</span>
            </button>
          </div>
          <div style="overflow-x:auto;">
            <table class="trans-history-table">
              <thead>
                <tr>
                  <th style="width:60px;">Step</th>
                  <th style="width:220px;">Agent Handover (From ➔ To)</th>
                  <th>Payload in Transit</th>
                  <th style="width:160px;">Tier 0 AWS CAS Mutex</th>
                  <th style="width:160px;">Tier 1 Cedar Decision</th>
                  <th style="width:160px;">Tier 2 Whiteboard Status</th>
                  <th style="width:110px;">Hash Digest</th>
                </tr>
              </thead>
              <tbody id="transHistoryBody">
                <tr>
                  <td colspan="7" style="text-align:center; color:var(--text-muted); padding:16px;">
                    No handover transitions executed yet. Click <strong>"Auto-Play All 10 Handovers"</strong> or <strong>"Next Agent Handover"</strong> above.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    """

    # Un-activate tabPipeline and insert tabAgentProp right above tabPipeline
    src = src.replace(
        '<div class="tab-content active" id="tabPipeline">',
        tab_agent_prop_html + '\n    <div class="tab-content" id="tabPipeline">'
    )

    # 5. Update switchTab function in JS
    switch_tab_orig = """      const map = {
        pipeline: { btn: 'tabBtnPipeline', pane: 'tabPipeline' },
        whiteboard: { btn: 'tabBtnWhiteboard', pane: 'tabWhiteboard' },
        quorum: { btn: 'tabBtnQuorum', pane: 'tabQuorum' },
        traceability: { btn: 'tabBtnTraceability', pane: 'tabTraceability' },
        audit: { btn: 'tabBtnAudit', pane: 'tabAudit' }
      };"""

    switch_tab_new = """      const map = {
        agentprop: { btn: 'tabBtnAgentProp', pane: 'tabAgentProp' },
        pipeline: { btn: 'tabBtnPipeline', pane: 'tabPipeline' },
        whiteboard: { btn: 'tabBtnWhiteboard', pane: 'tabWhiteboard' },
        quorum: { btn: 'tabBtnQuorum', pane: 'tabQuorum' },
        traceability: { btn: 'tabBtnTraceability', pane: 'tabTraceability' },
        audit: { btn: 'tabBtnAudit', pane: 'tabAudit' }
      };"""

    src = src.replace(switch_tab_orig, switch_tab_new)

    # 6. Inject the JavaScript Engine for Agent-to-Agent & 3-Tier Dual Propagation
    dual_prop_js = """
    /* =========================================================================
       DUAL PROPAGATION ENGINE: AGENT-TO-AGENT & 3-TIER RECURSIVE SYNCHRONIZATION
       ========================================================================= */
    const AGENTS_METADATA = [
      { id: 1, name: "Aggregate Demand", short: "Aggregator", icon: "📊", pod: "Demand", color: "#7c3aed", role: "History Rollup" },
      { id: 2, name: "Baseline Forecast", short: "Forecaster", icon: "📈", pod: "Demand", color: "#7c3aed", role: "ARIMA/Prophet" },
      { id: 3, name: "Commercial Consensus", short: "Consensus", icon: "🤝", pod: "Demand", color: "#7c3aed", role: "Uplift Review" },
      { id: 4, name: "DC Disaggregate", short: "Disaggregator", icon: "🗺️", pod: "Demand", color: "#7c3aed", role: "Regional DC Split" },
      { id: 5, name: "Order Net Consumption", short: "Consumer", icon: "🛒", pod: "Demand", color: "#7c3aed", role: "Order Netting" },
      { id: 6, name: "Dependent BOM Explode", short: "BOM Exploder", icon: "⚙️", pod: "Supply", color: "#2563eb", role: "84 Assemblies" },
      { id: 7, name: "Production PO Firming", short: "PO Firmer", icon: "📑", pod: "Supply", color: "#2563eb", role: "EMS Firm POs" },
      { id: 8, name: "SMT Capacity Pool", short: "Capacity Pooler", icon: "🏭", pod: "Supply", color: "#2563eb", role: "94% Line Load" },
      { id: 9, name: "Dynamic Safety Buffer", short: "Buffer Sentinel", icon: "🛡️", pod: "Supply", color: "#2563eb", role: "Safety Stock" },
      { id: 10, name: "Variance & Exception Monitor", short: "Variance Monitor", icon: "📡", pod: "Control", color: "#059669", role: "Variance Audit" },
      { id: 11, name: "Executive S&OP Sign-off", short: "S&OP Owner", icon: "👑", pod: "Control", color: "#059669", role: "WORM Commit" }
    ];

    const HANDOVER_STEPS = [
      {
        step: 1,
        fromId: 1,
        toId: 2,
        isCrossPod: false,
        payload: "24-Mo Sales History baseline rolled up: 12,500 units ($25.0M). Handover to ARIMA/Prophet fit.",
        tier0: {
          bedrock: "AWS Bedrock - Batch Inference Token Generation & Model Attestation",
          mutex: "DynamoDB PutItem lease: #lk-ddb-0102 on /sop/handover/stage-1 (15s lease expiry)",
          worm: "s3://sop-vault/audit/step-01-aggregate.json (SHA-256: 4a9f7e2c...)",
          kms: "arn:aws:kms:us-east-1:7829... / Event PutHandoverRecord verified in CloudTrail"
        },
        tier1: {
          cedar: "permit(principal == Agent::Aggregate, action == Action::Handover, resource == Stage::Forecast) -> PERMIT (0.7ms)",
          pager: "Evict raw 24-mo transaction logs to S3 cold store; page statistical summaries into 8k context",
          hash: "Block #1 signed: Hash(prev + state_diff) = 8e17b3c2... (Per-agent epistemic chain)",
          sandbox: "Nitro cgroup memory budget: 412MB / 2048MB. Wall-clock: 0.12s / 15.0s"
        },
        tier2: {
          liaison: "Intra-Demand Pod direct mesh link (Hop 1/3, latency 4ms). Watts-Strogatz shortcut route.",
          whiteboard: "Lane Demand: written 'Stage 1 Aggregated baseline 12.5k units' (VectorClock: [1,0,0])",
          quorum: "(2f + 1) Quorum satisfied. 5/5 Byzantine nodes verified statistical baseline distribution.",
          breaker: "Breaker #20 armed: Zero anomaly detected in baseline sales distribution"
        }
      },
      {
        step: 2,
        fromId: 2,
        toId: 3,
        isCrossPod: false,
        payload: "ML blended forecast output: 12,500 units ($25.0M). Handover for commercial promotion uplift review.",
        tier0: {
          bedrock: "AWS Bedrock Claude 3.5 Sonnet / Llama-3-70B model evaluation & confidence scoring",
          mutex: "DynamoDB PutItem lease: #lk-ddb-0203 (Conditional: expected_version=1)",
          worm: "s3://sop-vault/audit/step-02-forecast.json (SHA-256: d82a1109...)",
          kms: "KMS encrypted handover envelope; CloudTrail event #tr-9921 recorded"
        },
        tier1: {
          cedar: "permit(principal == Agent::Forecast, action == Action::ProposeUplift, resource == Committee::Commercial) -> PERMIT (0.8ms)",
          pager: "Page model confidence intervals into working memory; evict hyperparameter tuning buffers",
          hash: "Block #2 signed: Hash(prev + delta) = 12fa098b...",
          sandbox: "Process sandboxed in isolated container; CPU load 18%; memory nominal"
        },
        tier2: {
          liaison: "Intra-Demand Pod peer pulse (Hop 1/3, latency 3ms)",
          whiteboard: "Lane Demand: written 'ML Forecast 12.5k units submitted' (VectorClock: [2,0,0])",
          quorum: "4/5 Quorum consensus verified forecast bounds within 95% confidence interval",
          breaker: "Breaker #20 normal: Forecast growth rate +3.2% within historical variance band"
        }
      },
      {
        step: 3,
        fromId: 3,
        toId: 4,
        isCrossPod: false,
        payload: "+$5.0M promotional uplift approved ($30.0M total / 15,000 units). Handover for regional DC split.",
        tier0: {
          bedrock: "AWS Bedrock Nitro Enclave verified mathematical consistency & arithmetic verification",
          mutex: "DynamoDB PutItem lease: #lk-ddb-0304 (Conditional check: uplift <= $10.0M cap)",
          worm: "s3://sop-vault/audit/step-03-consensus.json (SHA-256: 7f3c44bb...)",
          kms: "Event ConsensusSigned: CFO & CMO digital signatures authenticated via KMS"
        },
        tier1: {
          cedar: "permit(principal == Agent::Consensus, action == Action::AuthorizeUplift, resource == Budget::Marketing) -> PERMIT (0.6ms)",
          pager: "Page commercial meeting notes into persistent summary; flush meeting transcripts",
          hash: "Block #3 signed: Hash(prev + delta) = c891a277...",
          sandbox: "Container memory: 520MB / 2048MB. Sandboxed execution validated"
        },
        tier2: {
          liaison: "Intra-Demand Pod direct pulse (Hop 1/3, latency 4ms)",
          whiteboard: "Lane Demand: written 'Consensus approved +$5.0M uplift' (VectorClock: [3,0,0])",
          quorum: "5/5 Byzantine consensus reached across Financial, Commercial & Supply stakeholders",
          breaker: "Dual-key authorization check passed: VP Sales + VP Supply signed off"
        }
      },
      {
        step: 4,
        fromId: 4,
        toId: 5,
        isCrossPod: false,
        payload: "15,000 units apportioned across 6 regional Distribution Centers. Handover for customer order netting.",
        tier0: {
          bedrock: "AWS Lambda Step Functions distributed map execution across 6 DC partitions",
          mutex: "DynamoDB PutItem lease: #lk-ddb-0405 (Regional DC partition mutex)",
          worm: "s3://sop-vault/audit/step-04-disaggregate.json (SHA-256: 39de5811...)",
          kms: "Event DCQuotaAllocation: KMS envelope encryption verified"
        },
        tier1: {
          cedar: "permit(principal == Agent::Disaggregate, action == Action::AllocateQuota, resource == DC::All) -> PERMIT (0.9ms)",
          pager: "Load regional distribution matrix; page out past allocation tables",
          hash: "Block #4 signed: Hash(prev + delta) = 99cb3402...",
          sandbox: "Regional partition sandbox completed in 0.28s"
        },
        tier2: {
          liaison: "Intra-Demand Pod direct pulse (Hop 1/3, latency 3ms)",
          whiteboard: "Lane Demand: written 'Regional DC quotas disaggregated' (VectorClock: [4,0,0])",
          quorum: "5/5 Quorum certified sum of DC allocations equals total consensus plan (15,000 units)",
          breaker: "Zero quota leakage detected; total allocation conserved"
        }
      },
      {
        step: 5,
        fromId: 5,
        toId: 6,
        isCrossPod: true,
        payload: "Net unconsumed demand committed: 14,200 units ($28.4M). Crossing Demand-to-Supply Liaison Bridge #1.",
        tier0: {
          bedrock: "AWS Bedrock Cross-VPC PrivateLink tunnel attestation & secure payload envelope",
          mutex: "DynamoDB Cross-Pod Master Lock: #lk-ddb-pod-demand-supply (Lease ID: #xpod-883a, TTL 30s)",
          worm: "s3://sop-vault/audit/step-05-liaison-bridge-demand-to-supply.json (SHA-256: ee81ff44...)",
          kms: "Event CrossPodBridgeCrossing: IAM role cross-boundary attestation certified"
        },
        tier1: {
          cedar: "permit(principal == Pod::Demand, action == Action::CrossPodHandoff, resource == Pod::Supply) -> PERMIT (1.1ms)",
          pager: "Demand Pod episodic memory serialized and committed; Supply Pod working memory initialized",
          hash: "Block #5 signed: Cross-pod link Hash = 4b77ac90...",
          sandbox: "Cross-pod boundary check passed: Zero privileged token leakage"
        },
        tier2: {
          liaison: "⚡ CROSS-POD LIAISON SHORTCUT BRIDGE #1 ENGAGED (Watts-Strogatz shortcut link, Hop count: 1/3, 12ms)",
          whiteboard: "Lane Demand -> Supply: handover payload posted; Supply lane unlocked (VectorClock: [5,1,0])",
          quorum: "Consensus Quorum: 5/5 nodes certified demand net baseline before supply activation",
          breaker: "Boundary sentinel passed: Demand net orders matched booked ERP backlog"
        }
      },
      {
        step: 6,
        fromId: 6,
        toId: 7,
        isCrossPod: false,
        payload: "14,200 finished goods exploded into 84 sub-assemblies & 4 critical ASICs. Handover for EMS PO firming.",
        tier0: {
          bedrock: "AWS Nitro Enclave BOM Explosion verification engine & supplier lead-time check",
          mutex: "DynamoDB Row Lock: #lk-ddb-0607 (Component inventory reservation)",
          worm: "s3://sop-vault/audit/step-06-bom-explosion.json (SHA-256: 62bc998d...)",
          kms: "Event BomExploded: 84 Subassemblies audited against supplier master contract"
        },
        tier1: {
          cedar: "permit(principal == Agent::DepDemand, action == Action::ReserveBOM, resource == MRP::ASIC) -> PERMIT (0.8ms)",
          pager: "Page 84-level BOM tree into structured vector cache; evict obsolete supplier catalogs",
          hash: "Block #6 signed: Hash(prev + delta) = 5d9921e3...",
          sandbox: "Nitro container execution: 0.35s duration, zero network escape"
        },
        tier2: {
          liaison: "Intra-Supply Pod direct mesh link (Hop 1/3, latency 4ms)",
          whiteboard: "Lane Supply: written 'BOM exploded into 84 assemblies' (VectorClock: [5,2,0])",
          quorum: "5/5 Quorum certified component lead times and factory delivery schedules",
          breaker: "Breaker #20 monitoring: PO value $28.4M against authorized capital budget"
        }
      },
      {
        step: 7,
        fromId: 7,
        toId: 8,
        isCrossPod: false,
        payload: "14,200 production purchase orders firmed ($28.4M committed). Handover for line capacity pooling.",
        tier0: {
          bedrock: "AWS Bedrock Financial commitment token signature & EMS contract attestation",
          mutex: "DynamoDB PutItem lease: #lk-ddb-0708 (Firm PO CAS lock: state=COMMITTED)",
          worm: "s3://sop-vault/audit/step-07-po-firming.json (SHA-256: 1f93445b...)",
          kms: "Event POFirmCommit: Supplier EMS contract binding recorded with KMS signature"
        },
        tier1: {
          cedar: "permit(principal == Agent::Firming, action == Action::CommitPO, resource == Budget::CapitalCommitment) -> PERMIT (0.9ms)",
          pager: "Page PO manifest into working memory; clear transient vendor pricing quotes",
          hash: "Block #7 signed: Hash(prev + delta) = 88aa7429...",
          sandbox: "Sandbox memory: 460MB / 2048MB. Capital limit within authorized threshold"
        },
        tier2: {
          liaison: "Intra-Supply Pod peer pulse (Hop 1/3, latency 3ms)",
          whiteboard: "Lane Supply: written '14,200 production orders firmed' (VectorClock: [5,3,0])",
          quorum: "5/5 Quorum verified EMS manufacturing slot validity and slot reservation",
          breaker: "Breaker #20 check passed: PO hash matched contract pricing master"
        }
      },
      {
        step: 8,
        fromId: 8,
        toId: 9,
        isCrossPod: false,
        payload: "Lines 1–4 pooled at 94% utilization load. Handover for finished goods dynamic safety stock buffer calculation.",
        tier0: {
          bedrock: "AWS Bedrock MILP capacity optimizer attestation & utilization constraint check",
          mutex: "DynamoDB PutItem lease: #lk-ddb-0809 (Line utilization reservation)",
          worm: "s3://sop-vault/audit/step-08-capacity.json (SHA-256: c4086629...)",
          kms: "Event LineAllocationCommitted: Clean audit trail verified"
        },
        tier1: {
          cedar: "permit(principal == Agent::Capacity, action == Action::PoolLines, resource == Line::SMT_1_4) -> PERMIT (0.7ms)",
          pager: "Page line throughput telemetry into memory; evict temporary maintenance windows",
          hash: "Block #8 signed: Hash(prev + delta) = 7e110bfa...",
          sandbox: "SMT line solver completed in 0.41s within Nitro enclave"
        },
        tier2: {
          liaison: "Intra-Supply Pod peer pulse (Hop 1/3, latency 3ms)",
          whiteboard: "Lane Supply: written 'SMT lines pooled @ 94% capacity' (VectorClock: [5,4,0])",
          quorum: "5/5 Quorum consensus on capacity headroom (>5% reserve capacity maintained)",
          breaker: "Thermal & load limits respected across all 4 SMT manufacturing lines"
        }
      },
      {
        step: 9,
        fromId: 9,
        toId: 10,
        isCrossPod: true,
        payload: "2,400 safety buffer units ($4.8M) locked. Crossing Supply-to-Control Liaison Bridge #2.",
        tier0: {
          bedrock: "AWS Bedrock Cross-VPC Executive Governance Attestation & safety stock model check",
          mutex: "DynamoDB Cross-Pod Executive Lock: #lk-ddb-pod-supply-control (Lease ID: #xpod-994c, TTL 30s)",
          worm: "s3://sop-vault/audit/step-09-liaison-bridge-supply-to-control.json (SHA-256: b18f9060...)",
          kms: "Event CrossPodControlHandoff: Executive enclave token armed"
        },
        tier1: {
          cedar: "permit(principal == Pod::Supply, action == Action::SubmitPlanToControl, resource == Pod::Control) -> PERMIT (0.8ms)",
          pager: "Supply Pod working memory serialized and linked; Executive Control Pod context loaded",
          hash: "Block #9 signed: Hash(prev + delta) = 9a43fe11...",
          sandbox: "Cross-pod boundary check passed: Zero buffer deviation"
        },
        tier2: {
          liaison: "⚡ CROSS-POD LIAISON SHORTCUT BRIDGE #2 ENGAGED (Watts-Strogatz shortcut link, Hop count: 1/3, 11ms)",
          whiteboard: "Lane Control: written 'Supply plan submitted with 2.4k safety stock' (VectorClock: [5,5,1])",
          quorum: "5/5 Byzantine nodes verified buffer adequacy against service level SLA (98.5%)",
          breaker: "Inventory carrying cost model within corporate working capital target"
        }
      },
      {
        step: 10,
        fromId: 10,
        toId: 11,
        isCrossPod: false,
        payload: "Plan telemetry verified: +3.2% variance within 5.0% tolerance bounds. Handover for final executive ERP sign-off.",
        tier0: {
          bedrock: "AWS Bedrock Nitro Enclave Final Attestation & master cryptographic sealing",
          mutex: "DynamoDB Master S&OP Commit Lock: #lk-ddb-master-sop-commit-2026 (FINAL LEASE)",
          worm: "s3://sop-vault/audit/step-10-final-executive-plan.json (COMPLIANCE MODE WORM: Retention 7 Years)",
          kms: "Event ExecutiveSOPCommit: Master KMS key arn:aws:kms:us-east-1:7829:key/master-sop signed"
        },
        tier1: {
          cedar: "permit(principal == Agent::Monitor, action == Action::RequestExecutiveSignoff, resource == Plan::AnnualSOP) -> PERMIT (0.5ms)",
          pager: "Page full executive summary into working memory; seal episodic ledger into cold store",
          hash: "Block #10 signed: Final master chain digest Hash = 02fa883c...",
          sandbox: "Executive container execution completed: 0.19s, zero unhandled exceptions"
        },
        tier2: {
          liaison: "Intra-Control Pod direct pulse (Hop 1/3, latency 2ms)",
          whiteboard: "Lane Control: written 'Stage 11 Owner: Plan finalized & committed to immutable S3' (VectorClock: [5,5,2])",
          quorum: "Unanimous Quorum: 5/5 nodes signed off on master S&OP plan execution",
          breaker: "Governance certified: 100% compliant with enterprise risk & audit controls"
        }
      }
    ];

    let currentHandoverIndex = 0; // 0 to 9 (representing step 1 to 10)
    let isAutoPropagating = false;
    let propIntervalTimer = null;
    let propSpeedMs = 1200;
    let handoverHistory = [];

    function initPropagationMesh() {
      const container = document.getElementById('agentPipelineMeshContainer');
      if (!container) return;
      container.innerHTML = '';

      for (let i = 0; i < AGENTS_METADATA.length; i++) {
        const ag = AGENTS_METADATA[i];
        const node = document.createElement('div');
        node.className = 'agent-mesh-node';
        node.id = `meshNode-${ag.id}`;
        node.onclick = () => selectHandoverByAgent(ag.id);

        node.innerHTML = `
          <div class="mesh-node-icon">${ag.icon}</div>
          <div class="mesh-node-num">STAGE ${ag.id}</div>
          <div class="mesh-node-name">${ag.short}</div>
          <div class="mesh-node-role-badge" id="meshBadge-${ag.id}" style="background:${ag.pod === 'Demand' ? '#f5f3ff' : (ag.pod === 'Supply' ? '#eff6ff' : '#ecfdf5')}; color:${ag.color};">
            ${ag.pod}
          </div>
        `;
        container.appendChild(node);

        // Add wire arrow if not last node
        if (i < AGENTS_METADATA.length - 1) {
          const arrow = document.createElement('div');
          const isCross = (ag.id === 5 || ag.id === 9);
          arrow.className = `mesh-wire-arrow ${isCross ? 'cross-pod' : ''}`;
          arrow.id = `meshWire-${ag.id}`;
          arrow.title = isCross ? 'Cross-Pod Liaison Shortcut Bridge' : 'Intra-Pod Mesh Link';
          arrow.innerHTML = isCross ? '🌉' : '➔';
          container.appendChild(arrow);
        }
      }

      renderCurrentHandoverUI();
    }

    function selectHandoverByAgent(agentId) {
      if (isAutoPropagating) pauseAutoPropagation();
      let targetStep = agentId - 1;
      if (targetStep >= HANDOVER_STEPS.length) targetStep = HANDOVER_STEPS.length - 1;
      if (targetStep < 0) targetStep = 0;
      currentHandoverIndex = targetStep;
      renderCurrentHandoverUI();
      triggerHandoverPulseAnimation();
    }

    function renderCurrentHandoverUI() {
      const h = HANDOVER_STEPS[currentHandoverIndex];
      const srcAg = AGENTS_METADATA[h.fromId - 1];
      const tgtAg = AGENTS_METADATA[h.toId - 1];

      // 1. Update Mesh Nodes & Wire states
      document.querySelectorAll('.agent-mesh-node').forEach(n => {
        n.classList.remove('source-active', 'target-active', 'passed');
      });
      document.querySelectorAll('.mesh-wire-arrow').forEach(w => {
        w.classList.remove('wire-pulsing');
      });

      // Mark passed nodes
      for (let i = 1; i < h.fromId; i++) {
        const pNode = document.getElementById(`meshNode-${i}`);
        if (pNode) pNode.classList.add('passed');
      }

      // Mark active source and target
      const sNode = document.getElementById(`meshNode-${h.fromId}`);
      if (sNode) sNode.classList.add('source-active');
      const tNode = document.getElementById(`meshNode-${h.toId}`);
      if (tNode) tNode.classList.add('target-active');

      // Pulse the active wire
      const wire = document.getElementById(`meshWire-${h.fromId}`);
      if (wire) wire.classList.add('wire-pulsing');

      // 2. Update Handover Showcase Box
      document.getElementById('sourceAgentAvatar').textContent = srcAg.icon;
      document.getElementById('sourceAgentName').textContent = `Stage ${srcAg.id}: ${srcAg.name}`;
      document.getElementById('sourceAgentPod').textContent = `${srcAg.pod} Pod • ${srcAg.role}`;

      document.getElementById('targetAgentAvatar').textContent = tgtAg.icon;
      document.getElementById('targetAgentName').textContent = `Stage ${tgtAg.id}: ${tgtAg.name}`;
      document.getElementById('targetAgentPod').textContent = `${tgtAg.pod} Pod • ${tgtAg.role}`;

      document.getElementById('handoverStepBadge').textContent = `HANDOVER ${h.step} OF 10`;
      document.getElementById('handoverBeamGraphic').innerHTML = h.isCrossPod ? '⚡🌉⚡' : '➔➔➔';
      document.getElementById('handoverPayloadText').textContent = h.payload;

      // 3. Update 3-Tier Stack Primitives
      // Tier 0 AWS
      document.getElementById('tier0BedrockDesc').textContent = h.tier0.bedrock;
      document.getElementById('tier0MutexDesc').textContent = h.tier0.mutex;
      document.getElementById('tier0WormDesc').textContent = h.tier0.worm;
      document.getElementById('tier0KmsDesc').textContent = h.tier0.kms;
      document.getElementById('tier0StateText').textContent = `ACTIVE (LOCK #${h.step})`;

      // Tier 1 Kernel
      document.getElementById('tier1CedarDesc').textContent = h.tier1.cedar;
      document.getElementById('tier1PagerDesc').textContent = h.tier1.pager;
      document.getElementById('tier1HashDesc').textContent = h.tier1.hash;
      document.getElementById('tier1SandboxDesc').textContent = h.tier1.sandbox;
      document.getElementById('tier1StateText').textContent = `PERMIT (RING 0)`;

      // Tier 2 Swarm
      document.getElementById('tier2LiaisonDesc').textContent = h.tier2.liaison;
      document.getElementById('tier2WhiteboardDesc').textContent = h.tier2.whiteboard;
      document.getElementById('tier2QuorumDesc').textContent = h.tier2.quorum;
      document.getElementById('tier2BreakerDesc').textContent = h.tier2.breaker;
      document.getElementById('tier2StateText').textContent = `CONSENSUS REACHED`;

      // 4. Update sync status
      document.getElementById('propStatusBadge').textContent = `STEP ${h.step}/10 • SYNCHRONIZED`;
      document.getElementById('tierWaveStatusText').textContent = 
        `TIER 0 AWS LOCK ➔ TIER 1 CEDAR GATE ➔ TIER 2 SWARM WHITEBOARD (STEP ${h.step})`;

      // Record in history if not already recorded
      recordHandoverInLedger(h);
    }

    function triggerHandoverPulseAnimation() {
      const t0 = document.getElementById('tier0Card');
      const t1 = document.getElementById('tier1Card');
      const t2 = document.getElementById('tier2Card');
      const d0 = document.getElementById('tier0Dot');
      const d1 = document.getElementById('tier1Dot');
      const d2 = document.getElementById('tier2Dot');

      // Sequential bottom-up wave: Tier 0 -> Tier 1 -> Tier 2
      t0.classList.add('pulse-active');
      d0.classList.add('active-pulse');
      t1.classList.remove('pulse-active');
      d1.classList.remove('active-pulse');
      t2.classList.remove('pulse-active');
      d2.classList.remove('active-pulse');

      setTimeout(() => {
        t0.classList.remove('pulse-active');
        d0.classList.remove('active-pulse');
        t1.classList.add('pulse-active');
        d1.classList.add('active-pulse');
      }, Math.min(350, propSpeedMs * 0.3));

      setTimeout(() => {
        t1.classList.remove('pulse-active');
        d1.classList.remove('active-pulse');
        t2.classList.add('pulse-active');
        d2.classList.add('active-pulse');
      }, Math.min(700, propSpeedMs * 0.6));

      setTimeout(() => {
        t2.classList.remove('pulse-active');
        d2.classList.remove('active-pulse');
      }, Math.min(1050, propSpeedMs * 0.9));
    }

    function recordHandoverInLedger(h) {
      // Avoid duplicate consecutive entry
      if (handoverHistory.length > 0 && handoverHistory[handoverHistory.length - 1].step === h.step) {
        return;
      }

      const mockHash = "0x" + Math.random().toString(16).substring(2, 10);
      const record = {
        step: h.step,
        fromName: AGENTS_METADATA[h.fromId - 1].short,
        toName: AGENTS_METADATA[h.toId - 1].short,
        payload: h.payload,
        mutex: `DDB Lock: #lk-${h.step} (TTL 15s)`,
        cedar: `PERMIT (0.${6 + (h.step % 4)}ms)`,
        whiteboard: h.isCrossPod ? "⚡ Cross-Pod Bridge Written" : "Lane Updated (VC++)",
        hash: mockHash
      };
      handoverHistory.push(record);
      renderLedgerTable();
    }

    function renderLedgerTable() {
      const tbody = document.getElementById('transHistoryBody');
      const counter = document.getElementById('historyCounterPill');
      if (!tbody) return;

      counter.textContent = `${handoverHistory.length} Handovers Executed`;

      let html = '';
      for (let i = handoverHistory.length - 1; i >= 0; i--) {
        const r = handoverHistory[i];
        html += `
          <tr>
            <td><span class="table-step-pill">#${r.step}</span></td>
            <td><strong>${r.fromName}</strong> <span style="color:#7c3aed;">➔</span> <strong>${r.toName}</strong></td>
            <td style="font-family:var(--font-mono); font-size:11px; max-width:280px;">${r.payload}</td>
            <td><span class="status-badge badge-locked" style="font-size:10px;">${r.mutex}</span></td>
            <td><span class="status-badge badge-ok" style="font-size:10px;">${r.cedar}</span></td>
            <td><span class="status-badge" style="background:#f5f3ff; color:#7c3aed; font-size:10px;">${r.whiteboard}</span></td>
            <td style="font-family:var(--font-mono); font-size:10px; color:var(--text-muted);">${r.hash}</td>
          </tr>
        `;
      }
      tbody.innerHTML = html;
    }

    function clearPropagationHistory() {
      handoverHistory = [];
      const tbody = document.getElementById('transHistoryBody');
      const counter = document.getElementById('historyCounterPill');
      if (counter) counter.textContent = '0 Handovers Executed';
      if (tbody) {
        tbody.innerHTML = `
          <tr>
            <td colspan="7" style="text-align:center; color:var(--text-muted); padding:16px;">
              Ledger cleared. Click "Next Agent Handover" or "Auto-Play" to record new events.
            </td>
          </tr>
        `;
      }
    }

    function stepNextPropagation() {
      if (isAutoPropagating) pauseAutoPropagation();
      if (currentHandoverIndex < HANDOVER_STEPS.length - 1) {
        currentHandoverIndex++;
      } else {
        currentHandoverIndex = 0; // wrap around
      }
      renderCurrentHandoverUI();
      triggerHandoverPulseAnimation();
    }

    function stepPrevPropagation() {
      if (isAutoPropagating) pauseAutoPropagation();
      if (currentHandoverIndex > 0) {
        currentHandoverIndex--;
      } else {
        currentHandoverIndex = HANDOVER_STEPS.length - 1;
      }
      renderCurrentHandoverUI();
      triggerHandoverPulseAnimation();
    }

    function resetPropagationMatrix() {
      if (isAutoPropagating) pauseAutoPropagation();
      currentHandoverIndex = 0;
      renderCurrentHandoverUI();
      triggerHandoverPulseAnimation();
      showToast("↺ Propagation matrix reset to Stage 1 Handover");
    }

    function toggleAutoPropagationWave() {
      if (isAutoPropagating) {
        pauseAutoPropagation();
      } else {
        startAutoPropagation();
      }
    }

    function startAutoPropagation() {
      isAutoPropagating = true;
      document.getElementById('btnAutoPropIcon').textContent = '⏸';
      document.getElementById('btnAutoPropText').textContent = 'Pause Auto-Play';
      document.getElementById('propStatusBadge').textContent = 'AUTO-PROPAGATING WAVE...';
      document.getElementById('propStatusBadge').className = 'status-badge badge-warn';

      triggerHandoverPulseAnimation();

      propIntervalTimer = setInterval(() => {
        if (currentHandoverIndex < HANDOVER_STEPS.length - 1) {
          currentHandoverIndex++;
          renderCurrentHandoverUI();
          triggerHandoverPulseAnimation();
        } else {
          // Finished full cycle
          pauseAutoPropagation();
          document.getElementById('propStatusBadge').textContent = 'CYCLE COMPLETE • 10/10 COMMITTED';
          document.getElementById('propStatusBadge').className = 'status-badge badge-ok';
          showToast("✔ Full 10-Handover Dual Propagation Wave Completed!");
        }
      }, propSpeedMs);
    }

    function pauseAutoPropagation() {
      isAutoPropagating = false;
      if (propIntervalTimer) {
        clearInterval(propIntervalTimer);
        propIntervalTimer = null;
      }
      const icon = document.getElementById('btnAutoPropIcon');
      const text = document.getElementById('btnAutoPropText');
      if (icon) icon.textContent = '▶';
      if (text) text.textContent = 'Auto-Play All 10 Handovers';
      const badge = document.getElementById('propStatusBadge');
      if (badge) {
        badge.textContent = `PAUSED AT STEP ${currentHandoverIndex + 1}/10`;
        badge.className = 'status-badge badge-ok';
      }
    }

    function setPropSpeed(ms) {
      propSpeedMs = parseInt(ms, 10) || 1200;
      if (isAutoPropagating) {
        pauseAutoPropagation();
        startAutoPropagation();
      }
    }

    // Initialize propagation mesh when DOM is ready
    window.addEventListener('DOMContentLoaded', () => {
      initPropagationMesh();
    });
    """

    # Inject JS right before the last </script>
    last_script_idx = src.rfind("</script>")
    src = src[:last_script_idx] + "\n" + dual_prop_js + "\n" + src[last_script_idx:]

    with open(TARGET_HTML, "w", encoding="utf-8") as f:
        f.write(src)

    print(f"Successfully generated {TARGET_HTML}! Total size: {len(src)} bytes.")

if __name__ == "__main__":
    generate()
