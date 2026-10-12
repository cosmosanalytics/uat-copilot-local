# -*- coding: utf-8 -*-
"""
build_traced_comic.py
Builds the definitive Traced Copy of the 3-Tier Enterprise Agent Stack Comic Graphic Novel:
- RETAINS ALL ORIGINAL PICTURES / CARTOONS (SVG vector illustrations in every single panel of every episode)
- ADDS DOWNWARD TRACING TO TIER 0 AWS for all skills in Tier 1 (Skills #8-#14) and Tier 2 (Skills #15-#20)
- Preserves full cover art, character dialogue, comic sound effects, and production invariants
Outputs:
1. `comic_book_traced_printable.html` (Complete graphic novel with all SVG cartoons + downward traces)
2. `The_3_Tier_Enterprise_Agent_Stack_Traced_Comic_Story.pdf` (Compiled via headless Chrome)
3. `comic_book_traced_reader.html` (Mobile and desktop responsive reader with chapter selection)
"""

import os
import sys
import subprocess
import base64

sys.stdout.reconfigure(encoding='utf-8')

from build_complete_comic import generate_svg, illus_map, episodes

# Read cover image as base64
cover_img_path = r"c:\Users\richa\ai-engineering\comic_cover.jpg"
if os.path.exists(cover_img_path):
    with open(cover_img_path, "rb") as f:
        cover_b64 = base64.b64encode(f.read()).decode("utf-8")
        cover_data_uri = f"data:image/jpeg;base64,{cover_b64}"
else:
    cover_data_uri = ""

