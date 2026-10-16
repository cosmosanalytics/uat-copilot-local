# -*- coding: utf-8 -*-
"""
generate_oci_simulator.py
Builds the complete `ai_factory_oci_simulator.html` with Oracle Cloud (OCI) platform primitives,
WebLLM/WebGPU, Groq LPU, Pyodide tests, and interactive canvas.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("ai_factory_cloudflare_simulator.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace Page Title & Theme
html = html.replace("The AI Agent Factory • In-Browser Cloudflare Simulator",
                    "The AI Agent Factory • In-Browser Oracle Cloud (OCI) Simulator")
html = html.replace("--accent: #F6821F; /* Cloudflare Orange */",
                    "--accent: #C74634; /* Oracle Red */")
html = html.replace("--accent-light: #FFF1E5;", "--accent-light: #FBF2F1;")
html = html.replace("--accent-dark: #D96500;", "--accent-dark: #9E2B1E;")
html = html.replace("--cf-gold: #FAAD3F;", "--oci-gold: #F80000;")
html = html.replace("--accent: #F6821F;", "--accent: #C74634;")
html = html.replace("rgba(246, 130, 31, 0.16)", "rgba(199, 70, 52, 0.16)")
html = html.replace("rgba(246, 130, 31, 0.15)", "rgba(199, 70, 52, 0.15)")
html = html.replace("linear-gradient(135deg, #F6821F, #FAAD3F)", "linear-gradient(135deg, #C74634, #E0533C)")
html = html.replace("linear-gradient(135deg, #F6821F 0%, #FAAD3F 100%)", "linear-gradient(135deg, #C74634 0%, #E0533C 100%)")

# Replace Navbar & Branding
html = html.replace('<span class="cf-tag">Cloudflare Edge</span>', '<span class="cf-tag" style="background:#FBF2F1;color:#C74634;border:1px solid rgba(199,70,52,0.3);">Oracle Cloud OCI</span>')
html = html.replace("Assembly Robot • Workers, D1 &amp; Durable Objects • In-Browser Python Wasm (PyScript / Pyodide)",
                    "Assembly Robot • OCI NoSQL, Functions &amp; Generative AI • In-Browser Python Wasm (PyScript / Pyodide)")
html = html.replace("Browser-Native Cloudflare Simulator State", "Browser-Native Oracle Cloud Simulator State")

# Replace Preset Chips
html = html.replace("🛡️ Cloudflare FinTech (KV &amp; WAF)", "🛡️ OCI FinTech (NoSQL &amp; WAF)")
html = html.replace("⚡ Cloudflare SRE (Workflows &amp; Queues)", "⚡ OCI SRE (Process &amp; Queue)")
html = html.replace("🤝 Edge Swarm (Durable Objects &amp; WS)", "🤝 OCI Agent Swarm (Events &amp; GenAI)")
html = html.replace("⚖️ Edge Auditor (D1 &amp; Quorum)", "⚖️ OCI Auditor (NoSQL ACID &amp; Quorum)")

# Replace 7 Steps text
html = html.replace("Cloudflare BOM", "Oracle Cloud BOM")
html = html.replace("Cloudflare edge primitives", "Oracle Cloud OCI primitives")
html = html.replace("3-Shelf Cloudflare Parts Warehouse", "3-Shelf Oracle Cloud Parts Warehouse")

# Replace Shelf 0, 1, 2 items in HTML
old_shelf_html = '''          <div class="parts-grid" id="shelf0-grid">
            <div class="part-item active" id="part-kv" draggable="true" ondragstart="onWarehouseDragStart(event, 'kv')">📦 Workers KV</div>
            <div class="part-item active" id="part-d1" draggable="true" ondragstart="onWarehouseDragStart(event, 'd1')">🗄️ Cloudflare D1</div>
            <div class="part-item active" id="part-waf" draggable="true" ondragstart="onWarehouseDragStart(event, 'waf')">🛡️ Edge WAF &amp; Rate</div>
            <div class="part-item active" id="part-workers" draggable="true" ondragstart="onWarehouseDragStart(event, 'workers')">⚙️ Workers Isolate</div>
            <div class="part-item active" id="part-workersai" draggable="true" ondragstart="onWarehouseDragStart(event, 'workersai')">🧠 Workers AI</div>
            <div class="part-item active" id="part-analytics" draggable="true" ondragstart="onWarehouseDragStart(event, 'analytics')">📈 Analytics Engine</div>
          </div>
        </div>

        <!-- Shelf 1 -->
        <div class="shelf">
          <div class="shelf-header">
            <span class="shelf-tag t1">Tier 1 • One Agent Mind</span>
            <span class="shelf-desc">Decide, plan, stateful queues</span>
          </div>
          <div class="parts-grid" id="shelf1-grid">
            <div class="part-item active" id="part-queues" draggable="true" ondragstart="onWarehouseDragStart(event, 'queues')">🚦 Cloudflare Queues</div>
            <div class="part-item active" id="part-workflows" draggable="true" ondragstart="onWarehouseDragStart(event, 'workflows')">🔁 CF Workflows</div>
            <div class="part-item active" id="part-healthcheck" draggable="true" ondragstart="onWarehouseDragStart(event, 'healthcheck')">🔌 Health Breaker</div>
            <div class="part-item" id="part-vectorize" draggable="true" ondragstart="onWarehouseDragStart(event, 'vectorize')">🔍 CF Vectorize</div>
          </div>
        </div>

        <!-- Shelf 2 -->
        <div class="shelf">
          <div class="shelf-header">
            <span class="shelf-tag t2">Tier 2 • Multi-Agent Team</span>
            <span class="shelf-desc">Actors, distributed consensus</span>
          </div>
          <div class="parts-grid" id="shelf2-grid">
            <div class="part-item" id="part-durableobjects" draggable="true" ondragstart="onWarehouseDragStart(event, 'durableobjects')">📋 Durable Objects</div>
            <div class="part-item" id="part-quorum" draggable="true" ondragstart="onWarehouseDragStart(event, 'quorum')">⚖️ Quorum Vote</div>
            <div class="part-item" id="part-pubsub" draggable="true" ondragstart="onWarehouseDragStart(event, 'pubsub')">📢 Edge WebSockets</div>
          </div>'''

new_shelf_html = '''          <div class="parts-grid" id="shelf0-grid">
            <div class="part-item active" id="part-nosql" draggable="true" ondragstart="onWarehouseDragStart(event, 'nosql')">📦 OCI NoSQL TTL</div>
            <div class="part-item active" id="part-cache" draggable="true" ondragstart="onWarehouseDragStart(event, 'cache')">🗄️ OCI Cache Redis</div>
            <div class="part-item active" id="part-waf" draggable="true" ondragstart="onWarehouseDragStart(event, 'waf')">🛡️ OCI WAF &amp; Budget</div>
            <div class="part-item active" id="part-functions" draggable="true" ondragstart="onWarehouseDragStart(event, 'functions')">⚙️ OCI Functions</div>
            <div class="part-item active" id="part-genai" draggable="true" ondragstart="onWarehouseDragStart(event, 'genai')">🧠 OCI Generative AI</div>
            <div class="part-item active" id="part-monitoring" draggable="true" ondragstart="onWarehouseDragStart(event, 'monitoring')">📈 OCI Monitoring</div>
          </div>
        </div>

        <!-- Shelf 1 -->
        <div class="shelf">
          <div class="shelf-header">
            <span class="shelf-tag t1">Tier 1 • One Agent Mind</span>
            <span class="shelf-desc">Decide, plan, stateful queues</span>
          </div>
          <div class="parts-grid" id="shelf1-grid">
            <div class="part-item active" id="part-queue" draggable="true" ondragstart="onWarehouseDragStart(event, 'queue')">🚦 OCI Queue</div>
            <div class="part-item active" id="part-process" draggable="true" ondragstart="onWarehouseDragStart(event, 'process')">🔁 Process Automation</div>
            <div class="part-item active" id="part-breaker" draggable="true" ondragstart="onWarehouseDragStart(event, 'breaker')">🔌 Gateway Breaker</div>
            <div class="part-item" id="part-search" draggable="true" ondragstart="onWarehouseDragStart(event, 'search')">🔍 OCI OpenSearch</div>
          </div>
        </div>

        <!-- Shelf 2 -->
        <div class="shelf">
          <div class="shelf-header">
            <span class="shelf-tag t2">Tier 2 • Multi-Agent Team</span>
            <span class="shelf-desc">Actors, distributed consensus</span>
          </div>
          <div class="parts-grid" id="shelf2-grid">
            <div class="part-item" id="part-vault" draggable="true" ondragstart="onWarehouseDragStart(event, 'vault')">📋 OCI Vault HSM</div>
            <div class="part-item" id="part-quorum" draggable="true" ondragstart="onWarehouseDragStart(event, 'quorum')">⚖️ Region Quorum Vote</div>
            <div class="part-item" id="part-events" draggable="true" ondragstart="onWarehouseDragStart(event, 'events')">📢 OCI Events Stream</div>
          </div>'''

html = html.replace(old_shelf_html, new_shelf_html)

# Replace Receipt Header
html = html.replace("CLOUDFLARE ASSEMBLY RECEIPT (BOM)", "ORACLE CLOUD ASSEMBLY RECEIPT (BOM)")
html = html.replace("CLOUDFLARE BILL OF MATERIALS:", "ORACLE CLOUD BILL OF MATERIALS:")

# Replace Tabs
html = html.replace("Test Suite (8 Cloudflare Primitives)", "Test Suite (8 OCI Primitives)")
html = html.replace("Workers AI Softmax", "OCI GenAI Softmax")
html = html.replace("Python Cloudflare SDK Code", "Python OCI SDK Code")

# Replace JS Order Presets & PART_DEFINITIONS
old_js_presets_and_parts = '''  const ORDER_PRESETS = {
    bank: {
      text: "Low-latency Edge Banking QA agent. Never leak customer secrets. D1 atomic transactions and strict WAF rate limiting.",
      type: "Guarded Edge Bank Assistant",
      tier: 1,
      parts: ["kv", "d1", "waf", "workers", "workersai", "workflows", "healthcheck"],
      dep: ["waf", "workers", "kv"],
      trimmed: ["durableobjects", "quorum", "pubsub"],
      assumptions: ["Sub-50ms global response constraint", "No motor external writes without 2FA", "Strict Cloudflare WAF rate limit"],
      risks: ["Cross-site prompt injection (prevented via WAF + isolate memory sandbox)"]
    },
    server: {
      text: "Edge SRE monitoring agent. Drain Queues with visibility deadlines, trigger Workflows with backoff retries, failover pool.",
      type: "Resilient Edge SRE Operator",
      tier: 1,
      parts: ["analytics", "queues", "d1", "workflows", "healthcheck", "workers"],
      dep: ["queues", "healthcheck"],
      trimmed: ["vectorize", "quorum"],
      assumptions: ["Visibility timeout > task execution deadline", "Idempotent event commits in Cloudflare D1"],
      risks: ["Zombie message redelivery (mitigated via visibility lease backoff)"]
    },
    team: {
      text: "Multi-agent swarm running at the edge. Durable Objects synchronized whiteboard, WebSocket broadcasting, and quorum voting.",
      type: "Edge Consensus Multi-Agent Swarm",
      tier: 2,
      parts: ["kv", "pubsub", "workersai", "durableobjects", "workflows", "quorum"],
      dep: ["pubsub", "quorum", "durableobjects"],
      trimmed: [],
      assumptions: ["Distributed multi-agent team", "Durable Objects single-threaded actor storage prevents split-brain state"],
      risks: ["WebSocket connection storms (mitigated via edge queue buffering & DO transaction locks)"]
    },
    careful: {
      text: "Edge Compliance and Financial Auditor. Audit streaming ledger entries, verify against D1 database, purge stale KV records.",
      type: "Edge Compliance Auditor",
      tier: 2,
      parts: ["kv", "d1", "workersai", "workflows", "quorum", "vectorize"],
      dep: ["kv", "quorum"],
      trimmed: ["workers"],
      assumptions: ["Read-only compliance audit", "Parallel edge validation map", "Zero direct mutation authority"],
      risks: ["Stale edge cache reads (prevented via Workers KV TTL + D1 strong consistency)"]
    }
  };

  // Node catalog definition mapped to Cloudflare Platform Primitives
  const PART_DEFINITIONS = {
    kv: { name: "Workers KV TTL", tier: 0, icon: "📦", desc: "Low latency key-value with TTL expiration", out: ["data"], in: [] },
    d1: { name: "Cloudflare D1 SQL", tier: 0, icon: "🗄️", desc: "Serverless relational SQLite with atomic commit", out: ["rows"], in: ["query"] },
    waf: { name: "Edge WAF & Rate", tier: 0, icon: "🛡️", desc: "60 RPM edge rate cap & token budget tripwire", out: ["approved"], in: ["req"] },
    workers: { name: "Workers V8 Isolate", tier: 0, icon: "⚙️", desc: "Zero-cold-start serverless compute sandbox", out: ["res"], in: ["action"] },
    workersai: { name: "Workers AI (Llama 3)", tier: 0, icon: "🧠", desc: "Serverless GPU inference & reasoning", out: ["thought"], in: ["prompt"] },
    analytics: { name: "Analytics Engine", tier: 0, icon: "📈", desc: "High-cardinality telemetry & anomaly metrics", out: ["metrics"], in: ["log"] },
    queues: { name: "Cloudflare Queues", tier: 1, icon: "🚦", desc: "Guaranteed message delivery & visibility delay", out: ["task"], in: ["job"] },
    workflows: { name: "Cloudflare Workflows", tier: 1, icon: "🔁", desc: "Durable multi-step execution & auto retry", out: ["verified"], in: ["exec"] },
    healthcheck: { name: "Health Check Breaker", tier: 1, icon: "🔌", desc: "Origin failure circuit trip & half-open probe", out: ["safe"], in: ["call"] },
    vectorize: { name: "Cloudflare Vectorize", tier: 1, icon: "🔍", desc: "Edge vector database for RAG context search", out: ["chunks"], in: ["embed"] },
    durableobjects: { name: "Durable Objects Actor", tier: 2, icon: "📋", desc: "Stateful actor with transactional in-memory mutex", out: ["state"], in: ["sync"] },
    quorum: { name: "Evidence Quorum Vote", tier: 2, icon: "⚖️", desc: "2/3 edge majority consensus & validation", out: ["consensus"], in: ["votes"] },
    pubsub: { name: "Edge WebSockets", tier: 2, icon: "📢", desc: "Full-duplex real-time broadcasting across swarm", out: ["broadcast"], in: ["publish"] }
  };'''

new_js_presets_and_parts = '''  const ORDER_PRESETS = {
    bank: {
      text: "Production Oracle Cloud Banking QA Agent. Zero secret leaks. OCI NoSQL atomic row locks and strict OCI WAF rate limiting.",
      type: "Guarded OCI Bank Operator",
      tier: 1,
      parts: ["nosql", "cache", "waf", "functions", "genai", "process", "breaker"],
      dep: ["waf", "functions", "nosql"],
      trimmed: ["vault", "quorum", "events"],
      assumptions: ["Sub-50ms OCI local peering latency", "OCI Vault hardware KMS encryption", "Strict OCI WAF rate limiting"],
      risks: ["Prompt injection (prevented via OCI WAF + Compartment IAM isolation)"]
    },
    server: {
      text: "Oracle Cloud SRE Operator. Drain OCI Queues with visibility leases, trigger Process Automation with backoff retries, API Gateway circuit breaker failover.",
      type: "Resilient OCI SRE Operator",
      tier: 1,
      parts: ["monitoring", "queue", "cache", "process", "breaker", "functions"],
      dep: ["queue", "breaker"],
      trimmed: ["search", "quorum"],
      assumptions: ["Visibility timeout > function execution deadline", "Idempotent event commits in OCI NoSQL"],
      risks: ["Tenancy budget overruns (mitigated via OCI Cost Budgets & API Gateway circuit breaker)"]
    },
    team: {
      text: "Autonomous OCI agent swarm. OCI Vault synchronized identity, OCI Events streaming pub/sub, and quorum voting across Cohere models.",
      type: "OCI Consensus Multi-Agent Swarm",
      tier: 2,
      parts: ["nosql", "events", "genai", "vault", "process", "quorum"],
      dep: ["events", "quorum", "vault"],
      trimmed: [],
      assumptions: ["Distributed multi-agent team", "OCI NoSQL ACID row-level locks prevent split-brain state"],
      risks: ["Streaming event backpressure (mitigated via OCI Queue dead-letter channels)"]
    },
    careful: {
      text: "OCI Tenancy Compliance and Financial Auditor. Audit streaming ledger entries, verify against OCI NoSQL history, purge stale cache entries.",
      type: "OCI Compliance Auditor",
      tier: 2,
      parts: ["nosql", "cache", "genai", "process", "quorum", "search"],
      dep: ["nosql", "quorum"],
      trimmed: ["functions"],
      assumptions: ["Read-only compliance audit", "Parallel tenancy verification map", "Zero direct mutation authority"],
      risks: ["Stale cache reads (prevented via OCI NoSQL row TTL + Cache Redis invalidation)"]
    }
  };

  // Node catalog definition mapped to Oracle Cloud (OCI) Platform Primitives
  const PART_DEFINITIONS = {
    nosql: { name: "OCI NoSQL TTL", tier: 0, icon: "📦", desc: "Distributed NoSQL table with row-level TTL expiration and ACID lock", out: ["data"], in: [] },
    cache: { name: "OCI Cache Redis", tier: 0, icon: "🗄️", desc: "Managed in-memory cache with memory decay", out: ["rows"], in: ["query"] },
    waf: { name: "OCI WAF & Budget", tier: 0, icon: "🛡️", desc: "Web application firewall rate limiter & tenancy budget cap", out: ["approved"], in: ["req"] },
    functions: { name: "OCI Functions", tier: 0, icon: "⚙️", desc: "Zero-maintenance Fn Project serverless containers", out: ["res"], in: ["action"] },
    genai: { name: "OCI Generative AI", tier: 0, icon: "🧠", desc: "Dedicated AI cluster inference and enterprise reasoning", out: ["thought"], in: ["prompt"] },
    monitoring: { name: "OCI Monitoring", tier: 0, icon: "📈", desc: "Real-time metrics, alarms, and service connector telemetry", out: ["metrics"], in: ["log"] },
    queue: { name: "OCI Queue Messaging", tier: 1, icon: "🚦", desc: "High-throughput messaging queue with visibility timeout", out: ["task"], in: ["job"] },
    process: { name: "OCI Process Automate", tier: 1, icon: "🔁", desc: "Stateful orchestrator with automated retries and dead-letter handling", out: ["verified"], in: ["exec"] },
    breaker: { name: "API Gateway Breaker", tier: 1, icon: "🔌", desc: "API Gateway failure rate outlier breaker & health probe", out: ["safe"], in: ["call"] },
    search: { name: "OCI OpenSearch Vector", tier: 1, icon: "🔍", desc: "Managed semantic search & vector indexing for RAG", out: ["chunks"], in: ["embed"] },
    vault: { name: "OCI Vault Secret HSM", tier: 2, icon: "📋", desc: "KMS hardware security module & agent identity tokens", out: ["state"], in: ["sync"] },
    quorum: { name: "Region Quorum Vote", tier: 2, icon: "⚖️", desc: "2/3 cross-region fault-tolerant consensus & validation", out: ["consensus"], in: ["votes"] },
    events: { name: "OCI Events Streaming", tier: 2, icon: "📢", desc: "CloudEvents-compliant streaming event bus across agent fleet", out: ["broadcast"], in: ["publish"] }
  };'''

html = html.replace(old_js_presets_and_parts, new_js_presets_and_parts)

# Replace JS Classes
html = html.replace("SimWorkersKV", "SimOciNoSql")
html = html.replace("SimD1Database", "SimOciCacheRedis")
html = html.replace("SimEdgeWAFAndBudget", "SimOciWafAndBudget")
html = html.replace("SimCloudflareQueues", "SimOciQueue")
html = html.replace("SimEdgePriorityWorker", "SimOciPriorityWorker")
html = html.replace("SimCloudflareWorkflows", "SimOciProcessAutomation")
html = html.replace("SimCloudflareHealthBreaker", "SimOciCircuitBreaker")
html = html.replace("SimDurableObjectActor", "SimOciVaultActor")
html = html.replace("SimWorkersAI", "SimOciGenAI")

# Replace Reason & String labels in Sim
html = html.replace("Cloudflare WAF 1015: Rate Limit Exceeded", "OCI WAF 429: Rate Limit Exceeded")
html = html.replace("Structured Cloudflare Edge Blueprint", "Structured OCI Cloud Blueprint")
html = html.replace("Creative Zero-Trust Access Strategy", "Creative OCI IAM Compartment Policy")
html = html.replace("Balanced Global Cache Rule", "Balanced OCI Cache Redis Sharding")
html = html.replace("Lateral Durable Object Decomposition", "Lateral OCI Process Automation Decomposition")
html = html.replace("Cautious WAF Firewall Guardrail", "Cautious OCI Network Security Guardrail")

# Replace Sim Tests
old_tests = '''  const SIM_TESTS = [
    {
      id: "test1",
      name: "1. Workers KV TTL & Sweep",
      tool: "Workers KV",
      cloud: "Cloudflare Workers KV",
      rule: "kv.get('session') returns None after clock.advance(11); sweep purges expired keys",
      run: () => {
        const c = new SimClock();
        const kv = new SimWorkersKV(c);
        kv.put("session", "user_123", 10);
        c.advance(11);
        const hidden = kv.get("session") === null;
        const storedBeforeSweep = kv.get("session", false) !== null;
        const swept = kv.sweep() === 1;
        return hidden && storedBeforeSweep && swept;
      }
    },
    {
      id: "test2",
      name: "2. D1 SQL Atomic Transaction",
      tool: "Cloudflare D1",
      cloud: "Cloudflare D1 SQLite",
      rule: "atomic update succeeds; second concurrent attempt with invalid condition aborts",
      run: () => {
        const d1 = new SimD1Database();
        d1.execute_transaction("locks", "lease-1", { owner: "agent_A" }, cur => !cur);
        let secondFailed = false;
        try {
          d1.execute_transaction("locks", "lease-1", { owner: "agent_B" }, cur => !cur);
        } catch (e) {
          secondFailed = true;
        }
        return secondFailed && d1.query("locks", "lease-1").owner === "agent_A";
      }
    },
    {
      id: "test3",
      name: "3. Durable Objects Context Alarm",
      tool: "Durable Objects",
      cloud: "Cloudflare Durable Objects",
      rule: "in-memory actor state active at 60s; alarm decay clears memory at 121s",
      run: () => {
        const c = new SimClock();
        const doActor = new SimDurableObjectActor(c);
        doActor.set_memory("scratchpad", "context_state", 120);
        c.advance(60);
        const ok60 = doActor.get_memory("scratchpad") === "context_state";
        c.advance(65);
        const expired125 = doActor.get_memory("scratchpad") === null;
        return ok60 && expired125;
      }
    },
    {
      id: "test4",
      name: "4. Edge WAF & Budget Cap",
      tool: "Edge WAF",
      cloud: "Cloudflare WAF & Rules",
      rule: "request 61 blocked by WAF 1015; spend > $10.00 trips edge budget circuit",
      run: () => {
        const c = new SimClock();
        const waf = new SimEdgeWAFAndBudget(c, 10, 1.0);
        for (let i = 0; i < 10; i++) waf.allow_request(0.05);
        const blockedRpm = !waf.allow_request(0.05).ok;
        c.advance(65);
        const allowAgain = waf.allow_request(0.40).ok;
        const blockedBudget = !waf.allow_request(0.20).ok;
        return blockedRpm && allowAgain && blockedBudget;
      }
    },
    {
      id: "test5",
      name: "5. Queues Visibility Delay",
      tool: "Cloudflare Queues",
      cloud: "Cloudflare Queues",
      rule: "unacknowledged message becomes invisible for 30s timeout, then reappears",
      run: () => {
        const c = new SimClock();
        const q = new SimCloudflareQueues(c);
        q.send("edge_jobs", "ProcessInvoice");
        const m1 = q.receive("edge_jobs", 30);
        const m1Hidden = q.receive("edge_jobs", 30) === null;
        c.advance(35);
        const m1Reappears = q.receive("edge_jobs", 30) === "ProcessInvoice";
        return m1 === "ProcessInvoice" && m1Hidden && m1Reappears;
      }
    },
    {
      id: "test6",
      name: "6. Priority Worker (Critical 1st)",
      tool: "PriorityWorker",
      cloud: "Cloudflare Queues",
      rule: "critical queue drained before normal queue, batch queue drained last",
      run: () => {
        const c = new SimClock();
        const q = new SimCloudflareQueues(c);
        const w = new SimEdgePriorityWorker(q);
        q.send("batch", "batch_task");
        q.send("critical", "urgent_task");
        q.send("normal", "regular_task");
        const first = w.next();
        const second = w.next();
        const third = w.next();
        return first.message === "urgent_task" && second.message === "regular_task" && third.message === "batch_task";
      }
    },
    {
      id: "test7",
      name: "7. Workflows Retries & Fallback",
      tool: "Cloudflare Workflows",
      cloud: "Cloudflare Workflows",
      rule: "step retried 2 times on transient edge failure, fallback invoked cleanly",
      run: () => {
        const wf = new SimCloudflareWorkflows();
        let failCount = 0;
        const step = () => {
          failCount++;
          if (failCount < 3) throw new Error("Transient edge network glitch");
          return "success_recovered";
        };
        const res = wf.execute_step_with_retry(step, 2);
        return res.success && res.attempts === 3 && res.result === "success_recovered";
      }
    },
    {
      id: "test8",
      name: "8. Origin Health Circuit Breaker",
      tool: "HealthBreaker",
      cloud: "Cloudflare Health Checks",
      rule: "3 failures trip breaker to OPEN; 60s cooldown transitions to HALF-OPEN",
      run: () => {
        const c = new SimClock();
        const b = new SimCloudflareHealthBreaker(c, 3, 60);
        b.record_failure(); b.record_failure();
        const stillClosed = b.can_call();
        b.record_failure(); // 3rd failure trips
        const nowOpen = !b.can_call();
        c.advance(65);
        const halfOpen = b.can_call();
        b.record_success();
        const resetClosed = b.state === "CLOSED";
        return stillClosed && nowOpen && halfOpen && resetClosed;
      }
    }
  ];'''

new_tests = '''  const SIM_TESTS = [
    {
      id: "test1",
      name: "1. OCI NoSQL Row TTL & Sweep",
      tool: "OCI NoSQL",
      cloud: "Oracle Cloud NoSQL",
      rule: "nosql.get('session') returns None after clock.advance(11); sweep purges expired rows",
      run: () => {
        const c = new SimClock();
        const kv = new SimOciNoSql(c);
        kv.put("session", "user_123", 10);
        c.advance(11);
        const hidden = kv.get("session") === null;
        const storedBeforeSweep = kv.get("session", false) !== null;
        const swept = kv.sweep() === 1;
        return hidden && storedBeforeSweep && swept;
      }
    },
    {
      id: "test2",
      name: "2. OCI Cache Atomic Lock",
      tool: "OCI Cache Redis",
      cloud: "Oracle Cloud Cache with Redis",
      rule: "atomic update succeeds; second concurrent attempt with invalid condition aborts",
      run: () => {
        const d1 = new SimOciCacheRedis();
        d1.execute_transaction("locks", "lease-1", { owner: "agent_A" }, cur => !cur);
        let secondFailed = false;
        try {
          d1.execute_transaction("locks", "lease-1", { owner: "agent_B" }, cur => !cur);
        } catch (e) {
          secondFailed = true;
        }
        return secondFailed && d1.query("locks", "lease-1").owner === "agent_A";
      }
    },
    {
      id: "test3",
      name: "3. Ephemeral Cache Context Alarm",
      tool: "OCI Cache Memory",
      cloud: "Oracle Cloud Cache",
      rule: "in-memory actor state active at 60s; context decay clears memory at 121s",
      run: () => {
        const c = new SimClock();
        const doActor = new SimOciVaultActor(c);
        doActor.set_memory("scratchpad", "context_state", 120);
        c.advance(60);
        const ok60 = doActor.get_memory("scratchpad") === "context_state";
        c.advance(65);
        const expired125 = doActor.get_memory("scratchpad") === null;
        return ok60 && expired125;
      }
    },
    {
      id: "test4",
      name: "4. OCI WAF & Budget Cap",
      tool: "OCI WAF",
      cloud: "Oracle Cloud WAF & Budgets",
      rule: "request 61 blocked by OCI WAF; spend > $10.00 trips tenancy budget circuit",
      run: () => {
        const c = new SimClock();
        const waf = new SimOciWafAndBudget(c, 10, 1.0);
        for (let i = 0; i < 10; i++) waf.allow_request(0.05);
        const blockedRpm = !waf.allow_request(0.05).ok;
        c.advance(65);
        const allowAgain = waf.allow_request(0.40).ok;
        const blockedBudget = !waf.allow_request(0.20).ok;
        return blockedRpm && allowAgain && blockedBudget;
      }
    },
    {
      id: "test5",
      name: "5. OCI Queue Visibility Delay",
      tool: "OCI Queue",
      cloud: "Oracle Cloud Queue Service",
      rule: "unacknowledged message becomes invisible for 30s timeout, then reappears",
      run: () => {
        const c = new SimClock();
        const q = new SimOciQueue(c);
        q.send("oci_jobs", "ProcessInvoice");
        const m1 = q.receive("oci_jobs", 30);
        const m1Hidden = q.receive("oci_jobs", 30) === null;
        c.advance(35);
        const m1Reappears = q.receive("oci_jobs", 30) === "ProcessInvoice";
        return m1 === "ProcessInvoice" && m1Hidden && m1Reappears;
      }
    },
    {
      id: "test6",
      name: "6. Priority Worker (Critical 1st)",
      tool: "PriorityWorker",
      cloud: "Oracle Cloud Queue",
      rule: "critical queue drained before normal queue, batch queue drained last",
      run: () => {
        const c = new SimClock();
        const q = new SimOciQueue(c);
        const w = new SimOciPriorityWorker(q);
        q.send("batch", "batch_task");
        q.send("critical", "urgent_task");
        q.send("normal", "regular_task");
        const first = w.next();
        const second = w.next();
        const third = w.next();
        return first.message === "urgent_task" && second.message === "regular_task" && third.message === "batch_task";
      }
    },
    {
      id: "test7",
      name: "7. Process Automation Retries & Fallback",
      tool: "ProcessAutomation",
      cloud: "Oracle Cloud Process Automation",
      rule: "step retried 2 times on transient cloud failure, fallback invoked cleanly",
      run: () => {
        const wf = new SimOciProcessAutomation();
        let failCount = 0;
        const step = () => {
          failCount++;
          if (failCount < 3) throw new Error("Transient OCI gateway network glitch");
          return "success_recovered";
        };
        const res = wf.execute_step_with_retry(step, 2);
        return res.success && res.attempts === 3 && res.result === "success_recovered";
      }
    },
    {
      id: "test8",
      name: "8. API Gateway Circuit Breaker",
      tool: "GatewayBreaker",
      cloud: "Oracle Cloud API Gateway",
      rule: "3 failures trip breaker to OPEN; 60s cooldown transitions to HALF-OPEN",
      run: () => {
        const c = new SimClock();
        const b = new SimOciCircuitBreaker(c, 3, 60);
        b.record_failure(); b.record_failure();
        const stillClosed = b.can_call();
        b.record_failure(); // 3rd failure trips
        const nowOpen = !b.can_call();
        c.advance(65);
        const halfOpen = b.can_call();
        b.record_success();
        const resetClosed = b.state === "CLOSED";
        return stillClosed && nowOpen && halfOpen && resetClosed;
      }
    }
  ];'''

html = html.replace(old_tests, new_tests)

# Replace Python Code Template in JS
old_python_fn = '''  function updateGeneratedPythonCode(assembly) {
    const code = `#!/usr/bin/env python3
# ==============================================================================
# The AI Agent Factory • Cloudflare Workers Edge Platform
# Assembled Agent: ${assembly.agentType}
# Target Architecture: Tier ${assembly.tier} (${assembly.tier === 2 ? 'Multi-Agent Team' : 'Single Agent'})
# Flow Nodes: ${flowGraph.nodes.length} | Connections: ${flowGraph.connections.length}
# Executable Cloudflare Edge Python Simulator running via Pyodide in Browser
# ==============================================================================

import time
import math
import random

class Clock:
    def __init__(self):
        self.now = 0.0
    def advance(self, seconds: float):
        self.now += seconds

class CloudflareWorkersKV:
    """Simulates Cloudflare Workers KV with TTL Expiration."""
    def __init__(self, clock):
        self.clock = clock
        self.store = {}

    def put(self, key: str, val: str, ttl: float = 60.0):
        self.store[key] = {"val": val, "expire_at": self.clock.now + ttl}

    def get(self, key: str, filter_expired: bool = True):
        entry = self.store.get(key)
        if not entry:
            return None
        if filter_expired and entry["expire_at"] <= self.clock.now:
            return None # Expired by Workers KV engine
        return entry["val"]

    def sweep(self) -> int:
        expired = [k for k, v in self.store.items() if v["expire_at"] <= self.clock.now]
        for k in expired:
            del self.store[k]
        return len(expired)

class CloudflareD1Database:
    """Simulates Cloudflare D1 Relational SQLite with Atomic Commits."""
    def __init__(self):
        self.tables = {}

    def execute_transaction(self, table: str, key: str, record: dict, condition=None):
        self.tables.setdefault(table, {})
        cur = self.tables[table].get(key)
        if condition and not condition(cur):
            raise RuntimeError(f"D1_TRANSACTION_FAILED: Condition check failed for {key}")
        version = (cur["version"] + 1) if cur else 1
        self.tables[table][key] = {**record, "version": version}
        return self.tables[table][key]

    def query(self, table: str, key: str):
        return self.tables.get(table, {}).get(key)

class CloudflareQueues:
    """Simulates Cloudflare Queues with Guaranteed Visibility Leases."""
    def __init__(self, clock):
        self.clock = clock
        self.queues = {}

    def send(self, queue: str, message: str, delay_seconds: float = 0.0):
        self.queues.setdefault(queue, []).append({
            "body": message,
            "visible_at": self.clock.now + delay_seconds
        })

    def receive(self, queue: str, visibility_timeout: float = 30.0):
        for m in self.queues.get(queue, []):
            if m["visible_at"] <= self.clock.now:
                m["visible_at"] = self.clock.now + visibility_timeout
                return m["body"]
        return None

class EdgePriorityWorker:
    def __init__(self, queues, priority_order=["critical", "normal", "batch"]):
        self.queues = queues
        self.priority_order = priority_order

    def next(self):
        for q in self.priority_order:
            msg = self.queues.receive(q)
            if msg:
                return q, msg
        return None, None

class HealthCheckBreaker:
    """Cloudflare Health Check Origin Circuit Breaker."""
    def __init__(self, clock, threshold=3, cooldown=60.0):
        self.clock = clock
        self.threshold = threshold
        self.cooldown = cooldown
        self.failures = 0
        self.last_fail = 0.0
        self.state = "CLOSED"

    def record_failure(self):
        self.failures += 1
        self.last_fail = self.clock.now
        if self.failures >= self.threshold:
            self.state = "OPEN"

    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"

    def can_call(self) -> bool:
        if self.state == "CLOSED": return True
        if self.state == "OPEN":
            if self.clock.now - self.last_fail >= self.cooldown:
                self.state = "HALF-OPEN"
                return True
            return False
        return True

# ------------------------------------------------------------------------------
# Assembled Edge Agent System: ${assembly.agentType}
# ------------------------------------------------------------------------------
class AssembledCloudflareAgentSystem:
    def __init__(self):
        self.clock = Clock()
        self.kv = CloudflareWorkersKV(self.clock)
        self.d1 = CloudflareD1Database()
        self.queues = CloudflareQueues(self.clock)
        self.worker = EdgePriorityWorker(self.queues)
        self.breaker = HealthCheckBreaker(self.clock)
        self.invariants = ${JSON.stringify(assembly.assumptions)}

    def handle_request(self, payload: str):
        # 1. Evaluate Cloudflare Health Breaker
        if not self.breaker.can_call():
            return {"status": "TRIPPED", "error": "Health Breaker OPEN. Origin circuit tripped."}

        # 2. Enqueue in Cloudflare Queues (Critical queue)
        self.queues.send("critical", payload)
        queue_name, task = self.worker.next()

        # 3. Commit Atomic State in Cloudflare D1
        d1_record = self.d1.execute_transaction("transactions", "tx-001", {
            "task": task,
            "status": "COMMITTED"
        }, lambda cur: cur is None)

        return {
            "agent": "${assembly.agentType}",
            "edge_network": "Cloudflare Global Anycast",
            "queue": queue_name,
            "task": task,
            "d1_version": d1_record["version"],
            "status": "SUCCESS",
            "invariants_checked": True
        }

if __name__ == "__main__":
    agent = AssembledCloudflareAgentSystem()
    result = agent.handle_request("${assembly.orderText}")
    print("Cloudflare Edge Agent Result:", result)
`;
    document.getElementById("codeViewer").textContent = code;
  }'''

new_python_fn = '''  function updateGeneratedPythonCode(assembly) {
    const code = `#!/usr/bin/env python3
# ==============================================================================
# The AI Agent Factory • Oracle Cloud (OCI) Enterprise Platform
# Assembled Agent: ${assembly.agentType}
# Target Architecture: Tier ${assembly.tier} (${assembly.tier === 2 ? 'Multi-Agent Team' : 'Single Agent'})
# Flow Nodes: ${flowGraph.nodes.length} | Connections: ${flowGraph.connections.length}
# Executable Oracle Cloud OCI Python Simulator running via Pyodide in Browser
# ==============================================================================

import time
import math
import random

class Clock:
    def __init__(self):
        self.now = 0.0
    def advance(self, seconds: float):
        self.now += seconds

class OciNoSqlDatabase:
    """Simulates OCI NoSQL Table with Row-Level TTL Expiration."""
    def __init__(self, clock):
        self.clock = clock
        self.store = {}

    def put(self, key: str, val: str, ttl: float = 60.0):
        self.store[key] = {"val": val, "expire_at": self.clock.now + ttl}

    def get(self, key: str, filter_expired: bool = True):
        entry = self.store.get(key)
        if not entry:
            return None
        if filter_expired and entry["expire_at"] <= self.clock.now:
            return None # Expired by OCI NoSQL engine
        return entry["val"]

    def sweep(self) -> int:
        expired = [k for k, v in self.store.items() if v["expire_at"] <= self.clock.now]
        for k in expired:
            del self.store[k]
        return len(expired)

class OciCacheRedis:
    """Simulates OCI Cache with Redis Atomic Operations & Transactions."""
    def __init__(self):
        self.tables = {}

    def execute_transaction(self, table: str, key: str, record: dict, condition=None):
        self.tables.setdefault(table, {})
        cur = self.tables[table].get(key)
        if condition and not condition(cur):
            raise RuntimeError(f"OCI_CACHE_TRANSACTION_FAILED: Condition check failed for {key}")
        version = (cur["version"] + 1) if cur else 1
        self.tables[table][key] = {**record, "version": version}
        return self.tables[table][key]

    def query(self, table: str, key: str):
        return self.tables.get(table, {}).get(key)

class OciQueueService:
    """Simulates OCI Queue Service with Visibility Leases."""
    def __init__(self, clock):
        self.clock = clock
        self.queues = {}

    def send(self, queue: str, message: str, delay_seconds: float = 0.0):
        self.queues.setdefault(queue, []).append({
            "body": message,
            "visible_at": self.clock.now + delay_seconds
        })

    def receive(self, queue: str, visibility_timeout: float = 30.0):
        for m in self.queues.get(queue, []):
            if m["visible_at"] <= self.clock.now:
                m["visible_at"] = self.clock.now + visibility_timeout
                return m["body"]
        return None

class OciPriorityWorker:
    def __init__(self, queues, priority_order=["critical", "normal", "batch"]):
        self.queues = queues
        self.priority_order = priority_order

    def next(self):
        for q in self.priority_order:
            msg = self.queues.receive(q)
            if msg:
                return q, msg
        return None, None

class OciGatewayCircuitBreaker:
    """OCI API Gateway Circuit Breaker."""
    def __init__(self, clock, threshold=3, cooldown=60.0):
        self.clock = clock
        self.threshold = threshold
        self.cooldown = cooldown
        self.failures = 0
        self.last_fail = 0.0
        self.state = "CLOSED"

    def record_failure(self):
        self.failures += 1
        self.last_fail = self.clock.now
        if self.failures >= self.threshold:
            self.state = "OPEN"

    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"

    def can_call(self) -> bool:
        if self.state == "CLOSED": return True
        if self.state == "OPEN":
            if self.clock.now - self.last_fail >= self.cooldown:
                self.state = "HALF-OPEN"
                return True
            return False
        return True

# ------------------------------------------------------------------------------
# Assembled OCI Agent System: ${assembly.agentType}
# ------------------------------------------------------------------------------
class AssembledOciAgentSystem:
    def __init__(self):
        self.clock = Clock()
        self.nosql = OciNoSqlDatabase(self.clock)
        self.cache = OciCacheRedis()
        self.queues = OciQueueService(self.clock)
        self.worker = OciPriorityWorker(self.queues)
        self.breaker = OciGatewayCircuitBreaker(self.clock)
        self.invariants = ${JSON.stringify(assembly.assumptions)}

    def handle_request(self, payload: str):
        # 1. Evaluate OCI Gateway Breaker
        if not self.breaker.can_call():
            return {"status": "TRIPPED", "error": "Gateway Breaker OPEN. Origin circuit tripped."}

        # 2. Enqueue in OCI Queue (Critical queue)
        self.queues.send("critical", payload)
        queue_name, task = self.worker.next()

        # 3. Commit Atomic State in OCI Cache Redis
        cache_record = self.cache.execute_transaction("transactions", "tx-001", {
            "task": task,
            "status": "COMMITTED"
        }, lambda cur: cur is None)

        return {
            "agent": "${assembly.agentType}",
            "cloud_region": "Oracle Cloud Infrastructure (OCI) us-ashburn-1",
            "queue": queue_name,
            "task": task,
            "cache_version": cache_record["version"],
            "status": "SUCCESS",
            "invariants_checked": True
        }

if __name__ == "__main__":
    agent = AssembledOciAgentSystem()
    result = agent.handle_request("${assembly.orderText}")
    print("Oracle Cloud Agent Result:", result)
`;
    document.getElementById("codeViewer").textContent = code;
  }'''

html = html.replace(old_python_fn, new_python_fn)

# Replace copy toast and log event names
html = html.replace("Cloudflare Python code copied to clipboard!", "Oracle Cloud Python code copied to clipboard!")
html = html.replace("logCloudflareEvent", "logOciEvent")

with open("ai_factory_oci_simulator.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully written ai_factory_oci_simulator.html!")
