# -*- coding: utf-8 -*-
"""
build_side_by_side_skills_pdf.py
Generates the definitive 22-page landscape PDF in pure LIGHT MODE:
'20_Agentic_Skills_Side_By_Side_Guide.pdf'
Features:
- Page 1: Architectural Methodology Cover & The Skill Authoring Rosetta Stone (Light Mode)
- Pages 2-21: 20 Skills, 1 Page per Skill (Light Mode Side-by-Side: 4th-Grader Model vs. Production SKILL.md Contract)
- Page 22: The Master 3-Tier Enterprise Architecture Blueprint & Wire Graph (Light Mode Header)
"""

import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from PIL import Image
import fitz

from generate_connected_21_page_pdf import SKILLS_DATA as KID_SKILLS
from update_aws_basics_studio import SKILLS_DATA as PROD_SKILLS

PDF_OUTPUT = "20_Agentic_Skills_Side_By_Side_Guide.pdf"
GRAPH_PNG = "three_tier_skill_dependency_graph.png"

# Text wrapping helper
def wrap_text(c, text, font_name, font_size, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        if c.stringWidth(test_line, font_name, font_size) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

# Structured production data for the 20 skills
PROD_DETAILS = [
    # 1: aws-bedrock
    {
        "yaml": [
            ("name:", "aws-bedrock"),
            ("description:", "Foundation model proposal engine generating structured JSON"),
            ("tier:", "Level 0 (Cloud Primitives)"),
            ("ring:", "Ring 3 (Untrusted Proposal Space)"),
            ("permissions:", "[bedrock:InvokeModel]"),
            ("tools:", "[synthesize_proposal, validate_schema]")
        ],
        "axiom": "Inference engine in Ring 3; proposes state mutations with 0 IAM write access.",
        "invariants": [
            "• Zero Direct Execution: Never mutates databases or invokes live APIs directly.",
            "• Deterministic Schema: Output must strictly validate against JSON Schema.",
            "• Quarantined Payloads: All outputs marked RING3_PROPOSAL until kernel approval."
        ],
        "pipeline": [
            "1. Receives natural language objective & response schema from Kernel (#8).",
            "2. Invokes bedrock:InvokeModel with temperature <= 0.2.",
            "3. Validates output JSON against typed contract; quarantines payload.",
            "4. Hands proposal to Prefrontal Kernel Judge (#8) for verification."
        ],
        "failures": [
            "• Schema Parse Error: Returns REJECTED_SCHEMA for structured retry (max 2).",
            "• Rate Limit (429): Exponential backoff with full jitter (capped at 3 retries)."
        ]
    },
    # 2: aws-agentcore
    {
        "yaml": [
            ("name:", "aws-agentcore"),
            ("description:", "Cedar policy guardrail gate evaluating authorization AST"),
            ("tier:", "Level 0 (Cloud Primitives)"),
            ("ring:", "Ring 0 (Deterministic Gatekeeper)"),
            ("permissions:", "[agentcore:EvaluatePolicy, cedar:Authorize]"),
            ("tools:", "[evaluate_guardrail, inspect_syscall]")
        ],
        "axiom": "Authoritative gate evaluating Cedar AST policies against untrusted proposals.",
        "invariants": [
            "• Default Deny: Unmatched principal/action/resource triples are blocked.",
            "• Sub-10ms Latency: In-memory AST evaluation before any network I/O.",
            "• Immutable Rules: Cedar policy files sealed in versioned repositories."
        ],
        "pipeline": [
            "1. Intercepts proposed syscall from Kernel Propose-Decide (#8).",
            "2. Evaluates Cedar policy AST: Permit/Forbid on (Principal, Action, Resource).",
            "3. If FORBID: Emits immediate Ring 0 Security Violation alarm.",
            "4. If PERMIT: Generates signed ephemeral authorization token."
        ],
        "failures": [
            "• Unauthorized Syscall: Rejection logged to CloudWatch audit trail.",
            "• Syntax Error in Policy: Fails closed (DENY) to prevent security holes."
        ]
    },
    # 3: aws-s3-vault
    {
        "yaml": [
            ("name:", "aws-s3-vault"),
            ("description:", "Immutable WORM receipt vault with Object Lock compliance"),
            ("tier:", "Level 0 (Cloud Primitives)"),
            ("ring:", "Ring 0 (Physical Hardware Boundary)"),
            ("permissions:", "[s3:PutObject, s3:GetObjectLockLegalHold]"),
            ("tools:", "[store_compliance_receipt, get_immutable_fact]")
        ],
        "axiom": "Cryptographic WORM storage ensuring past execution records cannot be altered.",
        "invariants": [
            "• Strict WORM Compliance: S3 Object Lock retains objects for >= 7 years.",
            "• SHA-256 Checksums: Every receipt verified via Content-MD5 / SHA-256.",
            "• No Overwrites: Versioning enabled; s3:DeleteObject strictly forbidden."
        ],
        "pipeline": [
            "1. Ingests execution receipts from Context Pager (#12) & Episodic Ledger (#13).",
            "2. Calculates cryptographic SHA-256 digest of payload.",
            "3. Stores object under s3://agent-vault/{agent_id}/{timestamp}.json with ObjectLock.",
            "4. Returns immutable ARN receipt used by Grounding Certifier (#14)."
        ],
        "failures": [
            "• Checksum Mismatch: Aborts transaction; logs data corruption event.",
            "• Lock Expiry Attempt: S3 compliance mode denies administrative overrides."
        ]
    },
    # 4: aws-database
    {
        "yaml": [
            ("name:", "aws-database"),
            ("description:", "DynamoDB CAS mutex, OpenSearch vectors & Neptune graphs"),
            ("tier:", "Level 0 (Cloud Primitives)"),
            ("ring:", "Ring 0 (State & Storage Engine)"),
            ("permissions:", "[dynamodb:PutItem, opensearch:Search, neptune:Query]"),
            ("tools:", "[cas_acquire_lock, vector_knn_query, graph_triple_lookup]")
        ],
        "axiom": "Tri-store architecture: atomic locks, semantic embeddings, and graph relations.",
        "invariants": [
            "• Atomic CAS Concurrency: Mutex writes require conditional version check.",
            "• Vector Similarity Bound: Cosine similarity threshold >= 0.82 for facts.",
            "• Graph Integrity: Neptune entity relations must satisfy valid ontology."
        ],
        "pipeline": [
            "1. DynamoDB: Provides conditional write primitives for Kernel Mutex (#11).",
            "2. OpenSearch: Returns top-k semantic chunks with distance metrics.",
            "3. Neptune: Evaluates entity-relationship triples for Detective Triangulator (#14).",
            "4. Emits verified state snapshots to the central agent kernel."
        ],
        "failures": [
            "• ConditionalCheckFailed: DynamoDB indicates active lock contention.",
            "• Low Vector Score: Returns NO_SEMANTIC_MATCH to prevent hallucinated grounding."
        ]
    },
    # 5: aws-lambda
    {
        "yaml": [
            ("name:", "aws-lambda"),
            ("description:", "Isolated Firecracker microVM sandboxes for stateless tasks"),
            ("tier:", "Level 0 (Cloud Primitives)"),
            ("ring:", "Ring 3 (Isolated MicroVM Sandbox)"),
            ("permissions:", "[lambda:InvokeFunction]"),
            ("tools:", "[invoke_sandboxed_tool, terminate_microvm]")
        ],
        "axiom": "Zero-footprint ephemeral compute running calculations in Firecracker microVMs.",
        "invariants": [
            "• Strict Ephemerality: MicroVM disposed after task; 0 disk persistence.",
            "• Hard Wall-Clock Cap: Execution forcibly terminated after 15 seconds.",
            "• Resource Sandboxing: Memory capped at 512MB; isolated VPC subnet."
        ],
        "pipeline": [
            "1. Runbook Engine (#9) compiles atomic task into Python payload.",
            "2. Invokes Lambda function synchronously inside isolated Firecracker sandbox.",
            "3. Watchdog Supervisor (#10) starts external countdown timer.",
            "4. Collects stdout & return value; tears down sandbox immediately."
        ],
        "failures": [
            "• Timeout (15s): Lambda runtime terminates process; supervisor alerts swarm.",
            "• Memory Exhaustion (OOM): Returns OUT_OF_MEMORY error to Runbook Engine."
        ]
    },
    # 6: aws-stepfunctions
    {
        "yaml": [
            ("name:", "aws-stepfunctions"),
            ("description:", "Deterministic hierarchical finite state machine orchestrator"),
            ("tier:", "Level 0 (Cloud Primitives)"),
            ("ring:", "Ring 0 (Deterministic State Machine)"),
            ("permissions:", "[states:StartExecution, states:DescribeExecution]"),
            ("tools:", "[start_state_machine, advance_checkpoint, rollback_step]")
        ],
        "axiom": "Strict state transition engine guaranteeing runbooks follow exact recipes.",
        "invariants": [
            "• Forward-Only Progression: Steps cannot skip ahead without prerequisite success.",
            "• Automatic Compensation: Step failures trigger registered rollback handler.",
            "• Exact Event History: Every transition logged with monotonic sequence ID."
        ],
        "pipeline": [
            "1. Kernel Runbook Engine (#9) deploys Amazon States Language (ASL) definition.",
            "2. Advances through tasks: Step 1 -> Checkpoint -> Step 2 -> Checkpoint.",
            "3. Verifies each output payload against JSON Schema before next transition.",
            "4. Emits completion event to EventBridge Walkie-Talkie (#7)."
        ],
        "failures": [
            "• Step Task Failure: Executes Catch / Retry blocks with exponential backoff.",
            "• Irrecoverable Error: Triggers compensatory rollback to previous safe state."
        ]
    },
    # 7: aws-client-api
    {
        "yaml": [
            ("name:", "aws-client-api"),
            ("description:", "Amazon EventBridge pub/sub message bus and API Gateway"),
            ("tier:", "Level 0 (Cloud Primitives)"),
            ("ring:", "Ring 0 (Perimeter Ingress & Egress)"),
            ("permissions:", "[events:PutEvents, apigateway:POST]"),
            ("tools:", "[publish_swarm_event, broadcast_emergency_alarm]")
        ],
        "axiom": "High-throughput asynchronous event bus routing signals without broadcast shouting.",
        "invariants": [
            "• Targeted Routing: Event patterns match specific pods; 0 global broadcast spam.",
            "• At-Least-Once Delivery: Events buffered in DLQ if consumer is temporarily busy.",
            "• Strict OpenAPI Schema: Payload shape enforced at the API perimeter."
        ],
        "pipeline": [
            "1. Kernel Supervisor (#10) or Swarm Router publishes event to bus.",
            "2. EventBridge evaluates pattern filter: { detail-type: 'SwarmTaskDispatched' }.",
            "3. Delivers event directly to subscriber pod's dedicated queue.",
            "4. Emits metrics to CloudWatch for monitoring latency and hop counts."
        ],
        "failures": [
            "• Consumer Unreachable: Retries 3 times before routing to Dead Letter Queue (DLQ).",
            "• Malformed Payload: Rejected at ingress with HTTP 400 Bad Request."
        ]
    },
    # 8: kernel-propose-decide
    {
        "yaml": [
            ("name:", "kernel-propose-decide"),
            ("description:", "Prefrontal executive arbiter enforcing Ring 0 verdict over proposals"),
            ("tier:", "Level 1 (Agent OS Kernel)"),
            ("ring:", "Ring 0 (Executive Control)"),
            ("permissions:", "[kernel:EvaluateProposal, kernel:DispatchSyscall]"),
            ("tools:", "[evaluate_model_proposal, commit_kernel_verdict]")
        ],
        "axiom": "Separation of inference (Ring 3) from executive authority (Ring 0): Action = Verdict(Proposal).",
        "invariants": [
            "• Zero Direct Mutation: Ring 3 models hold 0 IAM credentials.",
            "• Mandatory Quorum Gate: Requires active Cedar (#2) & CAS lock (#11).",
            "• Strict Type Safety: Payloads failing JSON Schema trigger immediate halt."
        ],
        "pipeline": [
            "1. Ingests proposed tool call JSON from Bedrock (#1) or Liaison Router (#16).",
            "2. Validates payload against JSON Schema and active goal constraints.",
            "3. Verifies Cedar guardrails (#2) and DynamoDB CAS mutex lease (#11).",
            "4. Dispatches verified syscall to Level 0 AWS hardware; logs verdict to S3."
        ],
        "failures": [
            "• Schema Parse Failure: Returns REJECTED_SCHEMA for retry (max 2).",
            "• Policy Denial: Emits security alert and evicts bad proposal to ledger (#13)."
        ]
    },
    # 9: kernel-runbook-engine
    {
        "yaml": [
            ("name:", "kernel-runbook-engine"),
            ("description:", "Directed Acyclic Graph (DAG) procedural execution engine"),
            ("tier:", "Level 1 (Agent OS Kernel)"),
            ("ring:", "Ring 0 (Procedural Orchestrator)"),
            ("dependencies:", "[aws-stepfunctions, aws-lambda]"),
            ("tools:", "[compile_mission_dag, execute_step_barrier]")
        ],
        "axiom": "Decomposes complex objectives into verifiable DAG runbooks with step barriers.",
        "invariants": [
            "• Topological Order: No task executes until all parent nodes succeed.",
            "• Step Barrier Verification: Each phase output verified before next begins.",
            "• Reentrancy: Idempotent step keys allow safe resuming after reboot."
        ],
        "pipeline": [
            "1. Receives multi-pod mission topology from Swarm Topology Builder (#15).",
            "2. Compiles dependency DAG with clear step checkpoints.",
            "3. Dispatches individual steps to Step Functions (#6) & Lambda (#5).",
            "4. Records milestone completion receipts to Episodic Ledger (#13)."
        ],
        "failures": [
            "• DAG Node Failure: Halts branch execution; triggers compensatory rollback.",
            "• Cyclic Dependency: Static DAG validator rejects circular graphs at compile time."
        ]
    },
    # 10: kernel-supervisor-circuit
    {
        "yaml": [
            ("name:", "kernel-supervisor-circuit"),
            ("description:", "Execution watchdog monitoring loops, timeouts, and deadlocks"),
            ("tier:", "Level 1 (Agent OS Kernel)"),
            ("ring:", "Ring 0 (Supervisor Control)"),
            ("dependencies:", "[aws-client-api, aws-lambda]"),
            ("tools:", "[monitor_heartbeat, trip_circuit_breaker]")
        ],
        "axiom": "Watchdog supervisor enforcing timeouts and tripping circuit breakers on infinite loops.",
        "invariants": [
            "• Timeout Ceiling: Any single execution cycle hard-capped at 15 seconds.",
            "• Deadlock Detection: Repeated identical proposals trigger loop interrupt.",
            "• Unconditional Stop: Supervisor signal overrides active agent execution."
        ],
        "pipeline": [
            "1. Arm countdown egg timer when agent starts task.",
            "2. Ingests tick signals from Hop Limiter (#17) and Circuit Breaker (#20).",
            "3. If loop detected or timeout exceeded: trips breaker and stops agent.",
            "4. Radios emergency alert to EventBridge (#7) and triggers clean reset."
        ],
        "failures": [
            "• Agent Unresponsive: Forcefully terminates Firecracker MicroVM container.",
            "• Cascade Loop: Quarantines agent pod and notifies swarm coordinator."
        ]
    },
    # 11: kernel-mutex-lease
    {
        "yaml": [
            ("name:", "kernel-mutex-lease"),
            ("description:", "Distributed CAS mutex coordinator with automatic TTL leases"),
            ("tier:", "Level 1 (Agent OS Kernel)"),
            ("ring:", "Ring 0 (Concurrency Control)"),
            ("dependencies:", "[aws-database]"),
            ("tools:", "[acquire_lease, heartbeat_lease, release_lease]")
        ],
        "axiom": "Distributed lock manager preventing race conditions via atomic compare-and-swap (CAS).",
        "invariants": [
            "• Strict Mutual Exclusion: Exactly 1 agent holds the talking stick per resource.",
            "• Deadlock Immunity via TTL: Leases auto-expire in 15s if agent crashes.",
            "• Monotonic Fence Tokens: Incremental integer tokens reject stale out-of-order writes."
        ],
        "pipeline": [
            "1. Agent requests write access to shared resource (e.g. Whiteboard #18).",
            "2. Executes DynamoDB conditional PutItem with TTL and fence token.",
            "3. While task runs: refreshes TTL heartbeat every 5 seconds.",
            "4. Releases lease upon completion or revokes immediately if benched by #20."
        ],
        "failures": [
            "• Contention (409): Truncated binary exponential backoff with jitter.",
            "• Abandoned Lease: Automatic TTL expiration dissolves lock safely."
        ]
    },
    # 12: kernel-context-pager
    {
        "yaml": [
            ("name:", "kernel-context-pager"),
            ("description:", "Virtual memory manager paging inactive frames to S3 WORM safe"),
            ("tier:", "Level 1 (Agent OS Kernel)"),
            ("ring:", "Ring 0 (Memory Paging System)"),
            ("dependencies:", "[aws-s3-vault]"),
            ("tools:", "[page_out_cold_frames, page_in_frame, compact_context]")
        ],
        "axiom": "Virtual memory paging keeping working attention window sharp (8k tokens) without amnesia.",
        "invariants": [
            "• Bounded Attention Window: Active RAM capped at 8,192 tokens.",
            "• Zero Data Loss: Evicted cold frames stored immutably in S3 (#3).",
            "• Fast Hydration: Paged frames retrieved by key in < 25 milliseconds."
        ],
        "pipeline": [
            "1. Monitors active token count during reasoning loop.",
            "2. When token threshold >= 75%: evicts oldest reasoning frames to S3 Vault (#3).",
            "3. Leaves lightweight pointer stub: [PAGED: frame_id, s3_uri, summary].",
            "4. Pages frame back into memory only when specific reference is requested."
        ],
        "failures": [
            "• Memory Overflow: Emergency compaction strips scratchpad before LLM crash.",
            "• S3 Read Error: Retrieves verified copy from secondary backup replica."
        ]
    },
    # 13: kernel-episodic-ledger
    {
        "yaml": [
            ("name:", "kernel-episodic-ledger"),
            ("description:", "Append-only SHA-256 hash-chained immutable audit ledger"),
            ("tier:", "Level 1 (Agent OS Kernel)"),
            ("ring:", "Ring 0 (Audit & Ledger Engine)"),
            ("dependencies:", "[aws-s3-vault]"),
            ("tools:", "[append_block, verify_chain_integrity, export_audit_log]")
        ],
        "axiom": "Cryptographic hash-chain linking every action to its perception: Block(n) = SHA256(Block(n-1) + Data).",
        "invariants": [
            "• Append-Only: No block can ever be modified, erased, or reordered.",
            "• Cryptographic Chaining: Every block embeds previous block's SHA-256 hash.",
            "• WORM Durability: Flushed blocks written to S3 Object Lock vault (#3)."
        ],
        "pipeline": [
            "1. Ingests completed action record from Whiteboard (#18) or Runbook (#9).",
            "2. Combines previous block hash + timestamp + action payload.",
            "3. Computes new SHA-256 digest: seals wax stamp on new page.",
            "4. Pushes immutable block to S3 WORM safe for compliance auditing."
        ],
        "failures": [
            "• Tampering Attempt: Any altered past block breaks all downstream hash checks.",
            "• Network Partition: Buffers blocks locally in Ring 0 until S3 link resumes."
        ]
    },
    # 14: kernel-grounding-certifier
    {
        "yaml": [
            ("name:", "kernel-grounding-certifier"),
            ("description:", "Multi-source fact triangulation requiring 3 independent proofs"),
            ("tier:", "Level 1 (Agent OS Kernel)"),
            ("ring:", "Ring 0 (Truth Verification)"),
            ("dependencies:", "[aws-s3-vault, aws-database]"),
            ("tools:", "[triangulate_fact, verify_quorum_ballot]")
        ],
        "axiom": "Crushes hallucinations by demanding 3 independent physical proofs before certifying facts.",
        "invariants": [
            "• Triangulation Rule: Fact certified ONLY when S3 receipt, vector match & graph agree.",
            "• Strict Cosine Floor: Vector distance match must exceed 0.82 threshold.",
            "• Deterministic Receipts: Supplies verified cryptographic certificates to #19."
        ],
        "pipeline": [
            "1. Ingests candidate fact from model proposal.",
            "2. Checks Proof 1: S3 WORM receipt photo (#3).",
            "3. Checks Proof 2: OpenSearch vector cosine similarity in Database (#4).",
            "4. Checks Proof 3: Neptune entity graph relationship in Database (#4).",
            "5. If all 3 match: issues CERT_OK token up to Ballot Box (#19)."
        ],
        "failures": [
            "• Unconfirmed Fact: Flagged as UNVERIFIED_RUMOR; discarded from decision path.",
            "• Conflicting Proofs: Rejects proposal and logs conflict to Episodic Ledger (#13)."
        ]
    },
    # 15: swarm-topology-builder
    {
        "yaml": [
            ("name:", "swarm-topology-builder"),
            ("description:", "Watts-Strogatz small-world lattice generator with shortcut bridges"),
            ("tier:", "Level 2 (Multi-Agent Swarms)"),
            ("ring:", "Ring 0 (Swarm Fabric Governance)"),
            ("dependencies:", "[kernel-runbook-engine]"),
            ("tools:", "[generate_lattice, deploy_liaison_shortcuts, compute_metrics]")
        ],
        "axiom": "Generates small-world graphs (p=0.15): high clustering (C=0.68) with short paths (L=1.8).",
        "invariants": [
            "• Clustered Pods: Specialist agents grouped into tightly-coupled domains (Finance, etc.).",
            "• Bounded Diameter: Inter-cluster zip-lines keep network diameter <= 3 hops.",
            "• No All-to-All Mesh: Completely eliminates O(N^2) exponential message explosions."
        ],
        "pipeline": [
            "1. Organizes 12 agent nodes into 3 specialist pods (Finance, Compliance, Ops).",
            "2. Establishes dense local connections within each clubhouse.",
            "3. Rewires p=0.15 long-range shortcut bridges between pod liaison leaders.",
            "4. Feeds execution stages down into Kernel Runbook Engine (#9)."
        ],
        "failures": [
            "• Network Partition: Adds dynamic backup shortcut bridge if liaison fails.",
            "• Topology Drift: Periodically verifies clustering coefficient and path length."
        ]
    },
    # 16: swarm-liaison-router
    {
        "yaml": [
            ("name:", "swarm-liaison-router"),
            ("description:", "Cross-pod liaison ambassador routing notes without stampedes"),
            ("tier:", "Level 2 (Multi-Agent Swarms)"),
            ("ring:", "Ring 0 (Inter-Pod Routing)"),
            ("dependencies:", "[kernel-propose-decide]"),
            ("tools:", "[route_cross_pod_message, inspect_pod_envelope]")
        ],
        "axiom": "Designates ambassador nodes to mediate inter-pod messaging, preventing broadcast stampedes.",
        "invariants": [
            "• Isolated Pod Boundary: Raw internal pod messages never leak cross-pod.",
            "• Mandatory Kernel Gate: Every inter-pod envelope vetted by Judge (#8).",
            "• Bounded Bandwidth: Rate-limited message exchange via EventBridge bus."
        ],
        "pipeline": [
            "1. Pod member hands cross-discipline inquiry to designated Liaison Leader.",
            "2. Liaison inspects envelope; packages structured query.",
            "3. Transports message across golden shortcut bridge to peer Liaison.",
            "4. Receiving Liaison passes note through Kernel Propose-Decide (#8) before action."
        ],
        "failures": [
            "• Unauthorized Sender: Drops unvetted message; logs breach to supervisor.",
            "• Queue Backpressure: Throttles ingress traffic to prevent pod buffer overflow."
        ]
    },
    # 17: swarm-hop-limiter
    {
        "yaml": [
            ("name:", "swarm-hop-limiter"),
            ("description:", "Bounded TTL ticket puncher eliminating runaway gossip loops"),
            ("tier:", "Level 2 (Multi-Agent Swarms)"),
            ("ring:", "Ring 0 (Loop Prevention Engine)"),
            ("dependencies:", "[kernel-supervisor-circuit]"),
            ("tools:", "[punch_hop_ticket, check_ttl_budget, trip_hop_exhaustion]")
        ],
        "axiom": "Limits delegation depth with a strict 3-ticket budget, preventing infinite games of tag.",
        "invariants": [
            "• Hard Hop Ceiling: Maximum delegation depth strictly capped at <= 3 hops.",
            "• Monotonic Decrement: Every agent handoff consumes exactly 1 ticket.",
            "• Cycle Detection: Envelope maintains visited node hash list to prevent loops."
        ],
        "pipeline": [
            "1. Stamped message created with budget: ttlBudget = 3.",
            "2. Agent 1 -> Agent 2: Ticket #1 punched (ttl = 2).",
            "3. Agent 2 -> Agent 3: Ticket #2 punched (ttl = 1).",
            "4. If ticket count reaches 0 without task completion: signals Watchdog (#10)."
        ],
        "failures": [
            "• Zero Tickets Remaining: Trips Watchdog Sparky (#10) to halt loop immediately.",
            "• Circular Routing Detected: Drops packet and alerts circuit breaker (#20)."
        ]
    },
    # 18: swarm-shared-whiteboard
    {
        "yaml": [
            ("name:", "swarm-shared-whiteboard"),
            ("description:", "Partitioned O(N) blackboard shared memory with atomic lanes"),
            ("tier:", "Level 2 (Multi-Agent Swarms)"),
            ("ring:", "Ring 0 (Shared State Fabric)"),
            ("dependencies:", "[kernel-mutex-lease, kernel-episodic-ledger]"),
            ("tools:", "[read_lane_state, write_lane_atomic, seal_whiteboard_snapshot]")
        ],
        "axiom": "Replaces O(N^2) point-to-point chatter with an O(N) partitioned blackboard.",
        "invariants": [
            "• Partitioned Lane Ownership: Only Finance writes Finance; only Ops writes Ops.",
            "• Atomic Mutex Writes: Updating a lane requires holding Talking Stick (#11).",
            "• Immutable Final State: Finished boards stamped into Wax Diary (#13)."
        ],
        "pipeline": [
            "1. Agents read global board state with zero point-to-point network chatter.",
            "2. When pod has verified result: acquires Mutex lease from Talking Stick (#11).",
            "3. Commits typed update to designated lane (Finance, Compliance, or Ops).",
            "4. Emits lightweight state_changed event; seals final snapshot to S3 Ledger (#13)."
        ],
        "failures": [
            "• Write Collision: Backs off and retries via DynamoDB CAS mutex.",
            "• Corrupted Data: Consensus Arbiter (#19) invalidates poisoned entries."
        ]
    },
    # 19: swarm-consensus-arbiter
    {
        "yaml": [
            ("name:", "swarm-consensus-arbiter"),
            ("description:", "Byzantine fault-tolerant supermajority quorum arbiter"),
            ("tier:", "Level 2 (Multi-Agent Swarms)"),
            ("ring:", "Ring 0 (Consensus Engine)"),
            ("dependencies:", "[kernel-grounding-certifier]"),
            ("tools:", "[collect_ballot, compute_byzantine_quorum, commit_decision]")
        ],
        "axiom": "Supermajority consensus (>= 2/3 + 1) ensuring fair decisions even if nodes glitch or lie.",
        "invariants": [
            "• Byzantine Threshold: Requires >= 10 out of 12 votes (>= 2/3 + 1 supermajority).",
            "• Cryptographic Proof: Every ballot must carry valid Grounding Certificate (#14).",
            "• Liveness Guarantee: Up to 3 faulty or malicious agents cannot stall system."
        ],
        "pipeline": [
            "1. Swarm coordinator broadcasts high-stakes ballot proposal to all 12 nodes.",
            "2. Nodes vote YES/NO accompanied by 3-point fact proof from Detective (#14).",
            "3. Arbiter tabulates verified ballots: requires >= 10 matching votes.",
            "4. Commits binding supermajority verdict to S3 WORM Vault (#3)."
        ],
        "failures": [
            "• Quorum Not Reached: Motion rejected; falls back to human escalation.",
            "• Rogue Voting: Faulty agent ballots discarded; agent flagged for quarantine."
        ]
    },
    # 20: swarm-circuit-breaker
    {
        "yaml": [
            ("name:", "swarm-circuit-breaker"),
            ("description:", "Referee red card bencing faulty agents and revoking locks"),
            ("tier:", "Level 2 (Multi-Agent Swarms)"),
            ("ring:", "Ring 0 (Fault Isolation)"),
            ("dependencies:", "[kernel-supervisor-circuit, kernel-mutex-lease]"),
            ("tools:", "[detect_anomaly, bench_agent, revoke_all_leases]")
        ],
        "axiom": "Benches hallucinating or looping agents instantly to prevent cascading team failures.",
        "invariants": [
            "• Instant Quarantine: Benched agents immediately cut off from swarm network.",
            "• Mutex Lease Revocation: Forcibly snatches Talking Stick (#11) from benched node.",
            "• Dynamic Topology Healing: Reroutes liaison bridges around quarantined agent."
        ],
        "pipeline": [
            "1. Monitors agent error rates, timeouts, and ungrounded proposal attempts.",
            "2. If error count exceeds threshold (3 strikes): blows red card whistle.",
            "3. Signals Watchdog Sparky (#10) to terminate agent's execution thread.",
            "4. Revokes DynamoDB mutex lease (#11) and quarantines agent on bench for 5 min."
        ],
        "failures": [
            "• Cascade Panic: Quarantines up to 3 nodes independently while maintaining quorum.",
            "• Critical Pod Outage: Spawns fresh replacement MicroVM container via Lambda (#5)."
        ]
    }
]

def render_cover_page(c, width, height):
    # Pure clean light background
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.rect(0, 0, width, height, stroke=0, fill=1)

    # Top accent line
    c.setFillColor(colors.HexColor("#0284c7"))
    c.rect(0, height - 8, width, 8, stroke=0, fill=1)

    # Title container (clean white card with crisp border)
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#cbd5e1"))
    c.roundRect(30, height - 135, width - 60, 110, 10, stroke=1, fill=1)

    c.setFillColor(colors.HexColor("#0284c7"))
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(45, height - 48, "ENTERPRISE AI ARCHITECTURE • SPECIFICATION & PEDAGOGY")

    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 22)
    c.drawString(45, height - 76, "The 3-Tier Enterprise Agent Stack")

    c.setFillColor(colors.HexColor("#475569"))
    c.setFont("Helvetica", 11)
    c.drawString(45, height - 98, "Side-by-Side Study Guide: Production SKILL.md Specifications vs. 4th-Grader Mental Models")
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawString(45, height - 116, "Learn how to architect, structure, and document agentic skills with rigorous engineering contracts and intuitive metaphors.")

    # 3-Tier Summary Boxes in Light Mode
    box_w = (width - 60 - 30) / 3
    box_h = 75
    tiers = [
        ("TIER 0: CLOUD PRIMITIVES", "Skills #1 – #7", "Physical AWS hardware, DynamoDB CAS locks, S3 WORM vaults, Firecracker microVMs, and EventBridge buses.", "#ecfdf5", "#059669", "#065f46"),
        ("TIER 1: AGENT OS KERNEL", "Skills #8 – #14", "Individual robot brain: Prefrontal propose-decide gates, DAG runbooks, mutex leases, context pagers, and fact detectives.", "#eff6ff", "#2563eb", "#1e40af"),
        ("TIER 2: MULTI-AGENT SWARMS", "Skills #15 – #20", "Social clubhouse governance: Watts-Strogatz small worlds, liaison ambassadors, bounded hops, shared whiteboards & quorums.", "#faf5ff", "#7c3aed", "#5b21b6")
    ]
    for idx, (t_title, t_sub, t_desc, bg_color, border_color, text_color) in enumerate(tiers):
        bx = 30 + idx * (box_w + 15)
        by = height - 225
        c.setFillColor(colors.HexColor(bg_color))
        c.setStrokeColor(colors.HexColor(border_color))
        c.roundRect(bx, by, box_w, box_h, 8, stroke=1, fill=1)

        c.setFillColor(colors.HexColor(text_color))
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(bx + 12, by + box_h - 18, t_title)
        c.setFillColor(colors.HexColor("#0f172a"))
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(bx + 12, by + box_h - 32, t_sub)
        
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.HexColor("#334155"))
        lines = wrap_text(c, t_desc, "Helvetica", 7.5, box_w - 24)
        ly = by + box_h - 46
        for l in lines:
            c.drawString(bx + 12, ly, l)
            ly -= 9.5

    # ROSETTA STONE TRANSLATION TABLE (Light Mode)
    ty = height - 245
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#cbd5e1"))
    c.roundRect(30, 36, width - 60, ty - 36, 10, stroke=1, fill=1)

    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(45, ty - 22, "THE SKILL AUTHORING ROSETTA STONE: HOW PLAYGROUND ANALOGIES MAP TO CODE")

    # Table Header
    th_y = ty - 42
    c.setFillColor(colors.HexColor("#f1f5f9"))
    c.rect(42, th_y - 8, width - 84, 22, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(50, th_y + 4, "4TH-GRADER CARD COMPONENT")
    c.drawString(220, th_y + 4, "INTUITIVE PLAYGROUND METAPHOR")
    c.drawString(420, th_y + 4, "PRODUCTION SKILL.MD EQUIVALENT")
    c.drawString(610, th_y + 4, "RIGOROUS ENGINEERING CONTRACT")

    rows = [
        ("Hero Persona & Title", "Meet Buzzy the Robot / Talking Stick", "YAML Frontmatter (name, version)", "Unique identifier, tier level, privilege ring."),
        ("One-Sentence Pitch", "Super-fast imagination machine", "YAML 'description' field", "Semantic summary indexed by router models."),
        ("Playground Recess Story", "Buzzy writes on paper with hands locked", "1. Purpose & Architectural Boundary", "Strict operational boundary; separation of concerns."),
        ("Toy Box Flowchart", "Idea Box -> Paper Blueprint -> Safe World", "2. Interface Contract (JSON Schema)", "Typed JSON schema validating inputs & returns."),
        ("The Golden Rule", "'Wait for the stick before your turn!'", "3. Core System Invariants", "Non-negotiable invariants (CAS locks, zero IAM write)."),
        ("Page 22 Wire Connection", "Blue wire plugs down into Safe #3", "4. Execution Flow & Syscalls", "Deterministic state machine and downstream calls."),
        ("Superpower", "Crushes hallucinations with 3 clues", "5. Failure Modes & Self-Healing", "SLAs, timeout caps, fallback rollback handlers.")
    ]

    ry = th_y - 24
    for r_idx, (r1, r2, r3, r4) in enumerate(rows):
        if r_idx % 2 == 1:
            c.setFillColor(colors.HexColor("#f8fafc"))
            c.rect(42, ry - 6, width - 84, 18, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor("#0f172a"))
        c.drawString(50, ry + 2, r1)
        c.setFont("Helvetica", 7.2)
        c.setFillColor(colors.HexColor("#475569"))
        c.drawString(220, ry + 2, r2)
        c.setFont("Courier-Bold", 7.2)
        c.setFillColor(colors.HexColor("#0284c7"))
        c.drawString(420, ry + 2, r3)
        c.setFont("Helvetica", 7.2)
        c.setFillColor(colors.HexColor("#334155"))
        c.drawString(610, ry + 2, r4)
        ry -= 20

    # Footer note
    c.setFillColor(colors.HexColor("#64748b"))
    c.setFont("Helvetica", 8)
    c.drawString(45, 18, "Generated by Antigravity AI Engineering • 20 Skills Side-by-Side Study Guide (Light Mode)")
    c.drawRightString(width - 45, 18, "Page 1 of 22 • Methodology & Rosetta Stone")

    c.showPage()

def render_side_by_side_page(c, width, height, k_skill, p_skill, p_detail, page_num):
    tier_color = k_skill["tier_color"]
    col_w = 368
    col_h = 504
    left_x = 20
    right_x = 404
    col_y = 28

    # Background of entire page: crisp light canvas
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.rect(0, 0, width, height, stroke=0, fill=1)

    # 1. TOP HEADER BAR (height 50)
    c.setFillColor(tier_color)
    c.rect(0, height - 50, width, 50, stroke=0, fill=1)

    # Symbol Badge
    c.setFillColor(colors.white)
    c.roundRect(20, height - 40, 75, 30, 6, stroke=0, fill=1)
    c.setFillColor(tier_color)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawCentredString(57, height - 30, k_skill["symbol"])

    # Title & Subtitle
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13.5)
    c.drawString(108, height - 28, k_skill["title"])
    c.setFont("Helvetica", 8.5)
    c.drawString(108, height - 42, f"Side-by-Side Study: 4th-Grader Mental Model vs. Production SKILL.md Specification")

    # Tier Tag on Top Right
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(width - 20, height - 26, k_skill["tier"].upper())
    c.setFont("Helvetica", 8)
    c.drawRightString(width - 20, height - 40, f"Skill #{k_skill['page']} of 20")

    # 2. FOOTER
    c.setFillColor(colors.HexColor("#64748b"))
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(20, 14, "THE 3-TIER ENTERPRISE AGENT STACK — SIDE-BY-SIDE ARCHITECTURAL STUDY GUIDE (LIGHT MODE)")
    c.drawRightString(width - 20, 14, f"Skill #{k_skill['page']} of 20 | Page {page_num} of 22")

    # 3. LEFT COLUMN: 4TH-GRADER PLAYGROUND MENTAL MODEL (CLEAN WHITE CARD)
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#cbd5e1"))
    c.roundRect(left_x, col_y, col_w, col_h, 8, stroke=1, fill=1)

    # Left Header
    c.setFillColor(colors.HexColor("#eff6ff"))
    c.roundRect(left_x + 6, col_y + col_h - 32, col_w - 12, 26, 6, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#1e40af"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_x + 14, col_y + col_h - 22, "PLAYGROUND MENTAL MODEL (FOR 4TH GRADERS)")

    # Hero Persona
    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 11.5)
    c.drawString(left_x + 14, col_y + col_h - 50, f"Meet {k_skill['hero_name']}!")

    # One sentence box
    c.setFillColor(colors.HexColor("#f0fdf4"))
    c.setStrokeColor(colors.HexColor("#86efac"))
    c.roundRect(left_x + 12, col_y + col_h - 100, col_w - 24, 42, 6, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#166534"))
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(left_x + 20, col_y + col_h - 68, "WHAT IS THIS SKILL IN ONE SENTENCE?")
    c.setFont("Helvetica", 7.8)
    c.setFillColor(colors.HexColor("#14532d"))
    o_lines = wrap_text(c, k_skill["one_liner"], "Helvetica", 7.8, col_w - 40)
    oy = col_y + col_h - 80
    for ol in o_lines[:2]:
        c.drawString(left_x + 20, oy, ol)
        oy -= 10

    # Playground Story
    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(left_x + 14, col_y + col_h - 116, "The Playground Story (How It Works):")
    c.setFont("Helvetica", 7.6)
    c.setFillColor(colors.HexColor("#334155"))
    st_lines = wrap_text(c, k_skill["story"], "Helvetica", 7.6, col_w - 28)
    sy = col_y + col_h - 128
    for sl in st_lines[:6]:
        c.drawString(left_x + 14, sy, sl)
        sy -= 10.5

    # Visual Workflow Diagram Box
    dy_box = sy - 8
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.setStrokeColor(colors.HexColor("#e2e8f0"))
    c.roundRect(left_x + 12, dy_box - 54, col_w - 24, 56, 6, stroke=1, fill=1)

    step_w = 92
    step_h = 36
    c.setFillColor(colors.HexColor("#fef3c7"))
    c.setStrokeColor(colors.HexColor("#f59e0b"))
    c.roundRect(left_x + 18, dy_box - 46, step_w, step_h, 4, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#92400e"))
    c.setFont("Helvetica-Bold", 7.2)
    c.drawCentredString(left_x + 18 + step_w/2, dy_box - 24, "Step 1: Input")
    c.setFont("Helvetica", 6.6)
    c.drawCentredString(left_x + 18 + step_w/2, dy_box - 36, "Task proposed")

    c.setStrokeColor(colors.HexColor("#64748b"))
    c.line(left_x + 18 + step_w + 3, dy_box - 28, left_x + 18 + step_w + 22, dy_box - 28)

    c.setFillColor(colors.HexColor("#dbeafe"))
    c.setStrokeColor(colors.HexColor("#3b82f6"))
    c.roundRect(left_x + 18 + step_w + 26, dy_box - 46, step_w + 8, step_h, 4, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#1e40af"))
    c.setFont("Helvetica-Bold", 7.2)
    c.drawCentredString(left_x + 18 + step_w + 26 + (step_w+8)/2, dy_box - 24, "Step 2: Processing")
    c.setFont("Helvetica", 6.6)
    c.drawCentredString(left_x + 18 + step_w + 26 + (step_w+8)/2, dy_box - 36, "Isolated & gated")

    c.setStrokeColor(colors.HexColor("#64748b"))
    c.line(left_x + 18 + step_w*2 + 38, dy_box - 28, left_x + 18 + step_w*2 + 57, dy_box - 28)

    c.setFillColor(colors.HexColor("#dcfce7"))
    c.setStrokeColor(colors.HexColor("#22c55e"))
    c.roundRect(left_x + 18 + step_w*2 + 61, dy_box - 46, step_w, step_h, 4, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#166534"))
    c.setFont("Helvetica-Bold", 7.2)
    c.drawCentredString(left_x + 18 + step_w*2 + 61 + step_w/2, dy_box - 24, "Step 3: Safe State")
    c.setFont("Helvetica", 6.6)
    c.drawCentredString(left_x + 18 + step_w*2 + 61 + step_w/2, dy_box - 36, "Committed safely")

    # Wire connection box
    wy = dy_box - 64
    c.setFillColor(colors.HexColor("#faf5ff"))
    c.setStrokeColor(colors.HexColor("#d8b4fe"))
    c.roundRect(left_x + 12, wy - 48, col_w - 24, 48, 6, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#6b21a8"))
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(left_x + 20, wy - 14, f"MAP CONNECTION TO PAGE 22: Plugs into {k_skill['wire_target']}")
    c.setFont("Helvetica", 7.2)
    c.setFillColor(colors.HexColor("#581c87"))
    w_lines = wrap_text(c, k_skill["wire_expl"], "Helvetica", 7.2, col_w - 40)
    w_y = wy - 26
    for wl in w_lines[:2]:
        c.drawString(left_x + 20, w_y, wl)
        w_y -= 10

    # Superpower & Golden rule box
    gy = wy - 56
    c.setFillColor(colors.HexColor("#ecfdf5"))
    c.setStrokeColor(colors.HexColor("#a7f3d0"))
    c.roundRect(left_x + 12, gy - 50, col_w - 24, 50, 6, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#065f46"))
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(left_x + 20, gy - 14, f"Superpower: {k_skill['superpower'][:65]}")
    c.setFont("Helvetica-Bold", 7.8)
    c.drawString(left_x + 20, gy - 27, "The 4th Grader Golden Rule:")
    c.setFont("Helvetica-Oblique", 7.8)
    c.drawString(left_x + 20, gy - 39, f"\"{k_skill['kid_rule'][:65]}\"")

    # 4. RIGHT COLUMN: PRODUCTION SKILL.MD SPECIFICATION (LIGHT MODE WHITE CARD)
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#cbd5e1"))
    c.roundRect(right_x, col_y, col_w, col_h, 8, stroke=1, fill=1)

    # Right Header (Light Cyan/Sky)
    c.setFillColor(colors.HexColor("#f0f9ff"))
    c.roundRect(right_x + 6, col_y + col_h - 32, col_w - 12, 26, 6, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#0369a1"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(right_x + 14, col_y + col_h - 22, "PRODUCTION SKILL.MD SPECIFICATION (ENGINEERING CONTRACT)")

    # YAML Frontmatter Box (GitHub Light / VS Code Light theme)
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.setStrokeColor(colors.HexColor("#e2e8f0"))
    c.roundRect(right_x + 12, col_y + col_h - 130, col_w - 24, 92, 6, stroke=1, fill=1)

    c.setFont("Courier-Bold", 7)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawString(right_x + 20, col_y + col_h - 46, "---")

    yy = col_y + col_h - 56
    for key, val in p_detail["yaml"][:6]:
        c.setFont("Courier-Bold", 6.8)
        c.setFillColor(colors.HexColor("#be123c")) # Crimson key
        c.drawString(right_x + 20, yy, key)
        c.setFillColor(colors.HexColor("#0369a1")) # Sky blue value
        c.setFont("Courier", 6.8)
        kw = c.stringWidth(key, "Courier-Bold", 6.8)
        # Wrap or display cleanly
        c.drawString(right_x + 20 + kw + 4, yy, val[:50])
        yy -= 9.5
    c.setFont("Courier-Bold", 7)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawString(right_x + 20, yy, "---")

    # Specification Sections in Light Mode
    my = col_y + col_h - 142

    # 1. Purpose & Axiom
    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(right_x + 14, my, "1. Purpose & Architectural Boundary")
    my -= 10
    c.setFont("Helvetica", 7.2)
    c.setFillColor(colors.HexColor("#334155"))
    ax_lines = wrap_text(c, p_detail["axiom"], "Helvetica", 7.2, col_w - 28)
    for al in ax_lines[:2]:
        c.drawString(right_x + 14, my, al)
        my -= 9.5
    my -= 4

    # 2. Invariants
    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(right_x + 14, my, "2. Core System Invariants (Non-Negotiable)")
    my -= 10
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#1e293b"))
    for inv in p_detail["invariants"][:3]:
        c.drawString(right_x + 14, my, inv[:75])
        my -= 9.5
    my -= 4

    # 3. Execution Pipeline
    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(right_x + 14, my, "3. Execution Protocol & Syscalls")
    my -= 10
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#334155"))
    for stp in p_detail["pipeline"][:4]:
        c.drawString(right_x + 14, my, stp[:75])
        my -= 9.5
    my -= 4

    # 4. Failure Modes (Soft Rose Alert Container)
    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(right_x + 14, my, "4. Failure Modes & Self-Healing")
    my -= 10
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#b91c1c")) # Crimson for errors
    for fl in p_detail["failures"][:2]:
        c.drawString(right_x + 14, my, fl[:75])
        my -= 9.5

    c.showPage()

def render_blueprint_page(c, width, height):
    # Pure clean light background
    c.setFillColor(colors.HexColor("#f8fafc"))
    c.rect(0, 0, width, height, stroke=0, fill=1)

    # Top header bar (Light Mode purple theme)
    c.setFillColor(colors.HexColor("#7c3aed"))
    c.rect(0, height - 52, width, 52, stroke=0, fill=1)

    # Badge
    c.setFillColor(colors.white)
    c.roundRect(24, height - 42, 60, 30, 6, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#7c3aed"))
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(54, height - 32, "MAP")

    # Title
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(96, height - 32, "The Master Blueprint: All 20 Stories & Skills Connect!")

    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(width - 24, height - 26, "THE COMPLETE 3-TIER STACK")
    c.setFont("Helvetica", 8)
    c.drawRightString(width - 24, height - 40, "Summary Page • Page 22 of 22")

    # Subtitle banner (clean light slate)
    c.setFillColor(colors.HexColor("#f1f5f9"))
    c.rect(0, height - 76, width, 24, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#334155"))
    c.setFont("Helvetica-Bold", 8)
    sub = "Look at the colorful wires! Purple wires connect Playground Swarms (#15-20) to Robot Brains (#8-14). Blue wires connect Robot Brains down to Ground-Floor Cloud Safes (#1-7)!"
    c.drawCentredString(width / 2, height - 68, sub)

    # Embed High-Resolution Blueprint Diagram PNG
    if os.path.exists(GRAPH_PNG):
        dw = width - 40
        dh = height - 100
        dx = 20
        dy = 22
        c.drawImage(GRAPH_PNG, dx, dy, width=dw, height=dh, preserveAspectRatio=True, anchor='c')

    # Footer
    c.setFillColor(colors.HexColor("#64748b"))
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(20, 10, "THE 3-TIER ENTERPRISE AGENT STACK — 20 SKILLS COMPLETE DEPENDENCY BLUEPRINT (LIGHT MODE)")
    c.drawRightString(width - 20, 10, "Page 22 of 22 (Final Master Map)")
    c.showPage()

def build_pdf():
    c = canvas.Canvas(PDF_OUTPUT, pagesize=landscape(letter))
    width, height = landscape(letter) # 792 x 612

    print("Building Page 1: Cover & Methodology Rosetta Stone (Light Mode)...")
    render_cover_page(c, width, height)

    print("Building Pages 2 to 21: 20 Side-by-Side Skill Pages (Light Mode)...")
    for idx in range(20):
        k_s = KID_SKILLS[idx]
        p_s = PROD_SKILLS[idx]
        p_d = PROD_DETAILS[idx]
        page_num = idx + 2
        print(f"  Rendering Skill #{idx+1:02d}: {k_s['id']} (Page {page_num}/22)...")
        render_side_by_side_page(c, width, height, k_s, p_s, p_d, page_num)

    print("Building Page 22: Master Blueprint Landscape (Light Mode)...")
    render_blueprint_page(c, width, height)

    c.save()
    print(f"Successfully generated {PDF_OUTPUT} in Light Mode!")

if __name__ == "__main__":
    build_pdf()