# Downward Traceability Specifications for Tier 1 and Tier 2 Skills
TIER_DOWNWARD_TRACES = {
    # TIER 1 DOWNWARD TRACES (Skills 8 to 14 -> Tier 0 AWS)
    8: {
        "badge": "⬇️ DOWNWARD TRACE TO TIER 0 AWS",
        "badge_bg": "#2563eb",
        "title": "Skill #8 Propose-Decide ➔ Tier 0 Cloud Enforcement",
        "path": "Tier 1 Kernel Ring 0/3 Separation ➔ Tier 0 AWS IAM & EventBridge Bus",
        "steps": [
            ("Tier 1 Kernel Control", "Ring 0 Prefrontal Judge strips write credentials from LLM; only validated proposals pass."),
            ("Tier 0 AWS Primitive", "AWS IAM Session Policies enforce zero 'Allow' on mutation APIs for Bedrock worker role."),
            ("Tier 0 Storage Proof", "Verified proposal token pushed to Amazon EventBridge event bus with KMS HMAC signature.")
        ]
    },
    9: {
        "badge": "⬇️ DOWNWARD TRACE TO TIER 0 AWS",
        "badge_bg": "#2563eb",
        "title": "Skill #9 Runbook Engine ➔ Tier 0 Cloud Enforcement",
        "path": "Tier 1 Kernel Runbook DAG ➔ Tier 0 AWS Step Functions & Lambda",
        "steps": [
            ("Tier 1 Kernel Control", "Flight Checklist parser validates task schema, prerequisites, and idempotent rollback plan."),
            ("Tier 0 AWS Primitive", "AWS Step Functions executes immutable ASL state machine; unskippable step order."),
            ("Tier 0 MicroVM Node", "AWS Lambda runs isolated atomic tasks in Firecracker microVMs with strict memory caps.")
        ]
    },
    10: {
        "badge": "⬇️ DOWNWARD TRACE TO TIER 0 AWS",
        "badge_bg": "#2563eb",
        "title": "Skill #10 Kernel Supervisor ➔ Tier 0 Cloud Enforcement",
        "path": "Tier 1 Kernel 15s Watchdog ➔ Tier 0 AWS CloudWatch & Lambda Cgroups",
        "steps": [
            ("Tier 1 Kernel Control", "Supervisor thread monitors process heartbeat; kills rogue loops or memory leaks."),
            ("Tier 0 AWS Primitive", "AWS Lambda hypervisor enforces hard 15.0s TimeoutSeconds timer and memory cgroups."),
            ("Tier 0 Panic Route", "Amazon CloudWatch Alarm trips on timeout; dispatches SIGKILL and dumps state to S3 DLQ.")
        ]
    },
    11: {
        "badge": "⬇️ DOWNWARD TRACE TO TIER 0 AWS",
        "badge_bg": "#2563eb",
        "title": "Skill #11 Mutex Lease ➔ Tier 0 Cloud Enforcement",
        "path": "Tier 1 Kernel Mutex Token ➔ Tier 0 Amazon DynamoDB CAS Table",
        "steps": [
            ("Tier 1 Kernel Control", "Ring 0 Mutex coordinator grants temporary lease token with strictly fenced lease ID."),
            ("Tier 0 AWS Primitive", "Amazon DynamoDB PutItem executes atomic CAS: attribute_not_exists(lock) OR expiry < :now."),
            ("Tier 0 TTL Reaping", "DynamoDB Time-To-Live hardware thread auto-releases lock if agent node goes silent.")
        ]
    },
    12: {
        "badge": "⬇️ DOWNWARD TRACE TO TIER 0 AWS",
        "badge_bg": "#2563eb",
        "title": "Skill #12 Context Pager ➔ Tier 0 Cloud Enforcement",
        "path": "Tier 1 Kernel Virtual RAM ➔ Tier 0 ElastiCache Redis & Amazon S3",
        "steps": [
            ("Tier 1 Kernel Control", "Context Pager prunes transient tokens; pages active working memory into structured KV stores."),
            ("Tier 0 AWS Primitive", "Amazon ElastiCache Redis / DynamoDB DAX stores active turn vector cache in <1ms."),
            ("Tier 0 Cold Vault", "Amazon S3 Standard / Glacier Instant Retrieval stores full episodic dialogue history.")
        ]
    },
    13: {
        "badge": "⬇️ DOWNWARD TRACE TO TIER 0 AWS",
        "badge_bg": "#2563eb",
        "title": "Skill #13 Episodic Ledger ➔ Tier 0 Cloud Enforcement",
        "path": "Tier 1 Kernel Hash Chain ➔ Tier 0 Amazon S3 WORM & AWS KMS",
        "steps": [
            ("Tier 1 Kernel Control", "Epistemic Ledger links block diffs: Hash(N) = SHA256(Block_N + Hash_N-1) per agent."),
            ("Tier 0 AWS Primitive", "Amazon S3 Object Lock (Compliance Mode) locks block digest; impossible to overwrite."),
            ("Tier 0 CloudTrail Key", "AWS KMS HMAC-SHA256 signs ledger root; CloudTrail streams event to immutable SIEM.")
        ]
    },
    14: {
        "badge": "⬇️ DOWNWARD TRACE TO TIER 0 AWS",
        "badge_bg": "#2563eb",
        "title": "Skill #14 Grounding Certifier ➔ Tier 0 Cloud Enforcement",
        "path": "Tier 1 Kernel 3-Source Fact Gate ➔ Tier 0 AWS OpenSearch & Nitro Enclave",
        "steps": [
            ("Tier 1 Kernel Control", "Investigative Reporter demands 3 independent corroborating proofs before action certification."),
            ("Tier 0 AWS Primitive", "Amazon OpenSearch / Bedrock Knowledge Bases performs hybrid vector + BM25 citation match."),
            ("Tier 0 Attestation", "AWS Nitro Enclave cryptographically verifies citation cosine similarity before sign-off.")
        ]
    },

    # TIER 2 DOWNWARD TRACES (Skills 15 to 20 -> Tier 1 Kernel -> Tier 0 AWS)
    15: {
        "badge": "⬇️ FULL TRACE: TIER 2 ➔ TIER 1 ➔ TIER 0",
        "badge_bg": "#7c3aed",
        "title": "Skill #15 Topology Builder ➔ Kernel Gate ➔ Tier 0 Cloud Safes",
        "path": "Tier 2 Watts-Strogatz Graph ➔ Tier 1 Cedar Graph ACL ➔ Tier 0 DynamoDB & VPC",
        "steps": [
            ("Tier 2 Swarm Lattice", "Constructs small-world mesh with clustering coefficient C >= 0.6 and average path length L <= 3."),
            ("Tier 1 Kernel Gate", "Ring 0 Cedar Policy Gate evaluates inter-agent edge graph: permit(Edge::A, Edge::B)."),
            ("Tier 0 AWS Primitive", "Amazon DynamoDB Global Tables stores graph adjacency matrix; AWS PrivateLink routes traffic.")
        ]
    },
    16: {
        "badge": "⬇️ FULL TRACE: TIER 2 ➔ TIER 1 ➔ TIER 0",
        "badge_bg": "#7c3aed",
        "title": "Skill #16 Liaison Router ➔ Kernel Gate ➔ Tier 0 Cloud Safes",
        "path": "Tier 2 Cross-Pod Bridge ➔ Tier 1 Cedar Pod Boundary ➔ Tier 0 VPC Peering & KMS",
        "steps": [
            ("Tier 2 Swarm Lattice", "Liaison Agent bridges Demand Pod, Supply Pod, and Control Pod via dedicated embassy channels."),
            ("Tier 1 Kernel Gate", "Ring 0 Cedar evaluates cross-pod boundary rule; Ring 3 Epistemic Ledger logs the border crossing."),
            ("Tier 0 AWS Primitive", "AWS VPC Peering / Transit Gateway routes packets across VPCs; AWS KMS re-encrypts envelopes.")
        ]
    },
    17: {
        "badge": "⬇️ FULL TRACE: TIER 2 ➔ TIER 1 ➔ TIER 0",
        "badge_bg": "#7c3aed",
        "title": "Skill #17 Hop Limiter ➔ Kernel Gate ➔ Tier 0 Cloud Safes",
        "path": "Tier 2 3-Hop TTL Envelope ➔ Tier 1 Supervisor Counter ➔ Tier 0 SQS DLQ & Step Functions",
        "steps": [
            ("Tier 2 Swarm Lattice", "Attaches Hop Count = 3 metadata to all peer-to-peer inter-agent messages across the swarm."),
            ("Tier 1 Kernel Gate", "Ring 1 Supervisor decrements TTL; if Hop Count reaches 0, Supervisor halts thread before LLM call."),
            ("Tier 0 AWS Primitive", "Amazon SQS Dead Letter Queue (DLQ) captures expired packet; Step Functions limits DAG recursion.")
        ]
    },
    18: {
        "badge": "⬇️ FULL TRACE: TIER 2 ➔ TIER 1 ➔ TIER 0",
        "badge_bg": "#7c3aed",
        "title": "Skill #18 Shared Whiteboard ➔ Kernel Gate ➔ Tier 0 Cloud Safes",
        "path": "Tier 2 O(N) Shared Blackboard ➔ Tier 1 Context Pager ➔ Tier 0 DynamoDB CAS & Kinesis",
        "steps": [
            ("Tier 2 Swarm Lattice", "Maintains shared blackboard with partitioned lanes (Demand, Supply, Control) and vector clocks."),
            ("Tier 1 Kernel Gate", "Ring 2 Context Pager loads active lane slices; Ring 0 Cedar enforces lane write permissions."),
            ("Tier 0 AWS Primitive", "Amazon DynamoDB PutItem executes row-level CAS locks; Amazon Kinesis replicates updates across pods.")
        ]
    },
    19: {
        "badge": "⬇️ FULL TRACE: TIER 2 ➔ TIER 1 ➔ TIER 0",
        "badge_bg": "#7c3aed",
        "title": "Skill #19 Consensus Arbiter ➔ Kernel Gate ➔ Tier 0 Cloud Safes",
        "path": "Tier 2 Byzantine Quorum (2f+1) ➔ Tier 1 Cedar Ballot Gate ➔ Tier 0 Nitro Enclaves & KMS",
        "steps": [
            ("Tier 2 Swarm Lattice", "Collects independent cryptographic ballots across peer agents; demands supermajority consensus."),
            ("Tier 1 Kernel Gate", "Ring 0 Cedar verifies 2f+1 signed ballot tokens; Ring 3 Epistemic Ledger signs combined block."),
            ("Tier 0 AWS Primitive", "AWS Nitro Enclaves executes multi-party ballot tally; AWS KMS Multi-Region keys verify signatures.")
        ]
    },
    20: {
        "badge": "⬇️ FULL TRACE: TIER 2 ➔ TIER 1 ➔ TIER 0",
        "badge_bg": "#7c3aed",
        "title": "Skill #20 Circuit Breaker ➔ Kernel Gate ➔ Tier 0 Cloud Safes",
        "path": "Tier 2 3-Strike Anomaly Freeze ➔ Tier 1 Supervisor Kill ➔ Tier 0 EventBridge & IAM Revoke",
        "steps": [
            ("Tier 2 Swarm Lattice", "Detects erratic agent behavior (3 consecutive errors/duplicate POs); raises emergency red card."),
            ("Tier 1 Kernel Gate", "Ring 1 Supervisor forcefully strips active Mutex lease token; sends SIGKILL to container cgroup."),
            ("Tier 0 AWS Primitive", "Amazon EventBridge fires automated IAM detachment lambda; DynamoDB forcefully resets row mutex.")
        ]
    }
}

