# -*- coding: utf-8 -*-
"""
build_traced_comic.py
Generates the comprehensive Downward-Traced Copy of the 3-Tier Enterprise Agent Stack Comic:
For EACH skill in Tier 1 and Tier 2 (Skills #8 to #20), explicitly traces down all the way to Tier 0 AWS Cloud Primitives:
- Tier 2 Swarm Lattice -> Tier 1 Kernel OS -> Tier 0 AWS Infrastructure
- Tier 1 Kernel Controls -> Tier 0 AWS Infrastructure
Outputs:
1. `comic_book_traced_printable.html`
2. `The_3_Tier_Enterprise_Agent_Stack_Traced_Comic_Story.pdf`
3. `comic_book_traced_reader.html` (Responsive Mobile/Desktop Reader)
"""

import os
import sys
import subprocess
import base64
import shutil

sys.stdout.reconfigure(encoding='utf-8')

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
    # TIER 0 FOUNDATION SPECIFICATIONS (Skills 1 to 7)
    1: {
        "badge": "TIER 0 FOUNDATION PRIMITIVE",
        "badge_bg": "#059669",
        "title": "Hardware Root of Trust: Model Isolation",
        "path": "Ring 3 Proposal Space ➔ AWS Bedrock ➔ AWS Nitro Enclaves",
        "steps": [
            ("AWS Compute Engine", "AWS Bedrock Claude 3.5 Sonnet / Llama-3-70B running in isolated VPC tenants."),
            ("Zero Mutation Guarantee", "IAM execution credentials strictly stripped from model invocation envelope."),
            ("Hardware Protection", "Nitro Enclave cryptographically attests model output hash before kernel evaluation.")
        ]
    },
    2: {
        "badge": "TIER 0 FOUNDATION PRIMITIVE",
        "badge_bg": "#059669",
        "title": "Cryptographic Root of Trust: Hardware Attestation",
        "path": "Hardware Enclave ➔ AWS AgentCore ➔ Nitro Attestation Document (PCR0)",
        "steps": [
            ("Nitro Hypervisor", "Dedicated CPU/RAM hardware partition isolated from host OS; zero shared memory."),
            ("PCR0 Platform Registers", "Cryptographic measurement of kernel binary signed by AWS hardware certificate authority."),
            ("Cedar Policy Engine", "Deterministic Cedar AST compiled directly inside Enclave memory; sub-millisecond evaluation.")
        ]
    },
    3: {
        "badge": "TIER 0 FOUNDATION PRIMITIVE",
        "badge_bg": "#059669",
        "title": "Immutable Compliance Storage: S3 WORM Vault",
        "path": "Agent State Snapshot ➔ S3 Object Lock (Compliance Mode) ➔ AWS KMS",
        "steps": [
            ("Object Lock Compliance", "Strict WORM compliance: deletion or overwrite mathematically rejected even by AWS Root."),
            ("Customer KMS CMK", "Envelope encryption via customer-managed KMS key alias/sop-audit-ledger with 90-day rotation."),
            ("Audit Certification", "FINRA 17a-4 / SEC Rule compliant immutable log stream.")
        ]
    },
    4: {
        "badge": "TIER 0 FOUNDATION PRIMITIVE",
        "badge_bg": "#059669",
        "title": "Atomic State Engine: DynamoDB CAS Locks",
        "path": "State Mutex ➔ Amazon DynamoDB Conditional PutItem ➔ Global Tables",
        "steps": [
            ("Conditional CAS Lock", "PutItem conditional expression: attribute_not_exists(lock_id) OR lease_expiry < :now."),
            ("Automatic Lease TTL", "Hardware TTL thread reaps stale locks automatically after 15s node crash."),
            ("Global Table Sync", "Multi-region active-active replication with vector timestamps and sub-second convergence.")
        ]
    },
    5: {
        "badge": "TIER 0 FOUNDATION PRIMITIVE",
        "badge_bg": "#059669",
        "title": "Ephemeral Compute: Lambda MicroVM Cgroups",
        "path": "Task Execution ➔ AWS Lambda Firecracker MicroVM ➔ VPC PrivateLink",
        "steps": [
            ("Firecracker MicroVM", "Sub-5ms ephemeral container boot with dedicated Linux kernel and jailed cgroups."),
            ("Memory / Clock Budget", "Hard wall-clock timeout (max 15.0s) and memory ceiling (2048MB) enforced by hypervisor."),
            ("Zero Persistent State", "Ephemeral disk scrubbed upon container freeze; zero data leakage across invocations.")
        ]
    },
    6: {
        "badge": "TIER 0 FOUNDATION PRIMITIVE",
        "badge_bg": "#059669",
        "title": "Deterministic Orchestration: Step Functions Rail",
        "path": "Mission SOP ➔ AWS Step Functions (Express Workflows) ➔ IAM Role Boundaries",
        "steps": [
            ("Unskippable State DAG", "State transition JSON graph enforced by AWS orchestration engine; zero step skipping."),
            ("Heartbeat Watchdogs", "HeartbeatSeconds and TimeoutSeconds fire automated task retry or supervisor kill signal."),
            ("IAM Service Boundaries", "State tasks assume tightly scoped task-specific IAM session tokens per execution.")
        ]
    },
    7: {
        "badge": "TIER 0 FOUNDATION PRIMITIVE",
        "badge_bg": "#059669",
        "title": "Decoupled Event Bus: Amazon EventBridge",
        "path": "Swarm Signal ➔ Amazon EventBridge ➔ SQS Dead Letter Queue (DLQ)",
        "steps": [
            ("Event Pattern Matching", "Content-based filtering inspects event envelope headers before routing to workers."),
            ("Audit Archive", "EventBridge Archive preserves full replayable event stream for forensic investigation."),
            ("SQS DLQ Containment", "Poison pill or malformed payloads routed to quarantine DLQ; swarm protected from crash.")
        ]
    },

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
    font-size: 19px;
    color: #0f172a;
    letter-spacing: 0.5px;
    margin-top: 2px;
}
.spec-sub {
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 10px;
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
    padding: 9px;
    box-shadow: 3.5px 3.5px 0px #0f172a;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.panel-header {
    font-family: 'Impact', sans-serif;
    font-size: 13px;
    color: #0f172a;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 3px;
    margin-bottom: 5px;
}
.scene-desc {
    font-size: 10.5px;
    color: #475569;
    font-style: italic;
    line-height: 1.35;
    margin-bottom: 6px;
}
.sfx-badge {
    font-family: 'Impact', sans-serif;
    font-size: 13px;
    padding: 2px 9px;
    border: 2px solid #0f172a;
    border-radius: 6px;
    box-shadow: 2px 2px 0px #0f172a;
    display: inline-block;
    transform: rotate(-1deg);
    letter-spacing: 0.5px;
}
.speech-bubble {
    border: 2px solid #0f172a;
    border-radius: 8px;
    background: #f8fafc;
    padding: 6px 8px;
    margin-top: 5px;
    font-size: 10.5px;
    line-height: 1.3;
    box-shadow: 2px 2px 0px rgba(15, 23, 42, 0.15);
}
.speech-bubble strong {
    color: #0f172a;
}

