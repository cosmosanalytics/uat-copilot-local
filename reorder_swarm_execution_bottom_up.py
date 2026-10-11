# -*- coding: utf-8 -*-
"""
reorder_swarm_execution_bottom_up.py
Reorders the Multi-Agent Swarm progression in multi_agent_system_studio_app.html so that execution strictly starts from Tier 0 (AWS Cloud Foundation), proceeds through Tier 1 (Agent OS Kernel), and finishes at Tier 2 (Multi-Agent Swarm Governance):

Step 1: Tier 0 AWS Hardware Mutex & Vault Init
        (DynamoDB CAS Lock + S3 WORM Anchor initialization)
Step 2: Tier 0 Bedrock Foundation Model Proposal
        (Ring 3 LLM Proposal Synthesis across pods)
Step 3: Tier 1 Agent Kernel Ring 0 Cedar Arbiter
        (Cedar Guardrail Gatekeeper + Context Memory Pager)
Step 4: Tier 2 Watts-Strogatz Inter-Pod Liaison Routing
        (EventBridge Liaison Bridges + O(N) Whiteboard Commit)
Step 5: Tier 2 Byzantine Supermajority Quorum Seal
        (2/3 + 1 supermajority vote sealed into S3 WORM Compliance Vault)
"""

with open('multi_agent_system_studio_app.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Stepper Header and 5-Step Track HTML
old_stepper_track = """        <div class="stepper-track">
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
        </div>"""

new_stepper_track = """        <div class="stepper-track" style="grid-template-columns: repeat(5, 1fr);">
          <div class="step-item" id="mStep1">
            <div class="step-num">1</div>
            <div class="step-text">
              <span class="step-label">Cloud Mutex &amp; Vault</span>
              <span class="step-tier">Tier 0 Physical AWS</span>
            </div>
          </div>
          <div class="step-item" id="mStep2">
            <div class="step-num">2</div>
            <div class="step-text">
              <span class="step-label">Model Reasoning</span>
              <span class="step-tier">Tier 0 Bedrock (Ring 3)</span>
            </div>
          </div>
          <div class="step-item" id="mStep3">
            <div class="step-num">3</div>
            <div class="step-text">
              <span class="step-label">Prefrontal Kernel Gate</span>
              <span class="step-tier">Tier 1 Kernel OS (Ring 0)</span>
            </div>
          </div>
          <div class="step-item" id="mStep4">
            <div class="step-num">4</div>
            <div class="step-text">
              <span class="step-label">Liaison &amp; Whiteboard</span>
              <span class="step-tier">Tier 2 Swarm Lattice</span>
            </div>
          </div>
          <div class="step-item" id="mStep5">
            <div class="step-num">5</div>
            <div class="step-text">
              <span class="step-label">Byzantine Quorum</span>
              <span class="step-tier">Tier 2 Consensus (&ge;2/3+1)</span>
            </div>
          </div>
        </div>"""

html = html.replace(old_stepper_track, new_stepper_track)

# Update subtitle to reflect Bottom-Up progression
html = html.replace(
    '&bull; Hierarchical Watts-Strogatz &rarr; Kernel Ring 0 &rarr; Byzantine Quorum',
    '&bull; Grounded Bottom-Up Execution: Tier 0 AWS Hardware &rarr; Tier 1 Kernel OS &rarr; Tier 2 Swarm Governance'
)

# 2. Update updateSwarmStepUI and runSteppedSimulation logic
old_swarm_logic = """    function updateSwarmStepUI(activeStepNum, statusText) {
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

new_swarm_logic = """    function updateSwarmStepUI(activeStepNum, statusText) {
      document.getElementById('swarmStepperStatus').textContent = statusText;
      for (let i = 1; i <= 5; i++) {
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

html = html.replace(old_swarm_logic, new_swarm_logic)

with open('multi_agent_system_studio_app.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Successfully updated multi_agent_system_studio_app.html with Bottom-Up execution starting from Tier 0!")
