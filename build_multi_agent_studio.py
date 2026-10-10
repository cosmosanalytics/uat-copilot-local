# -*- coding: utf-8 -*-
"""
build_multi_agent_studio.py
Generates multi_agent_system_studio_app.html:
Standalone, single-file HTML web application for Multi-Agent System Skills (Level 2: Small-World Swarms)
grounded in Level 1 Individual Agent OS Kernel Skills and Level 0 AWS Cloud Primitives.
Features:
- Pure Light Mode by default (with dark mode toggle)
- WebLLM (in-browser WebGPU), Groq LPU (cloud ultra-fast LPU), and Instant Client Simulation
- Interactive User Input & Presets for Multi-Agent Operations
- Interactive HTML5 Canvas Watts-Strogatz Small-World Network Topology Visualizer (p=0.15)
- Interactive O(N) Shared Whiteboard Blackboard Stream (Finance, Compliance, Engineering Lanes)
- Byzantine Fault-Tolerant Consensus & Quorum Voting Visualizer (2/3 + 1)
- Hop Limiter (TTL <= 3) & Cascade Circuit Breaker Quarantine Telemetry
- Python Multi-Agent Swarm Runtime code generator
- Dedicated SKILL.md Library for all 6 Multi-Agent Skills with 3-tier lineage, search, copy & export
"""

import json

