# -*- coding: utf-8 -*-
"""
add_stepper_to_tier0_app.py
Adds the visual Stepper Progress Bar to aws_basics_studio_app.html so that ALL 3 APPS
consistently feature the same top Stepped Progression bar that animates in place without jumping:
- Step 1: DynamoDB CAS Mutex Lease
- Step 2: AgentCore Ring 0 Policy Check
- Step 3: Neptune & Vector Grounding
- Step 4: Isolated Lambda MicroVM Compute
- Step 5: Amazon S3 WORM Vault Seal
"""

with open('aws_basics_studio_app.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Stepper CSS to aws_basics_studio_app.html
stepper_css = """
    /* MULTI-TIER STEPPER PROGRESSION COMPONENT (AWS LEVEL 0) */
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
      color: var(--aws-orange);
    }
    .stepper-track {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
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
    .step-item.active {
      border-color: #ea580c;
      background: #fff7ed;
      box-shadow: 0 0 0 2px rgba(234, 88, 12, 0.2);
      transform: translateY(-1px);
    }
    .step-item.active .step-num {
      background: #ea580c;
      color: #ffffff;
      animation: pulseAwsStep 1.2s infinite ease-in-out;
    }
    .step-item.active .step-tier {
      color: #c2410c;
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
    @keyframes pulseAwsStep {
      0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(234, 88, 12, 0.4); }
      50% { transform: scale(1.1); box-shadow: 0 0 0 6px rgba(234, 88, 12, 0); }
    }
"""

if '.stepper-container' not in html:
    html = html.replace('/* Main View Area (Stage) */', stepper_css + '\n    /* Main View Area (Stage) */')

# 2. Add Stepper HTML right above .stage-tabs
stepper_html = """      <!-- MULTI-TIER STEPPED PROGRESSION TRACKER (AWS LEVEL 0) -->
      <div class="stepper-container" id="awsStepperContainer">
        <div class="stepper-header">
          <div class="stepper-title">
            <span>⚡ Level 0 Physical AWS Progression</span>
            <span style="font-size: 0.68rem; font-weight: 600; color: var(--text-muted);">&bull; DynamoDB Mutex &rarr; AgentCore Cedar &rarr; Graph Grounding &rarr; Lambda MicroVM &rarr; S3 Vault</span>
          </div>
          <div class="stepper-status" id="awsStepperStatus">READY &bull; IDLE</div>
        </div>
        <div class="stepper-track">
          <div class="step-item" id="aStep1">
            <div class="step-num">1</div>
            <div class="step-text">
              <span class="step-label">DynamoDB Mutex</span>
              <span class="step-tier">CAS Lock Acquisition</span>
            </div>
          </div>
          <div class="step-item" id="aStep2">
            <div class="step-num">2</div>
            <div class="step-text">
              <span class="step-label">AgentCore Guardrail</span>
              <span class="step-tier">Ring 0 Cedar Gate</span>
            </div>
          </div>
          <div class="step-item" id="aStep3">
            <div class="step-num">3</div>
            <div class="step-text">
              <span class="step-label">Neptune &amp; Vectors</span>
              <span class="step-tier">Knowledge Grounding</span>
            </div>
          </div>
          <div class="step-item" id="aStep4">
            <div class="step-num">4</div>
            <div class="step-text">
              <span class="step-label">Lambda MicroVM</span>
              <span class="step-tier">Isolated Sandbox</span>
            </div>
          </div>
          <div class="step-item" id="aStep5">
            <div class="step-num">5</div>
            <div class="step-text">
              <span class="step-label">S3 WORM Vault</span>
              <span class="step-tier">Compliance Receipt</span>
            </div>
          </div>
        </div>
      </div>
"""

if 'id="awsStepperContainer"' not in html:
    html = html.replace('<div class="stage-tabs">', stepper_html + '      <div class="stage-tabs">', 1)

# 3. Add updateAwsStepUI and update runSteppedAwsSimulation
old_aws_sim = """    async function runSteppedAwsSimulation(text, engineLabel) {
      const wait = (ms) => new Promise(res => setTimeout(res, ms));
      const lockKey = "job-" + Math.floor(1000 + Math.random()*9000);

      // Step 1: DynamoDB Mutex
      showToast('🔒 [Step 1/5] DynamoDB CAS acquiring distributed mutex lease...');
      document.getElementById('telemetryStatus').innerText = "ACQUIRING MUTEX LOCK (" + lockKey + ")";
      await wait(500);

      // Step 2: AgentCore Ring 0 Policy
      showToast('🛡️ [Step 2/5] Bedrock AgentCore evaluating Cedar Ring 0 invariants...');
      document.getElementById('telemetryStatus').innerText = "VERIFYING CEDAR POLICY INVARIANTS";
      await wait(500);

      // Step 3: Vector & Graph Retrieval
      showToast('🔍 [Step 3/5] Querying Neptune graph & vector embeddings...');
      document.getElementById('telemetryStatus').innerText = "GROUNDING VIA KNOWLEDGE GRAPH";
      await wait(500);

      // Step 4: Lambda MicroVM Sandbox
      showToast('⚡ [Step 4/5] Executing isolated AWS Lambda MicroVM...');
      document.getElementById('telemetryStatus').innerText = "DISPATCHING SANDBOXED LAMBDA";
      await wait(500);

      // Step 5: S3 WORM Vault Seal
      showToast('📦 [Step 5/5] Sealing SHA-256 compliance receipt in S3 WORM Vault...');
      document.getElementById('telemetryStatus').innerText = "SEALING WORM VAULT RECEIPT";
      await wait(450);

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
      showToast('✨ AWS Operations Pipeline executed & verified (' + engineLabel + ')!');
    }"""

new_aws_sim = """    function updateAwsStepUI(activeStepNum, statusText) {
      document.getElementById('awsStepperStatus').textContent = statusText;
      for (let i = 1; i <= 5; i++) {
        const el = document.getElementById('aStep' + i);
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

    async function runSteppedAwsSimulation(text, engineLabel) {
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

html = html.replace(old_aws_sim, new_aws_sim)

with open('aws_basics_studio_app.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("aws_basics_studio_app.html successfully updated with Visual Stepper!")
