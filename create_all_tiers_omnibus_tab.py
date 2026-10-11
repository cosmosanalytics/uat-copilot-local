# -*- coding: utf-8 -*-
"""
create_all_tiers_omnibus_tab.py
Adds a unified "Unified All-Tiers Matrix" tab to BOTH:
1. agent_kernel_studio_app.html (Single Agent)
   - Shows Tier 0 (AWS Primitives) + Tier 1 (Agent OS Kernel) side-by-side / stacked.
   - During execution, the tab does NOT switch away! Instead, active glowing pulse rings, status badges, and data flow indicators propagate step-by-step directly through all tiers on the single screen.
2. multi_agent_system_studio_app.html (Multi-Agent Swarm)
   - Shows all 3 tiers simultaneously:
     * Tier 0: Physical AWS Cloud Primitives (DynamoDB CAS Mutex, Bedrock Model, S3 WORM Vault)
     * Tier 1: Agent OS Kernel (Prefrontal Ring 0 Cedar Gatekeeper, Context Memory Pager)
     * Tier 2: Multi-Agent Swarm Lattice (Watts-Strogatz Liaison Router, O(N) Whiteboard, Byzantine Quorum)
   - During execution, it stays on this unified tab and visibly propagates bottom-up:
     Tier 0 (Mutex & Model) -> Tier 1 (Kernel Gate) -> Tier 2 (Whiteboard & Quorum) with glowing borders, animated data packets, and checkmarks.
"""

import re

# ========================================================
# 1. ENHANCE multi_agent_system_studio_app.html
# ========================================================
with open('multi_agent_system_studio_app.html', 'r', encoding='utf-8') as f:
    m_html = f.read()

# Add CSS for the unified tier matrix cards & active propagation glow
m_css_add = """
    /* UNIFIED ALL-TIERS PROPAGATION MATRIX */
    .unified-matrix-container {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .tier-stack-card {
      background: var(--bg-panel);
      border: 2px solid var(--border-subtle);
      border-radius: 12px;
      padding: 14px 18px;
      transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: var(--card-shadow);
      position: relative;
      overflow: hidden;
    }
    .tier-stack-card::before {
      content: "";
      position: absolute;
      top: 0; left: 0; bottom: 0;
      width: 5px;
      background: var(--border-subtle);
      transition: all 0.3s ease;
    }
    .tier-stack-card.tier-0-card::before { background: #059669; }
    .tier-stack-card.tier-1-card::before { background: #2563eb; }
    .tier-stack-card.tier-2-card::before { background: #7c3aed; }

    /* Active Glowing Propagation State */
    .tier-stack-card.active-propagating {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
    }
    .tier-stack-card.tier-0-card.active-propagating {
      border-color: #059669;
      background: #f0fdf4;
      box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.18);
    }
    .tier-stack-card.tier-1-card.active-propagating {
      border-color: #2563eb;
      background: #eff6ff;
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.18);
    }
    .tier-stack-card.tier-2-card.active-propagating {
      border-color: #7c3aed;
      background: #faf5ff;
      box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.2);
    }

    .tier-stack-card.completed-tier {
      border-color: #cbd5e1;
      opacity: 0.95;
    }

    .tier-head-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }
    .tier-title-badge {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 800;
      font-size: 0.88rem;
    }
    .pill-tier {
      font-size: 0.68rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      font-family: var(--font-mono);
    }
    .pill-t0 { background: #d1fae5; color: #065f46; border: 1px solid #a7f3d0; }
    .pill-t1 { background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }
    .pill-t2 { background: #ede9fe; color: #5b21b6; border: 1px solid #ddd6fe; }

    .tier-items-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 10px;
    }
    .tier-item-box {
      background: var(--bg-panel-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 4px;
      transition: all 0.25s ease;
    }
    .tier-item-box.highlight-item {
      background: #ffffff;
      border-color: currentColor;
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .tier-item-title {
      font-size: 0.76rem;
      font-weight: 800;
      color: var(--text-primary);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .tier-item-val {
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: var(--text-secondary);
      word-break: break-all;
    }

    .propagation-wire-row {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 2px 0;
      color: var(--text-muted);
      font-size: 0.72rem;
      font-weight: 700;
    }
    .wire-arrow {
      font-size: 1.1rem;
      line-height: 1;
      transition: all 0.3s ease;
    }
    .wire-active {
      color: #2563eb;
      font-weight: 800;
      animation: bounceWire 0.8s infinite alternate;
    }
    @keyframes bounceWire {
      from { transform: translateY(-2px); }
      to { transform: translateY(2px); }
    }
"""

if '.unified-matrix-container' not in m_html:
    m_html = m_html.replace('/* STAGE PANE (RIGHT) */', m_css_add + '\n    /* STAGE PANE (RIGHT) */')

# Add "Unified All-Tiers Matrix" tab button as the very first default active tab!
old_m_tabs = """      <div class="stage-tabs">
        <button class="tab-btn active" id="tabBtnTopology" onclick="switchStage('topology')">🕸️ Watts-Strogatz Network</button>"""

new_m_tabs = """      <div class="stage-tabs">
        <button class="tab-btn active" id="tabBtnAllTiers" onclick="switchStage('alltiers')">🌟 Unified All-Tiers Matrix</button>
        <button class="tab-btn" id="tabBtnTopology" onclick="switchStage('topology')">🕸️ Watts-Strogatz Network</button>"""

m_html = m_html.replace(old_m_tabs, new_m_tabs)

