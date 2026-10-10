# -*- coding: utf-8 -*-
"""
render_skill_dependency_diagram.py
Renders a visual architecture diagram of the 3-Tier Skill Dependencies
(Level 2 Swarm -> Level 1 Kernel -> Level 0 AWS Primitives) into a high-resolution PNG.
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>3-Tier Agent Skill Dependency Graph</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1720px;
    height: 1220px;
    background: #0B0F19;
    color: #F8FAFC;
    font-family: 'Plus Jakarta Sans', sans-serif;
    padding: 30px 40px;
    position: relative;
    overflow: hidden;
  }

  /* BACKGROUND SUBTLE GRID */
  body::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: 
      linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
    background-size: 36px 36px;
    pointer-events: none;
  }

  /* HEADER */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding-bottom: 20px;
    border-bottom: 2px solid rgba(255, 255, 255, 0.1);
    position: relative;
    z-index: 10;
  }
  .title-area h1 {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .title-area h1 span.gradient {
    background: linear-gradient(135deg, #A78BFA 0%, #60A5FA 50%, #34D399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .title-area p {
    font-size: 13.5px;
    color: #94A3B8;
    margin-top: 4px;
    font-weight: 500;
  }
  .legend-bar {
    display: flex;
    gap: 20px;
    font-size: 12px;
    font-family: 'JetBrains Mono', monospace;
    background: rgba(30, 41, 59, 0.7);
    padding: 8px 16px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
  }
  .legend-item { display: flex; align-items: center; gap: 8px; }
  .dot { width: 10px; height: 10px; border-radius: 50%; }

  /* MAIN TIERS LAYOUT */
  .canvas-workspace {
    position: relative;
    height: 1040px;
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    z-index: 10;
  }

  /* TIER STRIP CONTAINER */
  .tier-container {
    border-radius: 14px;
    padding: 16px 22px;
    position: relative;
    background: rgba(15, 23, 42, 0.75);
    backdrop-filter: blur(8px);
    border: 1.5px solid;
  }
  .tier-l2 {
    border-color: rgba(167, 139, 250, 0.4);
    box-shadow: 0 0 25px rgba(124, 58, 237, 0.12);
  }
  .tier-l1 {
    border-color: rgba(96, 165, 250, 0.4);
    box-shadow: 0 0 25px rgba(37, 99, 235, 0.12);
  }
  .tier-l0 {
    border-color: rgba(52, 211, 153, 0.4);
    box-shadow: 0 0 25px rgba(5, 150, 105, 0.12);
  }

  .tier-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
  }
  .tier-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 6px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }
  .badge-l2 { background: rgba(124, 58, 237, 0.25); color: #C4B5FD; border: 1px solid rgba(167, 139, 250, 0.4); }
  .badge-l1 { background: rgba(37, 99, 235, 0.25); color: #93C5FD; border: 1px solid rgba(96, 165, 250, 0.4); }
  .badge-l0 { background: rgba(5, 150, 105, 0.25); color: #6EE7B7; border: 1px solid rgba(52, 211, 153, 0.4); }

  .tier-role {
    font-size: 12px;
    font-weight: 600;
    color: #94A3B8;
  }

  /* SKILL CARDS GRID */
  .skills-row {
    display: grid;
    gap: 14px;
  }
  .grid-6 { grid-template-columns: repeat(6, 1fr); }
  .grid-7 { grid-template-columns: repeat(7, 1fr); }

  .skill-node {
    background: rgba(30, 41, 59, 0.85);
    border-radius: 10px;
    padding: 12px 14px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    flex-direction: column;
    gap: 6px;
    position: relative;
    transition: transform 0.2s ease;
  }
  .node-l2 { border-left: 3.5px solid #A78BFA; }
  .node-l1 { border-left: 3.5px solid #60A5FA; }
  .node-l0 { border-left: 3.5px solid #34D399; }

  .skill-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11.5px;
    font-weight: 700;
    color: #F8FAFC;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .skill-summary {
    font-size: 10.5px;
    color: #94A3B8;
    line-height: 1.36;
    min-height: 44px;
  }
  .skill-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 4px;
    padding-top: 6px;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
  }
  .tag-ring {
    padding: 1px 5px;
    border-radius: 4px;
    font-weight: 700;
  }
  .ring-0 { background: rgba(220, 38, 38, 0.2); color: #FCA5A5; }
  .ring-1 { background: rgba(217, 119, 6, 0.2); color: #FCD34D; }
  .ring-3 { background: rgba(59, 130, 246, 0.2); color: #93C5FD; }

  .arrow-label {
    font-size: 9px;
    color: #64748B;
  }

  /* SVG OVERLAY CANVAS FOR WIRES */
  #dependencyCanvas {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 5;
  }

  /* CALLOUT BOXES */
  .callout-strip {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 16px;
    margin-top: 14px;
  }
  .callout-box {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 11px;
    line-height: 1.4;
    color: #CBD5E1;
  }
  .callout-box strong { color: #F8FAFC; }
</style>
</head>
<body>

  <!-- HEADER -->
  <header class="header">
    <div class="title-area">
      <h1>The 3-Tier Enterprise Agent Stack &bull; <span class="gradient">Skill Dependency Graph</span></h1>
      <p>Unidirectional Architectural Invariants: Level 2 Swarms &rarr; Level 1 Kernel OS &rarr; Level 0 AWS Cloud Hardware Root</p>
    </div>
    <div class="legend-bar">
      <div class="legend-item"><div class="dot" style="background:#A78BFA"></div><span>Level 2: Swarm Coordination (6)</span></div>
      <div class="legend-item"><div class="dot" style="background:#60A5FA"></div><span>Level 1: Agent Kernel Harness (7)</span></div>
      <div class="legend-item"><div class="dot" style="background:#34D399"></div><span>Level 0: Physical AWS Primitives (7)</span></div>
    </div>
  </header>

  <!-- WORKSPACE -->
  <div class="canvas-workspace">

    <!-- LEVEL 2: MULTI-AGENT SWARMS -->
    <div class="tier-container tier-l2" id="tierL2">
      <div class="tier-header">
        <div style="display:flex; align-items:center; gap:10px;">
          <span class="tier-badge badge-l2">LEVEL 2 &bull; MULTI-AGENT SYSTEM</span>
          <span class="tier-role">Watts-Strogatz Small-World Governance &bull; O(N) Shared Blackboard &bull; Byzantine Quorum</span>
        </div>
        <span style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#A78BFA;">6 Swarm Skills</span>
      </div>
      <div class="skills-row grid-6">
        <div class="skill-node node-l2" id="node-s1">
          <div class="skill-name">swarm-topology-builder</div>
          <div class="skill-summary">Generates small-world lattice (p=0.15) with high clustering and short path lengths.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span class="arrow-label">&darr; to kernel-runbook</span>
          </div>
        </div>

        <div class="skill-node node-l2" id="node-s2">
          <div class="skill-name">swarm-liaison-router</div>
          <div class="skill-summary">Funnels cross-pod queries through dedicated bridge nodes without message flooding.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span class="arrow-label">&darr; to propose-decide</span>
          </div>
        </div>

        <div class="skill-node node-l2" id="node-s3">
          <div class="skill-name">swarm-hop-limiter</div>
          <div class="skill-summary">Enforces strict TTL and delegation budgets (MaxHops &le; 3) to kill runaway loops.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span class="arrow-label">&darr; to supervisor-circuit</span>
          </div>
        </div>

        <div class="skill-node node-l2" id="node-s4">
          <div class="skill-name">swarm-shared-whiteboard</div>
          <div class="skill-summary">Linear O(N) append-only blackboard state eliminating quadratic O(N²) chat storms.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span class="arrow-label">&darr; to episodic &amp; mutex</span>
          </div>
        </div>

        <div class="skill-node node-l2" id="node-s5">
          <div class="skill-name">swarm-consensus-arbiter</div>
          <div class="skill-summary">Solitary 2/3 + 1 Byzantine fault-tolerant quorum for high-stakes fund/schema actions.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span class="arrow-label">&darr; to grounding-cert</span>
          </div>
        </div>

        <div class="skill-node node-l2" id="node-s6">
          <div class="skill-name">swarm-circuit-breaker</div>
          <div class="skill-summary">Isolates hallucinating nodes: revokes CAS mutex leases and severs graph edges.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span class="arrow-label">&darr; to mutex &amp; supervisor</span>
          </div>
        </div>
      </div>
    </div>

    <!-- LEVEL 1: AGENT OS KERNEL -->
    <div class="tier-container tier-l1" id="tierL1">
      <div class="tier-header">
        <div style="display:flex; align-items:center; gap:10px;">
          <span class="tier-badge badge-l1">LEVEL 1 &bull; AGENT OS KERNEL</span>
          <span class="tier-role">Prefrontal Executive Control Suite &bull; Multi-Store Memory Suite &bull; Virtual Attention Pager</span>
        </div>
        <span style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#60A5FA;">7 Kernel Skills</span>
      </div>
      <div class="skills-row grid-7">
        <div class="skill-node node-l1" id="node-k1">
          <div class="skill-name">kernel-propose-decide</div>
          <div class="skill-summary">Separates untrusted Ring 3 model proposals from Ring 0 execution verdicts.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span class="arrow-label">&darr; to bedrock &amp; agentcore</span>
          </div>
        </div>

        <div class="skill-node node-l1" id="node-k2">
          <div class="skill-name">kernel-runbook-engine</div>
          <div class="skill-summary">Executes structured DAG workflow runbooks with step-barrier verification.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span class="arrow-label">&darr; to stepfunctions</span>
          </div>
        </div>

        <div class="skill-node node-l1" id="node-k3">
          <div class="skill-name">kernel-supervisor-circuit</div>
          <div class="skill-summary">Watchdog monitoring loop divergence, execution timeouts, and token burn budgets.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span class="arrow-label">&darr; to lambda &amp; client-api</span>
          </div>
        </div>

        <div class="skill-node node-l1" id="node-k4">
          <div class="skill-name">kernel-mutex-lease</div>
          <div class="skill-summary">Coordinates atomic CAS leases and background heartbeats with randomized backoff.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span class="arrow-label">&darr; to database (DynamoDB)</span>
          </div>
        </div>

        <div class="skill-node node-l1" id="node-k5">
          <div class="skill-name">kernel-context-pager</div>
          <div class="skill-summary">Virtual memory pager maintaining O(1) active token window with S3 frame eviction.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span class="arrow-label">&darr; to s3-vault</span>
          </div>
        </div>

        <div class="skill-node node-l1" id="node-k6">
          <div class="skill-name">kernel-episodic-ledger</div>
          <div class="skill-summary">Append-only SHA-256 hash-chained block ledger of all perceptions and decisions.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span class="arrow-label">&darr; to s3-vault (WORM)</span>
          </div>
        </div>

        <div class="skill-node node-l1" id="node-k7">
          <div class="skill-name">kernel-grounding-certifier</div>
          <div class="skill-summary">Triangulates assertions across S3 receipts, vector embeddings, and graph triples.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span class="arrow-label">&darr; to s3 &amp; database</span>
          </div>
        </div>
      </div>
    </div>

    <!-- LEVEL 0: PHYSICAL AWS PRIMITIVES -->
    <div class="tier-container tier-l0" id="tierL0">
      <div class="tier-header">
        <div style="display:flex; align-items:center; gap:10px;">
          <span class="tier-badge badge-l0">LEVEL 0 &bull; PHYSICAL AWS CLOUD PRIMITIVES</span>
          <span class="tier-role">Hardware Cloud Boundary &bull; Cryptographic WORM Receipts &bull; Isolated MicroVM Sandboxes</span>
        </div>
        <span style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#34D399;">7 Cloud Primitives</span>
      </div>
      <div class="skills-row grid-7">
        <div class="skill-node node-l0" id="node-a1">
          <div class="skill-name">aws-bedrock</div>
          <div class="skill-summary">Foundation model inference generating structured JSON proposals. Zero execution IAM.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-3">RING 3</span>
            <span style="color:#64748B;">Bedrock Models</span>
          </div>
        </div>

        <div class="skill-node node-l0" id="node-a2">
          <div class="skill-name">aws-agentcore</div>
          <div class="skill-summary">Ring 0 Cedar guardrails enforcing strict parameter bounds and syscall permissions.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span style="color:#64748B;">Cedar / IAM</span>
          </div>
        </div>

        <div class="skill-node node-l0" id="node-a3">
          <div class="skill-name">aws-s3-vault</div>
          <div class="skill-summary">Cryptographic WORM storage (Object Lock Compliance) with SHA-256 grounding receipts.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span style="color:#64748B;">S3 Object Lock</span>
          </div>
        </div>

        <div class="skill-node node-l0" id="node-a4">
          <div class="skill-name">aws-database</div>
          <div class="skill-summary">DynamoDB CAS mutex leasing, OpenSearch Serverless k-NN vectors, and Neptune graph.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span style="color:#64748B;">DynamoDB + Neptune</span>
          </div>
        </div>

        <div class="skill-node node-l0" id="node-a5">
          <div class="skill-name">aws-lambda</div>
          <div class="skill-summary">Ephemeral stateless compute in memory-capped (512MB/10s) Firecracker microVMs.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-1">RING 1</span>
            <span style="color:#64748B;">Firecracker VMs</span>
          </div>
        </div>

        <div class="skill-node node-l0" id="node-a6">
          <div class="skill-name">aws-stepfunctions</div>
          <div class="skill-summary">Deterministic Hierarchical Finite State Machine with automatic rollback compensation.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span style="color:#64748B;">State Machines</span>
          </div>
        </div>

        <div class="skill-node node-l0" id="node-a7">
          <div class="skill-name">aws-client-api</div>
          <div class="skill-summary">Perimeter OpenAPI v3 schema validator and Amazon EventBridge inter-cluster event bus.</div>
          <div class="skill-footer">
            <span class="tag-ring ring-0">RING 0</span>
            <span style="color:#64748B;">EventBridge + API GW</span>
          </div>
        </div>
      </div>
    </div>

    <!-- CALLOUT ANNOTATIONS -->
    <div class="callout-strip">
      <div class="callout-box" style="border-left: 3px solid #A78BFA;">
        <strong>1. Swarm-to-Kernel Delegation:</strong> Multi-agent swarms (L2) never make direct cloud calls. Every coordination step is mediated by individual agent kernels (L1) running Ring 0 propose-decide checks and CAS mutex leases.
      </div>
      <div class="callout-box" style="border-left: 3px solid #60A5FA;">
        <strong>2. The Axiom of Separation:</strong> Bedrock (L0) lives strictly in untrusted Ring 3. It proposes JSON schemas, but AgentCore (L0) and Kernel Propose-Decide (L1) evaluate Cedar guardrails before any mutation is allowed.
      </div>
      <div class="callout-box" style="border-left: 3px solid #34D399;">
        <strong>3. Zero Hallucination Amnesia:</strong> The Virtual Context Pager (L1) and Shared Whiteboard (L2) anchor all factual assertions into immutable S3 WORM receipts and DynamoDB CAS mutexes (L0) with SHA-256 checksums.
      </div>
    </div>

  </div>

  <!-- SVG DEPENDENCY CONNECTIONS -->
  <svg id="dependencyCanvas"></svg>

  <script>
    // Draw connecting bezier curves between specific nodes
    window.onload = function() {
      const svg = document.getElementById('dependencyCanvas');
      const connections = [
        // L2 -> L1
        { from: 'node-s1', to: 'node-k2', color: '#A78BFA' }, // topology -> runbook
        { from: 'node-s2', to: 'node-k1', color: '#A78BFA' }, // liaison -> propose-decide
        { from: 'node-s3', to: 'node-k3', color: '#A78BFA' }, // hop-limiter -> supervisor
        { from: 'node-s4', to: 'node-k6', color: '#A78BFA' }, // whiteboard -> episodic ledger
        { from: 'node-s4', to: 'node-k4', color: '#A78BFA' }, // whiteboard -> mutex
        { from: 'node-s5', to: 'node-k7', color: '#A78BFA' }, // consensus -> grounding certifier
        { from: 'node-s6', to: 'node-k3', color: '#A78BFA' }, // circuit breaker -> supervisor
        { from: 'node-s6', to: 'node-k4', color: '#A78BFA' }, // circuit breaker -> mutex lease

        // L1 -> L0
        { from: 'node-k1', to: 'node-a1', color: '#60A5FA' }, // propose-decide -> bedrock
        { from: 'node-k1', to: 'node-a2', color: '#60A5FA' }, // propose-decide -> agentcore
        { from: 'node-k2', to: 'node-a6', color: '#60A5FA' }, // runbook -> stepfunctions
        { from: 'node-k2', to: 'node-a5', color: '#60A5FA' }, // runbook -> lambda
        { from: 'node-k3', to: 'node-a5', color: '#60A5FA' }, // supervisor -> lambda
        { from: 'node-k3', to: 'node-a7', color: '#60A5FA' }, // supervisor -> client-api
        { from: 'node-k4', to: 'node-a4', color: '#60A5FA' }, // mutex -> database
        { from: 'node-k5', to: 'node-a3', color: '#60A5FA' }, // context-pager -> s3-vault
        { from: 'node-k6', to: 'node-a3', color: '#60A5FA' }, // episodic -> s3-vault
        { from: 'node-k7', to: 'node-a3', color: '#60A5FA' }, // grounding -> s3-vault
        { from: 'node-k7', to: 'node-a4', color: '#60A5FA' }, // grounding -> database
      ];

      // Helper to get element center bottom and top
      function getAnchor(id, isBottom) {
        const el = document.getElementById(id);
        const rect = el.getBoundingClientRect();
        return {
          x: rect.left + rect.width / 2,
          y: isBottom ? rect.bottom : rect.top
        };
      }

      let paths = '';
      connections.forEach(c => {
        const p1 = getAnchor(c.from, true);
        const p2 = getAnchor(c.to, false);
        const dy = p2.y - p1.y;
        const cy1 = p1.y + dy * 0.45;
        const cy2 = p2.y - dy * 0.45;

        paths += `
          <path d="M ${p1.x} ${p1.y} C ${p1.x} ${cy1}, ${p2.x} ${cy2}, ${p2.x} ${p2.y}"
                stroke="${c.color}" stroke-width="2" fill="none" opacity="0.55" stroke-dasharray="4 3" />
          <circle cx="${p1.x}" cy="${p1.y}" r="3" fill="${c.color}" />
          <circle cx="${p2.x}" cy="${p2.y}" r="3.5" fill="${c.color}" />
        `;
      });

      svg.innerHTML = paths;
    };
  </script>
</body>
</html>
"""

with open('three_tier_skill_dependency_graph.html', 'w', encoding='utf-8') as f:
    f.write(HTML_CONTENT)

print("Generated three_tier_skill_dependency_graph.html. Now rendering high-res PNG via headless Selenium...")

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1720,1220')
options.add_argument('--hide-scrollbars')
driver = webdriver.Chrome(options=options)

path = os.path.abspath('three_tier_skill_dependency_graph.html')
driver.get('file:///' + path.replace('\\', '/'))
time.sleep(1.5)

png_path = os.path.abspath('three_tier_skill_dependency_graph.png')
driver.save_screenshot(png_path)
driver.quit()

print(f"SUCCESS! High-res PNG rendered to {png_path}")