css = """
@page {
    size: 8.5in 11in;
    margin: 0;
}
* {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}
body {
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    background: #0f172a;
    color: #0f172a;
}
.page {
    width: 8.5in;
    height: 11in;
    max-height: 11in;
    padding: 0.28in 0.36in;
    page-break-after: always;
    break-after: page;
    position: relative;
    overflow: hidden;
    background: #f8fafc;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.header-bar {
    border: 3.5px solid #0f172a;
    border-radius: 12px;
    padding: 6px 14px;
    box-shadow: 4px 4px 0px #0f172a;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.tier-tag {
    font-size: 10px;
    font-weight: 900;
    padding: 2px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    display: inline-block;
}
.page-title {
    font-family: 'Impact', 'Arial Black', sans-serif;
    font-size: 18px;
    color: #0f172a;
    letter-spacing: 0.5px;
    margin-top: 1px;
}
.spec-sub {
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 9.5px;
    color: #334155;
    font-weight: 700;
}
.panels-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    gap: 6px;
}
.panel-grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    height: 100%;
}
.panel-grid-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 8px;
    height: 100%;
}
.comic-panel {
    border: 3px solid #0f172a;
    border-radius: 10px;
    background: #ffffff;
    padding: 7px 9px;
    box-shadow: 3.5px 3.5px 0px #0f172a;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.panel-header {
    font-family: 'Impact', sans-serif;
    font-size: 12.5px;
    color: #0f172a;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 2px;
    margin-bottom: 3px;
}
.scene-desc {
    font-size: 9.5px;
    color: #475569;
    font-style: italic;
    line-height: 1.25;
    margin-bottom: 4px;
}

/* CARTOON PICTURE / ILLUSTRATION BOXES */
.illus-box {
    border: 2.5px solid #0f172a;
    border-radius: 8px;
    background: #f1f5f9;
    overflow: hidden;
    margin: 3px 0;
    box-shadow: 2.5px 2.5px 0px rgba(15,23,42,0.15);
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 310px;
}
.illus-box-traced {
    border: 2.5px solid #0f172a;
    border-radius: 8px;
    background: #f1f5f9;
    overflow: hidden;
    margin: 2px 0;
    box-shadow: 2px 2px 0px rgba(15,23,42,0.15);
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 235px;
}
.illus-box-3col {
    border: 2.5px solid #0f172a;
    border-radius: 8px;
    background: #f1f5f9;
    overflow: hidden;
    margin: 3px 0;
    box-shadow: 2px 2px 0px rgba(15,23,42,0.15);
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 290px;
}

.sfx-badge {
    font-family: 'Impact', sans-serif;
    font-size: 12px;
    padding: 2px 8px;
    border: 2px solid #0f172a;
    border-radius: 5px;
    box-shadow: 2px 2px 0px #0f172a;
    display: inline-block;
    transform: rotate(-1deg);
    letter-spacing: 0.5px;
}
.speech-bubble {
    border: 2px solid #0f172a;
    border-radius: 7px;
    background: #f8fafc;
    padding: 4px 7px;
    margin-top: 3px;
    font-size: 9.5px;
    line-height: 1.25;
    box-shadow: 2px 2px 0px rgba(15, 23, 42, 0.12);
}
.speech-bubble strong {
    color: #0f172a;
}

/* DOWNWARD TRACEABILITY BOX */
.trace-card-box {
    border: 2.5px solid #0f172a;
    border-radius: 9px;
    background: #ffffff;
    padding: 6px 10px;
    margin-top: 5px;
    box-shadow: 3px 3px 0px #0f172a;
}
.trace-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1.5px solid #e2e8f0;
    padding-bottom: 3px;
    margin-bottom: 4px;
}
.trace-badge-tag {
    font-size: 9px;
    font-weight: 900;
    padding: 2px 7px;
    border-radius: 4px;
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
    text-transform: uppercase;
}
.trace-path-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    font-weight: 700;
    color: #475569;
}
.trace-steps-container {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 7px;
}
.trace-step-pill {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 4px 6px;
    display: flex;
    flex-direction: column;
    gap: 1px;
}
.trace-step-title {
    font-size: 9px;
    font-weight: 800;
    color: #0f172a;
    font-family: 'Segoe UI', sans-serif;
}
.trace-step-desc {
    font-size: 8.5px;
    color: #334155;
    line-height: 1.2;
    font-family: 'JetBrains Mono', monospace;
}

.rule-footer {
    border: 3px solid #0f172a;
    border-radius: 9px;
    background: #1e293b;
    color: #ffffff;
    padding: 6px 12px;
    box-shadow: 3px 3px 0px #0f172a;
    margin-top: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}
.rule-title {
    font-size: 9.5px;
    font-weight: 900;
    color: #f59e0b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.rule-text {
    font-size: 10px;
    font-style: italic;
    color: #e2e8f0;
    line-height: 1.25;
}
.superpower-tag {
    background: #0f172a;
    border: 2px solid #38bdf8;
    color: #38bdf8;
    font-weight: 800;
    font-size: 9.5px;
    padding: 3px 8px;
    border-radius: 5px;
    white-space: nowrap;
}
.page-footer-num {
    text-align: center;
    font-size: 8px;
    font-weight: 700;
    color: #64748b;
    margin-top: 2px;
}
"""