# Add Unified All-Tiers Content View
m_alltiers_content = """      <!-- TAB 0: UNIFIED ALL-TIERS PROPAGATION MATRIX -->
      <div class="stage-content" id="stageAllTiers" style="display: flex;">
        <div class="unified-matrix-container">

          <!-- TIER 0 CARD (Physical AWS Primitives) -->
          <div class="tier-stack-card tier-0-card" id="mCardTier0">
            <div class="tier-head-row">
              <div class="tier-title-badge">
                <span class="pill-tier pill-t0">TIER 0</span>
                <span>Physical AWS Cloud Primitives &amp; Foundation Model</span>
              </div>
              <span class="service-status status-ok" id="statusBadgeT0">IDLE &bull; READY</span>
            </div>
            <div class="tier-items-grid">
              <div class="tier-item-box" id="mBoxT0Mutex">
                <div class="tier-item-title"><span>🔒 DynamoDB Mutex</span><span id="mValT0MutexLock">UNLOCKED</span></div>
                <div class="tier-item-val" id="mValT0MutexKey">Key: distributed-swarm-lock-101</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Conditional CAS lease prevents concurrency collisions.</div>
              </div>
              <div class="tier-item-box" id="mBoxT0Model">
                <div class="tier-item-title"><span>🧠 Amazon Bedrock</span><span>Llama 3.3 / Claude</span></div>
                <div class="tier-item-val" id="mValT0ModelStatus">Untrusted Ring 3 Proposal Space</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Proposes structured JSON without execution IAM.</div>
              </div>
              <div class="tier-item-box" id="mBoxT0Vault">
                <div class="tier-item-title"><span>📦 S3 WORM Vault</span><span>ObjectLock: 7 Yrs</span></div>
                <div class="tier-item-val" id="mValT0VaultHash">SHA-256: e3b0c44298fc1c...</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Zero-hallucination compliance grounding receipts.</div>
              </div>
            </div>
          </div>

          <!-- PROPAGATION WIRE 0 -> 1 -->
          <div class="propagation-wire-row" id="mWire0to1">
            <span>&uarr; Physical CAS mutex &amp; Bedrock proposals feed into Agent OS Kernel &uarr;</span>
          </div>

          <!-- TIER 1 CARD (Agent OS Kernel) -->
          <div class="tier-stack-card tier-1-card" id="mCardTier1">
            <div class="tier-head-row">
              <div class="tier-title-badge">
                <span class="pill-tier pill-t1">TIER 1</span>
                <span>Individual Agent OS Kernel (Prefrontal Ring 0 &amp; Memory Pager)</span>
              </div>
              <span class="service-status status-proc" id="statusBadgeT1">RING 0 READY</span>
            </div>
            <div class="tier-items-grid">
              <div class="tier-item-box" id="mBoxT1Gate">
                <div class="tier-item-title"><span>🛡️ Cedar Guardrail Gate</span><span id="mValT1Decision">STANDBY</span></div>
                <div class="tier-item-val" id="mValT1Policy">Policy: Cedar::PermitSwarmDelegation</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Prefrontal Ring 0 intercepts and vets all syscall arguments.</div>
              </div>
              <div class="tier-item-box" id="mBoxT1Pager">
                <div class="tier-item-title"><span>💾 Context Pager</span><span>RAM Compacted</span></div>
                <div class="tier-item-val" id="mValT1Tokens">Active Window: 2,800 / 8,192 Tok</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Pages cold reasoning frames to S3 to prevent amnesia.</div>
              </div>
              <div class="tier-item-box" id="mBoxT1Ledger">
                <div class="tier-item-title"><span>⛓️ Episodic Hash-Chain</span><span>Block #412 Active</span></div>
                <div class="tier-item-val" id="mValT1LedgerHash">Block: 7a8f902c4b1e...</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Append-only audit trail connecting perception to decision.</div>
              </div>
            </div>
          </div>

          <!-- PROPAGATION WIRE 1 -> 2 -->
          <div class="propagation-wire-row" id="mWire1to2">
            <span>&uarr; Vetted individual kernel decisions propagate up to Multi-Agent Swarm Lattice &uarr;</span>
          </div>

          <!-- TIER 2 CARD (Multi-Agent Swarm) -->
          <div class="tier-stack-card tier-2-card" id="mCardTier2">
            <div class="tier-head-row">
              <div class="tier-title-badge">
                <span class="pill-tier pill-t2">TIER 2</span>
                <span>Watts-Strogatz Multi-Agent Swarm Coordination</span>
              </div>
              <span class="service-status status-proc" id="statusBadgeT2">LATTICE ONLINE</span>
            </div>
            <div class="tier-items-grid">
              <div class="tier-item-box" id="mBoxT2Liaison">
                <div class="tier-item-title"><span>🌉 Liaison Router</span><span>EventBridge Bus</span></div>
                <div class="tier-item-val" id="mValT2Hops">Max Hops: &le; 3 (Small-World)</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Inter-pod shortcut routing avoids O(N&sup2;) message storms.</div>
              </div>
              <div class="tier-item-box" id="mBoxT2Whiteboard">
                <div class="tier-item-title"><span>📋 O(N) Shared Whiteboard</span><span id="mValT2WbStatus">3 LANES SYNCED</span></div>
                <div class="tier-item-val" id="mValT2WbSummary">Finance &bull; Compliance &bull; Operations</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Single shared whiteboard state updated under CAS locks.</div>
              </div>
              <div class="tier-item-box" id="mBoxT2Quorum">
                <div class="tier-item-title"><span>⚖️ BFT Quorum Consensus</span><span id="mValT2QuorumVotes">10/12 SUPERMAJORITY</span></div>
                <div class="tier-item-val" id="mValT2QuorumStatus">Threshold: &ge; 2/3 + 1 Votes</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Cryptographically signed ballots sealed into S3 WORM vault.</div>
              </div>
            </div>
          </div>

        </div>
      </div>
"""

