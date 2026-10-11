# -*- coding: utf-8 -*-
"""
embed_topology_in_all_tiers_matrix.py
Embeds a dedicated Watts-Strogatz Topology canvas directly inside the Tier 2 section
of the "Unified All-Tiers Matrix" tab in multi_agent_system_studio_app.html!
This ensures that both:
1. Multi-Tier bottom-up propagation (Tier 0 -> Tier 1 -> Tier 2)
2. Watts-Strogatz small-world lattice packet propagation (Liaisons, shortcut bridges, animated golden pulses)
are simultaneously visible in a single unified view for screen recording!
"""

with open('multi_agent_system_studio_app.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add a mini topology canvas inside Tier 2 card
old_t2_card = """          <!-- TIER 2 CARD (Multi-Agent Swarm) -->
          <div class="tier-stack-card tier-2-card" id="mCardTier2">
            <div class="tier-head-row">
              <div class="tier-title-badge">
                <span class="pill-tier pill-t2">TIER 2</span>
                <span>Watts-Strogatz Multi-Agent Swarm Coordination</span>
              </div>
              <span class="service-status status-proc" id="statusBadgeT2">LATTICE ONLINE</span>
            </div>
            <div class="tier-items-grid">
              <div class="tier-item-box" id="mBoxT2Liaison">
                <div class="tier-item-title"><span>🌉 Liaison Router</span><span>EventBridge Bus</span></div>
                <div class="tier-item-val" id="mValT2Hops">Max Hops: &le; 3 (Small-World)</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Inter-pod shortcut routing avoids O(N&sup2;) message storms.</div>
              </div>
              <div class="tier-item-box" id="mBoxT2Whiteboard">
                <div class="tier-item-title"><span>📋 O(N) Shared Whiteboard</span><span id="mValT2WbStatus">3 LANES SYNCED</span></div>
                <div class="tier-item-val" id="mValT2WbSummary">Finance &bull; Compliance &bull; Operations</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Single shared whiteboard state updated under CAS locks.</div>
              </div>
              <div class="tier-item-box" id="mBoxT2Quorum">
                <div class="tier-item-title"><span>⚖️ BFT Quorum Consensus</span><span id="mValT2QuorumVotes">10/12 SUPERMAJORITY</span></div>
                <div class="tier-item-val" id="mValT2QuorumStatus">Threshold: &ge; 2/3 + 1 Votes</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Cryptographically signed ballots sealed into S3 WORM vault.</div>
              </div>
            </div>
          </div>"""

new_t2_card = """          <!-- TIER 2 CARD (Multi-Agent Swarm with Embedded Watts-Strogatz Canvas) -->
          <div class="tier-stack-card tier-2-card" id="mCardTier2">
            <div class="tier-head-row">
              <div class="tier-title-badge">
                <span class="pill-tier pill-t2">TIER 2</span>
                <span>Watts-Strogatz Multi-Agent Swarm Coordination (p=0.15 Small-World Lattice)</span>
              </div>
              <span class="service-status status-proc" id="statusBadgeT2">LATTICE ONLINE</span>
            </div>
            
            <!-- EMBEDDED TOPOLOGY VISUALIZER -->
            <div style="background: #0f172a; border-radius: 8px; padding: 8px; margin-bottom: 10px; border: 1px solid var(--border-subtle);">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; font-size:0.70rem; color:#94a3b8; font-family:var(--font-mono);">
                <span>🕸️ SMALL-WORLD PROPAGATION (SHORTCUT BRIDGES &bull; PACKET PULSES)</span>
                <span>Clustering: 0.68 &bull; Avg Path: 1.8 Hops</span>
              </div>
              <canvas id="matrixTopologyCanvas" width="860" height="200" style="width:100%; height:200px; display:block;"></canvas>
            </div>

            <div class="tier-items-grid">
              <div class="tier-item-box" id="mBoxT2Liaison">
                <div class="tier-item-title"><span>🌉 Liaison Router</span><span>EventBridge Bus</span></div>
                <div class="tier-item-val" id="mValT2Hops">Max Hops: &le; 3 (Small-World)</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Inter-pod shortcut routing avoids O(N&sup2;) message storms.</div>
              </div>
              <div class="tier-item-box" id="mBoxT2Whiteboard">
                <div class="tier-item-title"><span>📋 O(N) Shared Whiteboard</span><span id="mValT2WbStatus">3 LANES SYNCED</span></div>
                <div class="tier-item-val" id="mValT2WbSummary">Finance &bull; Compliance &bull; Operations</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Single shared whiteboard state updated under CAS locks.</div>
              </div>
              <div class="tier-item-box" id="mBoxT2Quorum">
                <div class="tier-item-title"><span>⚖️ BFT Quorum Consensus</span><span id="mValT2QuorumVotes">10/12 SUPERMAJORITY</span></div>
                <div class="tier-item-val" id="mValT2QuorumStatus">Threshold: &ge; 2/3 + 1 Votes</div>
                <div style="font-size:0.68rem; color:var(--text-muted);">Cryptographically signed ballots sealed into S3 WORM vault.</div>
              </div>
            </div>
          </div>"""

html = html.replace(old_t2_card, new_t2_card)

# Update drawTopologyCanvas to draw onto BOTH canvases (topologyCanvas and matrixTopologyCanvas)
old_draw = """    function drawTopologyCanvas(packetPos = 0) {
      const canvas = document.getElementById('topologyCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const w = canvas.width;
      const h = canvas.height;
      ctx.clearRect(0, 0, w, h);"""

new_draw = """    function drawTopologyCanvas(packetPos = 0) {
      const canvases = [
        document.getElementById('topologyCanvas'),
        document.getElementById('matrixTopologyCanvas')
      ].filter(Boolean);

      canvases.forEach(canvas => {
        const ctx = canvas.getContext('2d');
        const w = canvas.width;
        const h = canvas.height;
        ctx.clearRect(0, 0, w, h);

        const isMini = canvas.id === 'matrixTopologyCanvas';
        const scaleX = isMini ? (w / 900) : 1;
        const scaleY = isMini ? (h / 340) : 1;"""

html = html.replace(old_draw, new_draw)

# Adjust node coordinates and close loop over canvases
old_nodes_loop = """      // Draw Nodes
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
    }"""

new_nodes_loop = """      // Draw Nodes
        nodes.forEach(rawN => {
          const nx = rawN.x * scaleX;
          const ny = rawN.y * scaleY;
          const radius = (rawN.isLiaison ? 16 : 12) * (isMini ? 0.85 : 1);

          ctx.beginPath();
          ctx.arc(nx, ny, radius, 0, Math.PI * 2);
          ctx.fillStyle = rawN.color;
          ctx.fill();
          ctx.lineWidth = rawN.isLiaison ? 2.5 : 1.5;
          ctx.strokeStyle = rawN.isLiaison ? '#f59e0b' : '#ffffff';
          ctx.stroke();

          ctx.fillStyle = '#ffffff';
          ctx.font = (isMini ? 'bold 8px' : 'bold 10px') + ' JetBrains Mono';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(rawN.label, nx, ny);
        });
      });
    }"""

html = html.replace(old_nodes_loop, new_nodes_loop)

# Also scale edges
html = html.replace(
    "ctx.moveTo(n1.x, n1.y);\n        ctx.lineTo(n2.x, n2.y);",
    "ctx.moveTo(n1.x * scaleX, n1.y * scaleY);\n        ctx.lineTo(n2.x * scaleX, n2.y * scaleY);"
)

html = html.replace(
    "const px = n1.x + (n2.x - n1.x) * packetPos;\n          const py = n1.y + (n2.y - n1.y) * packetPos;",
    "const px = (n1.x + (n2.x - n1.x) * packetPos) * scaleX;\n          const py = (n1.y + (n2.y - n1.y) * packetPos) * scaleY;"
)

# Initial draw on matrix canvas on load
html = html.replace(
    "renderQuorumGrid();\n    }",
    "renderQuorumGrid();\n      setTimeout(() => drawTopologyCanvas(0), 100);\n    }"
)

with open('multi_agent_system_studio_app.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Successfully embedded Watts-Strogatz Topology canvas in Unified All-Tiers Matrix!")