def generate_traced_comic():
    pages_html = []

    # 1. COVER PAGE
    cover_page = f"""
    <div class="page" style="background: #090d16; color: #ffffff; padding: 0.28in 0.36in; justify-content: space-between;">
        <div style="border: 3px solid #38bdf8; border-radius: 12px; background: #0f172a; padding: 10px 16px; box-shadow: 0 4px 20px rgba(56,189,248,0.25); display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="background: #f59e0b; color: #000; font-weight: 900; font-size: 11px; padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">ANTIGRAVITY COMIC SERIES • ISSUE #1 (ORIGINAL WITH TRACING)</span>
                <div style="font-family: 'Impact', sans-serif; font-size: 25px; color: #38bdf8; letter-spacing: 1px; margin-top: 3px;">THE 3-TIER ENTERPRISE AGENT STACK</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 10px; color: #94a3b8; font-weight: bold;">SPECIAL ARCHITECTURAL EDITION</div>
                <div style="font-size: 11px; color: #10b981; font-weight: 900;">ALL PICTURES + TIER 0 DOWNWARD TRACING</div>
            </div>
        </div>

        <div style="margin: 8px 0; border: 4px solid #38bdf8; border-radius: 12px; overflow: hidden; box-shadow: 5px 5px 0px #0284c7; max-height: 4.6in;">
            <img src="{cover_data_uri}" style="width: 100%; height: auto; display: block;" alt="Comic Cover">
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div style="background: #1e293b; border: 2px solid #475569; border-radius: 10px; padding: 10px 14px;">
                <div style="font-size: 11px; font-weight: 900; color: #38bdf8; text-transform: uppercase; margin-bottom: 4px;">STARRING THE CITADEL HEROES</div>
                <div style="font-size: 10px; line-height: 1.45; color: #cbd5e1;">
                    • <strong>The Dreamer (Bedrock)</strong>: Savant architect with zero IAM write hands<br>
                    • <strong>Bouncer Cedar (AgentCore)</strong>: 2ms AST gatekeeper immune to injection<br>
                    • <strong>Sparky the Watchdog</strong>: Bulldog with 15s egg timer & kill switch<br>
                    • <strong>Marshal Redcard</strong>: Circuit breaker benching faulty swarm nodes
                </div>
            </div>
            <div style="background: #1e293b; border: 2px solid #475569; border-radius: 10px; padding: 10px 14px;">
                <div style="font-size: 11px; font-weight: 900; color: #10b981; text-transform: uppercase; margin-bottom: 4px;">THE DOWNWARD TRACEABILITY GUARANTEE</div>
                <div style="font-size: 10px; line-height: 1.45; color: #cbd5e1;">
                    • <strong>Tier 0 Cloud Primitives</strong>: WORM vaults, MicroVMs, DynamoDB CAS locks<br>
                    • <strong>Tier 1 Agent OS Kernel</strong>: Cedar gates, DAGs, RAM pagers & hash chains<br>
                    • <strong>Tier 2 Swarm Coordination</strong>: Small-world routing, quorums & red cards<br>
                    • <strong>100% Traceability</strong>: Every Tier 1 & 2 skill traces down to physical AWS hardware
                </div>
            </div>
        </div>

        <div style="background: #0f172a; border: 2px solid #f59e0b; border-radius: 8px; padding: 7px 14px; text-align: center; color: #f59e0b; font-size: 11px; font-weight: 800;">
            "Never trust an agent without physical cloud serialization. Every swarm skill traces down to Tier 0 AWS."
        </div>
    </div>
    """
    pages_html.append(cover_page)

    # 2. EPISODES 1 TO 22 (WITH FULL SVG PICTURES IN EVERY PANEL)
    for ep in episodes:
        p_num = ep["page_num"]
        tier_label = ep["tier"]
        tier_col = ep["tier_color"]
        tag_bg = ep["tag_bg"]
        title = ep["title"]
        spec = ep["spec"]
        layout = ep["layout"]
        superpower = ep["superpower"]
        rule = ep["rule"]

        # Determine if this page has a downward trace section (Tier 1 & Tier 2: Skills 8 to 20, corresponding to p_num 9 to 21)
        has_trace = (p_num in range(9, 22))
        trace_data = TIER_DOWNWARD_TRACES.get(p_num - 1)

        is_3col = (layout == "3-col")
        grid_class = "panel-grid-2" if layout == "2-col" else "panel-grid-3"
        illus_keys = illus_map.get(p_num, ["default", "default", "default"])

        panels_html = []

        for i, p in enumerate(ep["panels"]):
            p_head = p["head"]
            sfx_text, sfx_bg, sfx_col = p["sfx"]
            p_desc = p["desc"]
            
            # Fetch SVG cartoon illustration
            svg_kind = illus_keys[i] if i < len(illus_keys) else "default"
            svg_markup = generate_svg(svg_kind, is_3col=is_3col)

            dialogue_html = ""
            for speaker, text in p["dialogue"]:
                dialogue_html += f"""
                <div class="speech-bubble">
                    <strong>{speaker}:</strong> "{text}"
                </div>
                """

            # Adjust box class based on whether page has a trace box below
            if is_3col:
                box_class = "illus-box-3col"
            elif has_trace:
                box_class = "illus-box-traced"
            else:
                box_class = "illus-box"

            panel_markup = f"""
            <div class="comic-panel">
                <div>
                    <div class="panel-header">{p_head}</div>
                    <div class="scene-desc">{p_desc}</div>
                </div>
                <!-- CARTOON PICTURE / SVG ILLUSTRATION -->
                <div class="{box_class}">
                    {svg_markup}
                </div>
                <div>
                    <div style="text-align: center; margin: 2px 0;">
                        <span class="sfx-badge" style="background: {sfx_bg}; color: {sfx_col};">{sfx_text}</span>
                    </div>
                    {dialogue_html}
                </div>
            </div>
            """
            panels_html.append(panel_markup)

        panels_combined = "".join(panels_html)

        # Downward Traceability Section (for Tier 1 & Tier 2 skills)
        trace_markup = ""
        if has_trace and trace_data:
            steps_html = ""
            for step_title, step_desc in trace_data["steps"]:
                steps_html += f"""
                <div class="trace-step-pill">
                    <div class="trace-step-title">{step_title}</div>
                    <div class="trace-step-desc">{step_desc}</div>
                </div>
                """

            trace_markup = f"""
            <div class="trace-card-box">
                <div class="trace-header-row">
                    <span class="trace-badge-tag" style="background: {trace_data['badge_bg']};">{trace_data['badge']}</span>
                    <span class="trace-path-label">{trace_data['path']}</span>
                </div>
                <div class="trace-steps-container">
                    {steps_html}
                </div>
            </div>
            """

        page_markup = f"""
        <div class="page">
            <!-- Header -->
            <div class="header-bar" style="background: {tier_col};">
                <div>
                    <span class="tier-tag" style="background: {tag_bg}; color: #000;">{tier_label}</span>
                    <div class="page-title">{title}</div>
                </div>
                <div style="text-align: right;">
                    <div class="spec-sub">{spec}</div>
                    <div style="font-size: 9px; font-weight: 800; color: #0f172a; margin-top: 1px;">PAGE {p_num} OF 22 • TRACED COPY</div>
                </div>
            </div>

            <!-- Comic Panels with Full Cartoon Pictures -->
            <div class="panels-container">
                <div class="{grid_class}">
                    {panels_combined}
                </div>
            </div>

            <!-- Downward Traceability to Tier 0 Section (for Tier 1 & 2 skills) -->
            {trace_markup}

            <!-- Rule / Superpower Footer -->
            <div class="rule-footer">
                <div style="flex: 1;">
                    <div class="rule-title">💡 Production Law & Architectural Invariant</div>
                    <div class="rule-text">"{rule}"</div>
                </div>
                <div class="superpower-tag">
                    ⚡ {superpower}
                </div>
            </div>

            <div class="page-footer-num">
                The 3-Tier Enterprise Agent Stack (Traced Copy with Pictures) • Graphic Novel Episode {p_num} • Antigravity AI Engineering
            </div>
        </div>
        """
        pages_html.append(page_markup)

    all_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>The 3-Tier Enterprise Agent Stack - Traced Comic Copy with Pictures</title>
    <style>
{css}
    </style>
