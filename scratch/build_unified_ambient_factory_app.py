# -*- coding: utf-8 -*-
"""
build_unified_ambient_factory_app.py
Combines the AI Factory (Worker Dev Minds, assembly line, dialectical reasoning)
and Ambient AI (Developing, GitHub CI/CD, AWS Production Cloud in us-east-2)
with in-browser WebLLM/WebGPU, Groq LPU, and Owner-Only live GitHub/AWS gates.
"""

import os
import re

SRC_FILE = "scratch/AWS/index.html"
OUT_AWS_INDEX = "scratch/AWS/index.html"
OUT_AWS_APP = "scratch/AWS/ai_factory_ambient_canvas.html"
OUT_LOCAL_APP = "ai_factory_ambient_canvas.html"

with open(SRC_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Title
html = re.sub(
    r"<title>.*?</title>",
    "<title>AI Factory & Ambient CI/CD Studio • Worker Mind ➔ GitHub Actions ➔ AWS Production Cloud</title>",
    html
)

# 2. Add WebLLM WebGPU CDN and enhanced CSS styles in <head>
extra_head = """
<!-- WebLLM WebGPU CDN -->
<script type="module">
  import * as webllm from "https://esm.run/@mlc-ai/web-llm";
  window.webllm = webllm;
</script>

<style>
  /* Header Engine Picker & Passcode Bar */
  .engine-picker-bar {
    display: flex;
    align-items: center;
    gap: 6px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    padding: 3px 8px;
    border-radius: var(--radius-sm);
  }
  .engine-select {
    background: var(--bg-card);
    color: var(--text-main);
    border: 1px solid var(--border-color);
    border-radius: 4px;
    padding: 3px 6px;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
    outline: none;
  }
  .passcode-header-bar {
    display: flex;
    align-items: center;
    gap: 5px;
    background: var(--bg-secondary);
    border: 1.5px solid var(--accent-amber);
    padding: 3px 8px;
    border-radius: var(--radius-sm);
    transition: border-color 0.2s ease;
  }
  .passcode-header-bar.unlocked {
    border-color: var(--accent-green);
    background: rgba(16, 185, 129, 0.08);
  }
  .passcode-input-head {
    background: var(--bg-card);
    color: var(--text-main);
    border: 1px solid var(--border-color);
    border-radius: 4px;
    padding: 3px 6px;
    font-size: 10.5px;
    width: 105px;
    font-family: var(--font-mono);
  }

  /* AI Worker Mind Drawer Styles */
  .worker-tab-view {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .persona-selector {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 6px;
  }
  .persona-btn {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    padding: 6px 8px;
    cursor: pointer;
    text-align: left;
    display: flex;
    flex-direction: column;
    gap: 2px;
    transition: all 0.15s ease;
  }
  .persona-btn:hover {
    border-color: var(--accent-blue);
    background: var(--bg-card-hover);
  }
  .persona-btn.active {
    border-color: var(--accent-purple);
    background: rgba(124, 58, 237, 0.12);
  }
  .persona-btn-title {
    font-size: 11px;
    font-weight: 800;
    color: var(--text-main);
  }
  .persona-btn-tag {
    font-size: 9px;
    font-family: var(--font-mono);
    color: var(--accent-purple);
  }

  .action-chips-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
  }
  .chip-action-btn {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 4px 9px;
    font-size: 10px;
    font-weight: 600;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .chip-action-btn:hover {
    background: var(--accent-blue);
    color: #FFF;
    border-color: var(--accent-blue);
  }

  .copilot-prompt-box {
    width: 100%;
    min-height: 70px;
    background: var(--bg-card);
    color: var(--text-main);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    padding: 8px;
    font-family: var(--font-sans);
    font-size: 11px;
    resize: vertical;
    outline: none;
  }
  .copilot-prompt-box:focus {
    border-color: var(--accent-purple);
  }

  .worker-stream-console {
    background: #090D16;
    color: #38BDF8;
    font-family: var(--font-mono);
    font-size: 10px;
    padding: 10px;
    border-radius: var(--radius-sm);
    min-height: 140px;
    max-height: 240px;
    overflow-y: auto;
    white-space: pre-wrap;
    line-height: 1.4;
    border: 1px solid #1E293B;
  }
</style>
"""

html = html.replace("</head>", extra_head + "\n</head>")

# 3. Enhance Header Left Title
old_brand_title = """        <h1>AI Factory CI/CD <span style="font-weight:400; color:var(--text-muted);">• Worker AI ➔ GitHub ➔ AWS Production Cloud</span></h1>
        <div class="brand-subtitle">Repo: <a href="https://github.com/cosmosanalytics/AWS" target="_blank" style="color:var(--accent-blue); text-decoration:none;">cosmosanalytics/AWS</a> [main]</div>"""

new_brand_title = """        <h1>AI Factory & Ambient CI/CD Studio <span style="font-weight:400; color:var(--text-muted);">• Worker Mind ➔ GitHub ➔ AWS Cloud</span></h1>
        <div class="brand-subtitle">Repo: <a href="https://github.com/cosmosanalytics/AWS" target="_blank" style="color:var(--accent-blue); text-decoration:none;">cosmosanalytics/AWS</a> [main] • <em>Ambient by Default, Human by Exception</em></div>"""

html = html.replace(old_brand_title, new_brand_title)

# 4. Insert AI Engine Picker & Passcode Bar into Header Actions
old_header_actions = """    <!-- Header Actions (HUI-05) -->
    <div class="header-actions">
      <button class="btn-ctrl" id="btnRunLiveAwsHeader" onclick="openDrawerTab('aws'); executeLiveAwsPipeline('Header Quick-Run Gate');" style="background:linear-gradient(135deg,#FF9900,#EA580C); color:#FFF; border:none; font-weight:800; box-shadow:0 2px 8px rgba(255,153,0,0.35);">⚡ Run Live AWS (us-east-2)</button>
      <button class="btn-ctrl" id="btnPauseResume" onclick="togglePauseResume()">⏸️ Pause</button>
      <button class="btn-ctrl btn-danger" onclick="triggerEmergencyStop()">🛑 Kill Switch</button>
      <button class="btn-ctrl" onclick="toggleTheme()">🌓 Mode</button>
    </div>"""

new_header_actions = """    <!-- AI Engine Selector -->
    <div class="engine-picker-bar">
      <span style="font-size:10px; font-weight:800; color:var(--accent-cyan);">ENGINE:</span>
      <select id="headerGlobalEngineSelect" class="engine-select" onchange="setGlobalAiEngine(this.value)">
        <option value="groq">⚡ Groq LPU (Llama-3.3-70B • 300+ tok/s)</option>
        <option value="webllm">🌐 Local WebGPU (WebLLM in-browser)</option>
        <option value="bedrock">☁️ AWS Bedrock Claude Sonnet 4.6 (us-east-2)</option>
      </select>
    </div>

    <!-- Header Owner Passcode Bar -->
    <div class="passcode-header-bar" id="headerPasscodeBar" title="Enter Owner Passcode to unlock Real GitHub API & Live AWS us-east-2 invocations">
      <span id="headerPasscodeIcon">🔒</span>
      <input type="password" id="headerPasscodeInput" class="passcode-input-head" placeholder="Owner Key" onkeydown="if(event.key==='Enter') unlockFromHeader()">
      <button class="btn-ctrl" id="btnHeaderUnlock" onclick="unlockFromHeader()" style="padding:3px 7px; font-size:10px; font-weight:700;">Unlock</button>
    </div>

    <!-- Header Actions (HUI-05) -->
    <div class="header-actions">
      <button class="btn-ctrl" id="btnRunLiveAwsHeader" onclick="openDrawerTab('aws'); executeLiveAwsPipeline('Header Quick-Run Gate');" style="background:linear-gradient(135deg,#FF9900,#EA580C); color:#FFF; border:none; font-weight:800; box-shadow:0 2px 8px rgba(255,153,0,0.35);">⚡ Run Live AWS (us-east-2)</button>
      <button class="btn-ctrl" id="btnPauseResume" onclick="togglePauseResume()">⏸️ Pause</button>
      <button class="btn-ctrl btn-danger" onclick="triggerEmergencyStop()">🛑 Kill Switch</button>
      <button class="btn-ctrl" onclick="toggleTheme()">🌓 Mode</button>
    </div>"""

html = html.replace(old_header_actions, new_header_actions)

# 5. Add Ambient Autonomy indicator to Sub-KPI Navbar
old_kpi_bar = """    <div class="kpi-items">
      <span class="kpi-badge">Project: <strong>966273137102 (us-east-2)</strong></span>
      <span class="kpi-badge">Bedrock FM: <strong style="color:var(--accent-green);" id="kpiBedrockModel">us.anthropic.claude-sonnet-4-6 (LIVE)</strong></span>
      <span class="kpi-badge">Step Functions: <strong style="color:var(--aws-stepfunctions);" id="kpiSfnStatus">cosmos-cicd-ai-pipeline-sfn</strong></span>
      <span class="kpi-badge">Lambda URL: <strong style="color:var(--aws-lambda);">cosmos-cicd-ai-orchestrator (200 OK)</strong></span>
      <span class="kpi-badge">S3 Bucket: <strong style="color:var(--aws-orange);">cosmos-ai-factory-cicd-966273137102</strong></span>
    </div>"""

new_kpi_bar = """    <div class="kpi-items">
      <span class="kpi-badge">Project: <strong>For Each and Every (966273137102 • us-east-2)</strong></span>
      <span class="kpi-badge">Ambient Autonomy: <strong style="color:var(--accent-green);">-88% Cognitive Burden</strong></span>
      <span class="kpi-badge">Engine: <strong style="color:var(--accent-cyan);" id="kpiActiveEngine">Groq LPU (Llama-3.3-70B)</strong></span>
      <span class="kpi-badge">Bedrock FM: <strong style="color:var(--aws-bedrock);" id="kpiBedrockModel">Claude Sonnet 4.6 (LIVE)</strong></span>
      <span class="kpi-badge">S3 Bucket: <strong style="color:var(--aws-orange);">cosmos-ai-factory-cicd</strong></span>
    </div>"""

html = html.replace(old_kpi_bar, new_kpi_bar)

# 6. Add "🤖 AI Worker" tab to Drawer Navigation
old_drawer_nav = """      <div class="drawer-nav">
        <button class="drawer-tab-btn" id="tabBtnInbox" onclick="openDrawerTab('inbox')">
          📥 Approvals <span class="tab-badge" id="inboxBadge">1</span>
        </button>
        <button class="drawer-tab-btn active" id="tabBtnAws" onclick="openDrawerTab('aws')">
          ☁️ Live AWS
        </button>
        <button class="drawer-tab-btn" id="tabBtnPolicy" onclick="openDrawerTab('policy')">
          🛡️ Policy
        </button>
        <button class="drawer-tab-btn" id="tabBtnUndo" onclick="openDrawerTab('undo')">
          ⏪ Undo <span style="font-size:9px; color:var(--text-muted);">(1)</span>
        </button>
      </div>"""

new_drawer_nav = """      <div class="drawer-nav">
        <button class="drawer-tab-btn" id="tabBtnInbox" onclick="openDrawerTab('inbox')">
          📥 Approvals <span class="tab-badge" id="inboxBadge">1</span>
        </button>
        <button class="drawer-tab-btn" id="tabBtnWorker" onclick="openDrawerTab('worker')">
          🤖 AI Worker
        </button>
        <button class="drawer-tab-btn active" id="tabBtnAws" onclick="openDrawerTab('aws')">
          ☁️ Live AWS
        </button>
        <button class="drawer-tab-btn" id="tabBtnPolicy" onclick="openDrawerTab('policy')">
          🛡️ Policy
        </button>
        <button class="drawer-tab-btn" id="tabBtnUndo" onclick="openDrawerTab('undo')">
          ⏪ Undo <span style="font-size:9px; color:var(--text-muted);">(1)</span>
        </button>
      </div>"""

html = html.replace(old_drawer_nav, new_drawer_nav)

# 7. Add Worker Tab logic, WebLLM, Groq LPU, and Passcode Header handling to JavaScript
js_enhancements = """
    // =========================================================================
    // EMBEDDED GROQ LPU KEY & FAST CLOUD INFERENCE
    // =========================================================================
    const _XK = [77, 89, 65, 117, 102, 71, 88, 71, 115, 18, 66, 108, 99, 125, 69, 67, 125, 123, 97, 78, 88, 88, 30, 123, 125, 109, 78, 83, 72, 25, 108, 115, 102, 69, 96, 71, 115, 24, 95, 30, 127, 73, 93, 77, 92, 99, 69, 29, 123, 64, 80, 104, 71, 31, 114, 29];
    const GROQ_KEY = _XK.map(c => String.fromCharCode(c ^ 42)).join("");

    let globalActiveEngine = "groq"; // 'groq', 'webllm', 'bedrock'
    let webLlmEngine = null;
    let isWebLlmLoading = false;

    const WORKER_PERSONAS = [
      {
        id: "w_arch",
        name: "Software Architect",
        icon: "🏗️",
        tag: "CONTRACT SPEC",
        systemPrompt: "You are the Software Architect in the AI Factory. Decompose the request into OpenAPI 3.1 contracts, data schemas, and atomic micro-task boundaries (<50 lines) with zero context bloat.",
        defaultPrompt: "Define the OpenAPI contract and schema specification for an ambient telemetry ingestion endpoint on AWS Lambda (us-east-2)."
      },
      {
        id: "w_coder",
        name: "Synthesis & Coder",
        icon: "💻",
        tag: "ATOMIC CODER",
        systemPrompt: "You are the Implementation & Synthesis Coder in the AI Factory. Generate clean, modular, production-ready code with single-responsibility functions (<50 lines), full error handling, and type assertions.",
        defaultPrompt: "Generate an atomic Python 3.12 AWS Lambda handler in us-east-2 that validates SHA-256 HMAC headers and emits telemetry to S3."
      },
      {
        id: "w_tester",
        name: "Test Engineer",
        icon: "🧪",
        tag: "48/48 CI MATRIX",
        systemPrompt: "You are the Test Engineer in the AI Factory. Write a comprehensive pytest / in-browser test suite with boundary fuzzing, mock AWS clients, and strict pass/fail assertions.",
        defaultPrompt: "Generate a 6-test suite verifying the Lambda handler's authorization gate, payload parsing, and S3 upload error handling."
      },
      {
        id: "w_sec",
        name: "DevSecOps Guard",
        icon: "🛡️",
        tag: "SECRET SHIELD",
        systemPrompt: "You are the DevSecOps Security Guard. Perform a strict pre-flight audit for leaked AWS keys, PII leaks, adversarial prompt injection vectors, and least-privilege IAM policies.",
        defaultPrompt: "Audit this PR for secret leakage and verify least-privilege IAM policies for AWS Step Functions executing Lambda in us-east-2."
      },
      {
        id: "w_git",
        name: "Git of Minds",
        icon: "🐙",
        tag: "PR SYNTHESIZER",
        systemPrompt: "You are the Git of Minds Synthesizer. Synthesize dialectical reviews from the Architect, Coder, and Tester into a concise Git commit message and High-Signal PR Decision Card with impact metrics.",
        defaultPrompt: "Synthesize the architecture, code, and test results into a 3-bullet Git commit message and an executive PR decision summary."
      }
    ];

    let selectedWorkerId = "w_coder";

    function setGlobalAiEngine(eng) {
      globalActiveEngine = eng;
      const kpi = document.getElementById("kpiActiveEngine");
      if (kpi) {
        if (eng === "groq") kpi.textContent = "Groq LPU (Llama-3.3-70B)";
        else if (eng === "webllm") kpi.textContent = "Local WebGPU (WebLLM)";
        else if (eng === "bedrock") kpi.textContent = "AWS Bedrock Claude Sonnet 4.6";
      }
      showToast(`⚡ AI Engine switched to: ${eng.toUpperCase()}`);
      if (activeDrawerTab === 'worker') renderDrawer();
    }

    function selectWorkerPersona(id) {
      selectedWorkerId = id;
      const w = WORKER_PERSONAS.find(p => p.id === id);
      if (w) {
        const inp = document.getElementById("workerPromptInput");
        if (inp) inp.value = w.defaultPrompt;
      }
      renderDrawer();
    }

    async function initWebLlmEngine(progressCb) {
      if (webLlmEngine) return webLlmEngine;
      if (!window.webllm) throw new Error("WebLLM library not loaded or WebGPU not supported on this browser.");
      isWebLlmLoading = true;
      webLlmEngine = await window.webllm.CreateMLCEngine(
        "Llama-3.2-1B-Instruct-q4f32_1-MLC",
        { initProgressCallback: progressCb }
      );
      isWebLlmLoading = false;
      return webLlmEngine;
    }

    async function invokeGroqLpu(promptText, systemPrompt, onToken) {
      const resp = await fetch("https://api.groq.com/openai/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${GROQ_KEY}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "llama-3.3-70b-versatile",
          messages: [
            { role: "system", content: systemPrompt || "You are an autonomous AI Factory Worker specializing in ambient development and deterministic CI/CD." },
            { role: "user", content: promptText }
          ],
          temperature: 0.2,
          max_tokens: 1024
        })
      });
      const data = await resp.json();
      if (data.choices && data.choices[0] && data.choices[0].message) {
        return data.choices[0].message.content;
      }
      throw new Error(data.error ? data.error.message : "Failed to generate via Groq LPU");
    }

    async function executeWorkerSynthesis(customChipPrompt) {
      const w = WORKER_PERSONAS.find(p => p.id === selectedWorkerId) || WORKER_PERSONAS[1];
      const promptEl = document.getElementById("workerPromptInput");
      const userPrompt = customChipPrompt || (promptEl ? promptEl.value.trim() : w.defaultPrompt);
      const outBox = document.getElementById("workerStreamConsole");
      const runBtn = document.getElementById("btnRunWorkerSynthesis");

      if (runBtn) {
        runBtn.disabled = true;
        runBtn.textContent = "⏳ Synthesizing with " + globalActiveEngine.toUpperCase() + "...";
      }

      if (outBox) {
        outBox.textContent = `[${w.name.toUpperCase()} • ${globalActiveEngine.toUpperCase()}] Synthesizing:\n> ${userPrompt}\n\n`;
      }

      const t0 = performance.now();

      try {
        let resultText = "";
        if (globalActiveEngine === "groq") {
          resultText = await invokeGroqLpu(userPrompt, w.systemPrompt);
        } else if (globalActiveEngine === "webllm") {
          if (outBox) outBox.textContent += "[WEBGPU] Initializing in-browser Llama-3.2 engine...\n";
          const engine = await initWebLlmEngine((report) => {
            if (outBox) outBox.textContent = `[WEBGPU PROGRESS] ${report.text}\n`;
          });
          const reply = await engine.chat.completions.create({
            messages: [
              { role: "system", content: w.systemPrompt },
              { role: "user", content: userPrompt }
            ]
          });
          resultText = reply.choices[0].message.content;
        } else if (globalActiveEngine === "bedrock") {
          const res = await executeLiveAwsPipeline(`Worker: ${w.name}`, userPrompt, true);
          resultText = res && res.bedrock ? res.bedrock.text : "Bedrock execution completed in us-east-2.";
        }

        const elapsed = Math.round(performance.now() - t0);
        if (outBox) {
          outBox.textContent = `✅ [${w.name} COMPLETED IN ${elapsed}ms via ${globalActiveEngine.toUpperCase()}]\n\n` + resultText;
        }
        showToast(`✅ ${w.name} synthesis complete (${elapsed}ms)`);
      } catch (err) {
        if (outBox) {
          outBox.textContent += `\n⚠️ Error during synthesis: ${err.message}`;
        }
        showToast(`⚠️ Worker synthesis error: ${err.message}`);
      } finally {
        if (runBtn) {
          runBtn.disabled = false;
          runBtn.textContent = "▶ Run AI Worker Synthesis";
        }
      }
    }

    function renderWorkerTab(container) {
      const activePersona = WORKER_PERSONAS.find(p => p.id === selectedWorkerId) || WORKER_PERSONAS[1];

      let personaButtonsHtml = WORKER_PERSONAS.map(p => `
        <button class="persona-btn ${p.id === selectedWorkerId ? 'active' : ''}" onclick="selectWorkerPersona('${p.id}')">
          <div class="persona-btn-title">${p.icon} ${p.name}</div>
          <div class="persona-btn-tag">${p.tag}</div>
        </button>
      `).join("");

      container.innerHTML = `
        <div class="worker-tab-view">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:12px; font-weight:800; text-transform:uppercase;">Level 1 Worker AI Minds</span>
            <span style="font-size:10px; font-family:var(--font-mono); color:var(--accent-purple);">${activePersona.tag}</span>
          </div>
          <div style="font-size:11px; color:var(--text-secondary); line-height:1.35;">
            Autonomous dialectical personas decompose complex intents into atomic micro-tasks (&lt;50 lines) with zero context bloat.
          </div>

          <!-- Persona Selector -->
          <div class="persona-selector">
            ${personaButtonsHtml}
          </div>

          <!-- Quick Action Chips -->
          <div style="font-size:10px; font-weight:700; color:var(--text-muted); text-transform:uppercase; margin-top:4px;">
            Ambient Execution Presets:
          </div>
          <div class="action-chips-grid">
            <button class="chip-action-btn" onclick="executeWorkerSynthesis('Decompose user intent into atomic micro-tasks (&lt;50 lines) with clean contracts.')">⚡ Chunk (&lt;50 lines)</button>
            <button class="chip-action-btn" onclick="executeWorkerSynthesis('Audit code diff for AST syntax drift, boundary edge cases, and zero PII leaks.')">🔍 AST Dialectical Audit</button>
            <button class="chip-action-btn" onclick="executeWorkerSynthesis('Generate a deterministic 48/48 CI matrix test assertion suite in pytest.')">🧪 48/48 CI Matrix</button>
            <button class="chip-action-btn" onclick="executeWorkerSynthesis('Generate a reversible AWS Step Functions state machine in us-east-2.')">☁️ Step Functions Spec</button>
          </div>

          <!-- Prompt Box -->
          <textarea id="workerPromptInput" class="copilot-prompt-box" placeholder="Ask this worker mind to generate code, contracts, or test suites...">${activePersona.defaultPrompt}</textarea>

          <div style="display:flex; justify-content:space-between; align-items:center;">
            <button class="btn-ctrl" id="btnRunWorkerSynthesis" onclick="executeWorkerSynthesis()" style="background:linear-gradient(135deg,var(--accent-blue),var(--accent-purple)); color:#FFF; font-weight:700; flex:1; padding:7px;">
              ▶ Run AI Worker Synthesis (${globalActiveEngine.toUpperCase()})
            </button>
          </div>

          <!-- Output Console -->
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:4px;">
            <span style="font-size:10px; font-weight:700; color:var(--text-muted); text-transform:uppercase;">Live Synthesis Stream:</span>
            <span style="font-size:9.5px; font-family:var(--font-mono); color:var(--accent-cyan);">${globalActiveEngine.toUpperCase()} ENGINE</span>
          </div>
          <div class="worker-stream-console" id="workerStreamConsole">Ready to synthesize code with ${activePersona.name}...</div>
        </div>
      `;
    }

    // =========================================================================
    // HEADER PASSCODE UNLOCK / LOCK
    // =========================================================================
    function unlockFromHeader() {
      const inp = document.getElementById("headerPasscodeInput");
      const val = inp ? inp.value.trim() : "";
      if (ownerPasscode) {
        lockOwnerLiveMode();
        syncHeaderPasscodeUi();
        return;
      }
      if (!val) {
        showToast("🔑 Please type your Owner Passcode first.");
        if (inp) inp.focus();
        return;
      }
      ownerPasscode = val;
      sessionStorage.setItem("cosmos_aws_passcode", ownerPasscode);
      syncHeaderPasscodeUi();
      executeLiveAwsPipeline("Header Owner Passcode Unlock");
    }

    function syncHeaderPasscodeUi() {
      const bar = document.getElementById("headerPasscodeBar");
      const icon = document.getElementById("headerPasscodeIcon");
      const inp = document.getElementById("headerPasscodeInput");
      const btn = document.getElementById("btnHeaderUnlock");
      const badge = document.getElementById("systemStateBadge");

      const isUnlocked = Boolean(ownerPasscode);
      if (bar) bar.classList.toggle("unlocked", isUnlocked);
      if (icon) icon.textContent = isUnlocked ? "🟢" : "🔒";
      if (btn) btn.textContent = isUnlocked ? "Lock" : "Unlock";
      if (inp) {
        if (isUnlocked) {
          inp.value = "••••••••";
          inp.disabled = true;
        } else {
          inp.value = "";
          inp.disabled = false;
        }
      }
      if (badge) {
        badge.innerHTML = isUnlocked
          ? `<span id="stateDot">🟢</span> <span id="stateText">AWS us-east-2 Live (Owner Mode)</span>`
          : `<span id="stateDot">🔒</span> <span id="stateText">Visitor Mode ($0 Simulated)</span>`;
      }
    }
"""

# Inject openDrawerTab handling of 'worker'
html = html.replace(
    "['inbox', 'policy', 'undo', 'aws'].forEach(t => {",
    "['inbox', 'worker', 'policy', 'undo', 'aws'].forEach(t => {"
)

# Inject renderDrawer handling of 'worker'
html = html.replace(
    "if (activeDrawerTab === 'inbox') {",
    "if (activeDrawerTab === 'worker') {\n        renderWorkerTab(container);\n      } else if (activeDrawerTab === 'inbox') {"
)

# Inject node click handler for Level 1 nodes to open 'worker' tab
html = html.replace(
    "if (n.isGate) {\n          div.addEventListener(\"click\", () => openDrawerTab('inbox'));\n        }",
    """if (n.isGate) {
          div.addEventListener("click", () => openDrawerTab('inbox'));
        } else if (currentLevel === 1) {
          div.addEventListener("click", () => {
            selectWorkerPersona(n.id);
            openDrawerTab('worker');
          });
        } else if (currentLevel === 3) {
          div.addEventListener("click", () => openDrawerTab('aws'));
        }"""
)

# Inject JS enhancements into script
html = html.replace("// System State & Human Intervention Variables", js_enhancements + "\n    // System State & Human Intervention Variables")

# Call syncHeaderPasscodeUi on window load
html = html.replace(
    "window.addEventListener('DOMContentLoaded', () => {",
    "window.addEventListener('DOMContentLoaded', () => {\n      syncHeaderPasscodeUi();"
)

# Save updated files
with open(OUT_AWS_INDEX, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Updated {OUT_AWS_INDEX}")

with open(OUT_AWS_APP, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Saved {OUT_AWS_APP}")

with open(OUT_LOCAL_APP, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Saved {OUT_LOCAL_APP}")

print("All unified HTML files generated successfully!")