# Inject before stageTopology
m_html = m_html.replace('<!-- TAB 1: TOPOLOGY CANVAS -->', m_alltiers_content + '\n      <!-- TAB 1: TOPOLOGY CANVAS -->')

# Update switchStage in multi_agent_system_studio_app.html
old_m_switch = """    function switchStage(stage) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('stageTopology').style.display = stage === 'topology' ? 'flex' : 'none';"""

new_m_switch = """    function switchStage(stage) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      const allTiersEl = document.getElementById('stageAllTiers');
      if (allTiersEl) allTiersEl.style.display = stage === 'alltiers' ? 'flex' : 'none';
      document.getElementById('stageTopology').style.display = stage === 'topology' ? 'flex' : 'none';"""

m_html = m_html.replace(old_m_switch, new_m_switch)

old_m_switch_tabs = """      if (stage === 'topology') {
        document.getElementById('tabBtnTopology')?.classList.add('active');
        setTimeout(drawTopologyCanvas, 50);
      }"""

new_m_switch_tabs = """      if (stage === 'alltiers') {
        document.getElementById('tabBtnAllTiers')?.classList.add('active');
      }
      if (stage === 'topology') {
        document.getElementById('tabBtnTopology')?.classList.add('active');
        setTimeout(drawTopologyCanvas, 50);
      }"""

m_html = m_html.replace(old_m_switch_tabs, new_m_switch_tabs)

# Update runSteppedSimulation in multi_agent_system_studio_app.html so it stays on the unified tab and propagates live!
old_m_sim = """    async function runSteppedSimulation(goalText, modeTag) {
      const wait = (ms) => new Promise(res => setTimeout(res, ms));

      // STEP 1 (TIER 0): Physical AWS Cloud Grounding & Mutex Allocation
      updateSwarmStepUI(1, "STEP 1/5: TIER 0 AWS DYNAMODB MUTEX & S3 VAULT ANCHOR");
      showToast('🔒 [Step 1/5: Tier 0 AWS] Acquiring DynamoDB CAS mutex lease & S3 grounding vault...');
      await wait(650);

      // STEP 2 (TIER 0): Amazon Bedrock Foundation Model Proposal Synthesis (Ring 3)
      updateSwarmStepUI(2, "STEP 2/5: TIER 0 BEDROCK PROPOSAL GENERATION (RING 3)");
      showToast('🧠 [Step 2/5: Tier 0 Bedrock] Specialist LLMs generating typed proposal schemas in Ring 3...');
      await wait(650);

      // STEP 3 (TIER 1): Agent OS Prefrontal Kernel Gatekeeper & Context Pager
      updateSwarmStepUI(3, "STEP 3/5: TIER 1 AGENT OS KERNEL ARBITRATION (RING 0)");
      showToast('🛡️ [Step 3/5: Tier 1 Kernel] Enforcing Cedar guardrails & virtual context paging per agent...');
      await wait(700);

      // STEP 4 (TIER 2): Watts-Strogatz Inter-Pod Routing & O(N) Whiteboard Commit
      updateSwarmStepUI(4, "STEP 4/5: TIER 2 WATTS-STROGATZ LIAISON & WHITEBOARD");
      switchStage('topology');
      showToast('⚡ [Step 4/5: Tier 2 Swarm] Routing across EventBridge liaison bridges to O(N) Whiteboard...');
      animateLiaisonPackets(1800);
      await wait(600);

      switchStage('whiteboard');
      const customWb = [
        { author: "agent-fin-01 (Finance Liaison)", text: "Tier 0 DynamoDB CAS lock confirmed. Liquidity verified for: " + goalText.slice(0, 65) + "..." },
        { author: "agent-comp-01 (Compliance Liaison)", text: "Tier 1 Cedar guardrails enforced. Certified against S3 WORM and Neptune graph." },
        { author: "agent-ops-01 (Operations Liaison)", text: "Step Functions DAG initialized. Sandboxed MicroVM execution committed." }
      ];
      renderWhiteboardLanes(customWb);
      await wait(750);

      // STEP 5 (TIER 2): Byzantine Fault Tolerant Supermajority Quorum Vote
      updateSwarmStepUI(5, "STEP 5/5: TIER 2 BYZANTINE 2/3+1 QUORUM SEAL");
      switchStage('quorum');
      showToast('⚖️ [Step 5/5: Tier 2 Consensus] Gathering Byzantine ballots (>= 2/3 + 1 supermajority)...');
      const votes = [
        { id: "agent-fin-01", pod: "Finance", vote: "YES", cert: "WORM-OK" },
        { id: "agent-fin-02", pod: "Finance", vote: "YES", cert: "WORM-OK" },
        { id: "agent-fin-03", pod: "Finance", vote: "YES", cert: "WORM-OK" },
        { id: "agent-comp-01", pod: "Compliance", vote: "YES", cert: "WORM-OK" },
        { id: "agent-comp-02", pod: "Compliance", vote: "YES", cert: "WORM-OK" },
        { id: "agent-comp-03", pod: "Compliance", vote: "YES", cert: "WORM-OK" },
        { id: "agent-ops-01", pod: "Operations", vote: "YES", cert: "WORM-OK" },
        { id: "agent-ops-02", pod: "Operations", vote: "YES", cert: "WORM-OK" },
        { id: "agent-ops-03", pod: "Operations", vote: "YES", cert: "WORM-OK" },
        { id: "agent-ops-04", pod: "Operations", vote: "YES", cert: "WORM-OK" }
      ];
      renderQuorumGrid(votes);
      document.getElementById('quorumStatusBadge').textContent = `QUORUM ACHIEVED (10/12 VOTES >= 2/3+1) • ${modeTag}`;
      await wait(600);

      updateSwarmStepUI(6, "BOTTOM-UP TIER 0 &rarr; TIER 1 &rarr; TIER 2 CONVERGED & SEALED (100%)");
      showToast('✅ Multi-Agent Swarm successfully converged from Tier 0 to Tier 2!');
    }"""

