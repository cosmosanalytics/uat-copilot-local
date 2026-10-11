# -*- coding: utf-8 -*-
"""
fix_aws_basics_card_animation_and_stepper_grid.py
Fixes:
1. Stepper layout in aws_basics_studio_app.html:
   - Sets display: grid with grid-template-columns: repeat(5, 1fr) explicitly inline so items never stack vertically!
2. Active Card Highlighting & Animation under "AWS Infrastructure Grid":
   - Gives each card in #archGridContainer a unique ID:
     * card-bedrock
     * card-agentcore
     * card-s3vault
     * card-dynamodb
     * card-lambda
     * card-stepfunctions
   - Adds vibrant CSS glowing pulse animation (.card-active-pulse, .card-completed) with ring color, translateY(-3px), and box shadow.
   - During runSteppedAwsSimulation, sequentially highlights and pulses each respective service card as the step executes:
     * Step 1: Pulses DynamoDB Locks card (orange pulse #ea580c)
     * Step 2: Pulses AgentCore Policy & Bedrock cards (blue/green pulse)
     * Step 3: Pulses Neptune & Vector DB / Step Functions card
     * Step 4: Pulses AWS Lambda microVM card
     * Step 5: Pulses S3 Receipt Vault card
   - Dynamically updates the badges on the cards (e.g., "LOCKING (CAS)..." -> "LOCKED", "EVALUATING..." -> "PASS", etc.)
"""

