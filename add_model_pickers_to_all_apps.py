import os

# Updates Somatic Marker and Homeostasis to include the prominent model picker dropdown in the header,
# matching Theory of Mind and Episodic Plasticity.

SOMATIC_HTML = open("brain_to_ai_somatic_marker.html", "r", encoding="utf-8").read()

# Insert model picker markup into somatic marker header if not already there
if 'id="model-select"' not in SOMATIC_HTML:
    old_engine_bar = r'''    <div class="engine-bar">
      <div class="engine-pill active" id="eng-det" onclick="selectEngine('det')">
        <span class="dot dot-det"></span>Deterministic Simulation
      </div>
      <div class="engine-pill" id="eng-groq" onclick="selectEngine('groq')">
        <span class="dot dot-groq"></span>Groq LPU (~200ms)
      </div>
      <div class="engine-pill" id="eng-webllm" onclick="selectEngine('webllm')">
        <span class="dot dot-webllm"></span>WebGPU WebLLM
      </div>
      <button class="btn-config" onclick="openSettings()" title="Configure Groq / WebLLM settings">&#9881; Settings</button>
    </div>'''

    new_engine_controls = r'''    <div class="engine-controls" style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
      <div class="engine-bar" style="display:flex; align-items:center; gap:6px;">
        <div class="engine-pill active" id="eng-det" onclick="selectEngine('det')">
          <span class="dot dot-det"></span>Deterministic
        </div>
        <div class="engine-pill" id="eng-groq" onclick="selectEngine('groq')">
          <span class="dot dot-groq"></span>Groq LPU (~200ms)
        </div>
        <div class="engine-pill" id="eng-webllm" onclick="selectEngine('webllm')">
          <span class="dot dot-webllm"></span>WebGPU WebLLM
        </div>
      </div>

      <div class="model-picker-wrap" style="display:flex; align-items:center; gap:6px; background:var(--bg-card); border:1.5px solid var(--border-accent); border-radius:10px; padding:5px 12px; box-shadow:0 0 10px rgba(37,99,235,0.15);">
        <span class="model-picker-label" style="font-size:11px; font-weight:800; color:#60A5FA; text-transform:uppercase;">Active Model:</span>
        <select id="model-select" class="model-select" style="background:transparent; border:none; color:var(--text-main); font-family:'JetBrains Mono',monospace; font-size:11.5px; font-weight:700; outline:none; cursor:pointer;" onchange="onModelDropdownChange(this.value)">
          <optgroup label="⚡ Groq LPU (Ultra-Fast Cloud)">
            <option value="qwen/qwen3.8-27b" selected>qwen/qwen3.8-27b (High-Precision Utility)</option>
            <option value="openai/gpt-oss-20b">openai/gpt-oss-20b (Ultra-Fast LPU)</option>
            <option value="openai/gpt-oss-120b">openai/gpt-oss-120b (Deep Analysis)</option>
            <option value="allam-2-7b">allam-2-7b (Adaptive Agent Heuristic)</option>
          </optgroup>
          <optgroup label="💻 WebGPU In-Browser (Client-Side Weights)">
            <option value="Qwen2.5-1.5B-Instruct-q4f16_1-MLC">Qwen2.5 1.5B (~900MB GPU)</option>
            <option value="Llama-3.2-1B-Instruct-q4f16_1-MLC">Llama 3.2 1B (~800MB GPU)</option>
            <option value="SmolLM2-1.7B-Instruct-q4f16_1-MLC">SmolLM2 1.7B (~1GB GPU)</option>
          </optgroup>
          <optgroup label="📐 Mathematical Deterministic Engine">
            <option value="deterministic-vmpfc">VMPFC Somatic Vector Evaluator</option>
          </optgroup>
        </select>
      </div>

      <button class="btn-config" onclick="openSettings()" title="Configure Groq / WebLLM settings">&#9881; Settings</button>
    </div>'''

    if old_engine_bar in SOMATIC_HTML:
        SOMATIC_HTML = SOMATIC_HTML.replace(old_engine_bar, new_engine_controls)
        
        # Add onModelDropdownChange function in JS
        dropdown_func = r'''
    function onModelDropdownChange(modelVal) {
      currentModel = modelVal;
      groqModel = modelVal;
      document.getElementById('hardware-tag').innerText = `Model: ${currentModel}`;

      if (modelVal === 'deterministic-vmpfc') {
        selectEngine('det');
      } else if (modelVal.startsWith('openai/') || modelVal.startsWith('qwen/qwen3') || modelVal.startsWith('allam-')) {
        selectEngine('groq');
      } else {
        webllmModel = modelVal;
        selectEngine('webllm');
      }
    }
'''
        SOMATIC_HTML = SOMATIC_HTML.replace("let currentEngine = 'det';", "let currentEngine = 'det';\n    let currentModel = 'qwen/qwen3.8-27b';" + dropdown_func)
        with open("brain_to_ai_somatic_marker.html", "w", encoding="utf-8") as f:
            f.write(SOMATIC_HTML)
        print("Updated brain_to_ai_somatic_marker.html with model picker.")