new_m_sim = """    async function runSteppedSimulation(goalText, modeTag) {
      const wait = (ms) => new Promise(res => setTimeout(res, ms));

      // Stay on Unified All-Tiers Matrix view to show simultaneous propagation without jarring tab switching!
      switchStage('alltiers');

      // Clear all active tier states
      ['mCardTier0', 'mCardTier1', 'mCardTier2'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.remove('active-propagating', 'completed-tier');
      });
      document.getElementById('mWire0to1')?.classList.remove('wire-active');
      document.getElementById('mWire1to2')?.classList.remove('wire-active');

      // ----------------------------------------------------
      // STEP 1 (TIER 0): Physical AWS Cloud Grounding & Mutex Allocation
      // ----------------------------------------------------
      updateSwarmStepUI(1, "STEP 1/5: [TIER 0] DYNAMODB CAS MUTEX & S3 GROUNDING VAULT");
      document.getElementById('mCardTier0').classList.add('active-propagating');
      document.getElementById('statusBadgeT0').textContent = "ACQUIRING CAS LEASE...";
      document.getElementById('statusBadgeT0').className = "service-status status-proc";
      document.getElementById('mValT0MutexLock').textContent = "LOCKING (CAS)...";
      document.getElementById('mValT0MutexLock').style.color = "#d97706";
      showToast('🔒 [Step 1/5: Tier 0 AWS] Acquiring DynamoDB CAS mutex lease & S3 grounding vault...');
      await wait(700);

      document.getElementById('mValT0MutexLock').textContent = "LOCKED (EXCLUSIVE)";
      document.getElementById('mValT0MutexLock').style.color = "#059669";
      const randomReceipt = "rcpt-" + Math.floor(10000 + Math.random()*90000);
      document.getElementById('mValT0VaultHash').textContent = randomReceipt + " (SHA-256 VALID)";

      // ----------------------------------------------------
      // STEP 2 (TIER 0): Amazon Bedrock Foundation Model Proposal (Ring 3)
      // ----------------------------------------------------
      updateSwarmStepUI(2, "STEP 2/5: [TIER 0] BEDROCK SPECIALIST REASONING (RING 3)");
      document.getElementById('mValT0ModelStatus').textContent = "SYNTHESIZING PROPOSALS...";
      document.getElementById('mValT0ModelStatus').style.color = "#2563eb";
      showToast('🧠 [Step 2/5: Tier 0 Bedrock] Specialist LLMs generating typed proposal schemas in Ring 3...');
      await wait(700);

      document.getElementById('mValT0ModelStatus').textContent = "PROPOSALS COMPILED (TYPED JSON)";
      document.getElementById('statusBadgeT0').textContent = "TIER 0 SECURED ✔";
      document.getElementById('statusBadgeT0').className = "service-status status-ok";
      document.getElementById('mCardTier0').classList.remove('active-propagating');
      document.getElementById('mCardTier0').classList.add('completed-tier');

      // Propagate wire 0 -> 1
      document.getElementById('mWire0to1').classList.add('wire-active');
      await wait(350);

      // ----------------------------------------------------
      // STEP 3 (TIER 1): Agent OS Prefrontal Kernel Gatekeeper & Context Pager
      // ----------------------------------------------------
      updateSwarmStepUI(3, "STEP 3/5: [TIER 1] PREFRONTAL KERNEL RING 0 CEDAR ARBITER");
      document.getElementById('mCardTier1').classList.add('active-propagating');
      document.getElementById('statusBadgeT1').textContent = "EVALUATING CEDAR...";
      document.getElementById('statusBadgeT1').className = "service-status status-proc";
      document.getElementById('mValT1Decision').textContent = "EVALUATING...";
      document.getElementById('mValT1Decision').style.color = "#d97706";
      showToast('🛡️ [Step 3/5: Tier 1 Kernel] Enforcing Cedar guardrails & virtual context paging per agent...');
      await wait(750);

      document.getElementById('mValT1Decision').textContent = "ALLOW (RING 0 PASS)";
      document.getElementById('mValT1Decision').style.color = "#059669";
      document.getElementById('statusBadgeT1').textContent = "TIER 1 COMMITTED ✔";
      document.getElementById('statusBadgeT1').className = "service-status status-ok";
      document.getElementById('mCardTier1').classList.remove('active-propagating');
      document.getElementById('mCardTier1').classList.add('completed-tier');

      // Propagate wire 1 -> 2
      document.getElementById('mWire1to2').classList.add('wire-active');
      await wait(350);

      // ----------------------------------------------------
      // STEP 4 (TIER 2): Watts-Strogatz Inter-Pod Routing & O(N) Whiteboard Commit
      // ----------------------------------------------------
      updateSwarmStepUI(4, "STEP 4/5: [TIER 2] WATTS-STROGATZ SHORTCUTS & WHITEBOARD");
      document.getElementById('mCardTier2').classList.add('active-propagating');
      document.getElementById('statusBadgeT2').textContent = "ROUTING & SYNCING...";
      document.getElementById('statusBadgeT2').className = "service-status status-proc";
      showToast('⚡ [Step 4/5: Tier 2 Swarm] Routing across EventBridge liaison bridges to O(N) Whiteboard...');
      animateLiaisonPackets(1800);
      await wait(600);

      const customWb = [
        { author: "agent-fin-01 (Finance Liaison)", text: "Tier 0 DynamoDB CAS lock confirmed. Liquidity verified for: " + goalText.slice(0, 65) + "..." },
        { author: "agent-comp-01 (Compliance Liaison)", text: "Tier 1 Cedar guardrails enforced. Certified against S3 WORM and Neptune graph." },
        { author: "agent-ops-01 (Operations Liaison)", text: "Step Functions DAG initialized. Sandboxed MicroVM execution committed." }
      ];
      renderWhiteboardLanes(customWb);
      document.getElementById('mValT2WbStatus').textContent = "COMMITTED TO S3 VAULT";
      document.getElementById('mValT2WbStatus').style.color = "#059669";
      await wait(700);

      // ----------------------------------------------------
      // STEP 5 (TIER 2): Byzantine Fault Tolerant Supermajority Quorum Vote
      // ----------------------------------------------------
      updateSwarmStepUI(5, "STEP 5/5: [TIER 2] BYZANTINE 2/3+1 QUORUM SEAL");
      document.getElementById('statusBadgeT2').textContent = "COLLECTING BALLOTS...";
      showToast('⚖️ [Step 5/5: Tier 2 Consensus] Gathering Byzantine ballots (>= 2/3 + 1 supermajority)...');
      const votes = [
        { id: "agent-fin-01", pod: "Finance", vote: "YES", cert: "WORM-OK" },
        { id: "agent-fin-02", pod: "Finance", vote: "YES", cert: "WORM-OK" },
        { id: "agent-fin-03", pod: "Finance", vote: "YES", cert: "WORM-OK" },
        { id: "agent-comp-01", pod: "Compliance", vote: "YES", cert: "WORM-OK" },
        { id: "agent-comp-02", pod: "Compliance", vote: "YES", cert: "WORM-OK" },
        { id: "agent-comp-03", pod: "Compliance", vote: "YES", cert: "WORM-OK" },
        { id: "agent-ops-01", pod: "Operations", vote: "YES", cert: "WORM-OK" },
        { id: "agent-ops-02", pod: "Operations", vote: "YES", cert: "WORM-OK" },
        { id: "agent-ops-03", pod: "Operations", vote: "YES", cert: "WORM-OK" },
        { id: "agent-ops-04", pod: "Operations", vote: "YES", cert: "WORM-OK" }
      ];
      renderQuorumGrid(votes);
      document.getElementById('quorumStatusBadge').textContent = `QUORUM ACHIEVED (10/12 VOTES >= 2/3+1) • ${modeTag}`;
      document.getElementById('mValT2QuorumVotes').textContent = "10/12 (CERTIFIED & SEALED)";
      document.getElementById('mValT2QuorumVotes').style.color = "#059669";
      document.getElementById('statusBadgeT2').textContent = "TIER 2 QUORUM SEALED ✔";
      document.getElementById('statusBadgeT2').className = "service-status status-ok";
      document.getElementById('mCardTier2').classList.remove('active-propagating');
      document.getElementById('mCardTier2').classList.add('completed-tier');
      await wait(500);

      updateSwarmStepUI(6, "BOTTOM-UP TIER 0 -> TIER 1 -> TIER 2 ALL SYNCHRONIZED & COMMITTED (100%)");
      showToast('✅ Multi-Agent Swarm successfully propagated bottom-up across all 3 tiers!');
    }"""

