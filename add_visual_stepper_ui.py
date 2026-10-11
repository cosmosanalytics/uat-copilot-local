# -*- coding: utf-8 -*-
"""
add_visual_stepper_ui.py
Enhances agent_kernel_studio_app.html and multi_agent_system_studio_app.html with:
1. Prominent interactive Multi-Tier Stepped Progression Bar UI at the top of the main stage pane in both apps.
2. Animated pulse bars, active step glow, checkmarks, tier tags (Tier 0 Cloud Hardware, Tier 1 Kernel OS, Tier 2 Swarm Lattice).
3. Auto-switching / highlighting corresponding tabs and panels as each tier step executes.
4. Clean Light Mode styling with smooth transitions, progress meters, and status messages.
"""

# ========================================================
# 1. UPGRADE SINGLE AGENT KERNEL STUDIO (agent_kernel_studio_app.html)
# ========================================================
with open('agent_kernel_studio_app.html', 'r', encoding='utf-8') as f:
    k_html = f.read()

# Stepper CSS for Single Agent
k_stepper_css = """
    /* MULTI-TIER STEPPER PROGRESSION COMPONENT */
    .stepper-container {
      background: var(--bg-panel);
      border-bottom: 1.5px solid var(--border-subtle);
      padding: 12px 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .stepper-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.76rem;
    }
    .stepper-title {
      font-weight: 800;
      color: var(--text-primary);
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .stepper-status {
      font-family: var(--font-mono);
      font-weight: 700;
      font-size: 0.72rem;
      color: var(--accent-blue);
    }
    .stepper-track {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      position: relative;
    }
    .step-item {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 10px;
      border-radius: 8px;
      border: 1.5px solid var(--border-subtle);
      background: var(--bg-panel-subtle);
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .step-num {
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: #e2e8f0;
      color: #64748b;
      font-size: 0.70rem;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      transition: all 0.25s ease;
    }
    .step-text {
      display: flex;
      flex-direction: column;
      line-height: 1.2;
      overflow: hidden;
    }
    .step-label {
      font-size: 0.74rem;
      font-weight: 800;
      color: var(--text-primary);
      white-space: nowrap;
      text-overflow: ellipsis;
      overflow: hidden;
    }
    .step-tier {
      font-size: 0.65rem;
      font-weight: 700;
      color: var(--text-muted);
    }
    /* Active & Completed States */
    .step-item.active {
      border-color: #2563eb;
      background: #eff6ff;
      box-shadow: 0 0 0 2px rgba(37,99,235,0.15);
      transform: translateY(-1px);
    }
    .step-item.active .step-num {
      background: #2563eb;
      color: #ffffff;
      animation: pulseStep 1.2s infinite ease-in-out;
    }
    .step-item.active .step-tier {
      color: #1d4ed8;
      font-weight: 800;
    }
    .step-item.completed {
      border-color: #10b981;
      background: #f0fdf4;
    }
    .step-item.completed .step-num {
      background: #10b981;
      color: #ffffff;
    }
    .step-item.completed .step-tier {
      color: #047857;
    }
    @keyframes pulseStep {
      0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(37,99,235,0.4); }
      50% { transform: scale(1.1); box-shadow: 0 0 0 6px rgba(37,99,235,0); }
    }
"""

if '.stepper-container' not in k_html:
    k_html = k_html.replace('/* STAGE PANE (RIGHT) */', k_stepper_css + '\n    /* STAGE PANE (RIGHT) */')

# Stepper HTML markup placed right above .stage-tabs in agent_kernel_studio_app.html
k_stepper_html = """      <!-- MULTI-TIER STEPPED PROGRESSION TRACKER -->
      <div class="stepper-container" id="kernelStepperContainer">
        <div class="stepper-header">
          <div class="stepper-title">
            <span>⚡ Multi-Tier Kernel Progression</span>
            <span style="font-size: 0.68rem; font-weight: 600; color: var(--text-muted);">&bull; Hierarchical Ring 3 &rarr; Ring 0 &rarr; S3 Vault Pipeline</span>
          </div>
          <div class="stepper-status" id="kernelStepperStatus">READY &bull; IDLE</div>
        </div>
        <div class="stepper-track">
          <div class="step-item" id="kStep1">
            <div class="step-num">1</div>
            <div class="step-text">
              <span class="step-label">Ring 3 Synthesis</span>
              <span class="step-tier">Tier 0 Model (Bedrock)</span>
            </div>
          </div>
          <div class="step-item" id="kStep2">
            <div class="step-num">2</div>
            <div class="step-text">
              <span class="step-label">Ring 0 Cedar Gate</span>
              <span class="step-tier">Tier 1 Kernel Arbiter</span>
            </div>
          </div>
          <div class="step-item" id="kStep3">
            <div class="step-num">3</div>
            <div class="step-text">
              <span class="step-label">Context Virtualizer</span>
              <span class="step-tier">Tier 1 Memory Pager</span>
            </div>
          </div>
          <div class="step-item" id="kStep4">
            <div class="step-num">4</div>
            <div class="step-text">
              <span class="step-label">Episodic WORM Seal</span>
              <span class="step-tier">Tier 0 Physical Vault (S3)</span>
            </div>
          </div>
        </div>
      </div>
"""