</head>
<body>
{"".join(pages_html)}
</body>
</html>
"""

    # Write Printable HTML
    out_printable_html = "comic_book_traced_printable.html"
    with open(out_printable_html, "w", encoding="utf-8") as f:
        f.write(all_content)
    print(f"Generated {out_printable_html} with ALL CARTOONS ({len(all_content)} bytes)")

    # Compile PDF via Chrome / Edge Headless
    out_pdf = "The_3_Tier_Enterprise_Agent_Stack_Traced_Comic_Story.pdf"
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    abs_html = os.path.abspath(out_printable_html)
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={os.path.abspath(out_pdf)}",
        f"file:///{abs_html}"
    ]
    print(f"Compiling PDF with pictures & tracing via {chrome_path}...")
    subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(out_pdf):
        print(f"SUCCESS: Generated Traced PDF with PICTURES at {out_pdf} ({os.path.getsize(out_pdf)/(1024*1024):.2f} MB)")
    else:
        print("WARNING: PDF generation failed.")

    # Create Responsive Web Reader
    generate_traced_reader(all_content, out_pdf)

def generate_traced_reader(source_html, pdf_filename):
    responsive_css = """
<style>
@media (max-width: 850px) {
  body {
    padding: 0 !important;
  }
  .page {
    width: 100% !important;
    max-width: 100vw !important;
    height: auto !important;
    max-height: none !important;
    padding: 12px 10px !important;
    margin: 0 0 20px 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
  }
  .header-bar {
    flex-direction: column !important;
    gap: 6px !important;
    align-items: flex-start !important;
  }
  .panel-grid-2, .panel-grid-3 {
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
  }
  .illus-box, .illus-box-traced, .illus-box-3col {
    height: 260px !important;
  }
  .trace-steps-container {
    grid-template-columns: 1fr !important;
    gap: 6px !important;
  }
  img {
    max-width: 100% !important;
    height: auto !important;
  }
}