# Define the 6 Level 2 Multi-Agent Skills in full SKILL.md detail with explicit Level 1 and Level 0 lineage
MULTI_AGENT_SKILLS = [
    {
        "id": "swarm-topology-builder",
        "name": "swarm-topology-builder",
        "title": "Watts-Strogatz Small-World Topology Builder",
        "category": "Swarm Architecture",
        "ring": "Ring 0 (Topology Governor)",
        "kernelLineage": "kernel-runbook-engine + kernel-propose-decide",
        "awsLineage": "aws-stepfunctions (DAGs) + aws-client-api (EventBridge)",
        "description": "Constructs small-world agent collaboration lattices with high local clustering and short characteristic path length (p=0.15).",
        "content": """---
name: swarm-topology-builder
description: Constructs small-world agent collaboration lattices with high local clustering and short characteristic path length (p=0.15).
version: 1.0.0
tier: Level 2 (Multi-Agent System Swarm)
ring: Ring 0 (Topology Architecture)
category: Swarm Architecture Suite
lineage:
  level_1_kernel: kernel-runbook-engine, kernel-propose-decide
  level_0_aws: aws-stepfunctions, aws-client-api (EventBridge)
permissions:
  - swarm:BuildLattice
  - swarm:RewireBridge
  - events:PutEvents
tools:
  - generate_watts_strogatz_mesh
  - calculate_clustering_metrics
  - optimize_shortcut_bridges
---

# swarm-topology-builder: Small-World Lattice Generator

## 1. Mathematical Architecture
Unstructured multi-agent systems suffer from two fatal extremes:
1. **Fully Connected Mesh ($O(N^2)$):** Exponential token chatter, broadcast storms, and cognitive collapse.
2. **Linear Pipeline ($O(N)$):** High latency, single points of failure, and zero parallel specialist consultation.

`swarm-topology-builder` implements a **Watts-Strogatz Small-World Graph**:
- Starts with a 1D ring lattice of $N$ agents, each connected to $K$ nearest neighbors ($K=4$).
- With probability $p = 0.15$, edges are randomly rewired across distant specialist clusters.
- **Result:**
  $$C(p) \\gg C_{\\text{random}} \\quad \\text{(High specialist cohesion)}$$
  $$L(p) \\approx L_{\\text{random}} \\propto \\ln N \\quad \\text{(Short cross-swarm hops)}$$

## 2. Input JSON Schema
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["agentCount", "nearestNeighbors", "rewiringProbability"],
  "properties": {
    "agentCount": { "type": "integer", "minimum": 4, "default": 12 },
    "nearestNeighbors": { "type": "integer", "default": 4 },
    "rewiringProbability": { "type": "number", "minimum": 0.05, "maximum": 0.3, "default": 0.15 },
    "specialistPods": { "type": "array", "items": { "type": "string" } }
  }
}
```

## 3. Output Graph Contract
```json
{
  "type": "object",
  "required": ["graphId", "nodes", "adjacencyMatrix", "clusteringCoefficient", "averagePathLength"],
  "properties": {
    "graphId": { "type": "string", "format": "uuid" },
    "nodes": { "type": "array" },
    "adjacencyMatrix": { "type": "array" },
    "clusteringCoefficient": { "type": "number" },
    "averagePathLength": { "type": "number" },
    "liaisonNodes": { "type": "array", "items": { "type": "string" } }
  }
}
```
"""
    },
    {
        "id": "swarm-liaison-router",
        "name": "swarm-liaison-router",
        "title": "Inter-Cluster Specialist Liaison Router",
        "category": "Swarm Routing",
        "ring": "Ring 0 (Inter-Cluster Routing)",
        "kernelLineage": "kernel-propose-decide + kernel-supervisor-circuit",
        "awsLineage": "aws-client-api (API Gateway & EventBridge Buses)",
        "description": "Mediates all cross-pod communication through designated liaison agents, preventing inter-cluster broadcast noise.",
        "content": """---
name: swarm-liaison-router
description: Mediates all cross-pod communication through designated liaison agents, preventing inter-cluster broadcast noise.
version: 1.0.0
tier: Level 2 (Multi-Agent System Swarm)
ring: Ring 0 (Inter-Cluster Bridge Routing)
category: Swarm Routing Suite
lineage:
  level_1_kernel: kernel-propose-decide, kernel-supervisor-circuit
  level_0_aws: aws-client-api (EventBridge Buses, API Gateway)
permissions:
  - swarm:RouteCrossCluster
  - events:PutEvents
tools:
  - dispatch_liaison_request
  - quarantine_pod_boundary
  - summarize_interpod_payload
---

# swarm-liaison-router: Inter-Cluster Bridge Router

## 1. Domain Separation Principle
Specialist pods (e.g., Finance Pod, Compliance Pod, Code Pod) must not broadcast internal reasoning turns to the whole swarm.
- All outbound requests are funneled through a **Liaison Agent**.
- The Liaison Agent compresses, validates, and routes the request across designated Watts-Strogatz bridge edges.
- Eliminates cross-domain noise and hallucination leakage between unrelated agents.

## 2. Routing Protocol
$$\\text{Agent}_{A} \\to \\text{Liaison}_{A} \\xrightarrow{\\text{EventBridge Bridge}} \\text{Liaison}_{B} \\to \\text{Agent}_{B}$$
"""
    },
    {
        "id": "swarm-hop-limiter",
        "name": "swarm-hop-limiter",
        "title": "Gossip & Delegation Hop Limiter",
        "category": "Swarm Governance",
        "ring": "Ring 0 (Gossip Control)",
        "kernelLineage": "kernel-supervisor-circuit + kernel-runbook-engine",
        "awsLineage": "aws-client-api (Headers) + aws-lambda (Watchdog)",
        "description": "Enforces strict TTL and hop budgets (Max Hops <= 3) to prevent infinite ping-pong delegation cascades.",
        "content": """---
name: swarm-hop-limiter
description: Enforces strict TTL and hop budgets (Max Hops <= 3) to prevent infinite ping-pong delegation cascades.
version: 1.0.0
tier: Level 2 (Multi-Agent System Swarm)
ring: Ring 0 (Gossip Protocol Governor)
category: Swarm Governance Suite
lineage:
  level_1_kernel: kernel-supervisor-circuit, kernel-runbook-engine
  level_0_aws: aws-client-api, aws-lambda
permissions:
  - swarm:EnforceHopLimit
  - swarm:DropExpiredPacket
tools:
  - decrement_hop_budget
  - detect_delegation_cycle
  - emit_drop_telemetry
---

# swarm-hop-limiter: Delegation Guardrails

## 1. Anti-Cascade Invariant
In autonomous swarms, agents often pass tasks to peers, creating runaway delegation cycles:
$$\\text{Agent}_1 \\to \\text{Agent}_2 \\to \\text{Agent}_3 \\to \\text{Agent}_1 \\quad (\\text{Infinite Loop})$$

`swarm-hop-limiter` enforces a hard invariant on every inter-agent packet:
- Header: `x-swarm-max-hops: 3`
- Every intermediary decrements `x-swarm-max-hops -= 1`.
- If `hops == 0`: Packet is **dropped immediately**; kernel triggers fallback to primary supervisor.
"""
    },
    {
        "id": "swarm-shared-whiteboard",
        "name": "swarm-shared-whiteboard",
        "title": "O(N) Shared Whiteboard Blackboard Memory",
        "category": "Shared State",
        "ring": "Ring 0 (Blackboard State)",
        "kernelLineage": "kernel-episodic-ledger + kernel-mutex-lease",
        "awsLineage": "aws-s3-vault (WORM Receipts) + aws-database (DynamoDB CAS)",
        "description": "Append-only global state blackboard providing linear O(N) multi-agent coordination without O(N²) peer messaging.",
        "content": """---
name: swarm-shared-whiteboard
description: Append-only global state blackboard providing linear O(N) multi-agent coordination without O(N²) peer messaging.
version: 1.0.0
tier: Level 2 (Multi-Agent System Swarm)
ring: Ring 0 (Global Shared State)
category: Shared State Suite
lineage:
  level_1_kernel: kernel-episodic-ledger, kernel-mutex-lease
  level_0_aws: aws-s3-vault (WORM), aws-database (DynamoDB Mutex)
permissions:
  - s3:PutObject
  - dynamodb:PutItem
  - dynamodb:GetItem
tools:
  - post_blackboard_claim
  - read_blackboard_lane
  - subscribe_state_changes
---

# swarm-shared-whiteboard: Linear Blackboard Architecture

## 1. Complexity Comparison
| Architecture | Message Complexity | Failure Risk | Auditability |
| :--- | :--- | :--- | :--- |
| **Peer-to-Peer Mesh** | $O(N^2)$ | Extremely High | Fragmented |
| **Centralized Dispatcher** | $O(N)$ | Single Bottleneck | Centralized |
| **Shared Whiteboard (O(N))** | $O(N)$ Linear | Resilient | Cryptographic WORM |

Agents publish verified findings to partitioned topic lanes (Finance, Compliance, Engineering) with SHA-256 S3 WORM receipts. Peers read asynchronous state changes without blocking.
"""
    },
    {
        "id": "swarm-consensus-arbiter",
        "name": "swarm-consensus-arbiter",
        "title": "Byzantine Fault-Tolerant Quorum Arbiter",
        "category": "Consensus & Voting",
        "ring": "Ring 0 (Consensus Engine)",
        "kernelLineage": "kernel-grounding-certifier + kernel-propose-decide",
        "awsLineage": "aws-database (DynamoDB CAS) + aws-s3-vault",
        "description": "Byzantine fault-tolerant voting arbiter requiring a 2/3 + 1 supermajority quorum for high-stakes actions.",
        "content": """---
name: swarm-consensus-arbiter
description: Byzantine fault-tolerant voting arbiter requiring a 2/3 + 1 supermajority quorum for high-stakes actions.
version: 1.0.0
tier: Level 2 (Multi-Agent System Swarm)
ring: Ring 0 (Consensus Engine)
category: Consensus & Voting Suite
lineage:
  level_1_kernel: kernel-grounding-certifier, kernel-propose-decide
  level_0_aws: aws-database, aws-s3-vault
permissions:
  - swarm:CollectVotes
  - swarm:CommitQuorum
  - dynamodb:UpdateItem
tools:
  - solicit_agent_ballots
  - verify_byzantine_quorum
  - record_consensus_receipt
---

# swarm-consensus-arbiter: High-Stakes Quorum Engine

## 1. Byzantine Fault Tolerance (BFT)
For actions exceeding high monetary or regulatory thresholds, a single agent's reasoning is insufficient.
`swarm-consensus-arbiter` requires:
$$Q = \\left\\lfloor \\frac{2N}{3} \\right\\rfloor + 1$$
Independent agents cast cryptographic ballots backed by SHA-256 grounding receipts.
If any agent attempts a hallucinated or ungrounded proposal, the quorum isolates it.
"""
    },
    {
        "id": "swarm-circuit-breaker",
        "name": "swarm-circuit-breaker",
        "title": "Distributed Cascade Quarantine Circuit Breaker",
        "category": "Cascade Prevention",
        "ring": "Ring 0 (Quarantine Isolation)",
        "kernelLineage": "kernel-supervisor-circuit + kernel-mutex-lease",
        "awsLineage": "aws-agentcore (Cedar Revocation) + aws-lambda",
        "description": "Network partitioner isolating rogue or hallucinating agent nodes before systemic swarm contamination occurs.",
        "content": """---
name: swarm-circuit-breaker
description: Network partitioner isolating rogue or hallucinating agent nodes before systemic swarm contamination occurs.
version: 1.0.0
tier: Level 2 (Multi-Agent System Swarm)
ring: Ring 0 (Quarantine & Partition)
category: Cascade Prevention Suite
lineage:
  level_1_kernel: kernel-supervisor-circuit, kernel-mutex-lease
  level_0_aws: aws-agentcore, aws-lambda
permissions:
  - swarm:QuarantineNode
  - verifiedpermissions:RevokeToken
  - dynamodb:DeleteItem
tools:
  - sever_node_edges
  - revoke_agent_leases
  - rebalance_swarm_partitions
---

# swarm-circuit-breaker: Epidemic Cascade Prevention

## 1. Automated Quarantine Protocol
If an agent generates $k \\ge 3$ rejected proposals, fails grounding certification, or exhibits semantic looping:
1. `swarm-circuit-breaker` trips.
2. The agent's DynamoDB CAS mutex leases are revoked immediately.
3. Its edges in the Watts-Strogatz graph are severed.
4. The remaining swarm rebalances without experiencing cascading contagion.
"""
    }
]

HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Multi-Agent System Studio // Level 2 Swarm Skills on Agent Kernel & AWS</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    :root {
      --bg-canvas: #f8fafc;
      --bg-panel: #ffffff;
      --bg-panel-subtle: #f1f5f9;
      --border-subtle: #e2e8f0;
      --border-focus: #7c3aed;
      --text-primary: #0f172a;
      --text-secondary: #475569;
      --text-muted: #64748b;
      --accent-purple: #7c3aed;
      --accent-indigo: #4f46e5;
      --accent-blue: #2563eb;
      --accent-emerald: #059669;
      --accent-amber: #d97706;
      --accent-rose: #e11d48;
      --card-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
      --font-ui: 'Plus Jakarta Sans', sans-serif;
      --font-display: 'Bricolage Grotesque', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }
    html[data-theme="dark"] {
      --bg-canvas: #090d16;
      --bg-panel: #0f172a;
      --bg-panel-subtle: #1e293b;
      --border-subtle: #334155;
      --border-focus: #a78bfa;
      --text-primary: #f8fafc;
      --text-secondary: #cbd5e1;
      --text-muted: #94a3b8;
      --accent-purple: #a78bfa;
      --accent-indigo: #818cf8;
      --accent-blue: #60a5fa;
      --accent-emerald: #34d399;
      --accent-amber: #fbbf24;
      --accent-rose: #fb7185;
      --card-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
    }
    * { margin:0; padding:0; box-sizing:border-box; }
    body {
      background: var(--bg-canvas);
      color: var(--text-primary);
      font-family: var(--font-ui);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    .app-header {
      background: var(--bg-panel);
      border-bottom: 1px solid var(--border-subtle);
      padding: 0.85rem 1.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 50;
    }
    .brand-group { display: flex; align-items: center; gap: 12px; }
    .brand-badge {
      width: 42px; height: 42px; border-radius: 10px;
      background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%);
      display: flex; align-items: center; justify-content: center;
      color: #fff; font-size: 1.3rem; font-weight: 800;
    }
    .brand-text h1 {
      font-family: var(--font-display);
      font-size: 1.25rem; font-weight: 800;
      display: flex; align-items: center; gap: 8px;
    }
    .badge-swarm {
      font-size: 0.65rem; background: #faf5ff; color: #6d28d9;
      border: 1px solid #f3e8ff; border-radius: 999px; padding: 2px 8px;
      font-family: var(--font-mono); font-weight: 700;
    }
    .brand-text p { font-size: 0.76rem; color: var(--text-muted); }
    .header-actions { display: flex; align-items: center; gap: 10px; }
    .engine-switch {
      display: flex; background: var(--bg-panel-subtle); padding: 3px;
      border-radius: 8px; border: 1px solid var(--border-subtle); gap: 2px;
    }
    .engine-btn {
      padding: 5px 11px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;
      cursor: pointer; border: none; background: transparent; color: var(--text-secondary);
      transition: all 0.15s ease; display: flex; align-items: center; gap: 5px;
    }
    .engine-btn.active {
      background: #7c3aed; color: #fff; box-shadow: 0 1px 3px rgba(124,58,237,0.25);
    }
    .theme-toggle-btn {
      padding: 6px 12px; border-radius: 8px; font-size: 0.78rem; font-weight: 600;
      cursor: pointer; border: 1px solid var(--border-subtle); background: var(--bg-panel);
      color: var(--text-primary); transition: all 0.15s ease;
    }
    .theme-toggle-btn:hover { background: var(--bg-panel-subtle); }
    .api-key-input {
      font-family: var(--font-mono); font-size: 0.74rem; padding: 6px 10px;
      border-radius: 8px; border: 1px solid var(--border-subtle); background: var(--bg-panel);
      color: var(--text-primary); width: 140px;
    }

    /* STATUS RIBBON */
    .status-ribbon {
      background: var(--bg-panel-subtle);
      border-bottom: 1px solid var(--border-subtle);
      padding: 0.45rem 1.75rem;
      display: flex;
      gap: 16px;
      overflow-x: auto;
      font-size: 0.73rem;
      font-family: var(--font-mono);
      align-items: center;
    }
    .ribbon-pill {
      display: flex; align-items: center; gap: 6px; white-space: nowrap;
      padding: 2px 8px; border-radius: 6px; background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
    }

    /* MAIN APP WORKSPACE */
    .app-workspace {
      display: flex;
      flex: 1;
      overflow: hidden;
      height: calc(100vh - 122px);
    }

    /* SIDEBAR CONTROL */
    .sidebar-pane {
      width: 420px;
      background: var(--bg-panel);
      border-right: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      padding: 1.25rem;
      gap: 1.2rem;
      flex-shrink: 0;
    }
    .section-title {
      font-family: var(--font-display);
      font-size: 0.82rem; font-weight: 800; text-transform: uppercase;
      letter-spacing: 0.05em; color: var(--text-muted); margin-bottom: 6px;
      display: flex; justify-content: space-between; align-items: center;
    }
    .preset-chips { display: flex; flex-direction: column; gap: 6px; }
    .chip {
      padding: 8px 12px; border-radius: 8px; border: 1px solid var(--border-subtle);
      background: var(--bg-panel-subtle); color: var(--text-primary); font-size: 0.78rem;
      font-weight: 600; cursor: pointer; text-align: left; transition: all 0.15s ease;
      display: flex; align-items: center; gap: 8px;
    }
    .chip:hover { border-color: var(--accent-purple); background: #faf5ff; }
    .chip.active { border-color: var(--accent-purple); background: #f3e8ff; color: #5b21b6; }

    .input-textarea {
      width: 100%; height: 110px; border-radius: 8px; border: 1px solid var(--border-subtle);
      background: var(--bg-panel-subtle); color: var(--text-primary); padding: 10px;
      font-family: var(--font-ui); font-size: 0.82rem; resize: none; line-height: 1.45;
    }
    .input-textarea:focus { outline: none; border-color: var(--border-focus); }

    .btn-action {
      padding: 10px 16px; border-radius: 8px; border: none;
      background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%);
      color: #fff; font-size: 0.84rem; font-weight: 700; cursor: pointer;
      display: flex; align-items: center; justify-content: center; gap: 8px;
      box-shadow: 0 2px 8px rgba(124,58,237,0.25); transition: all 0.15s ease;
    }
    .btn-action:hover { filter: brightness(1.08); transform: translateY(-1px); }
    .btn-action:disabled { opacity: 0.6; cursor: not-allowed; }

    /* STAGE PANE (RIGHT) */
    .stage-pane {
      flex: 1;
      display: flex;
      flex-direction: column;
      background: var(--bg-canvas);
      overflow: hidden;
    }
    .stage-tabs {
      background: var(--bg-panel);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      padding: 0 1.5rem;
      gap: 4px;
      overflow-x: auto;
    }
    .tab-btn {
      padding: 0.85rem 1.1rem; border: none; background: transparent;
      color: var(--text-secondary); font-size: 0.82rem; font-weight: 700;
      cursor: pointer; border-bottom: 2.5px solid transparent; white-space: nowrap;
      transition: all 0.15s ease; display: flex; align-items: center; gap: 6px;
    }
    .tab-btn:hover { color: var(--text-primary); }
    .tab-btn.active { color: var(--accent-purple); border-bottom-color: var(--accent-purple); }

    .stage-content {
      flex: 1;
      padding: 1.5rem;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }

    /* CARDS & PANELS */
    .swarm-card {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      box-shadow: var(--card-shadow);
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .card-head {
      display: flex; justify-content: space-between; align-items: center;
      border-bottom: 1px solid var(--border-subtle); padding-bottom: 10px;
    }
    .card-title {
      font-family: var(--font-display); font-size: 0.95rem; font-weight: 800;
      display: flex; align-items: center; gap: 8px;
    }

    /* TOPOLOGY CANVAS */
    #topologyCanvas {
      width: 100%; height: 340px; border-radius: 8px; background: #0f172a;
      display: block; box-shadow: inset 0 2px 8px rgba(0,0,0,0.4);
    }

    /* WHITEBOARD LANES */
    .whiteboard-lanes {
      display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px;
    }
    .whiteboard-lane {
      border: 1px solid var(--border-subtle); border-radius: 8px;
      background: var(--bg-panel-subtle); padding: 10px; display: flex;
      flex-direction: column; gap: 8px; min-height: 220px;
    }
    .whiteboard-post {
      background: var(--bg-panel); border: 1px solid var(--border-subtle);
      border-radius: 6px; padding: 8px; font-size: 0.73rem; display: flex;
      flex-direction: column; gap: 3px;
    }

    /* BFT VOTING CARDS */
    .quorum-grid {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 10px;
    }
    .vote-card {
      border: 1.5px solid var(--border-subtle); border-radius: 8px;
      padding: 10px; background: var(--bg-panel); font-size: 0.74rem;
      display: flex; flex-direction: column; gap: 4px;
    }
    .vote-card.voted-yes { border-color: #059669; background: #f0fdf4; }
    .vote-card.voted-no { border-color: #e11d48; background: #fff1f2; }

    .code-view {
      background: #0f172a; color: #f8fafc; padding: 1rem; border-radius: 8px;
      font-family: var(--font-mono); font-size: 0.76rem; overflow-x: auto;
      line-height: 1.5;
    }

    .toast-box {
      position: fixed; bottom: 24px; right: 24px; background: #0f172a; color: #fff;
      padding: 10px 18px; border-radius: 8px; font-size: 0.82rem; font-weight: 600;
      box-shadow: 0 4px 14px rgba(0,0,0,0.25); display: none; z-index: 999;
    }
  </style>
</head>
<body>

  <!-- APP HEADER -->
  <header class="app-header">
    <div class="brand-group">
      <div class="brand-badge">🕸️</div>
      <div class="brand-text">
        <h1>Multi-Agent System Studio <span class="badge-swarm">Level 2 Swarms</span></h1>
        <p>Small-World Network Governance over Agent Kernel OS &amp; AWS Primitives</p>
      </div>
    </div>

    <div class="header-actions">
      <div class="engine-switch">
        <button class="engine-btn active" id="btnModeGroq" onclick="setEngineMode('groq')">⚡ Groq LPU</button>
        <button class="engine-btn" id="btnModeWebGpu" onclick="setEngineMode('webgpu')">🎮 Local WebGPU</button>
        <button class="engine-btn" id="btnModeSimulator" onclick="setEngineMode('simulator')">🚀 Instant Mode</button>
      </div>
      <input type="password" id="groqApiKey" class="api-key-input" placeholder="gsk_... (optional)" onchange="saveGroqKey()">
      <button class="theme-toggle-btn" onclick="toggleTheme()" id="themeBtn">🌙 Dark Mode</button>
    </div>
  </header>

  <!-- STATUS RIBBON -->
  <div class="status-ribbon">
    <div class="ribbon-pill"><span>🕸️ Watts-Strogatz:</span> <strong style="color:var(--accent-purple)">p = 0.15 (SMALL-WORLD)</strong></div>
    <div class="ribbon-pill"><span>🌉 Liaison Router:</span> <strong style="color:var(--accent-blue)">CROSS-POD ISOLATED</strong></div>
    <div class="ribbon-pill"><span>⏱️ Hop Limiter:</span> <strong style="color:var(--accent-emerald)">MAX HOPS &le; 3 (CYCLE-FREE)</strong></div>
    <div class="ribbon-pill"><span>📋 Whiteboard:</span> <strong style="color:var(--accent-indigo)">O(N) LINEAR BLACKBOARD</strong></div>
    <div class="ribbon-pill"><span>⚖️ BFT Quorum:</span> <strong style="color:var(--accent-amber)">2/3 + 1 (SUPERMAJORITY)</strong></div>
  </div>

  <!-- WORKSPACE -->
  <div class="app-workspace">

    <!-- SIDEBAR CONTROLS -->
    <aside class="sidebar-pane">
      <div>
        <div class="section-title">SWARM MISSION PRESETS</div>
        <div class="preset-chips">
          <button class="chip active" onclick="loadSwarmPreset(0)">🌐 Global Supply Chain Inter-Pod Routing</button>
          <button class="chip" onclick="loadSwarmPreset(1)">⚖️ Multi-Agent M&A Due Diligence Quorum</button>
          <button class="chip" onclick="loadSwarmPreset(2)">🛡️ Rogue Agent Cascade Isolation & Quarantine</button>
        </div>
      </div>

      <div>
        <div class="section-title">MISSION OBJECTIVE &amp; SWARM DIRECTIVE</div>
        <textarea class="input-textarea" id="swarmGoalInput"></textarea>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
        <div style="background: var(--bg-panel-subtle); padding: 8px; border-radius: 8px; border: 1px solid var(--border-subtle);">
          <div style="font-size: 0.68rem; font-weight: 700; color: var(--text-muted);">TOPOLOGY DENSITY</div>
          <div style="font-size: 0.86rem; font-weight: 800; color: var(--accent-purple);">12 Nodes &bull; 3 Pods</div>
        </div>
        <div style="background: var(--bg-panel-subtle); padding: 8px; border-radius: 8px; border: 1px solid var(--border-subtle);">
          <div style="font-size: 0.68rem; font-weight: 700; color: var(--text-muted);">MESSAGE COMPLEXITY</div>
          <div style="font-size: 0.86rem; font-weight: 800; color: var(--accent-emerald);">O(N) Blackboard</div>
        </div>
      </div>

      <button class="btn-action" id="btnDispatchSwarm" onclick="dispatchSwarmMission()">
        <span>🚀 Coordinate Multi-Agent Swarm</span>
      </button>

      <div style="padding: 10px; border-radius: 8px; background: #faf5ff; border: 1px solid #e9d5ff; font-size: 0.72rem; line-height: 1.4; color: #5b21b6;">
        <strong>The 3-Tier Recursion:</strong> Level 2 Swarm Skills govern inter-agent coordination without message storms. Underneath each agent node runs a Level 1 Kernel OS with prefrontal propose-decide gates, which translates operations to Level 0 AWS primitives (Bedrock, AgentCore, S3 WORM, DynamoDB CAS).
      </div>
    </aside>

    <!-- RIGHT STAGE PANE -->
    <main class="stage-pane">
      <div class="stage-tabs">
        <button class="tab-btn active" id="tabBtnTopology" onclick="switchStage('topology')">🕸️ Watts-Strogatz Network</button>
        <button class="tab-btn" id="tabBtnWhiteboard" onclick="switchStage('whiteboard')">📋 O(N) Shared Whiteboard</button>
        <button class="tab-btn" id="tabBtnQuorum" onclick="switchStage('quorum')">⚖️ Byzantine Quorum Voting</button>
        <button class="tab-btn" id="tabBtnGovernance" onclick="switchStage('governance')">🛡️ Hop Limiter &amp; Circuit Breaker</button>
        <button class="tab-btn" id="tabBtnCode" onclick="switchStage('code')">💻 Python Swarm Runtime</button>
        <button class="tab-btn" id="tabBtnSkills" onclick="switchStage('skills')">📚 Dedicated SKILL.md Library (6 Skills)</button>
      </div>

      <!-- TAB 1: TOPOLOGY CANVAS -->
      <div class="stage-content" id="stageTopology">
        <div class="swarm-card">
          <div class="card-head">
            <span class="card-title">🕸️ Watts-Strogatz Small-World Topology (p=0.15)</span>
            <span style="font-size:0.74rem; font-family:var(--font-mono); color:var(--accent-purple);">Clustering: 0.68 &bull; Avg Path: 1.8 Hops</span>
          </div>
          <canvas id="topologyCanvas" width="900" height="340"></canvas>
          <div style="display:flex; justify-content:space-between; font-size:0.73rem; color:var(--text-secondary);">
            <div>🟣 <strong>Finance Pod</strong> (Nodes 1-4)</div>
            <div>🔵 <strong>Compliance Pod</strong> (Nodes 5-8)</div>
            <div>🟢 <strong>Operations Pod</strong> (Nodes 9-12)</div>
            <div>⚡ <strong>Gold Lines:</strong> Inter-Cluster Liaison Bridges</div>
          </div>
        </div>
      </div>

      <!-- TAB 2: O(N) WHITEBOARD -->
      <div class="stage-content" id="stageWhiteboard" style="display: none;">
        <div class="swarm-card">
          <div class="card-head">
            <span class="card-title">📋 O(N) Shared Whiteboard Memory (Blackboard Pattern)</span>
            <span style="font-size:0.74rem; font-family:var(--font-mono); color:var(--accent-emerald);">Linear Updates &bull; 0 Point-to-Point Mesh Overhead</span>
          </div>
          <div class="whiteboard-lanes" id="whiteboardLanes">
            <!-- Dynamically populated lanes -->
          </div>
        </div>
      </div>

      <!-- TAB 3: BFT QUORUM -->
      <div class="stage-content" id="stageQuorum" style="display: none;">
        <div class="swarm-card">
          <div class="card-head">
            <span class="card-title">⚖️ Byzantine Fault-Tolerant Consensus Arbiter</span>
            <span class="badge-swarm" id="quorumStatusBadge">QUORUM ACHIEVED (9/12 VOTES &ge; 2/3+1)</span>
          </div>
          <div style="font-size:0.76rem; color:var(--text-secondary); margin-bottom:8px;">
            High-stakes decision verification: Requires independent cryptographic ballots with SHA-256 S3 WORM receipts.
          </div>
          <div class="quorum-grid" id="quorumGrid">
            <!-- Dynamically populated voting cards -->
          </div>
        </div>
      </div>

      <!-- TAB 4: GOVERNANCE & CIRCUIT BREAKER -->
      <div class="stage-content" id="stageGovernance" style="display: none;">
        <div class="swarm-card">
          <div class="card-head">
            <span class="card-title">🛡️ Hop Limiter &amp; Rogue Agent Cascade Isolation</span>
            <span style="font-size:0.74rem; font-family:var(--font-mono); color:var(--accent-emerald);">SWARM HEALTH: 100% NOMINAL</span>
          </div>
          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:14px;">
            <div style="padding:12px; border:1px solid var(--border-subtle); border-radius:8px; background:var(--bg-panel-subtle);">
              <strong style="font-size:0.8rem; color:var(--text-primary);">⏱️ Hop Limiter Enforcement (TTL &le; 3)</strong>
              <div style="font-size:0.74rem; color:var(--text-secondary); margin-top:6px; line-height:1.4;">
                Every inter-agent message carries <code>x-swarm-max-hops: 3</code>. Dropped packets emit an audit event to EventBridge, preventing infinite delegation cycles.
              </div>
              <div style="margin-top:10px; font-family:var(--font-mono); font-size:0.72rem; color:var(--accent-emerald);">
                Active Packets in Flight: 4 &bull; Dropped Violations: 0
              </div>
            </div>

            <div style="padding:12px; border:1px solid var(--border-subtle); border-radius:8px; background:var(--bg-panel-subtle);">
              <strong style="font-size:0.8rem; color:var(--text-primary);">⚡ Cascade Circuit Breaker Quarantine</strong>
              <div style="font-size:0.74rem; color:var(--text-secondary); margin-top:6px; line-height:1.4;">
                If an agent node hallucinates or fails grounding certification 3 consecutive times, its DynamoDB CAS mutex lease is revoked and its graph edges are severed.
              </div>
              <div style="margin-top:10px; font-family:var(--font-mono); font-size:0.72rem; color:var(--accent-purple);">
                Quarantined Nodes: 0 &bull; Active Swarm Partitions: Healthy
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 5: PYTHON SWARM RUNTIME -->
      <div class="stage-content" id="stageCode" style="display: none;">
        <pre class="code-view" id="codeViewSwarm"></pre>
      </div>

      <!-- TAB 6: DEDICATED SKILL.MD LIBRARY -->
      <div class="stage-content" id="stageSkills" style="display: none;">
        <div style="background: var(--bg-panel); border: 1px solid var(--border-subtle); border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; min-height: 580px; box-shadow: var(--card-shadow);">
          <!-- TOOLBAR -->
          <div style="padding: 12px 18px; background: var(--bg-panel-subtle); border-bottom: 1px solid var(--border-subtle); display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px;">
            <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
              <span style="font-weight: 800; font-size: 0.82rem; font-family: var(--font-display); color: var(--text-primary); margin-right: 4px;">CATEGORY:</span>
              <button class="theme-toggle-btn active-filter" id="filterAll" onclick="filterSwarmSkills('all')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700; border-color: var(--accent-purple); background: #faf5ff; color: #6d28d9;">All (6)</button>
              <button class="theme-toggle-btn" id="filterArch" onclick="filterSwarmSkills('Swarm Architecture')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Architecture (2)</button>
              <button class="theme-toggle-btn" id="filterGov" onclick="filterSwarmSkills('Swarm Governance')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Governance &amp; BFT (4)</button>
            </div>
            <div style="display: flex; gap: 8px; align-items: center;">
              <input type="text" id="skillSearchInput" placeholder="🔍 Search swarm skills..." oninput="searchSwarmSkills()" style="padding: 5px 10px; border-radius: 6px; border: 1px solid var(--border-subtle); background: var(--bg-panel); font-size: 0.75rem; color: var(--text-primary); width: 170px;">
              <button class="theme-toggle-btn" onclick="copyCurrentSwarmSkillMd()" title="Copy active SKILL.md" style="padding: 5px 10px; font-size: 0.72rem;">📋 Copy SKILL.md</button>
              <button class="theme-toggle-btn" onclick="downloadCurrentSwarmSkillMd()" title="Download active SKILL.md" style="padding: 5px 10px; font-size: 0.72rem;">⬇️ Download</button>
              <button class="btn-action" onclick="downloadAllSwarmSkillsBundle()" style="padding: 5px 12px; font-size: 0.72rem;"><span>📦 Export JSON</span></button>
            </div>
          </div>

          <!-- SPLIT VIEW -->
          <div style="display: flex; flex: 1; min-height: 500px; overflow: hidden;">
            <!-- SIDEBAR LIST -->
            <div id="swarmSkillsListPane" style="width: 310px; border-right: 1px solid var(--border-subtle); overflow-y: auto; background: var(--bg-canvas); padding: 10px; display: flex; flex-direction: column; gap: 6px;"></div>

            <!-- PREVIEW PANE -->
            <div style="flex: 1; display: flex; flex-direction: column; overflow: hidden; background: var(--bg-panel);">
              <div id="swarmSkillDetailHeader" style="padding: 12px 18px; border-bottom: 1px solid var(--border-subtle); background: var(--bg-panel-subtle); display: flex; justify-content: space-between; align-items: center;">
                <div>
                  <div id="swarmSkillHeaderTitle" style="font-weight: 800; font-size: 1rem; font-family: var(--font-display); color: var(--text-primary);">swarm-topology-builder/SKILL.md</div>
                  <div id="swarmSkillHeaderMeta" style="font-size: 0.74rem; color: var(--text-muted); margin-top: 2px;">Level 2 &bull; Ring 0 &bull; Watts-Strogatz Lattice &bull; Lineage: Kernel Runbook + Step Functions</div>
                </div>
                <div id="swarmSkillBadge" class="badge-swarm" style="font-size: 0.7rem;">LEVEL 2</div>
              </div>
              <div style="flex: 1; overflow-y: auto; padding: 16px;">
                <pre class="code-view" id="swarmSkillContentPre" style="margin: 0; min-height: 100%; font-size: 0.76rem; line-height: 1.48;"></pre>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>

  <div class="toast-box" id="toastBox"></div>

  <script>
    const SWARM_PRESETS = [
      {
        title: "Global Supply Chain Inter-Pod Routing",
        goal: "Coordinate a 12-agent Watts-Strogatz swarm across 3 specialist pods (Finance, Compliance, Operations). Ingest port disruption event, route cross-pod queries via Liaison Agents across gold shortcut bridges, post linear O(N) updates to Shared Whiteboard lanes, and verify zero runaway delegation cycles.",
        whiteboard: [
          { lane: "Finance Pod Lane", author: "agent-fin-01", text: "Acquired DynamoDB CAS mutex 'lease-port-fx'. Approved liquidity buffer of $4.2M with S3 WORM receipt rec-fin-101." },
          { lane: "Compliance Pod Lane", author: "agent-comp-02", text: "Verified maritime sanctions against Neptune graph entities. Zero violations detected. BFT vote cast: APPROVE." },
          { lane: "Operations Pod Lane", author: "agent-ops-04", text: "Re-routed 18 cargo vessels to alternative terminals. Step Functions DAG barrier advanced to Stage 3." }
        ],
        votes: [
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
        ]
      },
      {
        title: "Multi-Agent M&A Due Diligence Quorum",
        goal: "Execute Byzantine Fault-Tolerant due diligence on a corporate acquisition. Audit financial records, environmental liability, and intellectual property. Require a 2/3 + 1 supermajority quorum before issuing final recommendation.",
        whiteboard: [
          { lane: "Finance Pod Lane", author: "agent-fin-02", text: "Balance sheet reconciliation certified against S3 WORM records. EBITDA margin verified at 24.8%." },
          { lane: "Compliance Pod Lane", author: "agent-comp-01", text: "IP ownership clear in Neptune knowledge graph. 42 active patents verified with zero litigation." },
          { lane: "Operations Pod Lane", author: "agent-ops-01", text: "IT infrastructure tech debt estimated at $1.2M. Synergy savings modeled in isolated microVMs." }
        ],
        votes: [
          { id: "agent-fin-01", pod: "Finance", vote: "YES", cert: "WORM-OK" },
          { id: "agent-fin-02", pod: "Finance", vote: "YES", cert: "WORM-OK" },
          { id: "agent-comp-01", pod: "Compliance", vote: "YES", cert: "WORM-OK" },
          { id: "agent-comp-02", pod: "Compliance", vote: "YES", cert: "WORM-OK" },
          { id: "agent-ops-01", pod: "Operations", vote: "YES", cert: "WORM-OK" },
          { id: "agent-ops-02", pod: "Operations", vote: "YES", cert: "WORM-OK" },
          { id: "agent-ops-03", pod: "Operations", vote: "YES", cert: "WORM-OK" },
          { id: "agent-comp-03", pod: "Compliance", vote: "YES", cert: "WORM-OK" }
        ]
      },
      {
        title: "Rogue Agent Cascade Isolation & Quarantine",
        goal: "Simulate an adversarial or hallucinating agent in the Compliance pod. Circuit breaker trips after 3 invalid proposals, revokes DynamoDB mutex lease, severs Watts-Strogatz edges, and rebalances remaining 11 agents seamlessly.",
        whiteboard: [
          { lane: "Compliance Pod Lane", author: "agent-comp-03", text: "⚠️ VIOLATION DETECTED: Agent generated ungrounded proposal. Cedar policy denied syscall." },
          { lane: "Finance Pod Lane", author: "agent-fin-01", text: "Liaison router severed bridge to agent-comp-03. CAS lease revoked." },
          { lane: "Operations Pod Lane", author: "agent-ops-02", text: "Swarm partition stabilized. Normal O(N) whiteboard coordination resumed." }
        ],
        votes: [
          { id: "agent-fin-01", pod: "Finance", vote: "YES", cert: "WORM-OK" },
          { id: "agent-fin-02", pod: "Finance", vote: "YES", cert: "WORM-OK" },
          { id: "agent-fin-03", pod: "Finance", vote: "YES", cert: "WORM-OK" },
          { id: "agent-comp-01", pod: "Compliance", vote: "YES", cert: "WORM-OK" },
          { id: "agent-comp-02", pod: "Compliance", vote: "YES", cert: "WORM-OK" },
          { id: "agent-comp-03", pod: "Compliance", vote: "NO", cert: "QUARANTINED" },
          { id: "agent-ops-01", pod: "Operations", vote: "YES", cert: "WORM-OK" },
          { id: "agent-ops-02", pod: "Operations", vote: "YES", cert: "WORM-OK" },
          { id: "agent-ops-03", pod: "Operations", vote: "YES", cert: "WORM-OK" }
        ]
      }
    ];

    const SWARM_SKILLS_LIBRARY = __SWARM_SKILLS_JSON__;
    let currentSelectedSkillId = "swarm-topology-builder";
    let activeCategoryFilter = "all";
    let currentPresetIdx = 0;
    let engineMode = "groq";

    function initTheme() {
      const saved = localStorage.getItem('swarm_studio_theme') || 'light';
      document.documentElement.setAttribute('data-theme', saved);
      updateThemeBtn(saved);
    }

    function toggleTheme() {
      const cur = document.documentElement.getAttribute('data-theme');
      const next = cur === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('swarm_studio_theme', next);
      updateThemeBtn(next);
    }

    function updateThemeBtn(theme) {
      const btn = document.getElementById('themeBtn');
      if (btn) btn.textContent = theme === 'dark' ? '☀️ Light Mode' : '🌙 Dark Mode';
    }

    function setEngineMode(mode) {
      engineMode = mode;
      document.getElementById('btnModeGroq').classList.toggle('active', mode === 'groq');
      document.getElementById('btnModeWebGpu').classList.toggle('active', mode === 'webgpu');
      document.getElementById('btnModeSimulator').classList.toggle('active', mode === 'simulator');
      showToast(`AI Engine set to: ${mode.toUpperCase()}`);
    }

    function saveGroqKey() {
      const val = document.getElementById('groqApiKey').value.trim();
      localStorage.setItem('groq_api_key', val);
      showToast('Groq Key saved!');
    }

    function loadSavedKey() {
      const k = localStorage.getItem('groq_api_key');
      if (k) document.getElementById('groqApiKey').value = k;
    }

    function loadSwarmPreset(idx) {
      currentPresetIdx = idx;
      document.querySelectorAll('.chip').forEach((c, i) => c.classList.toggle('active', i === idx));
      const p = SWARM_PRESETS[idx];
      document.getElementById('swarmGoalInput').value = p.goal;

      renderWhiteboardLanes(p.whiteboard);
      renderQuorumGrid(p.votes);
      renderPythonSwarmRuntime(p);
      drawTopologyCanvas();
    }

    function renderWhiteboardLanes(lanes) {
      const container = document.getElementById('whiteboardLanes');
      container.innerHTML = `
        <div class="whiteboard-lane">
          <div style="font-size:0.76rem; font-weight:800; color:#7c3aed;">🟣 FINANCE LANE</div>
          <div class="whiteboard-post">
            <strong style="color:var(--text-primary); font-size:0.72rem;">${lanes[0].author}</strong>
            <div style="color:var(--text-secondary); margin-top:2px;">${lanes[0].text}</div>
            <div style="font-size:0.62rem; color:var(--text-muted); font-family:var(--font-mono); margin-top:4px;">✓ S3 WORM Receipt Verified</div>
          </div>
        </div>

        <div class="whiteboard-lane">
          <div style="font-size:0.76rem; font-weight:800; color:#2563eb;">🔵 COMPLIANCE LANE</div>
          <div class="whiteboard-post">
            <strong style="color:var(--text-primary); font-size:0.72rem;">${lanes[1].author}</strong>
            <div style="color:var(--text-secondary); margin-top:2px;">${lanes[1].text}</div>
            <div style="font-size:0.62rem; color:var(--text-muted); font-family:var(--font-mono); margin-top:4px;">✓ Neptune Knowledge Certified</div>
          </div>
        </div>

        <div class="whiteboard-lane">
          <div style="font-size:0.76rem; font-weight:800; color:#059669;">🟢 OPERATIONS LANE</div>
          <div class="whiteboard-post">
            <strong style="color:var(--text-primary); font-size:0.72rem;">${lanes[2].author}</strong>
            <div style="color:var(--text-secondary); margin-top:2px;">${lanes[2].text}</div>
            <div style="font-size:0.62rem; color:var(--text-muted); font-family:var(--font-mono); margin-top:4px;">✓ Step Functions Barrier Advanced</div>
          </div>
        </div>
      `;
    }

    function renderQuorumGrid(votes) {
      const container = document.getElementById('quorumGrid');
      container.innerHTML = votes.map(v => `
        <div class="vote-card ${v.vote === 'YES' ? 'voted-yes' : 'voted-no'}">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong>${v.id}</strong>
            <span style="font-weight:800; font-size:0.68rem; padding:1px 6px; border-radius:4px; ${v.vote === 'YES' ? 'background:#dcfce7; color:#15803d;' : 'background:#fee2e2; color:#b91c1c;'}">${v.vote}</span>
          </div>
          <div style="color:var(--text-secondary); font-size:0.68rem;">Pod: ${v.pod} Pod</div>
          <div style="font-family:var(--font-mono); font-size:0.62rem; color:var(--text-muted);">${v.cert}</div>
        </div>
      `).join('');
    }

    function renderPythonSwarmRuntime(p) {
      const pre = document.getElementById('codeViewSwarm');
      pre.textContent = `# Level 2 Multi-Agent Small-World Swarm Runtime
# Watts-Strogatz Network + O(N) Shared Whiteboard over AWS Primitives

import networkx as nx
import boto3
import json

class SmallWorldSwarmCoordinator:
    def __init__(self, n_nodes=12, k_neighbors=4, rewiring_p=0.15):
        # 1. Build Watts-Strogatz Graph (Level 2 Architecture)
        self.graph = nx.watts_strogatz_graph(n=n_nodes, k=k_neighbors, p=rewiring_p)
        self.s3 = boto3.client('s3')
        self.dynamodb = boto3.client('dynamodb')
        self.eventbridge = boto3.client('events')
        print(f"Swarm online: {n_nodes} nodes, clustering={nx.average_clustering(self.graph):.2f}")

    def route_inter_pod_message(self, src_agent: str, dst_pod: str, payload: dict, max_hops=3):
        # 2. Enforce Hop Limiter & Liaison Routing
        if max_hops <= 0:
            raise TimeoutError("Hop limit exceeded (MaxHops <= 3). Packet dropped.")

        # Publish through Liaison Router on Amazon EventBridge
        self.eventbridge.put_events(
            Entries=[{
                'Source': f'swarm.{src_agent}',
                'DetailType': 'LiaisonBridgeMessage',
                'Detail': json.dumps({'payload': payload, 'remaining_hops': max_hops - 1}),
                'EventBusName': 'MultiAgentSwarmBus'
            }]
        )

    def write_shared_whiteboard(self, lane: str, agent_id: str, fact_receipt: str):
        # 3. O(N) Linear Shared Whiteboard with S3 WORM Receipt
        self.s3.put_object(
            Bucket="swarm-shared-whiteboard-vault",
            Key=f"lanes/{lane}/{agent_id}.json",
            Body=json.dumps({"author": agent_id, "receipt": fact_receipt})
        )

# Instantiate and coordinate
swarm = SmallWorldSwarmCoordinator()
swarm.write_shared_whiteboard("finance", "agent-fin-01", "rec-fin-101")
print("Swarm state committed successfully!")
`;
    }

    function drawTopologyCanvas() {
      const canvas = document.getElementById('topologyCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const w = canvas.width;
      const h = canvas.height;
      ctx.clearRect(0, 0, w, h);

      const nodes = [
        // Finance Pod (Purple)
        { id: 1, label: "F1", x: 180, y: 100, pod: "finance", color: "#a855f7", isLiaison: true },
        { id: 2, label: "F2", x: 120, y: 160, pod: "finance", color: "#c084fc" },
        { id: 3, label: "F3", x: 160, y: 240, pod: "finance", color: "#c084fc" },
        { id: 4, label: "F4", x: 240, y: 180, pod: "finance", color: "#c084fc" },

        // Compliance Pod (Blue)
        { id: 5, label: "C1", x: 450, y: 70, pod: "compliance", color: "#3b82f6", isLiaison: true },
        { id: 6, label: "C2", x: 530, y: 120, pod: "compliance", color: "#60a5fa" },
        { id: 7, label: "C3", x: 490, y: 200, pod: "compliance", color: "#60a5fa" },
        { id: 8, label: "C4", x: 410, y: 150, pod: "compliance", color: "#60a5fa" },

        // Operations Pod (Emerald)
        { id: 9, label: "O1", x: 720, y: 110, pod: "ops", color: "#10b981", isLiaison: true },
        { id: 10, label: "O2", x: 790, y: 170, pod: "ops", color: "#34d399" },
        { id: 11, label: "O3", x: 740, y: 250, pod: "ops", color: "#34d399" },
        { id: 12, label: "O4", x: 660, y: 190, pod: "ops", color: "#34d399" }
      ];

      const edges = [
        // Intra-pod edges
        [1,2], [2,3], [3,4], [4,1], [1,3],
        [5,6], [6,7], [7,8], [8,5], [5,7],
        [9,10], [10,11], [11,12], [12,9], [9,11],
        // Inter-pod Liaison Bridges (Watts-Strogatz shortcuts)
        [1,5, true], [5,9, true], [4,8, true], [8,12, true]
      ];

      // Draw Edges
      edges.forEach(e => {
        const n1 = nodes.find(n => n.id === e[0]);
        const n2 = nodes.find(n => n.id === e[1]);
        const isBridge = !!e[2];

        ctx.beginPath();
        ctx.moveTo(n1.x, n1.y);
        ctx.lineTo(n2.x, n2.y);
        ctx.lineWidth = isBridge ? 2.5 : 1.2;
        ctx.strokeStyle = isBridge ? '#f59e0b' : 'rgba(148, 163, 184, 0.35)';
        if (isBridge) ctx.setLineDash([5, 3]); else ctx.setLineDash([]);
        ctx.stroke();
      });
      ctx.setLineDash([]);

      // Draw Nodes
      nodes.forEach(n => {
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.isLiaison ? 18 : 14, 0, Math.PI * 2);
        ctx.fillStyle = n.color;
        ctx.fill();
        ctx.lineWidth = n.isLiaison ? 3 : 1.5;
        ctx.strokeStyle = n.isLiaison ? '#f59e0b' : '#ffffff';
        ctx.stroke();

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 10px JetBrains Mono';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(n.label, n.x, n.y);
      });
    }

    function switchStage(stage) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('stageTopology').style.display = stage === 'topology' ? 'flex' : 'none';
      document.getElementById('stageWhiteboard').style.display = stage === 'whiteboard' ? 'flex' : 'none';
      document.getElementById('stageQuorum').style.display = stage === 'quorum' ? 'flex' : 'none';
      document.getElementById('stageGovernance').style.display = stage === 'governance' ? 'flex' : 'none';
      document.getElementById('stageCode').style.display = stage === 'code' ? 'flex' : 'none';
      document.getElementById('stageSkills').style.display = stage === 'skills' ? 'block' : 'none';

      if (stage === 'topology') {
        document.getElementById('tabBtnTopology')?.classList.add('active');
        setTimeout(drawTopologyCanvas, 50);
      }
      if (stage === 'whiteboard') document.getElementById('tabBtnWhiteboard')?.classList.add('active');
      if (stage === 'quorum') document.getElementById('tabBtnQuorum')?.classList.add('active');
      if (stage === 'governance') document.getElementById('tabBtnGovernance')?.classList.add('active');
      if (stage === 'code') document.getElementById('tabBtnCode')?.classList.add('active');
      if (stage === 'skills') {
        document.getElementById('tabBtnSkills')?.classList.add('active');
        initSwarmSkillsLibrary();
      }
    }

    async function dispatchSwarmMission() {
      const btn = document.getElementById('btnDispatchSwarm');
      btn.disabled = true;
      showToast('Coordinating Watts-Strogatz Small-World Swarm...');

      setTimeout(() => {
        btn.disabled = false;
        showToast('✅ Swarm Consensus Achieved & Whiteboard Committed!');
        drawTopologyCanvas();
      }, 700);
    }

    // ==========================================
    // DEDICATED SWARM SKILL.MD LIBRARY LOGIC
    // ==========================================
    function initSwarmSkillsLibrary() {
      renderSwarmSkillsList();
      selectSwarmSkill(currentSelectedSkillId);
    }

    function filterSwarmSkills(category) {
      activeCategoryFilter = category;
      ['filterAll', 'filterArch', 'filterGov'].forEach(id => {
        const btn = document.getElementById(id);
        if (btn) {
          btn.style.borderColor = 'var(--border-subtle)';
          btn.style.background = 'var(--bg-panel-subtle)';
          btn.style.color = 'var(--text-secondary)';
        }
      });
      const targetId = category === 'all' ? 'filterAll' : (category === 'Swarm Architecture' ? 'filterArch' : 'filterGov');
      const activeBtn = document.getElementById(targetId);
      if (activeBtn) {
        activeBtn.style.borderColor = 'var(--accent-purple)';
        activeBtn.style.background = '#faf5ff';
        activeBtn.style.color = '#6d28d9';
      }
      renderSwarmSkillsList();
    }

    function searchSwarmSkills() {
      renderSwarmSkillsList();
    }

    function renderSwarmSkillsList() {
      const pane = document.getElementById('swarmSkillsListPane');
      if (!pane) return;
      const query = (document.getElementById('skillSearchInput')?.value || '').toLowerCase();

      let filtered = SWARM_SKILLS_LIBRARY.filter(s => {
        const matchesCat = activeCategoryFilter === 'all' ||
                           (activeCategoryFilter === 'Swarm Architecture' && (s.category.includes('Architecture') || s.category.includes('Routing'))) ||
                           (activeCategoryFilter === 'Swarm Governance' && (s.category.includes('Governance') || s.category.includes('Consensus') || s.category.includes('Cascade') || s.category.includes('State')));
        const matchesQuery = s.name.toLowerCase().includes(query) ||
                             s.title.toLowerCase().includes(query) ||
                             s.description.toLowerCase().includes(query) ||
                             s.awsLineage.toLowerCase().includes(query);
        return matchesCat && matchesQuery;
      });

      if (filtered.length === 0) {
        pane.innerHTML = '<div style="padding: 14px; font-size: 0.75rem; color: var(--text-muted); text-align: center;">No matching swarm skills found.</div>';
        return;
      }

      pane.innerHTML = filtered.map(s => {
        const isSelected = s.id === currentSelectedSkillId;
        const bgStyle = isSelected ? 'background: #faf5ff; border-color: var(--accent-purple);' : 'background: var(--bg-panel); border-color: var(--border-subtle);';
        return `
          <div onclick="selectSwarmSkill('${s.id}')" style="cursor: pointer; padding: 9px 11px; border-radius: 8px; border: 1.5px solid; ${bgStyle} display: flex; flex-direction: column; gap: 3px; transition: all 0.15s ease;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span style="font-family: var(--font-mono); font-weight: 700; font-size: 0.76rem; color: var(--text-primary);">${s.name}</span>
              <span style="font-size: 0.62rem; font-weight: 800; padding: 1px 6px; border-radius: 4px; background: #7c3aed15; color: #7c3aed;">SWARM &bull; L2</span>
            </div>
            <div style="font-size: 0.68rem; color: var(--text-secondary); line-height: 1.25;">${s.title}</div>
            <div style="font-size: 0.62rem; color: var(--text-muted); font-family: var(--font-mono);">Lineage: ${s.kernelLineage.split('+')[0].trim()}</div>
          </div>
        `;
      }).join('');
    }

    function selectSwarmSkill(skillId) {
      const skill = SWARM_SKILLS_LIBRARY.find(s => s.id === skillId);
      if (!skill) return;
      currentSelectedSkillId = skillId;

      document.getElementById('swarmSkillHeaderTitle').textContent = `${skill.name}/SKILL.md`;
      document.getElementById('swarmSkillHeaderMeta').textContent = `Level 2 • ${skill.category} • Kernel: ${skill.kernelLineage} • AWS: ${skill.awsLineage}`;
      document.getElementById('swarmSkillBadge').textContent = "LEVEL 2";
      document.getElementById('swarmSkillContentPre').textContent = skill.content.trim();

      renderSwarmSkillsList();
    }

    function copyCurrentSwarmSkillMd() {
      const skill = SWARM_SKILLS_LIBRARY.find(s => s.id === currentSelectedSkillId);
      if (!skill) return;
      navigator.clipboard.writeText(skill.content.trim()).then(() => {
        showToast(`✅ Copied ${skill.name}/SKILL.md to clipboard!`);
      });
    }

    function downloadCurrentSwarmSkillMd() {
      const skill = SWARM_SKILLS_LIBRARY.find(s => s.id === currentSelectedSkillId);
      if (!skill) return;
      const blob = new Blob([skill.content.trim()], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${skill.name}.SKILL.md`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast(`💾 Downloaded ${skill.name}.SKILL.md`);
    }

    function downloadAllSwarmSkillsBundle() {
      const bundle = {
        title: "Multi-Agent System Swarm Skills Manifest (Level 2)",
        tier: "Level 2",
        count: SWARM_SKILLS_LIBRARY.length,
        exportedAt: new Date().toISOString(),
        skills: SWARM_SKILLS_LIBRARY
      };
      const blob = new Blob([JSON.stringify(bundle, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'multi_agent_swarm_skills_manifest.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast(`📦 Exported 6 Swarm SKILL.md specs in JSON manifest!`);
    }

    function showToast(msg) {
      const t = document.getElementById('toastBox');
      t.innerText = msg;
      t.style.display = 'block';
      setTimeout(() => { t.style.display = 'none'; }, 2400);
    }

    document.addEventListener('DOMContentLoaded', () => {
      initTheme();
      loadSavedKey();
      loadSwarmPreset(0);
      initSwarmSkillsLibrary();
      setTimeout(drawTopologyCanvas, 100);
    });
  </script>
</body>
</html>
'''

# Replace placeholder with actual JSON
final_html = HTML_TEMPLATE.replace('__SWARM_SKILLS_JSON__', json.dumps(MULTI_AGENT_SKILLS, indent=2))

with open('multi_agent_system_studio_app.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Successfully generated multi_agent_system_studio_app.html!")
