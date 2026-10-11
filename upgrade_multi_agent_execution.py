# -*- coding: utf-8 -*-
"""
upgrade_multi_agent_execution.py
Upgrades multi_agent_system_studio_app.html with:
1. Live Groq LPU Integration: Calls real Groq API with llama-3.3-70b-versatile, generating real multi-pod findings and votes.
2. Animated Multi-Tier Stepper: Visually walks through Stage 1 (Liaison Routing) -> Stage 2 (Specialist Deliberation) -> Stage 3 (Whiteboard Commit) -> Stage 4 (Byzantine Quorum) with glowing packet pulses on the Watts-Strogatz canvas!
3. Clear Latency & Mode Feedback: Shows real LPU latency vs step-by-step simulated swarm coordination.
"""

import re

with open('multi_agent_system_studio_app.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace drawTopologyCanvas to support animated packets
old_canvas_func = """    function drawTopologyCanvas() {
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
    }"""

new_canvas_func = """    let activePacketProgress = 0;
    let packetAnimationTimer = null;

    function drawTopologyCanvas(packetPos = 0) {
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

        // Animate packets traversing shortcut bridges if packetPos > 0
        if (isBridge && packetPos > 0) {
          const px = n1.x + (n2.x - n1.x) * packetPos;
          const py = n1.y + (n2.y - n1.y) * packetPos;
          ctx.save();
          ctx.beginPath();
          ctx.arc(px, py, 5.5, 0, Math.PI * 2);
          ctx.fillStyle = '#fbbf24';
          ctx.shadowColor = '#f59e0b';
          ctx.shadowBlur = 10;
          ctx.fill();
          ctx.restore();
        }
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

    function animateLiaisonPackets(durationMs = 1200) {
      const startTime = performance.now();
      if (packetAnimationTimer) cancelAnimationFrame(packetAnimationTimer);

      function step(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / durationMs, 1);
        drawTopologyCanvas(progress);
        if (progress < 1) {
          packetAnimationTimer = requestAnimationFrame(step);
        } else {
          drawTopologyCanvas(0);
        }
      }
      packetAnimationTimer = requestAnimationFrame(step);
    }"""

html = html.replace(old_canvas_func, new_canvas_func)

# Replace dispatchSwarmMission with real Groq LPU + Stepped Animated Multi-Agent Lifecycle
old_dispatch = """    async function dispatchSwarmMission() {
      const btn = document.getElementById('btnDispatchSwarm');
      btn.disabled = true;
      showToast('Coordinating Watts-Strogatz Small-World Swarm...');

      setTimeout(() => {
        btn.disabled = false;
        showToast('✅ Swarm Consensus Achieved & Whiteboard Committed!');
        drawTopologyCanvas();
      }, 700);
    }"""

new_dispatch = """    async function dispatchSwarmMission() {
      const btn = document.getElementById('btnDispatchSwarm');
      const goalText = document.getElementById('swarmGoalInput').value.trim();
      if (!goalText) {
        showToast('Please enter a swarm mission directive.');
        return;
      }

      btn.disabled = true;
      const apiKey = document.getElementById('groqApiKey')?.value?.trim() || localStorage.getItem('groq_api_key');

      // MODE 1: GROQ LPU REAL INFERENCE
      if (engineMode === 'groq') {
        if (!apiKey) {
          showToast('⚠️ No Groq API Key found. Running animated multi-tier simulation (or enter key above)!');
          await runSteppedSimulation(goalText, "SIMULATOR");
          btn.disabled = false;
          return;
        }

        showToast('⚡ [Groq LPU] Querying Llama 3.3 across 3 Specialist Pods...');
        animateLiaisonPackets(1800);
        const tStart = performance.now();

        try {
          const sysPrompt = "You are an autonomous Multi-Agent Swarm Coordinator running a 12-agent Watts-Strogatz small-world lattice with 3 specialist pods (Finance, Compliance, Operations). " +
            "Analyze the mission and output valid JSON ONLY with this structure: " +
            "{\\"financePod\\": \\"...\\", \\"compliancePod\\": \\"...\\", \\"operationsPod\\": \\"...\\", " +
            "\\"quorumVotes\\": [{\\"id\\": \\"agent-fin-01\\", \\"pod\\": \\"Finance\\", \\"vote\\": \\"YES\\", \\"cert\\": \\"WORM-OK\\"}, ...], " +
            "\\"verdict\\": \\"QUORUM ACHIEVED (10/12 VOTES >= 2/3+1)\\"}";

          const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${apiKey}`,
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              model: "llama-3.3-70b-versatile",
              messages: [
                { role: "system", content: sysPrompt },
                { role: "user", content: `Coordinate multi-agent swarm for: "${goalText}"` }
              ],
              temperature: 0.2,
              response_format: { type: "json_object" }
            })
          });

          if (!response.ok) {
            const errBody = await response.text();
            throw new Error(`Groq HTTP ${response.status}: ${errBody}`);
          }

          const data = await response.json();
          const tLatency = Math.round(performance.now() - tStart);
          const parsed = JSON.parse(data.choices[0].message.content);

          // Update Whiteboard with AI's real findings
          const wbLanes = [
            { author: "agent-fin-01 (Liaison)", text: parsed.financePod || "Finance liquidity verified." },
            { author: "agent-comp-01 (Liaison)", text: parsed.compliancePod || "Compliance verified in Neptune." },
            { author: "agent-ops-01 (Liaison)", text: parsed.operationsPod || "Operations DAG barrier advanced." }
          ];
          renderWhiteboardLanes(wbLanes);

          // Update Quorum with votes
          if (parsed.quorumVotes && parsed.quorumVotes.length) {
            renderQuorumGrid(parsed.quorumVotes);
          }
          document.getElementById('quorumStatusBadge').textContent = `${parsed.verdict || 'QUORUM ACHIEVED'} • GROQ LPU: ${tLatency}ms`;

          showToast(`✅ [Groq LPU] Swarm Coordinated in ${tLatency}ms!`);
        } catch (err) {
          console.error("Groq LPU Error:", err);
          showToast(`⚠️ Groq API Error (${err.message}). Falling back to multi-tier simulator.`);
          await runSteppedSimulation(goalText, "FALLBACK");
        }
        btn.disabled = false;
        return;
      }

      // MODE 2: INSTANT MULTI-TIER STEPPED SIMULATION
      await runSteppedSimulation(goalText, "INSTANT_STEPPED");
      btn.disabled = false;
    }

    async function runSteppedSimulation(goalText, modeTag) {
      showToast('⚡ [Stage 1/4] Inter-Pod Routing: Liaisons bridging EventBridge...');
      animateLiaisonPackets(1200);
      await new Promise(r => setTimeout(r, 650));

      showToast('🧠 [Stage 2/4] Specialist Pods Deliberating in Ring 0 MicroVMs...');
      await new Promise(r => setTimeout(r, 650));

      showToast('📋 [Stage 3/4] Publishing Linear O(N) Shared Whiteboard Lanes...');
      const customWb = [
        { author: "agent-fin-01 (Finance Liaison)", text: "Acquired DynamoDB CAS mutex. Liquidity allocated for: " + goalText.slice(0, 70) + "..." },
        { author: "agent-comp-01 (Compliance Liaison)", text: "Cedar guardrails verified. Grounding certified across S3 WORM & Neptune graph." },
        { author: "agent-ops-01 (Operations Liaison)", text: "Step Functions state machine initiated. Isolated microVM compute committed." }
      ];
      renderWhiteboardLanes(customWb);
      await new Promise(r => setTimeout(r, 650));

      showToast('⚖️ [Stage 4/4] Gathering Byzantine 2/3 + 1 Quorum Ballots...');
      const votes = [
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
      ];
      renderQuorumGrid(votes);
      document.getElementById('quorumStatusBadge').textContent = `QUORUM ACHIEVED (10/12 VOTES >= 2/3+1) • ${modeTag}`;
      await new Promise(r => setTimeout(r, 500));

      showToast('✅ Multi-Agent Consensus Sealed in S3 WORM Vault!');
    }"""

html = html.replace(old_dispatch, new_dispatch)

with open('multi_agent_system_studio_app.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Upgraded multi_agent_system_studio_app.html with live Groq LPU and animated multi-tier stepped execution!")
