# -*- coding: utf-8 -*-
"""
generate_kubernetes_simulator.py
Builds the complete `ai_factory_kubernetes_simulator.html` with Kubernetes cloud-native primitives,
WebLLM/WebGPU, Groq LPU, Pyodide tests, and interactive canvas.
"""

import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open("ai_factory_cloudflare_simulator.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace Page Title & Theme
html = html.replace("The AI Agent Factory • In-Browser Cloudflare Simulator",
                    "The AI Agent Factory • In-Browser Kubernetes Simulator")
html = html.replace("--accent: #F6821F; /* Cloudflare Orange */",
                    "--accent: #326CE5; /* Kubernetes Blue */")
html = html.replace("--accent-light: #FFF1E5;", "--accent-light: #EBF2FF;")
html = html.replace("--accent-dark: #D96500;", "--accent-dark: #1A4CB0;")
html = html.replace("--cf-gold: #FAAD3F;", "--k8s-cyan: #39B54A;")
html = html.replace("--accent: #F6821F;", "--accent: #326CE5;")
html = html.replace("rgba(246, 130, 31, 0.16)", "rgba(50, 108, 229, 0.16)")
html = html.replace("rgba(246, 130, 31, 0.15)", "rgba(50, 108, 229, 0.15)")
html = html.replace("linear-gradient(135deg, #F6821F, #FAAD3F)", "linear-gradient(135deg, #326CE5, #2251B5)")
html = html.replace("linear-gradient(135deg, #F6821F 0%, #FAAD3F 100%)", "linear-gradient(135deg, #326CE5 0%, #2251B5 100%)")

# Replace Navbar & Branding
html = html.replace('<span class="cf-tag">Cloudflare Edge</span>', '<span class="cf-tag" style="background:#EBF2FF;color:#326CE5;border:1px solid rgba(50,108,229,0.3);">Kubernetes K8s</span>')
html = html.replace("Assembly Robot • Workers, D1 &amp; Durable Objects • In-Browser Python Wasm (PyScript / Pyodide)",
                    "Assembly Robot • Envoy, etcd &amp; Knative • In-Browser Python Wasm (PyScript / Pyodide)")
html = html.replace("Browser-Native Cloudflare Simulator State", "Browser-Native Kubernetes Simulator State")

# Replace Preset Chips
html = html.replace("🛡️ Cloudflare FinTech (KV &amp; WAF)", "🛡️ K8s FinTech (etcd &amp; Envoy)")
html = html.replace("⚡ Cloudflare SRE (Workflows &amp; Queues)", "⚡ K8s SRE (Argo &amp; RabbitMQ)")
html = html.replace("🤝 Edge Swarm (Durable Objects &amp; WS)", "🤝 Pod Swarm (CRD &amp; CloudEvents)")
html = html.replace("⚖️ Edge Auditor (D1 &amp; Quorum)", "⚖️ Pod Auditor (etcd &amp; Quorum)")

# Replace 7 Steps text
html = html.replace("Cloudflare BOM", "Kubernetes BOM")
html = html.replace("Cloudflare edge primitives", "Kubernetes cloud-native primitives")
html = html.replace("3-Shelf Cloudflare Parts Warehouse", "3-Shelf Kubernetes Parts Warehouse")

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
            <div class="part-item active" id="part-etcd" draggable="true" ondragstart="onWarehouseDragStart(event, 'etcd')">📦 etcd Lease</div>
            <div class="part-item active" id="part-redis" draggable="true" ondragstart="onWarehouseDragStart(event, 'redis')">🗄️ Redis Cache</div>
            <div class="part-item active" id="part-envoy" draggable="true" ondragstart="onWarehouseDragStart(event, 'envoy')">🛡️ Envoy Rate Limit</div>
            <div class="part-item active" id="part-knative" draggable="true" ondragstart="onWarehouseDragStart(event, 'knative')">⚙️ Knative Serving</div>
            <div class="part-item active" id="part-vllm" draggable="true" ondragstart="onWarehouseDragStart(event, 'vllm')">🧠 vLLM / Ollama</div>
            <div class="part-item active" id="part-otel" draggable="true" ondragstart="onWarehouseDragStart(event, 'otel')">📈 OpenTelemetry</div>
          </div>
        </div>

        <!-- Shelf 1 -->
        <div class="shelf">
          <div class="shelf-header">
            <span class="shelf-tag t1">Tier 1 • One Agent Mind</span>
            <span class="shelf-desc">Decide, plan, stateful queues</span>
          </div>
          <div class="parts-grid" id="shelf1-grid">
            <div class="part-item active" id="part-rabbitmq" draggable="true" ondragstart="onWarehouseDragStart(event, 'rabbitmq')">🚦 RabbitMQ Queue</div>
            <div class="part-item active" id="part-argo" draggable="true" ondragstart="onWarehouseDragStart(event, 'argo')">🔁 Argo Workflows</div>
            <div class="part-item active" id="part-breaker" draggable="true" ondragstart="onWarehouseDragStart(event, 'breaker')">🔌 Envoy Breaker</div>
            <div class="part-item" id="part-qdrant" draggable="true" ondragstart="onWarehouseDragStart(event, 'qdrant')">🔍 Qdrant Vector</div>
          </div>
        </div>

        <!-- Shelf 2 -->
        <div class="shelf">
          <div class="shelf-header">
            <span class="shelf-tag t2">Tier 2 • Multi-Agent Team</span>
            <span class="shelf-desc">Actors, distributed consensus</span>
          </div>
          <div class="parts-grid" id="shelf2-grid">
            <div class="part-item" id="part-crd" draggable="true" ondragstart="onWarehouseDragStart(event, 'crd')">📋 K8s Operator CRD</div>
            <div class="part-item" id="part-quorum" draggable="true" ondragstart="onWarehouseDragStart(event, 'quorum')">⚖️ Pod Quorum Vote</div>
            <div class="part-item" id="part-cloudevents" draggable="true" ondragstart="onWarehouseDragStart(event, 'cloudevents')">📢 CloudEvents Bus</div>
          </div>'''

html = html.replace(old_shelf_html, new_shelf_html)

# Replace Receipt Header
html = html.replace("CLOUDFLARE ASSEMBLY RECEIPT (BOM)", "KUBERNETES ASSEMBLY RECEIPT (BOM)")
html = html.replace("CLOUDFLARE BILL OF MATERIALS:", "KUBERNETES BILL OF MATERIALS:")

# Replace Tabs
html = html.replace("Test Suite (8 Cloudflare Primitives)", "Test Suite (8 K8s Primitives)")
html = html.replace("Workers AI Softmax", "vLLM Softmax")
html = html.replace("Python Cloudflare SDK Code", "Python Kubernetes SDK Code")

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
      text: "Production K8s Banking QA Agent. Zero secret leaks. etcd Raft distributed lease locks and Envoy Gateway token-bucket rate limiting.",
      type: "Guarded K8s Bank Operator",
      tier: 1,
      parts: ["etcd", "redis", "envoy", "knative", "vllm", "argo", "breaker"],
      dep: ["envoy", "knative", "etcd"],
      trimmed: ["crd", "quorum", "cloudevents"],
      assumptions: ["Sub-50ms cluster response constraint", "Zero unauthorized state mutations", "Strict Envoy token-bucket rate limit"],
      risks: ["Pod prompt injection (prevented via Envoy WAF filter + gVisor sandboxing)"]
    },
    server: {
      text: "Kubernetes Cluster SRE Operator. Drain RabbitMQ priority queues, trigger Argo Workflows with backoff retries, Envoy circuit breaker failover.",
      type: "Resilient K8s Cluster SRE Operator",
      tier: 1,
      parts: ["otel", "rabbitmq", "redis", "argo", "breaker", "knative"],
      dep: ["rabbitmq", "breaker"],
      trimmed: ["qdrant", "quorum"],
      assumptions: ["Visibility timeout > pod execution deadline", "Idempotent pod retries via Redis lease locks"],
      risks: ["CrashLoopBackOff cascades (mitigated via Envoy circuit breaker & dead-letter queue)"]
    },
    team: {
      text: "Autonomous multi-pod agent swarm running on K8s. Redis Cluster distributed whiteboard, CloudEvents pub/sub, and quorum voting across pods.",
      type: "K8s CloudEvents Multi-Pod Swarm",
      tier: 2,
      parts: ["etcd", "cloudevents", "vllm", "crd", "argo", "quorum"],
      dep: ["cloudevents", "quorum", "crd"],
      trimmed: [],
      assumptions: ["Distributed multi-pod agent team", "etcd Raft leader election prevents split-brain state"],
      risks: ["Event storm cascades (mitigated via Knative Eventing broker & backpressure buffering)"]
    },
    careful: {
      text: "Cluster Security & Compliance Auditor. Audit streaming pod logs, verify against etcd state, purge stale Redis lease records.",
      type: "K8s Compliance & Pod Auditor",
      tier: 2,
      parts: ["etcd", "redis", "vllm", "argo", "quorum", "qdrant"],
      dep: ["etcd", "quorum"],
      trimmed: ["knative"],
      assumptions: ["Read-only cluster compliance audit", "Parallel pod verification map", "Zero direct mutation authority"],
      risks: ["Stale cache reads (prevented via etcd Raft leases + Redis TTL expiration)"]
    }
  };

  // Node catalog definition mapped to Kubernetes Platform Primitives
  const PART_DEFINITIONS = {
    etcd: { name: "etcd Raft TTL Lease", tier: 0, icon: "📦", desc: "Distributed key-value store with TTL lease & watch API", out: ["data"], in: [] },
    redis: { name: "Redis Cluster Cache", tier: 0, icon: "🗄️", desc: "In-memory working memory with exponential TTL decay", out: ["rows"], in: ["query"] },
    envoy: { name: "Envoy Gateway Rate", tier: 0, icon: "🛡️", desc: "Token bucket rate limiter & ingress gatekeeper", out: ["approved"], in: ["req"] },
    knative: { name: "Knative Serving Pod", tier: 0, icon: "⚙️", desc: "Zero-scale serverless pod execution container", out: ["res"], in: ["action"] },
    vllm: { name: "vLLM / Ollama Operator", tier: 0, icon: "🧠", desc: "Self-hosted GPU LLM inference engine & reasoning", out: ["thought"], in: ["prompt"] },
    otel: { name: "Prometheus & OpenTelemetry", tier: 0, icon: "📈", desc: "Cluster-wide SLI/SLO metrics & trace collector", out: ["metrics"], in: ["log"] },
    rabbitmq: { name: "RabbitMQ / Pulsar Queue", tier: 1, icon: "🚦", desc: "Dead-letter queues & visibility timeout preemption", out: ["task"], in: ["job"] },
    argo: { name: "Argo Workflows / Temporal", tier: 1, icon: "🔁", desc: "Durable DAG execution & automatic exponential retry", out: ["verified"], in: ["exec"] },
    breaker: { name: "Envoy Circuit Breaker", tier: 1, icon: "🔌", desc: "Outlier detection & 3-failure trip / half-open probe", out: ["safe"], in: ["call"] },
    qdrant: { name: "Qdrant / Milvus Operator", tier: 1, icon: "🔍", desc: "Cloud-native vector database for semantic RAG", out: ["chunks"], in: ["embed"] },
    crd: { name: "K8s Custom Resource (CRD)", tier: 2, icon: "📋", desc: "Declarative operator controller with reconcile loop", out: ["state"], in: ["sync"] },
    quorum: { name: "Raft Pod Quorum Consensus", tier: 2, icon: "⚖️", desc: "2/3 cluster majority consensus & validation", out: ["consensus"], in: ["votes"] },
    cloudevents: { name: "Knative Eventing Bus", tier: 2, icon: "📢", desc: "CloudEvents Broker & Trigger pub/sub across pods", out: ["broadcast"], in: ["publish"] }
  };'''

html = html.replace(old_js_presets_and_parts, new_js_presets_and_parts)

# Replace JS Classes
html = html.replace("SimWorkersKV", "SimEtcdLease")
html = html.replace("SimD1Database", "SimRedisCluster")
html = html.replace("SimEdgeWAFAndBudget", "SimEnvoyRateLimiter")
html = html.replace("SimCloudflareQueues", "SimK8sPriorityQueue")
html = html.replace("SimEdgePriorityWorker", "SimK8sPriorityWorker")
html = html.replace("SimCloudflareWorkflows", "SimArgoWorkflows")
html = html.replace("SimCloudflareHealthBreaker", "SimEnvoyCircuitBreaker")
html = html.replace("SimDurableObjectActor", "SimK8sPodActor")
html = html.replace("SimWorkersAI", "SimVllmAI")

# Replace Reason & String labels in Sim
html = html.replace("Cloudflare WAF 1015: Rate Limit Exceeded", "Envoy Rate Limit: 429 Too Many Requests")
html = html.replace("Structured Cloudflare Edge Blueprint", "Structured Kubernetes Pod Blueprint")
html = html.replace("Creative Zero-Trust Access Strategy", "Creative Istio Service Mesh Policy")
html = html.replace("Balanced Global Cache Rule", "Balanced Redis Cluster Sharding")
html = html.replace("Lateral Durable Object Decomposition", "Lateral Custom Resource Definition DAG")
html = html.replace("Cautious WAF Firewall Guardrail", "Cautious Envoy Network Security Policy")

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
      name: "1. etcd Raft TTL Lease & Sweep",
      tool: "etcd Lease",
      cloud: "Kubernetes etcd v3",
      rule: "etcd.get('session') returns None after clock.advance(11); sweep purges expired leases",
      run: () => {
        const c = new SimClock();
        const kv = new SimEtcdLease(c);
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
      name: "2. Redis Cluster Distributed Mutex",
      tool: "Redis Lock",
      cloud: "Kubernetes Redis Cluster",
      rule: "atomic lock acquire succeeds; second concurrent pod attempt aborts cleanly",
      run: () => {
        const d1 = new SimRedisCluster();
        d1.execute_transaction("locks", "lease-1", { owner: "pod_A" }, cur => !cur);
        let secondFailed = false;
        try {
          d1.execute_transaction("locks", "lease-1", { owner: "pod_B" }, cur => !cur);
        } catch (e) {
          secondFailed = true;
        }
        return secondFailed && d1.query("locks", "lease-1").owner === "pod_A";
      }
    },
    {
      id: "test3",
      name: "3. Ephemeral Pod Scratchpad Decay",
      tool: "Pod Scratchpad",
      cloud: "Kubernetes Pod Memory",
      rule: "in-memory pod state active at 60s; context decay clears state at 121s",
      run: () => {
        const c = new SimClock();
        const doActor = new SimK8sPodActor(c);
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
      name: "4. Envoy Token-Bucket Rate Limiter",
      tool: "Envoy Gateway",
      cloud: "Kubernetes Envoy Gateway",
      rule: "request 61 blocked by Envoy 429; spend > $10.00 trips cluster compute budget circuit",
      run: () => {
        const c = new SimClock();
        const waf = new SimEnvoyRateLimiter(c, 10, 1.0);
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
      name: "5. RabbitMQ Queue Visibility Delay",
      tool: "RabbitMQ Queue",
      cloud: "Kubernetes RabbitMQ / Pulsar",
      rule: "unacknowledged message becomes invisible for 30s timeout, then reappears for retry",
      run: () => {
        const c = new SimClock();
        const q = new SimK8sPriorityQueue(c);
        q.send("k8s_jobs", "ProcessInvoice");
        const m1 = q.receive("k8s_jobs", 30);
        const m1Hidden = q.receive("k8s_jobs", 30) === null;
        c.advance(35);
        const m1Reappears = q.receive("k8s_jobs", 30) === "ProcessInvoice";
        return m1 === "ProcessInvoice" && m1Hidden && m1Reappears;
      }
    },
    {
      id: "test6",
      name: "6. Priority Worker (Critical Pod 1st)",
      tool: "PriorityWorker",
      cloud: "Kubernetes Knative / Pod Worker",
      rule: "critical queue drained before normal queue, batch queue drained last",
      run: () => {
        const c = new SimClock();
        const q = new SimK8sPriorityQueue(c);
        const w = new SimK8sPriorityWorker(q);
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
      name: "7. Argo Workflows Retries & Fallback",
      tool: "Argo Workflows",
      cloud: "Kubernetes Argo / Temporal",
      rule: "step retried 2 times on transient pod failure, fallback invoked cleanly",
      run: () => {
        const wf = new SimArgoWorkflows();
        let failCount = 0;
        const step = () => {
          failCount++;
          if (failCount < 3) throw new Error("Transient pod container restart");
          return "success_recovered";
        };
        const res = wf.execute_step_with_retry(step, 2);
        return res.success && res.attempts === 3 && res.result === "success_recovered";
      }
    },
    {
      id: "test8",
      name: "8. Envoy Outlier Circuit Breaker",
      tool: "EnvoyBreaker",
      cloud: "Kubernetes Envoy Outlier Detection",
      rule: "3 failures trip breaker to OPEN; 60s cooldown transitions to HALF-OPEN",
      run: () => {
        const c = new SimClock();
        const b = new SimEnvoyCircuitBreaker(c, 3, 60);
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
# The AI Agent Factory • Kubernetes Cloud-Native Platform
# Assembled Agent: ${assembly.agentType}
# Target Architecture: Tier ${assembly.tier} (${assembly.tier === 2 ? 'Multi-Pod Team' : 'Single Pod'})
# Flow Nodes: ${flowGraph.nodes.length} | Connections: ${flowGraph.connections.length}
# Executable Kubernetes Python Simulator running via Pyodide in Browser
# ==============================================================================

import time
import math
import random

class Clock:
    def __init__(self):
        self.now = 0.0
    def advance(self, seconds: float):
        self.now += seconds

class K8sEtcdLease:
    """Simulates etcd v3 Raft Leases with TTL Expiration."""
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
            return None # Lease expired by etcd engine
        return entry["val"]

    def sweep(self) -> int:
        expired = [k for k, v in self.store.items() if v["expire_at"] <= self.clock.now]
        for k in expired:
            del self.store[k]
        return len(expired)

class K8sRedisCluster:
    """Simulates Kubernetes Redis Cluster with Atomic Locks & Distributed Mutex."""
    def __init__(self):
        self.tables = {}

    def execute_transaction(self, table: str, key: str, record: dict, condition=None):
        self.tables.setdefault(table, {})
        cur = self.tables[table].get(key)
        if condition and not condition(cur):
            raise RuntimeError(f"REDIS_MUTEX_FAILED: Condition check failed for {key}")
        version = (cur["version"] + 1) if cur else 1
        self.tables[table][key] = {**record, "version": version}
        return self.tables[table][key]

    def query(self, table: str, key: str):
        return self.tables.get(table, {}).get(key)

class K8sRabbitMQQueue:
    """Simulates Kubernetes RabbitMQ / Pulsar Queues with Guaranteed Visibility Leases."""
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

class K8sPriorityPodWorker:
    def __init__(self, queues, priority_order=["critical", "normal", "batch"]):
        self.queues = queues
        self.priority_order = priority_order

    def next(self):
        for q in self.priority_order:
            msg = self.queues.receive(q)
            if msg:
                return q, msg
        return None, None

class EnvoyCircuitBreaker:
    """Kubernetes Envoy Outlier Detection Circuit Breaker."""
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
# Assembled Kubernetes Agent System: ${assembly.agentType}
# ------------------------------------------------------------------------------
class AssembledKubernetesAgentSystem:
    def __init__(self):
        self.clock = Clock()
        self.etcd = K8sEtcdLease(self.clock)
        self.redis = K8sRedisCluster()
        self.queues = K8sRabbitMQQueue(self.clock)
        self.worker = K8sPriorityPodWorker(self.queues)
        self.breaker = EnvoyCircuitBreaker(self.clock)
        self.invariants = ${JSON.stringify(assembly.assumptions)}

    def handle_request(self, payload: str):
        # 1. Evaluate Envoy Outlier Circuit Breaker
        if not self.breaker.can_call():
            return {"status": "TRIPPED", "error": "Envoy Breaker OPEN. Service outlier tripped."}

        # 2. Enqueue in RabbitMQ Queues (Critical queue)
        self.queues.send("critical", payload)
        queue_name, task = self.worker.next()

        # 3. Commit Atomic State in Redis Cluster
        redis_record = self.redis.execute_transaction("transactions", "tx-001", {
            "task": task,
            "status": "COMMITTED"
        }, lambda cur: cur is None)

        return {
            "agent": "${assembly.agentType}",
            "orchestrator": "Kubernetes K8s Control Plane",
            "queue": queue_name,
            "task": task,
            "redis_version": redis_record["version"],
            "status": "SUCCESS",
            "invariants_checked": True
        }

if __name__ == "__main__":
    agent = AssembledKubernetesAgentSystem()
    result = agent.handle_request("${assembly.orderText}")
    print("Kubernetes Agent Result:", result)
`;
    document.getElementById("codeViewer").textContent = code;
  }'''

html = html.replace(old_python_fn, new_python_fn)

# Replace copy toast and log event names
html = html.replace("Cloudflare Python code copied to clipboard!", "Kubernetes Python code copied to clipboard!")
html = html.replace("logCloudflareEvent", "logKubernetesEvent")

with open("ai_factory_kubernetes_simulator.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully written ai_factory_kubernetes_simulator.html!")