m_html = m_html.replace(old_m_sim, new_m_sim)

with open('multi_agent_system_studio_app.html', 'w', encoding='utf-8') as f:
    f.write(m_html)
print("multi_agent_system_studio_app.html upgraded with Unified All-Tiers Matrix!")

# ========================================================
# 2. ENHANCE agent_kernel_studio_app.html
# ========================================================
with open('agent_kernel_studio_app.html', 'r', encoding='utf-8') as f:
    k_html = f.read()

# Add CSS for single agent kernel all-tiers view
k_css_add = """
    /* UNIFIED ALL-TIERS PROPAGATION MATRIX (SINGLE AGENT) */
    .unified-matrix-container {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .tier-stack-card {
      background: var(--bg-panel);
      border: 2px solid var(--border-subtle);
      border-radius: 12px;
      padding: 14px 18px;
      transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: var(--card-shadow);
      position: relative;
      overflow: hidden;
    }
    .tier-stack-card::before {
      content: "";
      position: absolute;
      top: 0; left: 0; bottom: 0;
      width: 5px;
      background: var(--border-subtle);
      transition: all 0.3s ease;
    }
    .tier-stack-card.tier-0-card::before { background: #059669; }
    .tier-stack-card.tier-1-card::before { background: #2563eb; }

    .tier-stack-card.active-propagating {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
    }
    .tier-stack-card.tier-0-card.active-propagating {
      border-color: #059669;
      background: #f0fdf4;
      box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.18);
    }
    .tier-stack-card.tier-1-card.active-propagating {
      border-color: #2563eb;
      background: #eff6ff;
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.18);
    }
    .tier-stack-card.completed-tier {
      border-color: #cbd5e1;
      opacity: 0.95;
    }

    .tier-head-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }
    .tier-title-badge {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 800;
      font-size: 0.88rem;
    }
    .pill-tier {
      font-size: 0.68rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      font-family: var(--font-mono);
    }
    .pill-t0 { background: #d1fae5; color: #065f46; border: 1px solid #a7f3d0; }
    .pill-t1 { background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }

    .tier-items-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 10px;
    }
    .tier-item-box {
      background: var(--bg-panel-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .tier-item-title {
      font-size: 0.76rem;
      font-weight: 800;
      color: var(--text-primary);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .tier-item-val {
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: var(--text-secondary);
      word-break: break-all;
    }
    .propagation-wire-row {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 2px 0;
      color: var(--text-muted);
      font-size: 0.72rem;
      font-weight: 700;
    }
    .wire-active {
      color: #2563eb;
      font-weight: 800;
    }
"""

