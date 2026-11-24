/**
 * AgentCore.js - Reusable 6-Layer Closed-Loop Agent Architecture Runtime
 * 
 * Replaces conventional single-turn prompting and rigid DAG chatbots with a 
 * formalized closed-loop control system comprising:
 * 
 *   Layer 1: Perception & State Space Ingestion (StateSpace)
 *   Layer 2: Symbolic & World Modeling (WorldModel)
 *   Layer 3: Reasoning & Policy Engine (PolicyEngine)
 *   Layer 4: Deterministic Invariant & Safety Oracle (InvariantOracle)
 *   Layer 5: Actuation & Artifact Generation (Actuator)
 *   Layer 6: Telemetry, Observability & Feedback Loop (TelemetryLoop)
 */

(function(window) {
  'use strict';

  // --- LAYER DEFINITIONS ---
  const SIX_LAYERS = [
    { id: 'L1', name: 'State Space', desc: 'Perception, Context & Input Parameter Ingestion', icon: 'database', color: 'blue' },
    { id: 'L2', name: 'World Model', desc: 'Symbolic State, Graph Ontologies & Environmental Dynamics', icon: 'share-2', color: 'indigo' },
    { id: 'L3', name: 'Policy Engine', desc: 'Recursive Reasoning, Swarm Consensus & Trajectory Search', icon: 'cpu', color: 'purple' },
    { id: 'L4', name: 'Invariant Oracle', desc: 'Deterministic Safety Bounds, Proofs & Mathematical Assertions', icon: 'shield-check', color: 'emerald' },
    { id: 'L5', name: 'Actuation', desc: 'Committed Executables, Artifact Generation & System Mutation', icon: 'zap', color: 'amber' },
    { id: 'L6', name: 'Telemetry Loop', desc: 'Closed-Loop Scoring, Continuous Feedback & Self-Correction', icon: 'activity', color: 'rose' }
  ];

  // --- TRI-ENGINE INFERENCE ADAPTER ---
  class EngineProvider {
    constructor(defaultEngine = 'instant') {
      this.currentEngine = defaultEngine;
      this.groqApiKey = localStorage.getItem('agentcore_groq_key') || '';
      this.webllmModel = 'Qwen2.5-0.5B-Instruct-q4f16_1-MLC';
      this.webllmEngine = null;
      this.listeners = [];
    }

    setEngine(engine) {
      this.currentEngine = engine;
      this.notifyListeners({ type: 'engine_changed', engine });
    }

    addListener(fn) {
      this.listeners.push(fn);
    }

    notifyListeners(event) {
      this.listeners.forEach(fn => fn(event));
    }

    async infer({ prompt, systemPrompt = '', temperature = 0.2, fallbackResult = null }) {
      if (this.currentEngine === 'groq' && this.groqApiKey) {
        try {
          const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${this.groqApiKey}`
            },
            body: JSON.stringify({
              model: 'llama-3.3-70b-versatile',
              messages: [
                { role: 'system', content: systemPrompt },
                { role: 'user', content: prompt }
              ],
              temperature
            })
          });
          const data = await res.json();
          if (data.choices && data.choices[0]) {
            return data.choices[0].message.content;
          }
        } catch (e) {
          console.warn('[AgentCore] Groq inference failed, falling back to heuristic:', e);
        }
      }

      // Instant Sandbox / Local fallback
      return typeof fallbackResult === 'function' ? fallbackResult() : fallbackResult;
    }
  }

  // --- 6-LAYER REUSABLE AGENT BASE CLASS ---
  class ReusableAgent {
    constructor(config = {}) {
      this.id = config.id || 'agent-' + Math.random().toString(36).substring(7);
      this.name = config.name || 'Autonomous Agent';
      this.engine = new EngineProvider(config.defaultEngine || 'instant');

      // 6 Core Architectural Layers
      this.stateSpace = config.stateSpace || { inputs: {}, current: null };
      this.worldModel = config.worldModel || { graph: {}, invariants: [] };
      this.policyEngine = config.policyEngine || (async (state, world) => ({ action: 'noop' }));
      this.invariantOracle = config.invariantOracle || ((state, proposal) => ({ valid: true, violations: [] }));
      this.actuator = config.actuator || (async (proposal) => ({ committed: true }));
      this.telemetryLoop = config.telemetryLoop || { history: [], metrics: {} };

      this.stepCounter = 0;
    }

    /**
     * Executes one complete iteration of the 6-Layer Closed Loop
     */
    async executeCycle(inputPayload, onLayerProgress = null) {
      this.stepCounter++;
      const cycleLog = { cycle: this.stepCounter, timestamp: Date.now(), layers: {} };

      // Layer 1: Ingest into State Space
      if (onLayerProgress) onLayerProgress('L1', 'Ingesting perception and grounding state space');
      this.stateSpace.current = inputPayload;
      cycleLog.layers.L1 = { input: inputPayload };

      // Layer 2: Update World Model
      if (onLayerProgress) onLayerProgress('L2', 'Updating symbolic mental model and topology');
      if (this.worldModel.update) {
        await this.worldModel.update(this.stateSpace.current);
      }
      cycleLog.layers.L2 = { worldState: this.worldModel };

      // Layer 3: Policy Search & Reasoning
      if (onLayerProgress) onLayerProgress('L3', 'Running heuristic policy search and trajectory formulation');
      const proposal = await this.policyEngine(this.stateSpace.current, this.worldModel, this.engine);
      cycleLog.layers.L3 = { proposal };

      // Layer 4: Mathematical Invariant & Safety Verification
      if (onLayerProgress) onLayerProgress('L4', 'Evaluating proposal against formal invariant oracle');
      const verification = this.invariantOracle(this.stateSpace.current, proposal);
      cycleLog.layers.L4 = { verification };

      if (!verification.valid) {
        cycleLog.layers.L5 = { committed: false, reason: 'Invariant breach' };
        if (onLayerProgress) onLayerProgress('L4', `Invariant breach detected: ${verification.violations.join(', ')}`);
        return { success: false, reason: 'Invariant breach', verification, cycleLog };
      }

      // Layer 5: Actuation & Artifact Generation
      if (onLayerProgress) onLayerProgress('L5', 'Commiting actuation and publishing artifacts');
      const actuationResult = await this.actuator(proposal);
      cycleLog.layers.L5 = { committed: true, result: actuationResult };

      // Layer 6: Telemetry & Closed-Loop Scoring
      if (onLayerProgress) onLayerProgress('L6', 'Recording telemetry and closing self-improvement loop');
      if (this.telemetryLoop.record) {
        this.telemetryLoop.record(cycleLog);
      }
      cycleLog.layers.L6 = { status: 'recorded' };

      return { success: true, result: actuationResult, cycleLog };
    }
  }

  // --- UI HELPER: 6-LAYER ARCHITECTURE BADGE BAR ---
  function renderSixLayerHeader(activeLayer = null) {
    return `
      <div class="bg-slate-100 border border-slate-200 rounded-xl p-2 mb-3 flex items-center justify-between text-[11px] font-mono overflow-x-auto gap-1">
        <span class="text-slate-500 font-bold uppercase tracking-wider text-[10px] pl-1 flex items-center gap-1">
          <span class="w-1.5 h-1.5 rounded-full bg-indigo-600"></span> 6-Layer Architecture:
        </span>
        <div class="flex items-center gap-1">
          ${SIX_LAYERS.map(layer => {
            const isActive = activeLayer === layer.id;
            const activeClass = isActive 
              ? 'bg-indigo-600 text-white font-bold shadow-xs' 
              : 'bg-white text-slate-700 hover:bg-slate-50 border border-slate-200/80';
            return `
              <span class="px-2 py-0.5 rounded-md ${activeClass} transition flex items-center gap-1 whitespace-nowrap" title="${layer.desc}">
                <span class="font-bold">${layer.id}</span>
                <span class="hidden md:inline">${layer.name}</span>
              </span>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }

  // Expose to window
  window.AgentCore = {
    SIX_LAYERS,
    EngineProvider,
    ReusableAgent,
    renderSixLayerHeader
  };

})(window);