.comic-nav-bar {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: #0f172a;
  border-bottom: 2px solid #10b981;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.4);
}
.comic-nav-title {
  font-family: 'Impact', sans-serif;
  color: #10b981;
  font-size: 18px;
  letter-spacing: 0.5px;
}
.comic-nav-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}
.comic-nav-btn {
  background: #f59e0b;
  color: #000;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: 800;
  font-size: 12px;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.comic-nav-select {
  background: #1e293b;
  color: #f8fafc;
  border: 1px solid #475569;
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}
</style>
"""

    nav_bar = f"""
<div class="comic-nav-bar">
  <div class="comic-nav-title">🎨 THE 3-TIER AGENT STACK COMIC (PICTURES + TRACING)</div>
  <div class="comic-nav-actions">
    <select class="comic-nav-select" onchange="jumpToEpisode(this.value)">
      <option value="0">📖 Cover: Wild West vs Citadel</option>
      <option value="1">Ep 1: The Rosetta Stone</option>
      <option value="2">Ep 2: Amazon Bedrock (T0)</option>
      <option value="3">Ep 3: AgentCore / Nitro (T0)</option>
      <option value="4">Ep 4: Amazon S3 Vault (T0)</option>
      <option value="5">Ep 5: AWS Database (T0)</option>
      <option value="6">Ep 6: AWS Lambda (T0)</option>
      <option value="7">Ep 7: AWS Step Functions (T0)</option>
      <option value="8">Ep 8: Amazon EventBridge (T0)</option>
      <option value="9">Ep 9: Propose-Decide ➔ T0</option>
      <option value="10">Ep 10: Runbook Engine ➔ T0</option>
      <option value="11">Ep 11: Kernel Supervisor ➔ T0</option>
      <option value="12">Ep 12: Mutex Lease ➔ T0</option>
      <option value="13">Ep 13: Context Pager ➔ T0</option>
      <option value="14">Ep 14: Episodic Ledger ➔ T0</option>
      <option value="15">Ep 15: Grounding Certifier ➔ T0</option>
      <option value="16">Ep 16: Topology Builder ➔ T1 ➔ T0</option>
      <option value="17">Ep 17: Liaison Router ➔ T1 ➔ T0</option>
      <option value="18">Ep 18: Hop Limiter ➔ T1 ➔ T0</option>
      <option value="19">Ep 19: Shared Whiteboard ➔ T1 ➔ T0</option>
      <option value="20">Ep 20: Consensus Arbiter ➔ T1 ➔ T0</option>
      <option value="21">Ep 21: Circuit Breaker ➔ T1 ➔ T0</option>
      <option value="22">Ep 22: Master Blueprint Trace</option>
    </select>
    <a href="https://github.com/cosmosanalytics/uat-copilot-local/raw/main/{pdf_filename}" class="comic-nav-btn" download>
      ⬇️ Download Traced PDF
    </a>
  </div>
</div>
<script>
function jumpToEpisode(idx) {{
  const pages = document.querySelectorAll('.page');
  const target = pages[parseInt(idx, 10)];
  if (target) {{
    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }}
}}
</script>
"""

    reader_html = source_html.replace("</head>", responsive_css + "\n</head>")
    reader_html = reader_html.replace("<body>", "<body>\n" + nav_bar)

    out_reader = "comic_book_traced_reader.html"
    with open(out_reader, "w", encoding="utf-8") as f:
        f.write(reader_html)
    print(f"Generated {out_reader} ({len(reader_html)} bytes)")

if __name__ == "__main__":
    generate_traced_comic()