/* DOWNWARD TRACEABILITY BOX */
.trace-card-box {
    border: 2.5px solid #0f172a;
    border-radius: 9px;
    background: #ffffff;
    padding: 7px 11px;
    margin-top: 6px;
    box-shadow: 3px 3px 0px #0f172a;
}
.trace-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1.5px solid #e2e8f0;
    padding-bottom: 4px;
    margin-bottom: 5px;
}
.trace-badge-tag {
    font-size: 9.5px;
    font-weight: 900;
    padding: 2px 7px;
    border-radius: 4px;
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
    text-transform: uppercase;
}
.trace-path-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    font-weight: 700;
    color: #475569;
}
.trace-steps-container {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 8px;
}
.trace-step-pill {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 5px 7px;
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.trace-step-title {
    font-size: 9.5px;
    font-weight: 800;
    color: #0f172a;
    font-family: 'Segoe UI', sans-serif;
}
.trace-step-desc {
    font-size: 9px;
    color: #334155;
    line-height: 1.25;
    font-family: 'JetBrains Mono', monospace;
}

.rule-footer {
    border: 3px solid #0f172a;
    border-radius: 10px;
    background: #1e293b;
    color: #ffffff;
    padding: 7px 14px;
    box-shadow: 3px 3px 0px #0f172a;
    margin-top: 6px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
}
.rule-title {
    font-size: 10px;
    font-weight: 900;
    color: #f59e0b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.rule-text {
    font-size: 11px;
    font-style: italic;
    color: #e2e8f0;
    line-height: 1.3;
}
.superpower-tag {
    background: #0f172a;
    border: 2px solid #38bdf8;
    color: #38bdf8;
    font-weight: 800;
    font-size: 10px;
    padding: 3px 9px;
    border-radius: 6px;
    white-space: nowrap;
}
.page-footer-num {
    text-align: center;
    font-size: 8.5px;
    font-weight: 700;
    color: #64748b;
    margin-top: 2px;
}
"""

def generate_traced_comic():
    from generate_comic_pdf import episodes

    pages_html = []

    # 1. COVER PAGE
    cover_page = f"""
    <div class="page" style="background: #090d16; color: #ffffff; padding: 0.28in 0.36in; justify-content: space-between;">
        <div style="border: 3px solid #38bdf8; border-radius: 12px; background: #0f172a; padding: 10px 16px; box-shadow: 0 4px 20px rgba(56,189,248,0.25); display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="background: #f59e0b; color: #000; font-weight: 900; font-size: 11px; padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">ANTIGRAVITY COMIC SERIES • ISSUE #1 (TRACED EDITION)</span>
                <div style="font-family: 'Impact', sans-serif; font-size: 25px; color: #38bdf8; letter-spacing: 1px; margin-top: 3px;">THE 3-TIER ENTERPRISE AGENT STACK</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 10px; color: #94a3b8; font-weight: bold;">SPECIAL ARCHITECTURAL EDITION</div>
                <div style="font-size: 11px; color: #10b981; font-weight: 900;">TIER 1 & 2 TRACED DOWN TO TIER 0 AWS</div>
            </div>
        </div>

        <div style="margin: 8px 0; border: 4px solid #38bdf8; border-radius: 12px; overflow: hidden; box-shadow: 5px 5px 0px #0284c7; max-height: 4.6in;">
            <img src="{cover_data_uri}" style="width: 100%; height: auto; display: block;" alt="Comic Cover">
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div style="background: #1e293b; border: 2px solid #475569; border-radius: 10px; padding: 10px 14px;">
                <div style="font-size: 11px; font-weight: 900; color: #38bdf8; text-transform: uppercase; margin-bottom: 4px;">STARRING THE CITADEL CAST</div>
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
                    • <strong>100% Traceability</strong>: Every high-level swarm move maps to physical AWS hardware
                </div>
            </div>
        </div>

        <div style="background: #0f172a; border: 2px solid #f59e0b; border-radius: 8px; padding: 7px 14px; text-align: center; color: #f59e0b; font-size: 11px; font-weight: 800;">
            "Never trust an agent without physical cloud serialization. Every swarm skill traces down to Tier 0 AWS."
        </div>
    </div>
    """
    pages_html.append(cover_page)

    # 2. EPISODES 1 TO 22
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

        # Comic Panels
        panels_html = []
        grid_class = "panel-grid-2" if layout == "2-col" else "panel-grid-3"

        for p in ep["panels"]:
            p_head = p["head"]
            sfx_text, sfx_bg, sfx_col = p["sfx"]
            p_desc = p["desc"]
            
            dialogue_html = ""
            for speaker, text in p["dialogue"]:
                dialogue_html += f"""
                <div class="speech-bubble">
                    <strong>{speaker}:</strong> "{text}"
                </div>
                """

            panel_markup = f"""
            <div class="comic-panel">
                <div>
                    <div class="panel-header">{p_head}</div>
                    <div class="scene-desc">{p_desc}</div>
                    <div style="text-align: center; margin: 3px 0;">
                        <span class="sfx-badge" style="background: {sfx_bg}; color: {sfx_col};">{sfx_text}</span>
                    </div>
                </div>
                <div>
                    {dialogue_html}
                </div>
            </div>
            """
            panels_html.append(panel_markup)

        panels_combined = "".join(panels_html)

        # Downward Traceability Section
        trace_data = TIER_DOWNWARD_TRACES.get(p_num - 1) # Skills 1 to 20 correspond to p_num 2 to 21
        trace_markup = ""

        if trace_data:
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
        elif p_num == 1:
            trace_markup = """
            <div class="trace-card-box">
                <div class="trace-header-row">
                    <span class="trace-badge-tag" style="background: #eab308;">THE ROSETTA STONE PRINCIPLE</span>
                    <span class="trace-path-label">Tier 2 Swarm Lattice ➔ Tier 1 Agent Kernel OS ➔ Tier 0 Cloud Safes</span>
                </div>
                <div class="trace-steps-container">
                    <div class="trace-step-pill">
                        <div class="trace-step-title">Tier 2: Multi-Agent Swarms</div>
                        <div class="trace-step-desc">Small-world topology, cross-pod liaison channels, O(N) whiteboards, Byzantine quorum.</div>
                    </div>
                    <div class="trace-step-pill">
                        <div class="trace-step-title">Tier 1: Individual Agent Kernel</div>
                        <div class="trace-step-desc">Ring 0 Cedar deterministic gate, 15s supervisor watchdogs, context paging, hash chain.</div>
                    </div>
                    <div class="trace-step-pill">
                        <div class="trace-step-title">Tier 0: Cloud Primitives</div>
                        <div class="trace-step-desc">DynamoDB CAS mutex locks, S3 WORM vaults, Nitro Enclaves, KMS key attestation.</div>
                    </div>
                </div>
            </div>
            """
        elif p_num == 22:
            trace_markup = """
            <div class="trace-card-box">
                <div class="trace-header-row">
                    <span class="trace-badge-tag" style="background: #eab308;">MASTER ARCHITECTURAL TRACEABILITY COMPLETE</span>
                    <span class="trace-path-label">20 Skills Fully Grounded in AWS Physical Infrastructure</span>
                </div>
                <div class="trace-steps-container">
                    <div class="trace-step-pill">
                        <div class="trace-step-title">Swarm Resilience Guarantee</div>
                        <div class="trace-step-desc">Zero cascade crashes; circuit breaker benches faulty nodes in <50ms.</div>
                    </div>
                    <div class="trace-step-pill">
                        <div class="trace-step-title">Deterministic Kernel Gate</div>
                        <div class="trace-step-desc">Cedar evaluates AST rules in <1ms; unvetted mutations rejected at OS level.</div>
                    </div>
                    <div class="trace-step-pill">
                        <div class="trace-step-title">Physical Cloud Immutability</div>
                        <div class="trace-step-desc">DynamoDB CAS prevents race conditions; S3 Object Lock enforces 7-year WORM compliance.</div>
                    </div>
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
                    <div style="font-size: 9.5px; font-weight: 800; color: #0f172a; margin-top: 2px;">PAGE {p_num} OF 22 • TRACED COPY</div>
                </div>
            </div>

            <!-- Comic Panels -->
            <div class="panels-container">
                <div class="{grid_class}">
                    {panels_combined}
                </div>
            </div>

            <!-- Downward Traceability to Tier 0 Section -->
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
                The 3-Tier Enterprise Agent Stack (Traced Copy) • Graphic Novel Episode {p_num} • Antigravity AI Engineering
            </div>
        </div>
        """
        pages_html.append(page_markup)

    all_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>The 3-Tier Enterprise Agent Stack - Downward Traced Comic Copy</title>
    <style>
{css}
    </style>
</head>
<body>
{"".join(pages_html)}
</body>
</html>
"""

    # 3. Write Printable HTML
    out_printable_html = "comic_book_traced_printable.html"
    with open(out_printable_html, "w", encoding="utf-8") as f:
        f.write(all_content)
    print(f"Generated {out_printable_html} ({len(all_content)} bytes)")

    # 4. Generate PDF via Edge / Chrome Headless
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
    print(f"Compiling PDF via {chrome_path}...")
    subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(out_pdf):
        print(f"SUCCESS: Generated PDF at {out_pdf} ({os.path.getsize(out_pdf)/(1024*1024):.2f} MB)")
    else:
        print("WARNING: PDF generation failed, check browser path.")

    # 5. Create Responsive Web Reader for GitHub Pages
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
  <div class="comic-nav-title">⬇️ THE 3-TIER AGENT STACK COMIC (TRACED COPY)</div>
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