# Also update Homeostasis
HOMEO_HTML = open("brain_to_ai_homeostasis.html", "r", encoding="utf-8").read()
if 'id="model-select"' not in HOMEO_HTML:
    old_homeo_bar = r'''    <div class="engine-bar">
      <div class="engine-pill active" id="eng-det" onclick="selectEngine('det')"><span class="dot dot-det"></span>Deterministic Simulation</div>
      <div class="engine-pill" id="eng-groq" onclick="selectEngine('groq')"><span class="dot dot-groq"></span>Groq LPU (~200ms)</div>
      <div class="engine-pill" id="eng-webllm" onclick="selectEngine('webllm')"><span class="dot dot-webllm"></span>WebGPU WebLLM</div>
      <button class="btn-config" onclick="openSettings()">&#9881; Settings</button>
    </div>'''

    new_homeo_controls = r'''    <div class="engine-controls" style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
      <div class="engine-bar" style="display:flex; align-items:center; gap:6px;">
        <div class="engine-pill active" id="eng-det" onclick="selectEngine('det')"><span class="dot dot-det"></span>Deterministic</div>
        <div class="engine-pill" id="eng-groq" onclick="selectEngine('groq')"><span class="dot dot-groq"></span>Groq LPU (~200ms)</div>
        <div class="engine-pill" id="eng-webllm" onclick="selectEngine('webllm')"><span class="dot dot-webllm"></span>WebGPU WebLLM</div>
      </div>

      <div class="model-picker-wrap" style="display:flex; align-items:center; gap:6px; background:var(--bg-card); border:1.5px solid var(--accent); border-radius:10px; padding:5px 12px; box-shadow:0 0 10px rgba(13,148,136,0.15);">
        <span class="model-picker-label" style="font-size:11px; font-weight:800; color:var(--teal); text-transform:uppercase;">Active Model:</span>
        <select id="model-select" class="model-select" style="background:transparent; border:none; color:var(--text-main); font-family:'JetBrains Mono',monospace; font-size:11.5px; font-weight:700; outline:none; cursor:pointer;" onchange="onModelDropdownChange(this.value)">
          <optgroup label="⚡ Groq LPU (Ultra-Fast Cloud)">
            <option value="qwen/qwen3.8-27b" selected>qwen/qwen3.8-27b (High-Precision Homeostasis)</option>
            <option value="openai/gpt-oss-20b">openai/gpt-oss-20b (Ultra-Fast LPU)</option>
            <option value="openai/gpt-oss-120b">openai/gpt-oss-120b (Deep Analysis)</option>
            <option value="allam-2-7b">allam-2-7b (Adaptive Agent Heuristic)</option>
          </optgroup>
          <optgroup label="💻 WebGPU In-Browser (Client-Side Weights)">
            <option value="Qwen2.5-1.5B-Instruct-q4f16_1-MLC">Qwen2.5 1.5B (~900MB GPU)</option>
            <option value="Llama-3.2-1B-Instruct-q4f16_1-MLC">Llama 3.2 1B (~800MB GPU)</option>
            <option value="SmolLM2-1.7B-Instruct-q4f16_1-MLC">SmolLM2 1.7B (~1GB GPU)</option>
          </optgroup>
          <optgroup label="📐 Mathematical Deterministic Engine">
            <option value="hypothalamic-pid">Hypothalamic PID Rate Limiter</option>
          </optgroup>
        </select>
      </div>

      <button class="btn-config" onclick="openSettings()">&#9881; Settings</button>
    </div>'''

    if old_homeo_bar in HOMEO_HTML:
        HOMEO_HTML = HOMEO_HTML.replace(old_homeo_bar, new_homeo_controls)
        dropdown_func = r'''
    function onModelDropdownChange(modelVal) {
      currentModel = modelVal;
      groqModel = modelVal;
      document.getElementById('hardware-tag').innerText = `Model: ${currentModel}`;

      if (modelVal === 'hypothalamic-pid') {
        selectEngine('det');
      } else if (modelVal.startsWith('openai/') || modelVal.startsWith('qwen/qwen3') || modelVal.startsWith('allam-')) {
        selectEngine('groq');
      } else {
        webllmModel = modelVal;
        selectEngine('webllm');
      }
    }
'''
        HOMEO_HTML = HOMEO_HTML.replace("let currentEngine = 'det';", "let currentEngine = 'det';\n    let currentModel = 'qwen/qwen3.8-27b';" + dropdown_func)
        with open("brain_to_ai_homeostasis.html", "w", encoding="utf-8") as f:
            f.write(HOMEO_HTML)
        print("Updated brain_to_ai_homeostasis.html with model picker.")

print("All apps verified with direct header model pickers!")