if 'id="kernelStepperContainer"' not in k_html:
    k_html = k_html.replace('<div class="stage-tabs">', k_stepper_html + '      <div class="stage-tabs">', 1)

# Stepper Javascript Logic
old_k_simulation = """    async function runSteppedKernelSimulation(goalText, engineLabel) {
      const wait = (ms) => new Promise(res => setTimeout(res, ms));

      // Tier 1 - Stage 1: Ring 3 Synthesis
      showToast('🧠 [Stage 1/4] Ring 3 Model synthesizing typed JSON proposal...');
      document.getElementById('executiveGateStatus').textContent = 'SYNTHESIZING PROPOSAL...';
      document.getElementById('executiveGateStatus').style.background = '#fef3c7';
      document.getElementById('executiveGateStatus').style.color = '#b45309';
      await wait(600);

      // Tier 1 - Stage 2: Ring 0 Cedar Guardrail Check
      showToast('🛡️ [Stage 2/4] Ring 0 Prefrontal Gate enforcing Cedar invariants...');
      document.getElementById('executiveGateStatus').textContent = 'EVALUATING CEDAR POLICY...';
      await wait(650);

      // Tier 1 - Stage 3: Virtual Context Paging
      showToast('💾 [Stage 3/4] Virtual Context Pager compacting attention window...');
      await wait(600);

      // Tier 1 - Stage 4: Cryptographic WORM Hash Chain
      showToast('⛓️ [Stage 4/4] Sealing episodic state transition into S3 WORM Vault...');
      await wait(550);

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
      showToast('✅ Multi-Tier Agent Kernel verified and committed (' + engineLabel + ')!');
    }"""