with open('aws_basics_studio_app.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS for .stepper-track and .service-card animations
old_stepper_css = """.stepper-track {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 10px;
      position: relative;
    }"""

new_stepper_css = """.stepper-track {
      display: grid !important;
      grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
      gap: 10px;
      position: relative;
      width: 100%;
    }
    @media (max-width: 900px) {
      .stepper-track {
        grid-template-columns: repeat(2, 1fr) !important;
      }
    }

    /* CARD PULSE ANIMATION UNDER INFRASTRUCTURE GRID */
    .service-card {
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .service-card.card-active-pulse {
      border-color: #ea580c !important;
      background: #fff7ed !important;
      transform: translateY(-4px) scale(1.02);
      box-shadow: 0 10px 25px -5px rgba(234, 88, 12, 0.25), 0 0 0 3px rgba(234, 88, 12, 0.3) !important;
      z-index: 5;
    }
    .service-card.card-completed {
      border-color: #10b981 !important;
      background: #f0fdf4 !important;
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.12);
    }
    .service-card.card-completed .service-status {
      background: #d1fae5;
      color: #065f46;
    }
"""

html = html.replace(old_stepper_css, new_stepper_css)

# Ensure stepper-track has inline style fallback so it never stacks
html = html.replace(
    '<div class="stepper-track">',
    '<div class="stepper-track" style="display:grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap:10px; width:100%;">'
)

# 2. Update renderServiceGrid to give each card a unique ID and clean status spans
old_render_grid = """    function renderServiceGrid(p) {
      const container = document.getElementById('archGridContainer');
      container.innerHTML = `
        <div class="service-card active">
          <div class="service-card-head">
            <span class="service-title">🧠 Amazon Bedrock</span>
            <span class="service-status status-proc">INFERENCE</span>
          </div>
          <div style="font-size: 0.76rem; color: var(--text-secondary);">Proposes action schemas without execution authority.</div>
          <div class="service-metric-row">
            <span>Model: Claude 3.5 Sonnet / Llama 3.3</span>
            <span>Latency: 142ms</span>
          </div>
        </div>

        <div class="service-card active">
          <div class="service-card-head">
            <span class="service-title">🛡️ AgentCore Policy</span>
            <span class="service-status status-ok">RING 0 PASS</span>
          </div>
          <div style="font-size: 0.76rem; color: var(--text-secondary);">Validates syscall arguments against Cedar guardrail rules.</div>
          <div class="service-metric-row">
            <span>Policy: LockEnforced &bull; NoDelete</span>
            <span>Violations: 0</span>
          </div>
        </div>

        <div class="service-card active">
          <div class="service-card-head">
            <span class="service-title">📦 S3 Receipt Vault</span>
            <span class="service-status status-ok">WORM COMPLIANT</span>
          </div>
          <div style="font-size: 0.76rem; color: var(--text-secondary);">Immutable storage with SHA-256 cryptographically signed receipts.</div>
          <div class="service-metric-row">
            <span>Bucket: s3://grounding-vault-prod</span>
            <span>Checksum: SHA-256</span>
          </div>
        </div>

        <div class="service-card active">
          <div class="service-card-head">
            <span class="service-title">🗄️ DynamoDB Locks</span>
            <span class="service-status status-lock">MUTEX ACQUIRED</span>
          </div>
          <div style="font-size: 0.76rem; color: var(--text-secondary);">Distributed mutex leasing preventing two-agent race conditions.</div>
          <div class="service-metric-row">
            <span>Key: ${p.lockKey}</span>
            <span>Lease: 15.0s</span>
          </div>
        </div>

        <div class="service-card active">
          <div class="service-card-head">
            <span class="service-title">⚡ AWS Lambda</span>
            <span class="service-status status-ok">ISOLATED VM</span>
          </div>
          <div style="font-size: 0.76rem; color: var(--text-secondary);">Ephemeral Firecracker microVM executing tool calculations.</div>
          <div class="service-metric-row">
            <span>Handler: ${p.lambdaFn}</span>
            <span>Mem: 512MB</span>
          </div>
        </div>

        <div class="service-card active">
          <div class="service-card-head">
            <span class="service-title">🔄 Step Functions</span>
            <span class="service-status status-proc">STEP 3/5 ACTIVE</span>
          </div>
          <div style="font-size: 0.76rem; color: var(--text-secondary);">Deterministic HFSM state transitions and automated rollbacks.</div>
          <div class="service-metric-row">
            <span>Execution: arn:aws:states:123456</span>
            <span>Retries: 0</span>
          </div>
        </div>
      `;
    }"""

new_render_grid = """    function renderServiceGrid(p) {
      const container = document.getElementById('archGridContainer');
      container.innerHTML = `
        <div class="service-card" id="cardBedrock">
          <div class="service-card-head">
            <span class="service-title">🧠 Amazon Bedrock</span>
            <span class="service-status status-proc" id="cardBadgeBedrock">INFERENCE</span>
          </div>
          <div style="font-size: 0.76rem; color: var(--text-secondary);">Proposes action schemas without execution authority.</div>
          <div class="service-metric-row">
            <span>Model: Claude 3.5 / Llama 3.3</span>
            <span>Untrusted Ring 3</span>
          </div>
        </div>

        <div class="service-card" id="cardAgentCore">
          <div class="service-card-head">
            <span class="service-title">🛡️ AgentCore Policy</span>
            <span class="service-status status-ok" id="cardBadgeAgentCore">RING 0 PASS</span>
          </div>
          <div style="font-size: 0.76rem; color: var(--text-secondary);">Validates syscall arguments against Cedar guardrail rules.</div>
          <div class="service-metric-row">
            <span>Policy: LockEnforced &bull; NoDelete</span>
            <span>Violations: 0</span>
          </div>
        </div>

        <div class="service-card" id="cardS3Vault">
          <div class="service-card-head">
            <span class="service-title">📦 S3 Receipt Vault</span>
            <span class="service-status status-ok" id="cardBadgeS3Vault">WORM COMPLIANT</span>
          </div>
          <div style="font-size: 0.76rem; color: var(--text-secondary);">Immutable storage with SHA-256 cryptographically signed receipts.</div>
          <div class="service-metric-row">
            <span>Bucket: s3://grounding-vault-prod</span>
            <span id="cardHashS3">Checksum: SHA-256</span>
          </div>
        </div>

        <div class="service-card" id="cardDynamoDB">
          <div class="service-card-head">
            <span class="service-title">🗄️ DynamoDB Locks</span>
            <span class="service-status status-lock" id="cardBadgeDynamoDB">MUTEX ACQUIRED</span>
          </div>
          <div style="font-size: 0.76rem; color: var(--text-secondary);">Distributed mutex leasing preventing two-agent race conditions.</div>
          <div class="service-metric-row">
            <span id="cardLockKey">Key: ${p.lockKey}</span>
            <span>Lease: 15.0s</span>
          </div>
        </div>

        <div class="service-card" id="cardLambda">
          <div class="service-card-head">
            <span class="service-title">⚡ AWS Lambda</span>
            <span class="service-status status-ok" id="cardBadgeLambda">ISOLATED VM</span>
          </div>
          <div style="font-size: 0.76rem; color: var(--text-secondary);">Ephemeral Firecracker microVM executing tool calculations.</div>
          <div class="service-metric-row">
            <span>Handler: ${p.lambdaFn}</span>
            <span>Mem: 512MB</span>
          </div>
        </div>

        <div class="service-card" id="cardStepFunctions">
          <div class="service-card-head">
            <span class="service-title">🔄 Step Functions</span>
            <span class="service-status status-proc" id="cardBadgeStepFunctions">HFSM COMPLETED</span>
          </div>
          <div style="font-size: 0.76rem; color: var(--text-secondary);">Deterministic HFSM state transitions and automated rollbacks.</div>
          <div class="service-metric-row">
            <span>Execution: arn:aws:states:123456</span>
            <span>Retries: 0</span>
          </div>
        </div>
      `;
    }"""

html = html.replace(old_render_grid, new_render_grid)

# 3. Animate the Cards in runSteppedAwsSimulation
old_stepped_sim = """    async function runSteppedAwsSimulation(text, engineLabel) {
      const wait = (ms) => new Promise(res => setTimeout(res, ms));
      const lockKey = "job-" + Math.floor(1000 + Math.random()*9000);

      // Stay on Architecture Grid view throughout simulation - no jumping!
      switchStage('arch');

      // Step 1: DynamoDB Mutex
      updateAwsStepUI(1, "STEP 1/5: DYNAMODB CONDITIONAL CAS MUTEX LEASE");
      showToast('🔒 [Step 1/5] DynamoDB CAS acquiring distributed mutex lease...');
      document.getElementById('telemetryStatus').innerText = "ACQUIRING MUTEX LOCK (" + lockKey + ")";
      await wait(600);

      // Step 2: AgentCore Ring 0 Policy
      updateAwsStepUI(2, "STEP 2/5: AGENTCORE RING 0 CEDAR POLICY VERIFICATION");
      showToast('🛡️ [Step 2/5] Bedrock AgentCore evaluating Cedar Ring 0 invariants...');
      document.getElementById('telemetryStatus').innerText = "VERIFYING CEDAR POLICY INVARIANTS";
      await wait(600);

      // Step 3: Vector & Graph Retrieval
      updateAwsStepUI(3, "STEP 3/5: NEPTUNE GRAPH & VECTOR SEMANTIC GROUNDING");
      showToast('🔍 [Step 3/5] Querying Neptune graph & vector embeddings...');
      document.getElementById('telemetryStatus').innerText = "GROUNDING VIA KNOWLEDGE GRAPH";
      await wait(600);

      // Step 4: Lambda MicroVM Sandbox
      updateAwsStepUI(4, "STEP 4/5: ISOLATED LAMBDA MICROVM DISPATCH");
      showToast('⚡ [Step 4/5] Executing isolated AWS Lambda MicroVM...');
      document.getElementById('telemetryStatus').innerText = "DISPATCHING SANDBOXED LAMBDA";
      await wait(600);

      // Step 5: S3 WORM Vault Seal
      updateAwsStepUI(5, "STEP 5/5: AMAZON S3 WORM COMPLIANCE VAULT SEAL");
      showToast('📦 [Step 5/5] Sealing SHA-256 compliance receipt in S3 WORM Vault...');
      document.getElementById('telemetryStatus').innerText = "SEALING WORM VAULT RECEIPT";
      await wait(550);

      const customP = {
        title: "Dynamic Operational Pipeline",
        goal: text,
        lockKey: lockKey,
        lockOwner: "agent-os-worker-01",
        lambdaFn: "ExecuteSandboxedDirective",
        states: [
          "1. DynamoDB CAS LockAcquired (" + lockKey + ")",
          "2. EnforceAgentCorePolicyRing0 (CEDAR ALLOW)",
          "3. QueryVectorAndNeptuneGraph (0.94 cosine sim)",
          "4. ExecuteIsolatedLambdaCompute (MicroVM sandbox)",
          "5. SealWormReceiptInS3Vault (ObjectLock compliance)"
        ]
      };

      applyAwsExecutionResult(customP, text, engineLabel);
      updateAwsStepUI(6, "PHYSICAL PIPELINE COMMITTED & SEALED (100%)");
      showToast('✨ AWS Operations Pipeline executed & verified (' + engineLabel + ')!');
    }"""

new_stepped_sim = """    function clearCardAnimationClasses() {
      ['cardBedrock', 'cardAgentCore', 'cardS3Vault', 'cardDynamoDB', 'cardLambda', 'cardStepFunctions'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.remove('card-active-pulse', 'card-completed');
      });
    }

    async function runSteppedAwsSimulation(text, engineLabel) {
      const wait = (ms) => new Promise(res => setTimeout(res, ms));
      const lockKey = "job-" + Math.floor(1000 + Math.random()*9000);

      // Stay on Architecture Grid view throughout simulation
      switchStage('arch');
      clearCardAnimationClasses();

      // Step 1: DynamoDB Mutex Card Pulses
      updateAwsStepUI(1, "STEP 1/5: DYNAMODB CONDITIONAL CAS MUTEX LEASE");
      const cardDyn = document.getElementById('cardDynamoDB');
      if (cardDyn) {
        cardDyn.classList.add('card-active-pulse');
        document.getElementById('cardBadgeDynamoDB').textContent = "ACQUIRING LEASE...";
        document.getElementById('cardBadgeDynamoDB').className = "service-status status-proc";
      }
      showToast('🔒 [Step 1/5] DynamoDB CAS acquiring distributed mutex lease...');
      document.getElementById('telemetryStatus').innerText = "ACQUIRING MUTEX LOCK (" + lockKey + ")";
      await wait(750);

      if (cardDyn) {
        cardDyn.classList.remove('card-active-pulse');
        cardDyn.classList.add('card-completed');
        document.getElementById('cardBadgeDynamoDB').textContent = "MUTEX ACQUIRED";
        document.getElementById('cardBadgeDynamoDB').className = "service-status status-ok";
        document.getElementById('cardLockKey').textContent = "Key: " + lockKey;
      }

      // Step 2: AgentCore Policy & Bedrock Inference Card Pulses
      updateAwsStepUI(2, "STEP 2/5: AGENTCORE RING 0 CEDAR POLICY VERIFICATION");
      const cardAc = document.getElementById('cardAgentCore');
      const cardBed = document.getElementById('cardBedrock');
      if (cardAc) cardAc.classList.add('card-active-pulse');
      if (cardBed) cardBed.classList.add('card-active-pulse');
      showToast('🛡️ [Step 2/5] Bedrock AgentCore evaluating Cedar Ring 0 invariants...');
      document.getElementById('telemetryStatus').innerText = "VERIFYING CEDAR POLICY INVARIANTS";
      await wait(750);

      if (cardAc) {
        cardAc.classList.remove('card-active-pulse');
        cardAc.classList.add('card-completed');
        document.getElementById('cardBadgeAgentCore').textContent = "RING 0 VERIFIED";
      }
      if (cardBed) {
        cardBed.classList.remove('card-active-pulse');
        cardBed.classList.add('card-completed');
        document.getElementById('cardBadgeBedrock').textContent = "PROPOSAL PASSED";
      }

      // Step 3: Step Functions HFSM Card Pulses
      updateAwsStepUI(3, "STEP 3/5: STEP FUNCTIONS HFSM STATE MACHINE PROGRESSION");
      const cardSf = document.getElementById('cardStepFunctions');
      if (cardSf) {
        cardSf.classList.add('card-active-pulse');
        document.getElementById('cardBadgeStepFunctions').textContent = "EXECUTING DAG...";
      }
      showToast('🔄 [Step 3/5] Advancing Step Functions state barriers...');
      document.getElementById('telemetryStatus').innerText = "STEP FUNCTIONS BARRIER 3/5";
      await wait(700);

      if (cardSf) {
        cardSf.classList.remove('card-active-pulse');
        cardSf.classList.add('card-completed');
        document.getElementById('cardBadgeStepFunctions').textContent = "DAG COMMITTED";
      }

      // Step 4: Lambda MicroVM Sandbox Pulses
      updateAwsStepUI(4, "STEP 4/5: ISOLATED LAMBDA MICROVM DISPATCH");
      const cardLam = document.getElementById('cardLambda');
      if (cardLam) {
        cardLam.classList.add('card-active-pulse');
        document.getElementById('cardBadgeLambda').textContent = "COMPUTING IN VM...";
      }
      showToast('⚡ [Step 4/5] Executing isolated AWS Lambda MicroVM...');
      document.getElementById('telemetryStatus').innerText = "DISPATCHING SANDBOXED LAMBDA";
      await wait(700);

      if (cardLam) {
        cardLam.classList.remove('card-active-pulse');
        cardLam.classList.add('card-completed');
        document.getElementById('cardBadgeLambda').textContent = "EXECUTION SUCCESS";
      }

      // Step 5: S3 WORM Vault Seal Pulses
      updateAwsStepUI(5, "STEP 5/5: AMAZON S3 WORM COMPLIANCE VAULT SEAL");
      const cardS3 = document.getElementById('cardS3Vault');
      if (cardS3) {
        cardS3.classList.add('card-active-pulse');
        document.getElementById('cardBadgeS3Vault').textContent = "LOCKING SHA-256...";
      }
      showToast('📦 [Step 5/5] Sealing SHA-256 compliance receipt in S3 WORM Vault...');
      document.getElementById('telemetryStatus').innerText = "SEALING WORM VAULT RECEIPT";
      await wait(650);

      const receiptHex = "rcpt-" + Math.floor(10000 + Math.random()*90000);
      if (cardS3) {
        cardS3.classList.remove('card-active-pulse');
        cardS3.classList.add('card-completed');
        document.getElementById('cardBadgeS3Vault').textContent = "COMPLIANCE LOCKED";
        document.getElementById('cardHashS3').textContent = receiptHex + " (SHA-256 OK)";
      }

      const customP = {
        title: "Dynamic Operational Pipeline",
        goal: text,
        lockKey: lockKey,
        lockOwner: "agent-os-worker-01",
        lambdaFn: "ExecuteSandboxedDirective",
        states: [
          "1. DynamoDB CAS LockAcquired (" + lockKey + ")",
          "2. EnforceAgentCorePolicyRing0 (CEDAR ALLOW)",
          "3. QueryVectorAndNeptuneGraph (0.94 cosine sim)",
          "4. ExecuteIsolatedLambdaCompute (MicroVM sandbox)",
          "5. SealWormReceiptInS3Vault (ObjectLock compliance)"
        ]
      };

      // Update secondary tables and logs
      renderMutexTable(customP);
      renderHfsmVisualizer(customP.states);
      renderBotoCode(customP);

      const logBox = document.getElementById('telemetryLogLines');
      const ts = new Date().toLocaleTimeString();
      logBox.innerHTML += `
        <div class="log-line"><span class="log-ts">${ts}</span> <span class="log-svc">[Engine: ${engineLabel}]</span> Model proposed directive: "${text.slice(0, 35)}..."</div>
        <div class="log-line"><span class="log-ts">${ts}</span> <span class="log-svc">[DynamoDB]</span> <span class="log-ok">Conditional PUT succeeded for key '${lockKey}'. Exclusive lease active.</span></div>
        <div class="log-line"><span class="log-ts">${ts}</span> <span class="log-svc">[S3Vault]</span> <span class="log-ok">WORM receipt generated: ${receiptHex} and verified with SHA-256 checksum.</span></div>
      `;
      document.getElementById('telemetryStatus').innerText = "PIPELINE COMMITTED (" + engineLabel + ")";

      updateAwsStepUI(6, "PHYSICAL PIPELINE COMMITTED & SEALED (100%)");
      showToast('✨ AWS Operations Pipeline executed & verified (' + engineLabel + ')!');
    }"""

html = html.replace(old_stepped_sim, new_stepped_sim)

with open('aws_basics_studio_app.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("aws_basics_studio_app.html updated with fixed horizontal stepper grid and active service card pulse animation!")