if '.unified-matrix-container' not in k_html:
    k_html = k_html.replace('/* STAGE PANE (RIGHT) */', k_css_add + '\n    /* STAGE PANE (RIGHT) */')

# Add "Unified All-Tiers Matrix" tab button as default active tab
old_k_tabs = """      <div class="stage-tabs">
        <button class="tab-btn active" id="tabBtnExecutive" onclick="switchStage('executive')">👑 Executive &amp; Syscall Gate</button>"""

new_k_tabs = """      <div class="stage-tabs">
        <button class="tab-btn active" id="tabBtnAllTiers" onclick="switchStage('alltiers')">🌟 Unified All-Tiers Matrix</button>
        <button class="tab-btn" id="tabBtnExecutive" onclick="switchStage('executive')">👑 Executive &amp; Syscall Gate</button>"""

k_html = k_html.replace(old_k_tabs, new_k_tabs)

# Add Unified All-Tiers Content View in agent_kernel_studio_app.html
k_alltiers_content = """      <!-- TAB 0: UNIFIED ALL-TIERS PROPAGATION MATRIX -->
      <div class="stage-content" id="stageAllTiers" style="display: flex;">
        <div class="unified-matrix-container">

          <!-- TIER 0: AWS CLOUD PRIMITIVES -->
          <div class="tier-stack-card tier-0-card" id="kCardTier0">
            <div class="tier-head-row">
              <div class="tier-title-badge">
                <span class="pill-tier pill-t0">TIER 0</span>
                <span>Physical AWS Cloud Primitives (DynamoDB &bull; Bedrock &bull; S3 Vault)</span>
              </div>
              <span class="service-status status-ok" id="kStatusBadgeT0">HARDWARE READY</span>
            </div>
            <div class="tier-items-grid">
              <div class="tier-item-box" id="kBoxT0Mutex">
                <div class="tier-item-title"><span>🔒 DynamoDB Mutex</span><span id="kValT0MutexLock">ACQUIRED</span></div>
                <div class="tier-item-val" id="kValT0MutexKey">Key: agent-single-lock-404</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Atomic conditional put lease avoids state corruption.</div>
              </div>
              <div class="tier-item-box" id="kBoxT0Bedrock">
                <div class="tier-item-title"><span>🧠 Amazon Bedrock</span><span>Ring 3 Inference</span></div>
                <div class="tier-item-val" id="kValT0ModelStatus">Untrusted Proposal Generator</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Proposes structured JSON payloads without execution IAM.</div>
              </div>
              <div class="tier-item-box" id="kBoxT0Vault">
                <div class="tier-item-title"><span>📦 S3 WORM Vault</span><span>ObjectLock Active</span></div>
                <div class="tier-item-val" id="kValT0VaultHash">SHA-256: 3c8d19a04f21...</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Cryptographic Write-Once-Read-Many receipts.</div>
              </div>
            </div>
          </div>

          <!-- PROPAGATION WIRE -->
          <div class="propagation-wire-row" id="kWire0to1">
            <span>&uarr; Physical CAS mutex &amp; Bedrock proposals arbitrated by Agent OS Kernel &uarr;</span>
          </div>

          <!-- TIER 1: AGENT OS KERNEL -->
          <div class="tier-stack-card tier-1-card" id="kCardTier1">
            <div class="tier-head-row">
              <div class="tier-title-badge">
                <span class="pill-tier pill-t1">TIER 1</span>
                <span>Individual Agent OS Kernel (Prefrontal Ring 0 &amp; Multi-Store Memory)</span>
              </div>
              <span class="service-status status-proc" id="kStatusBadgeT1">KERNEL ONLINE</span>
            </div>
            <div class="tier-items-grid">
              <div class="tier-item-box" id="kBoxT1Gate">
                <div class="tier-item-title"><span>🛡️ Cedar Guardrail Gate</span><span id="kValT1Decision">READY</span></div>
                <div class="tier-item-val" id="kValT1Policy">Policy: Cedar::PermitAuditedOperation</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Prefrontal Ring 0 intercepts and evaluates untrusted proposals.</div>
              </div>
              <div class="tier-item-box" id="kBoxT1Pager">
                <div class="tier-item-title"><span>💾 Virtual Context Pager</span><span>O(1) Attention</span></div>
                <div class="tier-item-val" id="kValT1Tokens">Window: 2,700 / 8,192 Tok (Hot RAM)</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Evicts cold frames to S3 vault to preserve attention window.</div>
              </div>
              <div class="tier-item-box" id="kBoxT1Ledger">
                <div class="tier-item-title"><span>⛓️ Episodic Hash-Chain</span><span>Ledger Block #14</span></div>
                <div class="tier-item-val" id="kValT1LedgerHash">Block: 9e2c401f8a12...</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Append-only cryptographic receipt guaranteeing audit integrity.</div>
              </div>
            </div>
          </div>

        </div>
      </div>
"""