new_k_simulation = """    function updateKernelStepUI(activeStepNum, statusText) {
      document.getElementById('kernelStepperStatus').textContent = statusText;
      for (let i = 1; i <= 4; i++) {
        const el = document.getElementById('kStep' + i);
        if (!el) continue;
        el.classList.remove('active', 'completed');
        if (i < activeStepNum) {
          el.classList.add('completed');
          el.querySelector('.step-num').textContent = '✓';
        } else if (i === activeStepNum) {
          el.classList.add('active');
          el.querySelector('.step-num').textContent = i;
        } else {
          el.querySelector('.step-num').textContent = i;
        }
      }
    }

    async function runSteppedKernelSimulation(goalText, engineLabel) {
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

k_html = k_html.replace(old_k_simulation, new_k_simulation)

with open('agent_kernel_studio_app.html', 'w', encoding='utf-8') as f:
    f.write(k_html)
print("Updated agent_kernel_studio_app.html with interactive multi-tier stepper!")

# ========================================================
# 2. UPGRADE MULTI-AGENT SWARM STUDIO (multi_agent_system_studio_app.html)
# ========================================================
with open('multi_agent_system_studio_app.html', 'r', encoding='utf-8') as f:
    m_html = f.read()

# Stepper CSS for Multi-Agent Swarm
m_stepper_css = """
    /* MULTI-TIER STEPPER PROGRESSION COMPONENT (SWARM) */
    .stepper-container {
      background: var(--bg-panel);
      border-bottom: 1.5px solid var(--border-subtle);
      padding: 12px 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .stepper-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.76rem;
    }
    .stepper-title {
      font-weight: 800;
      color: var(--text-primary);
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .stepper-status {
      font-family: var(--font-mono);
      font-weight: 700;
      font-size: 0.72rem;
      color: var(--accent-purple);
    }
    .stepper-track {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      position: relative;
    }
    .step-item {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 10px;
      border-radius: 8px;
      border: 1.5px solid var(--border-subtle);
      background: var(--bg-panel-subtle);
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .step-num {
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: #e2e8f0;
      color: #64748b;
      font-size: 0.70rem;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      transition: all 0.25s ease;
    }
    .step-text {
      display: flex;
      flex-direction: column;
      line-height: 1.2;
      overflow: hidden;
    }
    .step-label {
      font-size: 0.74rem;
      font-weight: 800;
      color: var(--text-primary);
      white-space: nowrap;
      text-overflow: ellipsis;
      overflow: hidden;
    }
    .step-tier {
      font-size: 0.65rem;
      font-weight: 700;
      color: var(--text-muted);
    }
    /* Active & Completed States */
    .step-item.active {
      border-color: #7c3aed;
      background: #faf5ff;
      box-shadow: 0 0 0 2px rgba(124,58,237,0.18);
      transform: translateY(-1px);
    }
    .step-item.active .step-num {
      background: #7c3aed;
      color: #ffffff;
      animation: pulseSwarmStep 1.2s infinite ease-in-out;
    }
    .step-item.active .step-tier {
      color: #6d28d9;
      font-weight: 800;
    }
    .step-item.completed {
      border-color: #10b981;
      background: #f0fdf4;
    }
    .step-item.completed .step-num {
      background: #10b981;
      color: #ffffff;
    }
    .step-item.completed .step-tier {
      color: #047857;
    }
    @keyframes pulseSwarmStep {
      0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(124,58,237,0.4); }
      50% { transform: scale(1.1); box-shadow: 0 0 0 6px rgba(124,58,237,0); }
    }
"""

if '.stepper-container' not in m_html:
    m_html = m_html.replace('/* STAGE PANE (RIGHT) */', m_stepper_css + '\n    /* STAGE PANE (RIGHT) */')

# Stepper HTML markup placed right above .stage-tabs in multi_agent_system_studio_app.html
m_stepper_html = """      <!-- MULTI-TIER STEPPED PROGRESSION TRACKER (SWARM) -->
      <div class="stepper-container" id="swarmStepperContainer">
        <div class="stepper-header">
          <div class="stepper-title">
            <span>⚡ Multi-Tier Swarm Progression</span>
            <span style="font-size: 0.68rem; font-weight: 600; color: var(--text-muted);">&bull; Hierarchical Watts-Strogatz &rarr; Kernel Ring 0 &rarr; Byzantine Quorum</span>
          </div>
          <div class="stepper-status" id="swarmStepperStatus">READY &bull; IDLE</div>
        </div>
        <div class="stepper-track">
          <div class="step-item" id="mStep1">
            <div class="step-num">1</div>
            <div class="step-text">
              <span class="step-label">Liaison Shortcut Routing</span>
              <span class="step-tier">Tier 2 Swarm Lattice</span>
            </div>
          </div>
          <div class="step-item" id="mStep2">
            <div class="step-num">2</div>
            <div class="step-text">
              <span class="step-label">Pod Deliberation</span>
              <span class="step-tier">Tier 1 Kernel Ring 0</span>
            </div>
          </div>
          <div class="step-item" id="mStep3">
            <div class="step-num">3</div>
            <div class="step-text">
              <span class="step-label">O(N) Whiteboard Commit</span>
              <span class="step-tier">Tier 0 DynamoDB CAS</span>
            </div>
          </div>
          <div class="step-item" id="mStep4">
            <div class="step-num">4</div>
            <div class="step-text">
              <span class="step-label">Byzantine Quorum Vote</span>
              <span class="step-tier">Tier 0 S3 WORM Vault</span>
            </div>
          </div>
        </div>
      </div>
"""

if 'id="swarmStepperContainer"' not in m_html:
    m_html = m_html.replace('<div class="stage-tabs">', m_stepper_html + '      <div class="stage-tabs">', 1)

# Stepper Javascript Logic in multi_agent_system_studio_app.html
old_m_simulation = """    async function runSteppedSimulation(goalText, modeTag) {
      showToast('⚡ [Stage 1/4] Inter-Pod Routing: Liaisons bridging EventBridge...');
      animateLiaisonPackets(1200);
      await new Promise(r => setTimeout(r, 650));

      showToast('🧠 [Stage 2/4] Specialist Pods Deliberating in Ring 0 MicroVMs...');
      await new Promise(r => setTimeout(r, 650));

      showToast('📋 [Stage 3/4] Publishing Linear O(N) Shared Whiteboard Lanes...');
      const customWb = [
        { author: "agent-fin-01 (Finance Liaison)", text: "Acquired DynamoDB CAS mutex. Liquidity allocated for: " + goalText.slice(0, 70) + "..." },
        { author: "agent-comp-01 (Compliance Liaison)", text: "Cedar guardrails verified. Grounding certified across S3 WORM & Neptune graph." },
        { author: "agent-ops-01 (Operations Liaison)", text: "Step Functions state machine initiated. Isolated microVM compute committed." }
      ];
      renderWhiteboardLanes(customWb);
      await new Promise(r => setTimeout(r, 650));

      showToast('⚖️ [Stage 4/4] Gathering Byzantine 2/3 + 1 Quorum Ballots...');
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
      await new Promise(r => setTimeout(r, 500));

      showToast('✅ Multi-Agent Consensus Sealed in S3 WORM Vault!');
    }"""

new_m_simulation = """    function updateSwarmStepUI(activeStepNum, statusText) {
      document.getElementById('swarmStepperStatus').textContent = statusText;
      for (let i = 1; i <= 4; i++) {
        const el = document.getElementById('mStep' + i);
        if (!el) continue;
        el.classList.remove('active', 'completed');
        if (i < activeStepNum) {
          el.classList.add('completed');
          el.querySelector('.step-num').textContent = '✓';
        } else if (i === activeStepNum) {
          el.classList.add('active');
          el.querySelector('.step-num').textContent = i;
        } else {
          el.querySelector('.step-num').textContent = i;
        }
      }
    }

    async function runSteppedSimulation(goalText, modeTag) {
      const wait = (ms) => new Promise(res => setTimeout(res, ms));

      // Stage 1: Inter-Pod Shortcut Routing (Tier 2 Swarm Watts-Strogatz Lattice)
      updateSwarmStepUI(1, "STAGE 1/4: INTER-POD SHORTCUT ROUTING (TIER 2)");
      switchStage('topology');
      showToast('⚡ [Stage 1/4] Inter-Pod Routing: Liaisons bridging EventBridge...');
      animateLiaisonPackets(1800);
      await wait(800);

      // Stage 2: Specialist Pod Deliberation (Tier 1 Individual Agent OS Kernel)
      updateSwarmStepUI(2, "STAGE 2/4: POD KERNEL RING 0 DELIBERATION (TIER 1)");
      showToast('🧠 [Stage 2/4] Specialist Pods Deliberating in Ring 0 MicroVMs...');
      await wait(750);

      // Stage 3: Publishing O(N) Shared Whiteboard (Tier 0 DynamoDB CAS Mutex)
      updateSwarmStepUI(3, "STAGE 3/4: ATOMIC O(N) WHITEBOARD COMMIT (TIER 0)");
      switchStage('whiteboard');
      showToast('📋 [Stage 3/4] Publishing Linear O(N) Shared Whiteboard Lanes...');
      const customWb = [
        { author: "agent-fin-01 (Finance Liaison)", text: "Acquired DynamoDB CAS mutex. Liquidity allocated for: " + goalText.slice(0, 70) + "..." },
        { author: "agent-comp-01 (Compliance Liaison)", text: "Cedar guardrails verified. Grounding certified across S3 WORM & Neptune graph." },
        { author: "agent-ops-01 (Operations Liaison)", text: "Step Functions state machine initiated. Isolated microVM compute committed." }
      ];
      renderWhiteboardLanes(customWb);
      await wait(800);

      // Stage 4: Byzantine Quorum Ballots Sealed (Tier 0 S3 WORM Compliance Vault)
      updateSwarmStepUI(4, "STAGE 4/4: BYZANTINE 2/3+1 QUORUM SEAL (TIER 0)");
      switchStage('quorum');
      showToast('⚖️ [Stage 4/4] Gathering Byzantine 2/3 + 1 Quorum Ballots...');
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

      updateSwarmStepUI(5, "ALL 3 ARCHITECTURAL TIERS CONVERGED & SEALED (100%)");
      showToast('✅ Multi-Agent Consensus Sealed in S3 WORM Vault!');
    }"""

m_html = m_html.replace(old_m_simulation, new_m_simulation)

with open('multi_agent_system_studio_app.html', 'w', encoding='utf-8') as f:
    f.write(m_html)
print("Updated multi_agent_system_studio_app.html with interactive multi-tier stepper!")