# Inject before stageExecutive
k_html = k_html.replace('<!-- TAB 1: EXECUTIVE & SYSCALL GATE -->', k_alltiers_content + '\n      <!-- TAB 1: EXECUTIVE & SYSCALL GATE -->')

# Update switchStage in agent_kernel_studio_app.html
old_k_switch = """    function switchStage(stage) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('stageExecutive').style.display = stage === 'executive' ? 'flex' : 'none';"""

new_k_switch = """    function switchStage(stage) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      const allTiersEl = document.getElementById('stageAllTiers');
      if (allTiersEl) allTiersEl.style.display = stage === 'alltiers' ? 'flex' : 'none';
      document.getElementById('stageExecutive').style.display = stage === 'executive' ? 'flex' : 'none';"""

k_html = k_html.replace(old_k_switch, new_k_switch)

old_k_switch_tabs = """      if (stage === 'executive') document.getElementById('tabBtnExecutive')?.classList.add('active');"""
new_k_switch_tabs = """      if (stage === 'alltiers') document.getElementById('tabBtnAllTiers')?.classList.add('active');
      if (stage === 'executive') document.getElementById('tabBtnExecutive')?.classList.add('active');"""

k_html = k_html.replace(old_k_switch_tabs, new_k_switch_tabs)

# Update runSteppedKernelSimulation in agent_kernel_studio_app.html so it stays on the unified tab and propagates live!
old_k_sim = """    async function runSteppedKernelSimulation(goalText, engineLabel) {
      const wait = (ms) => new Promise(res => setTimeout(res, ms));

      // Step 1: Ring 3 Untrusted Synthesis (Tier 0 Bedrock Model)
      updateKernelStepUI(1, "STAGE 1/4: RING 3 MODEL PROPOSAL SYNTHESIS");
      switchStage('executive');
      showToast('🧠 [Stage 1/4] Ring 3 Model proposing typed JSON syscall...');
      document.getElementById('executiveGateStatus').textContent = 'PROPOSAL SYNTHESIS IN PROGRESS...';
      document.getElementById('executiveGateStatus').style.background = '#fef3c7';
      document.getElementById('executiveGateStatus').style.color = '#b45309';
      await wait(700);

      // Step 2: Ring 0 Cedar Guardrail Check (Tier 1 Prefrontal Kernel Arbiter)
      updateKernelStepUI(2, "STAGE 2/4: RING 0 CEDAR GUARDRAIL ARBITRATION");
      showToast('🛡️ [Stage 2/4] Ring 0 Prefrontal Gate enforcing Cedar invariants...');
      document.getElementById('executiveGateStatus').textContent = 'EVALUATING CEDAR POLICY & MUTEX...';
      document.getElementById('executiveGateStatus').style.background = '#e0e7ff';
      document.getElementById('executiveGateStatus').style.color = '#3730a3';
      await wait(750);

      // Step 3: Context Pager Virtual Memory Compaction (Tier 1 Memory Suite)
      updateKernelStepUI(3, "STAGE 3/4: CONTEXT VIRTUALIZER RAM COMPACTION");
      switchStage('pager');
      showToast('💾 [Stage 3/4] Virtual Context Pager compacting attention window...');
      await wait(700);

      // Step 4: Cryptographic WORM Hash Chain (Tier 0 S3 Object Lock Vault)
      updateKernelStepUI(4, "STAGE 4/4: S3 WORM LEDGER HASH-CHAINING");
      switchStage('ledger');
      showToast('⛓️ [Stage 4/4] Sealing episodic state transition into S3 WORM Vault...');
      await wait(650);

      const mockResult = {
        action: "ExecuteBoundedSyscall",
        resource: "arn:aws:s3:::agent-worm-ledger-prod",
        policy: "Cedar::EnforceAuditTrailStrict",
        decision: "ALLOW",
        hash: Array.from({length: 16}, () => Math.floor(Math.random()*16).toString(16)).join(''),
        tokens: 3150,
        reason: "Ring 0 gatekeeper verified immutable audit trail and zero unauthorized mutations."
      };

      applyKernelExecutionResult(mockResult, engineLabel);
      updateKernelStepUI(5, "ALL 4 TIERS COMMITTED & SEALED (100%)");
      switchStage('executive');
      showToast('✅ Multi-Tier Agent Kernel verified and committed (' + engineLabel + ')!');
    }"""

new_k_sim = """    async function runSteppedKernelSimulation(goalText, engineLabel) {
      const wait = (ms) => new Promise(res => setTimeout(res, ms));

      // Stay on the Unified All-Tiers Matrix view to show propagation live!
      switchStage('alltiers');

      // Reset card states
      ['kCardTier0', 'kCardTier1'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.remove('active-propagating', 'completed-tier');
      });
      document.getElementById('kWire0to1')?.classList.remove('wire-active');

      // ----------------------------------------------------
      // STEP 1: Tier 0 Physical AWS Hardware Mutex & Storage
      // ----------------------------------------------------
      updateKernelStepUI(1, "STAGE 1/4: [TIER 0] DYNAMODB CAS MUTEX & S3 VAULT INIT");
      document.getElementById('kCardTier0').classList.add('active-propagating');
      document.getElementById('kStatusBadgeT0').textContent = "CAS LOCKING...";
      document.getElementById('kStatusBadgeT0').className = "service-status status-proc";
      document.getElementById('kValT0MutexLock').textContent = "LOCKING (CAS)...";
      document.getElementById('kValT0MutexLock').style.color = "#d97706";
      showToast('🔒 [Stage 1/4: Tier 0 AWS] Acquiring DynamoDB conditional mutex lease...');
      await wait(700);

      document.getElementById('kValT0MutexLock').textContent = "LOCKED (EXCLUSIVE)";
      document.getElementById('kValT0MutexLock').style.color = "#059669";

      // ----------------------------------------------------
      // STEP 2: Tier 0 Amazon Bedrock Ring 3 Model Synthesis
      // ----------------------------------------------------
      updateKernelStepUI(2, "STAGE 2/4: [TIER 0] BEDROCK PROPOSAL GENERATION (RING 3)");
      document.getElementById('kValT0ModelStatus').textContent = "PROPOSAL SYNTHESIS...";
      document.getElementById('kValT0ModelStatus').style.color = "#2563eb";
      showToast('🧠 [Stage 2/4: Tier 0 Bedrock] Model proposing typed JSON syscall payload...');
      await wait(750);

      document.getElementById('kValT0ModelStatus').textContent = "PROPOSAL EMITTED (RING 3)";
      document.getElementById('kStatusBadgeT0').textContent = "TIER 0 PASS ✔";
      document.getElementById('kStatusBadgeT0').className = "service-status status-ok";
      document.getElementById('kCardTier0').classList.remove('active-propagating');
      document.getElementById('kCardTier0').classList.add('completed-tier');

      // Propagate wire 0 -> 1
      document.getElementById('kWire0to1').classList.add('wire-active');
      await wait(350);

      // ----------------------------------------------------
      // STEP 3: Tier 1 Ring 0 Cedar Guardrail Arbitration & Attention Paging
      // ----------------------------------------------------
      updateKernelStepUI(3, "STAGE 3/4: [TIER 1] RING 0 CEDAR ARBITER & CONTEXT PAGER");
      document.getElementById('kCardTier1').classList.add('active-propagating');
      document.getElementById('kStatusBadgeT1').textContent = "EVALUATING CEDAR...";
      document.getElementById('kStatusBadgeT1').className = "service-status status-proc";
      document.getElementById('kValT1Decision').textContent = "EVALUATING...";
      document.getElementById('kValT1Decision').style.color = "#d97706";
      showToast('🛡️ [Stage 3/4: Tier 1 Kernel] Ring 0 Prefrontal Gate enforcing Cedar invariants...');
      await wait(700);

      document.getElementById('kValT1Decision').textContent = "ALLOW (RING 0 PASS)";
      document.getElementById('kValT1Decision').style.color = "#059669";
      document.getElementById('kValT1Tokens').textContent = "Compacted to 2,450 Tokens (Cold Frames paged to S3)";

      // ----------------------------------------------------
      // STEP 4: Tier 0 S3 WORM Vault Hash Seal
      // ----------------------------------------------------
      updateKernelStepUI(4, "STAGE 4/4: [TIER 0] CRYPTOGRAPHIC WORM HASH STAMP");
      showToast('⛓️ [Stage 4/4: Tier 0 S3 Vault] Sealing episodic state transition into S3 WORM Vault...');
      const newHash = Array.from({length: 16}, () => Math.floor(Math.random()*16).toString(16)).join('');
      document.getElementById('kValT1LedgerHash').textContent = "Block: " + newHash + "...";
      document.getElementById('kValT0VaultHash').textContent = "WORM Receipt: " + newHash + " (SHA-256)";
      document.getElementById('kStatusBadgeT1').textContent = "TIER 1 COMMITTED ✔";
      document.getElementById('kStatusBadgeT1').className = "service-status status-ok";
      document.getElementById('kCardTier1').classList.remove('active-propagating');
      document.getElementById('kCardTier1').classList.add('completed-tier');
      await wait(600);

      const mockResult = {
        action: "ExecuteBoundedSyscall",
        resource: "arn:aws:s3:::agent-worm-ledger-prod",
        policy: "Cedar::EnforceAuditTrailStrict",
        decision: "ALLOW",
        hash: newHash,
        tokens: 3150,
        reason: "Ring 0 gatekeeper verified immutable audit trail and zero unauthorized mutations."
      };

      applyKernelExecutionResult(mockResult, engineLabel);
      updateKernelStepUI(5, "TIER 0 & TIER 1 FULLY SYNCHRONIZED & COMMITTED (100%)");
      showToast('✅ Multi-Tier Agent Kernel verified and committed (' + engineLabel + ')!');
    }"""

k_html = k_html.replace(old_k_sim, new_k_sim)

with open('agent_kernel_studio_app.html', 'w', encoding='utf-8') as f:
    f.write(k_html)
print("agent_kernel_studio_app.html upgraded with Unified All-Tiers Matrix!")
