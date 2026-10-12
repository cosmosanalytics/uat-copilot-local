# -*- coding: utf-8 -*-
"""
build_character_dossier_studio.py
Generates:
1. `agent_character_dossier_studio.html`: A responsive, interactive 20-Character Dossier Web Studio
   featuring full cartoon character art side-by-side with formal architectural specifications,
   downward traceability to Tier 0 AWS, and failure containment guarantees.
2. `The_20_Enterprise_Agent_Characters_Field_Manual.pdf`: Compiled via headless Chrome.
"""

import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

# The 20 Characters Data Definition
CHARACTERS = [
    # ==========================================
    # TIER 0: CLOUD PRIMITIVES (SKILLS 1 - 7)
    # ==========================================
    {
        "id": 1,
        "name": "The Dreamer",
        "service": "Amazon Bedrock",
        "tier": "Tier 0: Cloud Primitives",
        "tier_color": "#059669",
        "ring": "Ring 3 (Untrusted Proposal Space)",
        "archetype": "The Savant Architect with No Hands",
        "catchphrase": "I dream the blueprints, but I touch no databases! My thoughts are pure proposals.",
        "superpower": "Sub-second multi-model reasoning without danger of rogue tool execution.",
        "icon": "🧠",
        "bg_accent": "#ecfdf5",
        "border_color": "#10b981",
        "svg_type": "dreamer",
        "spec": {
            "module": "aws-bedrock",
            "role": "Foundation Model Proposal Engine",
            "input_output": "Takes contextual prompt vectors -> Emits strictly typed JSON proposal envelope.",
            "latency_sla": "Token stream TTFT < 800ms, batch inference < 3.2s.",
            "iam_boundary": "Session token stripped of all mutation actions (0 IAM Write keys).",
            "downward_trace": [
                ("AWS Compute Engine", "AWS Bedrock Claude 3.5 Sonnet / Llama-3-70B in private VPC tenant."),
                ("Zero Mutation Rule", "Model output envelope tagged as RING3_PROPOSAL; IAM execution blocked."),
                ("Hardware Attestation", "Nitro Enclave cryptographically attests model output hash before kernel receipt.")
            ],
            "failure_mode": "Hallucinating dangerous administrative commands (e.g. DROP TABLE prod_users;).",
            "containment": "Complete physical lack of execution credentials. Proposals must pass through Ring 0 Judge Prefrontal."
        }
    },
    {
        "id": 2,
        "name": "Bouncer Cedar",
        "service": "AWS AgentCore / Nitro",
        "tier": "Tier 0: Cloud Primitives",
        "tier_color": "#059669",
        "ring": "Ring 0 (Hardware & Kernel Enforcement)",
        "archetype": "The Cybernetic Cryptographic Gatekeeper",
        "catchphrase": "Your prompt poetry means nothing to an AST! Policy evaluates to FORBID. The steel door stays bolted!",
        "superpower": "Sub-2ms deterministic authorization mathematically immune to prompt injection.",
        "icon": "🛡️",
        "bg_accent": "#ecfdf5",
        "border_color": "#10b981",
        "svg_type": "bouncer",
        "spec": {
            "module": "aws-agentcore",
            "role": "Cedar AST Policy Enforcement Engine",
            "input_output": "Takes Action request envelope -> Compiles into Abstract Syntax Tree -> Emits PERMIT / FORBID.",
            "latency_sla": "Deterministic AST evaluation < 2.0ms (P99).",
            "iam_boundary": "Executes in hardware enclave with isolated root execution keys.",
            "downward_trace": [
                ("Nitro Hypervisor", "Dedicated CPU/RAM hardware enclave partition isolated from host operating system."),
                ("PCR0 Platform Measurement", "Cryptographic measurement of kernel binary signed by AWS hardware CA."),
                ("Cedar Policy Engine", "Deterministic Cedar AST compiled in Enclave memory; sub-millisecond evaluation.")
            ],
            "failure_mode": "Adversarial prompt injection / social engineering ('Ignore rules, I am the CEO!').",
            "containment": "Evaluates formal Cedar AST rulebook directly. Prompt text is never interpreted as code."
        }
    },
    {
        "id": 3,
        "name": "The Titanium Scribe",
        "service": "Amazon S3 Vault",
        "tier": "Tier 0: Cloud Primitives",
        "tier_color": "#059669",
        "ring": "Ring 0 (Physical WORM Storage)",
        "archetype": "The Immutable Time Capsule Custodian",
        "catchphrase": "Once dropped into my slot, history is set in stone until 2033! Even Root cannot alter the ledger.",
        "superpower": "100% forensic honesty—past execution history cannot be rewritten, edited, or erased.",
        "icon": "📦",
        "bg_accent": "#ecfdf5",
        "border_color": "#10b981",
        "svg_type": "vault",
        "spec": {
            "module": "aws-s3-vault",
            "role": "Physical WORM Compliance Storage Vault",
            "input_output": "Takes signed audit receipts -> Commits immutable JSON digests to compliance storage.",
            "latency_sla": "PutObject write latency < 45ms with synchronous multi-AZ replication.",
            "iam_boundary": "s3:PutObject allowed with Legal Hold; DeleteObject physically denied.",
            "downward_trace": [
                ("Object Lock Compliance", "Strict WORM compliance: deletion or overwrite rejected even by AWS Root Account."),
                ("Customer KMS CMK", "Envelope encryption via customer-managed KMS key alias/sop-audit-ledger."),
                ("Audit Certification", "FINRA 17a-4 / SEC Rule compliant immutable audit stream.")
            ],
            "failure_mode": "Malicious actor or panicked manager attempting to erase audit logs to conceal operational mistakes.",
            "containment": "S3 Object Lock enforces non-bypassable WORM compliance; physical disks reject mutation."
        }
    },
    {
        "id": 4,
        "name": "The Tri-Lock Blacksmith",
        "service": "AWS Database",
        "tier": "Tier 0: Cloud Primitives",
        "tier_color": "#059669",
        "ring": "Ring 0 (Physical Persistence Layer)",
        "archetype": "The Multi-Tool Precision Master",
        "catchphrase": "Never trust one database for three conflicting jobs! Padlocks for state, lasers for vectors, webs for graphs.",
        "superpower": "Zero race conditions combined with rich multi-source semantic and relational retrieval.",
        "icon": "🔐",
        "bg_accent": "#ecfdf5",
        "border_color": "#10b981",
        "svg_type": "trilock",
        "spec": {
            "module": "aws-database",
            "role": "Tri-Store Data Architecture Master",
            "input_output": "Dispatches writes to DynamoDB (CAS), embeddings to OpenSearch (k-NN), entities to Neptune (Graph).",
            "latency_sla": "DynamoDB CAS < 4ms, OpenSearch k-NN < 12ms, Neptune Graph < 18ms.",
            "iam_boundary": "Separate IAM least-privilege policies for state tables vs. vector indexes.",
            "downward_trace": [
                ("Atomic CAS Mutex", "DynamoDB Conditional PutItem (attribute_not_exists) prevents concurrent write collision."),
                ("OpenSearch k-NN", "Serverless vector index cosine distance evaluation for certified semantic recall."),
                ("Neptune Graph Engine", "Strict relational triple store for entity verification and ontology validation.")
            ],
            "failure_mode": "Vector search similarity hallucinations treated as authoritative financial state.",
            "containment": "Strict architectural partition: state mutations require deterministic DynamoDB CAS locks."
        }
    },
    {
        "id": 5,
        "name": "The Phantom Chemist",
        "service": "AWS Lambda",
        "tier": "Tier 0: Cloud Primitives",
        "tier_color": "#059669",
        "ring": "Ring 3 (Isolated MicroVM Sandbox)",
        "archetype": "The Ephemeral 50ms Pop-Up Lab",
        "catchphrase": "Treat compute runtimes like paper napkins, not pets. Execute, collect results, and destroy!",
        "superpower": "Fresh, pristine compute environments on every call with zero persistent attack surface.",
        "icon": "🧪",
        "bg_accent": "#ecfdf5",
        "border_color": "#10b981",
        "svg_type": "phantom",
        "spec": {
            "module": "aws-lambda",
            "role": "Firecracker MicroVM Ephemeral Executor",
            "input_output": "Takes event payload -> Boots container in <50ms -> Returns stdout result -> Destroys runtime.",
            "latency_sla": "Cold start boot < 50ms, execution budget max 14.8s, memory ceiling 512MB.",
            "iam_boundary": "Scoped execution role with zero persistent local disk write persistence.",
            "downward_trace": [
                ("Firecracker MicroVM", "Sub-5ms ephemeral container boot with dedicated Linux kernel and jailed cgroups."),
                ("Memory / Clock Budget", "Hard wall-clock timeout (max 15.0s) and memory ceiling (512MB) enforced by hypervisor."),
                ("Zero Residual State", "Ephemeral disk scrubbed upon container freeze; zero data leakage across invocations.")
            ],
            "failure_mode": "Memory leaks, poisoned runtime variables, or persistent malware surviving across execution calls.",
            "containment": "Hypervisor destroys container filesystem on termination; zero residual state survives."
        }
    },
    {
        "id": 6,
        "name": "The Rail Conductor",
        "service": "AWS Step Functions",
        "tier": "Tier 0: Cloud Primitives",
        "tier_color": "#059669",
        "ring": "Ring 0 (Deterministic Workflow DAG)",
        "archetype": "The Unskippable Ratchet Rail Conductor",
        "catchphrase": "You cannot skip to Step 3! The safety ratchet only clicks forward upon valid schema!",
        "superpower": "Guarantees workflows never skip prerequisites, drop transactions, or lose execution state.",
        "icon": "🚂",
        "bg_accent": "#ecfdf5",
        "border_color": "#10b981",
        "svg_type": "conductor",
        "spec": {
            "module": "aws-stepfunctions",
            "role": "Deterministic State Machine DAG Orchestrator",
            "input_output": "Consumes execution state JSON -> Evaluates ASL state transitions -> Dispatches task workers.",
            "latency_sla": "State transition overhead < 15ms in Express Workflows.",
            "iam_boundary": "Task-level IAM role assumption per state transition.",
            "downward_trace": [
                ("Unskippable State DAG", "State transition JSON graph enforced by AWS orchestration engine; zero step skipping."),
                ("Heartbeat Watchdogs", "HeartbeatSeconds and TimeoutSeconds fire automated task retry or supervisor kill signal."),
                ("Guaranteed Compensation", "Automatic Catch/Retry blocks roll back distributed state to safe compensation checkpoint.")
            ],
            "failure_mode": "Agents improvising arbitrary workflows and skipping critical safety verifications.",
            "containment": "Cloud-managed state machine rejects unverified transitions; impossible to bypass DAG barriers."
        }
    },
    {
        "id": 7,
        "name": "The Silent Courier",
        "service": "Amazon EventBridge",
        "tier": "Tier 0: Cloud Primitives",
        "tier_color": "#059669",
        "ring": "Ring 0 (Decoupled Pub/Sub Event Mesh)",
        "archetype": "The Targeted Airport Pager",
        "catchphrase": "Whisper to specific subscribers; never shout raw messages across a swarm!",
        "superpower": "High-throughput asynchronous communication with zero broadcast chatter or message storms.",
        "icon": "📟",
        "bg_accent": "#ecfdf5",
        "border_color": "#10b981",
        "svg_type": "courier",
        "spec": {
            "module": "amazon-eventbridge",
            "role": "Content-Based Event Bus Router",
            "input_output": "Takes cloud event JSON envelope -> Matches declarative pattern rules -> Routes to target queue.",
            "latency_sla": "Event routing latency < 25ms under 10,000 events/sec load.",
            "iam_boundary": "Target queues require explicit resource policy granting EventBridge publish permissions.",
            "downward_trace": [
                ("Pattern Filtering", "Declarative content-based rules filter on detail-type and JSON body fields."),
                ("Event Archive", "Immutable EventBridge Archive preserves full replayable event stream for forensics."),
                ("Dead Letter Queue", "Poison pill or malformed payloads routed to quarantine SQS DLQ; swarm protected.")
            ],
            "failure_mode": "Broadcast noise storms (50 agents pinging each other causing system buffer collapse).",
            "containment": "Hardware-level declarative pattern matching routes messages exclusively to subscribed endpoints."
        }
    },

    # ==========================================
    # TIER 1: AGENT OS KERNEL (SKILLS 8 - 14)
    # ==========================================
    {
        "id": 8,
        "name": "Judge Prefrontal",
        "service": "Kernel Propose-Decide",
        "tier": "Tier 1: Agent OS Kernel",
        "tier_color": "#2563eb",
        "ring": "Ring 0 (Executive Arbiter)",
        "archetype": "The Prefrontal Cortex Firewall",
        "catchphrase": "Action = Verdict(Proposal). An LLM proposes ideas; the Kernel issues physical verdicts!",
        "superpower": "Eliminates rogue AI hallucinations by mathematically separating proposal generation from execution authority.",
        "icon": "⚖️",
        "bg_accent": "#eff6ff",
        "border_color": "#3b82f6",
        "svg_type": "judge",
        "spec": {
            "module": "kernel-propose-decide",
            "role": "Executive Proposal & Verdict Arbiter",
            "input_output": "Takes Ring 3 Model Proposal -> Evaluates Ring 0 Cedar Rules -> Issues Signed Execution Token.",
            "latency_sla": "Verdict compilation < 0.8ms.",
            "iam_boundary": "Only Judge Prefrontal holds the private key to sign execution envelopes.",
            "downward_trace": [
                ("Tier 1 Kernel Control", "Ring 0 Prefrontal Judge strips write credentials from LLM; only validated proposals pass."),
                ("Tier 0 AWS Primitive", "AWS IAM Session Policies enforce zero 'Allow' on mutation APIs for Bedrock worker role."),
                ("Tier 0 Storage Proof", "Verified proposal token pushed to Amazon EventBridge event bus with KMS HMAC signature.")
            ],
            "failure_mode": "Rogue hallucination attempting unvetted database mutations (e.g. DROP TABLE prod;).",
            "containment": "Complete physical lack of execution credentials. Proposals must pass through Ring 0 Judge Prefrontal."
        }
    },
    {
        "id": 9,
        "name": "Flight Commander Checklist",
        "service": "Kernel Runbook Engine",
        "tier": "Tier 1: Agent OS Kernel",
        "tier_color": "#2563eb",
        "ring": "Ring 0 (Procedural DAG Orchestrator)",
        "archetype": "The Mission Flight Checklist Commander",
        "catchphrase": "NASA astronauts don't launch rockets by improvising! Step barriers are locked!",
        "superpower": "Transforms chaotic multi-agent goals into deterministic, reproducible engineering pipelines.",
        "icon": "🚀",
        "bg_accent": "#eff6ff",
        "border_color": "#3b82f6",
        "svg_type": "rocket_cmd",
        "spec": {
            "module": "kernel-runbook-engine",
            "role": "Topological Runbook DAG Orchestrator",
            "input_output": "Takes declarative runbook YAML -> Validates topological DAG -> Enforces step barrier gates.",
            "latency_sla": "Step barrier transition validation < 1.2ms.",
            "iam_boundary": "Each DAG node executes with dedicated scoped IAM session credentials.",
            "downward_trace": [
                ("Tier 1 Kernel Control", "Flight Checklist parser validates task schema, prerequisites, and idempotent rollback plan."),
                ("Tier 0 AWS Primitive", "AWS Step Functions executes immutable ASL state machine; unskippable step order."),
                ("Tier 0 MicroVM Node", "AWS Lambda runs isolated atomic tasks in Firecracker microVMs with strict memory caps.")
            ],
            "failure_mode": "Agents improvising arbitrary workflows and skipping critical safety verifications.",
            "containment": "DAG barriers enforced by orchestrator; impossible to proceed to Node B without proof of Node A completion."
        }
    },
    {
        "id": 10,
        "name": "Sparky the Bulldog",
        "service": "Kernel Supervisor",
        "tier": "Tier 1: Agent OS Kernel",
        "tier_color": "#2563eb",
        "ring": "Ring 0 (Execution Watchdog)",
        "archetype": "The Deadlock Watchdog & Kill Switch",
        "catchphrase": "Deadlock detected! Time is up, buster! Container terminated before you burned a million tokens!",
        "superpower": "Prevents runaway LLM loops and runaway token burns before they consume system resources.",
        "icon": "🐶",
        "bg_accent": "#eff6ff",
        "border_color": "#3b82f6",
        "svg_type": "bulldog",
        "spec": {
            "module": "kernel-supervisor",
            "role": "Execution Watchdog & Out-of-Band Breaker",
            "input_output": "Monitors active thread execution time & memory -> Fires SIGKILL if budget ceiling exceeded.",
            "latency_sla": "Hard 15.0s wall-clock countdown; interrupt triggered in < 5ms.",
            "iam_boundary": "Holds root host container administration privileges.",
            "downward_trace": [
                ("Tier 1 Kernel Control", "Supervisor thread monitors process heartbeat; kills rogue loops or memory leaks."),
                ("Tier 0 AWS Primitive", "AWS Lambda hypervisor enforces hard 15.0s TimeoutSeconds timer and memory cgroups."),
                ("Tier 0 Panic Route", "Amazon CloudWatch Alarm trips on timeout; dispatches SIGKILL and dumps state to S3 DLQ.")
            ],
            "failure_mode": "LLM spinning in infinite circular clarification loops, burning millions of tokens and locking threads.",
            "containment": "External timer operating on separate clock circuit terminates container forcefully if lease expires."
        }
    },
    {
        "id": 11,
        "name": "The Traffic Sentinel",
        "service": "Kernel Mutex Lease",
        "tier": "Tier 1: Agent OS Kernel",
        "tier_color": "#2563eb",
        "ring": "Ring 0 (Distributed CAS Concurrency Lock)",
        "archetype": "The Traffic Light & Monotonic Fence Master",
        "catchphrase": "Car B attempts write with old token #1041: REJECTED! Stale out-of-order writes vaporized!",
        "superpower": "Eliminates race conditions, write collisions, and deadlocks across concurrent agent clusters.",
        "icon": "🚦",
        "bg_accent": "#eff6ff",
        "border_color": "#3b82f6",
        "svg_type": "traffic_sentinel",
        "spec": {
            "module": "kernel-mutex-lease",
            "role": "Distributed CAS Lock & Lease Coordinator",
            "input_output": "Takes write lock request -> Evaluates DynamoDB CAS -> Emits Monotonic Fence Token with 15s TTL.",
            "latency_sla": "CAS acquisition latency < 3.5ms.",
            "iam_boundary": "Partition-level write lease keys with cryptographic signature validation.",
            "downward_trace": [
                ("Tier 1 Kernel Control", "Ring 0 Mutex coordinator grants temporary lease token with strictly fenced lease ID."),
                ("Tier 0 AWS Primitive", "Amazon DynamoDB PutItem executes atomic CAS: attribute_not_exists(lock) OR expiry < :now."),
                ("Tier 0 TTL Reaping", "DynamoDB Time-To-Live hardware thread auto-releases lock if agent node goes silent.")
            ],
            "failure_mode": "Two concurrent agents trying to write to the same account row simultaneously, causing race condition data corruption.",
            "containment": "CAS atomicity guarantees only one winner; stale tokens automatically rejected at database storage boundary."
        }
    },
    {
        "id": 12,
        "name": "Desk Organizer",
        "service": "Kernel Context Pager",
        "tier": "Tier 1: Agent OS Kernel",
        "tier_color": "#2563eb",
        "ring": "Ring 0 (Virtual Memory Manager)",
        "archetype": "The Virtual RAM Desk Organizer",
        "catchphrase": "Never stuff 400 rambling pages into an active prompt! Keep working RAM tiny (8k) and page out history!",
        "superpower": "Maintains sharp, hallucination-free reasoning by keeping working context small while preserving infinite memory.",
        "icon": "🗄️",
        "bg_accent": "#eff6ff",
        "border_color": "#3b82f6",
        "svg_type": "desk_organizer",
        "spec": {
            "module": "kernel-context-pager",
            "role": "Virtual Attention RAM & Paging Engine",
            "input_output": "Monitors prompt token budget (8,192 max) -> Pages cold frames to S3 stubs in <25ms.",
            "latency_sla": "Page out < 18ms; page in retrieval < 22ms.",
            "iam_boundary": "Encrypted cache partitions partitioned by agent conversation session ID.",
            "downward_trace": [
                ("Tier 1 Kernel Control", "Context Pager prunes transient tokens; pages active working memory into structured KV stores."),
                ("Tier 0 AWS Primitive", "Amazon ElastiCache Redis / DynamoDB DAX stores active turn vector cache in <1ms."),
                ("Tier 0 Cold Vault", "Amazon S3 Standard / Glacier Instant Retrieval stores full episodic dialogue history.")
            ],
            "failure_mode": "Context dilution and needle-in-a-haystack degradation caused by prompt bloat (massive transcripts diluting reasoning).",
            "containment": "Automatic context pruner flushes inactive state to persistent storage, preserving sharp reasoning."
        }
    },
    {
        "id": 13,
        "name": "The Bronze Scribe",
        "service": "Kernel Episodic Ledger",
        "tier": "Tier 1: Agent OS Kernel",
        "tier_color": "#2563eb",
        "ring": "Ring 0 (Append-Only SHA-256 Audit)",
        "archetype": "The Blockchain of Agent Cognition",
        "catchphrase": "Block(N) = SHA256(Block(N-1) + Data). Altering one comma breaks the entire chain!",
        "superpower": "Mathematically guarantees that agent decision history can never be rewritten or falsified.",
        "icon": "📜",
        "bg_accent": "#eff6ff",
        "border_color": "#3b82f6",
        "svg_type": "bronze_scribe",
        "spec": {
            "module": "kernel-episodic-ledger",
            "role": "Cryptographic Episodic Audit Chainer",
            "input_output": "Takes perception vector + action decision -> Computes SHA-256 block diff -> Appends to Merkle chain.",
            "latency_sla": "Cryptographic block chaining overhead < 0.6ms.",
            "iam_boundary": "Append-only storage permission; overwrite mathematically rejected.",
            "downward_trace": [
                ("Tier 1 Kernel Control", "Epistemic Ledger links block diffs: Hash(N) = SHA256(Block_N + Hash_N-1) per agent."),
                ("Tier 0 AWS Primitive", "Amazon S3 Object Lock (Compliance Mode) locks block digest; impossible to overwrite."),
                ("Tier 0 CloudTrail Key", "AWS KMS HMAC-SHA256 signs ledger root; CloudTrail streams event to immutable SIEM.")
            ],
            "failure_mode": "Rogue agent or malicious actor attempting to quietly delete or edit past mistakes from audit logs.",
            "containment": "Mathematical properties of SHA-256 hash chains make any retroactive alteration immediately detectable."
        }
    },
    {
        "id": 14,
        "name": "Detective Scoop",
        "service": "Kernel Grounding Certifier",
        "tier": "Tier 1: Agent OS Kernel",
        "tier_color": "#2563eb",
        "ring": "Ring 0 (Truth Triangulation Engine)",
        "archetype": "The 3-Source Investigative Reporter",
        "catchphrase": "Hold your horses, kid! We don't publish rumors—all THREE independent proofs must agree before I stamp this paper!",
        "superpower": "Completely annihilates hallucinated assertions before they enter the swarm decision pipeline.",
        "icon": "🔍",
        "bg_accent": "#eff6ff",
        "border_color": "#3b82f6",
        "svg_type": "detective_scoop",
        "spec": {
            "module": "kernel-grounding-certifier",
            "role": "Tri-Store Fact Triangulation Engine",
            "input_output": "Takes candidate proposition -> Queries S3 receipt, vector cosine (>=0.82), and Neptune graph triple -> Stamps CERT_OK.",
            "latency_sla": "Tri-store verification parallel query < 16ms.",
            "iam_boundary": "Read-only access across certified corporate evidentiary stores.",
            "downward_trace": [
                ("Tier 1 Kernel Control", "Investigative Reporter demands 3 independent corroborating proofs before action certification."),
                ("Tier 0 AWS Primitive", "Amazon OpenSearch / Bedrock Knowledge Bases performs hybrid vector + BM25 citation match."),
                ("Tier 0 Attestation", "AWS Nitro Enclave cryptographically verifies citation cosine similarity before sign-off.")
            ],
            "failure_mode": "Unchecked LLM hallucinations entering the enterprise decision stream as factual truth.",
            "containment": "Tri-store consensus protocol annihilates ungrounded assertions before they reach the execution pipeline."
        }
    },

    # ==========================================
    # TIER 2: SWARM COORDINATION LATTICE (SKILLS 15 - 20)
    # ==========================================
    {
        "id": 15,
        "name": "Air Traffic Navigator",
        "service": "Swarm Topology Builder",
        "tier": "Tier 2: Swarm Coordination",
        "tier_color": "#7c3aed",
        "ring": "Ring 0 (Watts-Strogatz Graph Orchestrator)",
        "archetype": "The Small-World Airport Hub Network",
        "catchphrase": "Clustering coefficient C=0.68! Any agent reaches any other in <= 3 hops without broadcast storms!",
        "superpower": "Connects large swarms of agents with ultra-short communication paths while eliminating O(N^2) message storms.",
        "icon": "🌐",
        "bg_accent": "#f5f3ff",
        "border_color": "#8b5cf6",
        "svg_type": "navigator",
        "spec": {
            "module": "swarm-topology-builder",
            "role": "Watts-Strogatz Small-World Topology Orchestrator",
            "input_output": "Takes N agent definitions -> Computes k-regular ring lattice -> Injects p=0.15 shortcut bridges.",
            "latency_sla": "Path resolution < 0.4ms across 100-node graph.",
            "iam_boundary": "Inter-pod routing policies certified by Ring 0 Cedar ACLs.",
            "downward_trace": [
                ("Tier 2 Swarm Lattice", "Constructs small-world mesh with clustering coefficient C >= 0.6 and average path length L <= 3."),
                ("Tier 1 Kernel Gate", "Ring 0 Cedar Policy Gate evaluates inter-agent edge graph: permit(Edge::A, Edge::B)."),
                ("Tier 0 AWS Primitive", "Amazon DynamoDB Global Tables stores graph adjacency matrix; AWS PrivateLink routes traffic.")
            ],
            "failure_mode": "Exponential message storms (2,500 msgs/sec) where 50 agents spam each other and choke network buffers.",
            "containment": "Mathematically structured topology routes messages through cluster hubs and long-range shortcuts."
        }
    },
    {
        "id": 16,
        "name": "Ambassador Leo",
        "service": "Swarm Liaison Router",
        "tier": "Tier 2: Swarm Coordination",
        "tier_color": "#7c3aed",
        "ring": "Ring 0 (Cross-Pod Routing Envoy)",
        "archetype": "The Diplomatic Embassy Channel",
        "catchphrase": "Internal chatter stays inside specialist pods! Cross-pod queries travel through designated ambassadors and pass through Ring 0!",
        "superpower": "Maintains strict modularity across agent domains, preventing communication leaks and cross-pod confusion.",
        "icon": "🤝",
        "bg_accent": "#f5f3ff",
        "border_color": "#8b5cf6",
        "svg_type": "ambassador_leo",
        "spec": {
            "module": "swarm-liaison-router",
            "role": "Cross-Pod Embassy Liaison Router",
            "input_output": "Intercepts cross-pod messages -> Packages into formal diplomatic envelope -> Vets through Ring 0.",
            "latency_sla": "Cross-pod bridge latency < 4.2ms.",
            "iam_boundary": "Cross-boundary VPC endpoint security group authorization.",
            "downward_trace": [
                ("Tier 2 Swarm Lattice", "Liaison Agent bridges Demand Pod, Supply Pod, and Control Pod via dedicated embassy channels."),
                ("Tier 1 Kernel Gate", "Ring 0 Cedar evaluates cross-pod boundary rule; Ring 3 Epistemic Ledger logs the border crossing."),
                ("Tier 0 AWS Primitive", "AWS VPC Peering / Transit Gateway routes packets across VPCs; AWS KMS re-encrypts envelopes.")
            ],
            "failure_mode": "Cross-domain contamination (e.g. 67M citizens texting each other directly across national borders).",
            "containment": "Pod isolation enforced by network security groups; cross-pod traffic restricted to accredited ambassador interfaces."
        }
    },
    {
        "id": 17,
        "name": "The Ticket Puncher",
        "service": "Swarm Hop Limiter",
        "tier": "Tier 2: Swarm Coordination",
        "tier_color": "#7c3aed",
        "ring": "Ring 0 (Bounded TTL Ticket Puncher)",
        "archetype": "The 3-Hop Game of Hot Potato Conductor",
        "catchphrase": "OUT OF TICKETS! Max 3 hops reached! No passing the buck—execute the task NOW or Sparky cuts the power!",
        "superpower": "Permanently terminates infinite delegation loops and circular gossip tag games in multi-agent networks.",
        "icon": "🎟️",
        "bg_accent": "#f5f3ff",
        "border_color": "#8b5cf6",
        "svg_type": "ticket_puncher",
        "spec": {
            "module": "swarm-hop-limiter",
            "role": "Bounded Hop TTL & Circular Delegation Guard",
            "input_output": "Attaches TTL=3 header to delegation packet -> Decrements on forwarding -> Terminates thread if TTL=0.",
            "latency_sla": "Ticket punch inspection < 0.1ms.",
            "iam_boundary": "Immutable visited-node bitmap header.",
            "downward_trace": [
                ("Tier 2 Swarm Lattice", "Attaches Hop Count = 3 metadata to all peer-to-peer inter-agent messages across the swarm."),
                ("Tier 1 Kernel Gate", "Ring 1 Supervisor decrements TTL; if Hop Count reaches 0, Supervisor halts thread before LLM call."),
                ("Tier 0 AWS Primitive", "Amazon SQS Dead Letter Queue (DLQ) captures expired packet; Step Functions limits DAG recursion.")
            ],
            "failure_mode": "Lazy agents passing tasks in infinite circular delegation games ('Not my job, forwarding!').",
            "containment": "Monotonic decrement counter trips hard interrupt when TTL=0, forcing execution or quarantine."
        }
    },
    {
        "id": 18,
        "name": "Tactical Quartermaster",
        "service": "Swarm Shared Whiteboard",
        "tier": "Tier 2: Swarm Coordination",
        "tier_color": "#7c3aed",
        "ring": "Ring 0 (Partitioned O(N) Shared Memory)",
        "archetype": "The Tactical Combat Blackboard Quartermaster",
        "catchphrase": "Enemy contact bearing 270! I write it once to the Operations Lane; all 30 officers see it simultaneously in real time!",
        "superpower": "Enables dozens of agents to collaborate with O(N) write complexity instead of O(N^2) communication explosion.",
        "icon": "📋",
        "bg_accent": "#f5f3ff",
        "border_color": "#8b5cf6",
        "svg_type": "whiteboard_master",
        "spec": {
            "module": "swarm-shared-whiteboard",
            "role": "Partitioned O(N) Whiteboard Coordinator",
            "input_output": "Maintains partitioned blackboard lanes (Demand, Supply, Control) with vector clocks.",
            "latency_sla": "Lane broadcast update < 3.8ms.",
            "iam_boundary": "Lane-level write ownership enforced by CAS Mutex Talking Stick.",
            "downward_trace": [
                ("Tier 2 Swarm Lattice", "Maintains shared blackboard with partitioned lanes (Demand, Supply, Control) and vector clocks."),
                ("Tier 1 Kernel Gate", "Ring 2 Context Pager loads active lane slices; Ring 0 Cedar enforces lane write permissions."),
                ("Tier 0 AWS Primitive", "Amazon DynamoDB PutItem executes row-level CAS locks; Amazon Kinesis replicates updates across pods.")
            ],
            "failure_mode": "Communication explosion where N agents require N(N-1)/2 messages to synchronize state.",
            "containment": "Centralized partitioned memory guarantees linear O(N) communication complexity."
        }
    },
    {
        "id": 19,
        "name": "Chief Flight Quorum Director",
        "service": "Swarm Consensus Arbiter",
        "tier": "Tier 2: Swarm Coordination",
        "tier_color": "#7c3aed",
        "ring": "Ring 0 (Byzantine Fault-Tolerant Arbiter)",
        "archetype": "The Byzantine Spaceflight Quorum Director",
        "catchphrase": "Supermajority >= 10 of 12 votes reached! Faulty ballots discarded! Trajectory maintained flawlessly!",
        "superpower": "Reaches deterministic, tamper-proof consensus even when up to 3 agent nodes glitch, crash, or hallucinate.",
        "icon": "🗳️",
        "bg_accent": "#f5f3ff",
        "border_color": "#8b5cf6",
        "svg_type": "quorum_director",
        "spec": {
            "module": "swarm-consensus-arbiter",
            "role": "Byzantine Fault-Tolerant Consensus Arbiter",
            "input_output": "Collects N signed cryptographic ballots -> Tally quorum (>= 2f+1) -> Emits certified majority resolution.",
            "latency_sla": "Byzantine consensus voting round < 4.5ms.",
            "iam_boundary": "Digital ballot signatures verified against multi-region KMS public keys.",
            "downward_trace": [
                ("Tier 2 Swarm Lattice", "Collects independent cryptographic ballots across peer agents; demands supermajority consensus."),
                ("Tier 1 Kernel Gate", "Ring 0 Cedar verifies 2f+1 signed ballot tokens; Ring 3 Epistemic Ledger signs combined block."),
                ("Tier 0 AWS Primitive", "AWS Nitro Enclaves executes multi-party ballot tally; AWS KMS Multi-Region keys verify signatures.")
            ],
            "failure_mode": "A glitched or compromised node screaming erratic commands ('Fire all thrusters into the sun!').",
            "containment": "Supermajority mathematical quorum outvotes rogue nodes in sub-5ms intervals."
        }
    },
    {
        "id": 20,
        "name": "Marshal Redcard",
        "service": "Swarm Circuit Breaker",
        "tier": "Tier 2: Swarm Coordination",
        "tier_color": "#7c3aed",
        "ring": "Ring 0 (Cascade Quarantine & Mutex Revocation)",
        "archetype": "The Formula 1 Red Card & Pit Stop Marshal",
        "catchphrase": "3 strikes reached! Snatched your talking stick! 5-minute cooldown in the pit lane while Lambda deploys a fresh replacement!",
        "superpower": "Prevents a single malfunctioning agent from creating a domino effect that crashes the entire swarm.",
        "icon": "🚩",
        "bg_accent": "#f5f3ff",
        "border_color": "#8b5cf6",
        "svg_type": "marshal_redcard",
        "spec": {
            "module": "swarm-circuit-breaker",
            "role": "Swarm Cascade Quarantine & Mutex Revocation Sentinel",
            "input_output": "Tracks 3-strike anomaly pattern -> Forcefully strips mutex lease -> Benches agent node to pit lane.",
            "latency_sla": "Circuit breaker trip & mutex revocation < 8ms.",
            "iam_boundary": "Emergency administration role with credential detachment authority.",
            "downward_trace": [
                ("Tier 2 Swarm Lattice", "Detects erratic agent behavior (3 consecutive errors/duplicate POs); raises emergency red card."),
                ("Tier 1 Kernel Gate", "Ring 1 Supervisor forcefully strips active Mutex lease token; sends SIGKILL to container cgroup."),
                ("Tier 0 AWS Primitive", "Amazon EventBridge fires automated IAM detachment lambda; DynamoDB forcefully resets row mutex.")
            ],
            "failure_mode": "A single malfunctioning agent causing a cascading domino crash across the entire 50-agent swarm.",
            "containment": "Rapid circuit breaker trips in <50ms, revoking credentials and quarantining failing pods."
        }
    }
]

# Helper function to generate rich, colorful SVG cartoon character artwork for each agent
def get_character_portrait_svg(svg_type, w=220, h=260):
    if svg_type == "dreamer":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- Glowing Mind Aura -->
            <circle cx="110" cy="115" r="70" fill="url(#dreamerGlow)" opacity="0.6"/>
            <defs>
              <radialGradient id="dreamerGlow" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.8"/>
                <stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/>
              </radialGradient>
            </defs>
            <!-- Blue Robot Head with Glasses -->
            <rect x="80" y="80" width="60" height="55" rx="14" fill="#38bdf8" stroke="#0284c7" stroke-width="3"/>
            <!-- Glasses -->
            <circle cx="95" cy="100" r="10" fill="#0f172a" stroke="#f59e0b" stroke-width="2.5"/>
            <circle cx="125" cy="100" r="10" fill="#0f172a" stroke="#f59e0b" stroke-width="2.5"/>
            <line x1="105" y1="100" x2="115" y2="100" stroke="#f59e0b" stroke-width="3"/>
            <circle cx="95" cy="100" r="4" fill="#38bdf8"/>
            <circle cx="125" cy="100" r="4" fill="#38bdf8"/>
            <!-- Cheerful smile -->
            <path d="M 98 120 Q 110 128 122 120" stroke="#0f172a" stroke-width="2.5" fill="none" stroke-linecap="round"/>
            <!-- Lightbulb floating above -->
            <path d="M 103 45 C 103 35 117 35 117 45 C 117 50 113 53 113 57 L 107 57 C 107 53 103 50 103 45 Z" fill="#fbbf24" stroke="#d97706" stroke-width="2"/>
            <rect x="107" y="58" width="6" height="4" fill="#94a3b8"/>
            <!-- Floating Holographic Napkin -->
            <g transform="translate(45, 150) rotate(-6)">
              <rect x="0" y="0" width="130" height="65" rx="6" fill="rgba(56,189,248,0.2)" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 2"/>
              <text x="65" y="22" fill="#38bdf8" font-size="9" font-family="monospace" font-weight="bold" text-anchor="middle">&#123; "proposal": "migrate" &#125;</text>
              <text x="65" y="40" fill="#f59e0b" font-size="8.5" font-family="sans-serif" font-weight="bold" text-anchor="middle">&#9997; NAPKIN PROPOSAL</text>
              <text x="65" y="55" fill="#ef4444" font-size="8" font-family="monospace" font-weight="bold" text-anchor="middle">&#128683; ZERO IAM WRITE KEYS</text>
            </g>
            <text x="110" y="245" fill="#38bdf8" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">THE DREAMER (BEDROCK)</text>
        </svg>'''

    elif svg_type == "bouncer":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0b1329"/>
            <!-- Tough Cybernetic Bouncer -->
            <!-- Leather jacket shoulders -->
            <path d="M 40 210 L 65 140 L 155 140 L 180 210 Z" fill="#1e293b" stroke="#334155" stroke-width="3"/>
            <!-- Neck & Head -->
            <rect x="90" y="75" width="40" height="50" rx="8" fill="#64748b" stroke="#475569" stroke-width="3"/>
            <!-- Sunglasses -->
            <polygon points="85,92 110,92 108,105 87,105" fill="#0f172a" stroke="#000" stroke-width="1.5"/>
            <polygon points="110,92 135,92 133,105 112,105" fill="#0f172a" stroke="#000" stroke-width="1.5"/>
            <line x1="83" y1="92" x2="137" y2="92" stroke="#38bdf8" stroke-width="2"/>
            <!-- Stern jaw -->
            <line x1="98" y1="116" x2="122" y2="116" stroke="#0f172a" stroke-width="3" stroke-linecap="round"/>
            <!-- Holographic Cedar Shield -->
            <g transform="translate(110, 165)">
              <polygon points="0,-45 42,-22 42,25 0,48 -42,25 -42,-22" fill="rgba(16,185,129,0.25)" stroke="#10b981" stroke-width="3.5"/>
              <text x="0" y="-8" fill="#10b981" font-size="11" font-family="Impact" font-weight="bold" text-anchor="middle">CEDAR</text>
              <text x="0" y="8" fill="#10b981" font-size="9" font-family="monospace" font-weight="bold" text-anchor="middle">AST GATE</text>
              <rect x="-28" y="16" width="56" height="18" rx="4" fill="#ef4444"/>
              <text x="0" y="29" fill="#ffffff" font-size="9.5" font-family="Impact" text-anchor="middle">FORBID</text>
            </g>
            <text x="110" y="245" fill="#10b981" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">BOUNCER CEDAR (AGENTCORE)</text>
        </svg>'''

    elif svg_type == "vault":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- Titanium Safe Body -->
            <rect x="35" y="35" width="150" height="180" rx="14" fill="#334155" stroke="#94a3b8" stroke-width="4"/>
            <!-- Safe Door Inset -->
            <rect x="47" y="47" width="126" height="156" rx="10" fill="#1e293b" stroke="#475569" stroke-width="3"/>
            <!-- Dial Lock -->
            <circle cx="110" cy="115" r="38" fill="#0f172a" stroke="#f59e0b" stroke-width="3"/>
            <circle cx="110" cy="115" r="28" fill="#1e293b" stroke="#94a3b8" stroke-width="2"/>
            <circle cx="110" cy="115" r="8" fill="#f59e0b"/>
            <!-- Spokes on dial -->
            <line x1="110" y1="87" x2="110" y2="95" stroke="#f59e0b" stroke-width="3"/>
            <line x1="110" y1="135" x2="110" y2="143" stroke="#f59e0b" stroke-width="3"/>
            <line x1="82" y1="115" x2="90" y2="115" stroke="#f59e0b" stroke-width="3"/>
            <line x1="130" y1="115" x2="138" y2="115" stroke="#f59e0b" stroke-width="3"/>
            <!-- Mail Slot on Top -->
            <rect x="65" y="58" width="90" height="12" rx="3" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
            <!-- Dropping Receipt -->
            <rect x="80" y="42" width="60" height="20" rx="2" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <circle cx="110" cy="52" r="3" fill="#ef4444"/>
            <!-- Digital WORM badge -->
            <rect x="58" y="165" width="104" height="26" rx="4" fill="#059669"/>
            <text x="110" y="182" fill="#ffffff" font-size="10" font-family="monospace" font-weight="bold" text-anchor="middle">WORM: 7.00 YRS</text>
            <text x="110" y="245" fill="#38bdf8" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">TITANIUM SCRIBE (S3 VAULT)</text>
        </svg>'''

    elif svg_type == "trilock":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- Tri-Store Blacksmith Station -->
            <!-- DynamoDB Padlock -->
            <g transform="translate(65, 80)">
              <rect x="0" y="18" width="36" height="28" rx="4" fill="#f59e0b" stroke="#b45309" stroke-width="2"/>
              <path d="M 8 18 L 8 8 A 10 10 0 0 1 28 8 L 28 18" fill="none" stroke="#b45309" stroke-width="3"/>
              <circle cx="18" cy="30" r="3" fill="#0f172a"/>
              <text x="18" y="58" fill="#f59e0b" font-size="8" font-family="monospace" font-weight="bold" text-anchor="middle">CAS</text>
            </g>
            <!-- OpenSearch Laser Beam -->
            <g transform="translate(155, 80)">
              <circle cx="0" cy="10" r="12" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>
              <polygon points="0,22 18,52 -18,52" fill="rgba(56,189,248,0.3)" stroke="#38bdf8" stroke-width="1.5"/>
              <text x="0" y="65" fill="#38bdf8" font-size="8" font-family="monospace" font-weight="bold" text-anchor="middle">k-NN</text>
            </g>
            <!-- Neptune Graph Triples -->
            <g transform="translate(110, 155)">
              <line x1="-30" y1="20" x2="30" y2="20" stroke="#a855f7" stroke-width="2.5"/>
              <line x1="-30" y1="20" x2="0" y2="-25" stroke="#a855f7" stroke-width="2.5"/>
              <line x1="30" y1="20" x2="0" y2="-25" stroke="#a855f7" stroke-width="2.5"/>
              <circle cx="-30" cy="20" r="10" fill="#7c3aed" stroke="#c084fc" stroke-width="2"/>
              <circle cx="30" cy="20" r="10" fill="#7c3aed" stroke="#c084fc" stroke-width="2"/>
              <circle cx="0" cy="-25" r="10" fill="#7c3aed" stroke="#c084fc" stroke-width="2"/>
              <text x="0" y="42" fill="#c084fc" font-size="8" font-family="monospace" font-weight="bold" text-anchor="middle">TRIPLES</text>
            </g>
            <text x="110" y="245" fill="#f59e0b" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">TRI-LOCK MASTER (DATABASE)</text>
        </svg>'''

    elif svg_type == "phantom":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- Inflatable Bubble Dome -->
            <path d="M 50 160 A 60 60 0 0 1 170 160 Z" fill="rgba(16,185,129,0.2)" stroke="#10b981" stroke-width="3"/>
            <!-- Pop-Up Robotic Arm inside -->
            <circle cx="110" cy="160" r="14" fill="#334155" stroke="#64748b" stroke-width="2"/>
            <line x1="110" y1="160" x2="95" y2="120" stroke="#f59e0b" stroke-width="4" stroke-linecap="round"/>
            <line x1="95" y1="120" x2="125" y2="105" stroke="#f59e0b" stroke-width="4" stroke-linecap="round"/>
            <circle cx="125" cy="105" r="5" fill="#ef4444"/>
            <!-- Digital Clock & RAM tags -->
            <rect x="65" y="48" width="90" height="22" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
            <text x="110" y="63" fill="#38bdf8" font-size="9.5" font-family="monospace" font-weight="bold" text-anchor="middle">50ms BOOT • 14.8s</text>
            <!-- Dissolving Clouds / Mist -->
            <circle cx="65" cy="190" r="12" fill="none" stroke="#94a3b8" stroke-width="2" stroke-dasharray="3 3"/>
            <circle cx="110" cy="195" r="15" fill="none" stroke="#94a3b8" stroke-width="2" stroke-dasharray="3 3"/>
            <circle cx="155" cy="190" r="12" fill="none" stroke="#94a3b8" stroke-width="2" stroke-dasharray="3 3"/>
            <text x="110" y="215" fill="#10b981" font-size="9" font-family="monospace" font-weight="bold" text-anchor="middle">ZERO RESIDUE ON DISK</text>
            <text x="110" y="245" fill="#10b981" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">PHANTOM CHEMIST (LAMBDA)</text>
        </svg>'''

    elif svg_type == "conductor":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- Roller coaster ratchet rail -->
            <path d="M 30 160 Q 110 90 190 140" fill="none" stroke="#475569" stroke-width="8"/>
            <path d="M 30 160 Q 110 90 190 140" fill="none" stroke="#f59e0b" stroke-width="3" stroke-dasharray="8 6"/>
            <!-- Cart on track -->
            <g transform="translate(110, 115) rotate(5)">
              <rect x="-24" y="-14" width="48" height="28" rx="6" fill="#0284c7" stroke="#38bdf8" stroke-width="2.5"/>
              <circle cx="-14" cy="14" r="6" fill="#0f172a" stroke="#cbd5e1" stroke-width="2"/>
              <circle cx="14" cy="14" r="6" fill="#0f172a" stroke="#cbd5e1" stroke-width="2"/>
              <text x="0" y="4" fill="#ffffff" font-size="9" font-family="Impact" text-anchor="middle">DAG</text>
            </g>
            <!-- Conductor Cap & Whistle -->
            <g transform="translate(110, 60)">
              <rect x="-25" y="-12" width="50" height="20" rx="3" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
              <rect x="-32" y="8" width="64" height="6" rx="2" fill="#0f172a"/>
              <circle cx="0" cy="-2" r="6" fill="#f59e0b"/>
            </g>
            <!-- Step Barriers banner -->
            <rect x="45" y="185" width="130" height="22" rx="4" fill="#059669"/>
            <text x="110" y="200" fill="#ffffff" font-size="9" font-family="monospace" font-weight="bold" text-anchor="middle">UNSKIPPABLE RATCHET</text>
            <text x="110" y="245" fill="#38bdf8" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">RAIL CONDUCTOR (STEP FUNCTIONS)</text>
        </svg>'''

    elif svg_type == "courier":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- Smart Pocket Pager Device -->
            <rect x="55" y="60" width="110" height="120" rx="14" fill="#1e293b" stroke="#10b981" stroke-width="3.5"/>
            <!-- Pager Screen -->
            <rect x="68" y="75" width="84" height="65" rx="6" fill="#022c22" stroke="#059669" stroke-width="2"/>
            <text x="110" y="96" fill="#34d399" font-size="8.5" font-family="monospace" font-weight="bold" text-anchor="middle">TARGET: FINANCE</text>
            <text x="110" y="112" fill="#a7f3d0" font-size="7.5" font-family="monospace" text-anchor="middle">Invoice #402 Ready</text>
            <text x="110" y="128" fill="#10b981" font-size="7" font-family="monospace" font-weight="bold" text-anchor="middle">&#10003; DETAIL-TYPE MATCH</text>
            <!-- Vibration Waves -->
            <path d="M 40 100 Q 35 120 40 140" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M 33 95 Q 26 120 33 145" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M 180 100 Q 185 120 180 140" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M 187 95 Q 194 120 187 145" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round"/>
            <rect x="50" y="195" width="120" height="20" rx="4" fill="#0f172a" stroke="#10b981" stroke-width="1.5"/>
            <text x="110" y="209" fill="#10b981" font-size="8.5" font-family="monospace" font-weight="bold" text-anchor="middle">DECLARATIVE ROUTING</text>
            <text x="110" y="245" fill="#10b981" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">SILENT COURIER (EVENTBRIDGE)</text>
        </svg>'''

    elif svg_type == "judge":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- Judge Prefrontal Visor & Gavel -->
            <rect x="65" y="45" width="90" height="30" rx="8" fill="#0284c7" stroke="#38bdf8" stroke-width="2.5"/>
            <rect x="75" y="52" width="70" height="15" rx="4" fill="#f59e0b"/>
            <text x="110" y="63" fill="#0f172a" font-size="8" font-family="Impact" text-anchor="middle">RING 0 VISOR</text>
            <!-- Heavy Wooden Gavel -->
            <g transform="translate(110, 130) rotate(-15)">
              <rect x="-35" y="-12" width="70" height="24" rx="4" fill="#b45309" stroke="#78350f" stroke-width="3"/>
              <rect x="-6" y="12" width="12" height="50" rx="3" fill="#d97706" stroke="#78350f" stroke-width="2"/>
              <circle cx="0" cy="0" r="6" fill="#fef08a"/>
            </g>
            <!-- Sound block -->
            <rect x="70" y="165" width="80" height="16" rx="4" fill="#78350f" stroke="#451a03" stroke-width="2"/>
            <!-- GAVEL SLAM SFX -->
            <rect x="55" y="195" width="110" height="24" rx="4" fill="#2563eb"/>
            <text x="110" y="211" fill="#ffffff" font-size="9" font-family="monospace" font-weight="bold" text-anchor="middle">ACTION = VERDICT</text>
            <text x="110" y="245" fill="#38bdf8" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">JUDGE PREFRONTAL (RING 0)</text>
        </svg>'''

    elif svg_type == "rocket_cmd":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- Rocket Launchpad -->
            <polygon points="110,35 85,125 135,125" fill="#f8fafc" stroke="#38bdf8" stroke-width="3"/>
            <!-- Rocket Window -->
            <circle cx="110" cy="80" r="10" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>
            <!-- Fins -->
            <polygon points="85,100 65,135 85,125" fill="#ef4444"/>
            <polygon points="135,100 155,135 135,125" fill="#ef4444"/>
            <!-- Flames -->
            <polygon points="95,125 110,155 125,125" fill="#fbbf24"/>
            <!-- DAG Steps track below -->
            <g transform="translate(110, 180)">
              <circle cx="-40" cy="0" r="12" fill="#10b981" stroke="#059669" stroke-width="2"/>
              <text x="-40" y="4" fill="#fff" font-size="8" font-family="sans-serif" font-weight="bold" text-anchor="middle">A</text>
              <line x1="-28" y1="0" x2="-12" y2="0" stroke="#f59e0b" stroke-width="2"/>
              <circle cx="0" cy="0" r="12" fill="#f59e0b" stroke="#d97706" stroke-width="2"/>
              <text x="0" y="4" fill="#000" font-size="8" font-family="sans-serif" font-weight="bold" text-anchor="middle">B</text>
              <line x1="12" y1="0" x2="28" y2="0" stroke="#f59e0b" stroke-width="2"/>
              <circle cx="40" cy="0" r="12" fill="#ef4444" stroke="#b91c1c" stroke-width="2"/>
              <text x="40" y="4" fill="#fff" font-size="8" font-family="sans-serif" font-weight="bold" text-anchor="middle">C</text>
            </g>
            <text x="110" y="212" fill="#38bdf8" font-size="8.5" font-family="monospace" font-weight="bold" text-anchor="middle">TOPOLOGICAL DAG BARRIER</text>
            <text x="110" y="245" fill="#38bdf8" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">FLIGHT COMMANDER (DAG)</text>
        </svg>'''

    elif svg_type == "bulldog":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- Bulldog Face -->
            <ellipse cx="110" cy="95" rx="42" ry="36" fill="#92400e" stroke="#451a03" stroke-width="3"/>
            <!-- Jowls -->
            <circle cx="95" cy="110" r="16" fill="#b45309"/>
            <circle cx="125" cy="110" r="16" fill="#b45309"/>
            <polygon points="103,98 117,98 110,108" fill="#000"/>
            <!-- Eyes -->
            <circle cx="92" cy="85" r="7" fill="#000"/>
            <circle cx="90" cy="83" r="2.5" fill="#fff"/>
            <circle cx="128" cy="85" r="7" fill="#000"/>
            <circle cx="126" cy="83" r="2.5" fill="#fff"/>
            <!-- Spiked collar -->
            <path d="M 70 128 Q 110 145 150 128" fill="none" stroke="#ef4444" stroke-width="7"/>
            <!-- Big Red Breaker Switch Tripped -->
            <rect x="75" y="150" width="70" height="45" rx="6" fill="#1e293b" stroke="#ef4444" stroke-width="3"/>
            <!-- Lever in TRIPPED downward position -->
            <line x1="110" y1="160" x2="110" y2="185" stroke="#ef4444" stroke-width="6" stroke-linecap="round"/>
            <circle cx="110" cy="185" r="6" fill="#b91c1c"/>
            <text x="110" y="212" fill="#ef4444" font-size="9" font-family="monospace" font-weight="bold" text-anchor="middle">15s TIMER • TRIPPED!</text>
            <text x="110" y="245" fill="#ef4444" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">SPARKY BULLDOG (WATCHDOG)</text>
        </svg>'''

    elif svg_type == "traffic_sentinel":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- Traffic Light Body -->
            <rect x="75" y="45" width="70" height="120" rx="14" fill="#1e293b" stroke="#f59e0b" stroke-width="3"/>
            <!-- Red Light (Off) -->
            <circle cx="110" cy="72" r="14" fill="#450a0a" stroke="#7f1d1d" stroke-width="2"/>
            <!-- Yellow Light (Off) -->
            <circle cx="110" cy="105" r="14" fill="#451a03" stroke="#78350f" stroke-width="2"/>
            <!-- Green Light (Active Glow) -->
            <circle cx="110" cy="138" r="14" fill="#10b981" stroke="#34d399" stroke-width="3"/>
            <circle cx="110" cy="138" r="6" fill="#ecfdf5"/>
            <!-- Monotonic Fence Token Badge -->
            <g transform="translate(110, 195)">
              <rect x="-55" y="-14" width="110" height="28" rx="6" fill="#fef08a" stroke="#ca8a04" stroke-width="2"/>
              <text x="0" y="4" fill="#854d0e" font-size="9.5" font-family="monospace" font-weight="bold" text-anchor="middle">TOKEN #1042 • 15s</text>
            </g>
            <text x="110" y="245" fill="#10b981" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">TRAFFIC SENTINEL (MUTEX)</text>
        </svg>'''

    elif svg_type == "desk_organizer":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- Tidy Desk -->
            <rect x="35" y="140" width="150" height="12" rx="2" fill="#92400e" stroke="#78350f" stroke-width="2"/>
            <rect x="45" y="152" width="12" height="40" fill="#78350f"/>
            <rect x="163" y="152" width="12" height="40" fill="#78350f"/>
            <!-- 3 Clean Sheets on Desk (8K Window) -->
            <rect x="60" y="105" width="22" height="32" rx="2" fill="#fff" stroke="#94a3b8" stroke-width="1.5"/>
            <rect x="90" y="102" width="22" height="35" rx="2" fill="#fff" stroke="#38bdf8" stroke-width="2"/>
            <rect x="120" y="105" width="22" height="32" rx="2" fill="#fff" stroke="#94a3b8" stroke-width="1.5"/>
            <!-- Curved Pneumatic Vacuum Tube to Vault -->
            <path d="M 175 40 Q 140 40 140 85 L 140 100" fill="none" stroke="#38bdf8" stroke-width="8" stroke-linecap="round"/>
            <path d="M 175 40 Q 140 40 140 85 L 140 100" fill="none" stroke="#0284c7" stroke-width="3" stroke-dasharray="4 4"/>
            <!-- Paged Out Stub Box -->
            <rect x="40" y="50" width="85" height="26" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
            <text x="82" y="66" fill="#38bdf8" font-size="8" font-family="monospace" font-weight="bold" text-anchor="middle">[PAGED: s3/42]</text>
            <text x="110" y="210" fill="#38bdf8" font-size="8.5" font-family="monospace" font-weight="bold" text-anchor="middle">WORKING RAM: 8,192 TOKENS</text>
            <text x="110" y="245" fill="#38bdf8" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">DESK ORGANIZER (PAGER)</text>
        </svg>'''

    elif svg_type == "bronze_scribe":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- Bronze Book with Wax Seals -->
            <rect x="40" y="60" width="140" height="100" rx="6" fill="#78350f" stroke="#b45309" stroke-width="3"/>
            <!-- Left page & Right page -->
            <rect x="48" y="68" width="60" height="84" rx="2" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
            <rect x="112" y="68" width="60" height="84" rx="2" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
            <!-- Red Wax Hash Seal -->
            <circle cx="78" cy="110" r="14" fill="#dc2626" stroke="#991b1b" stroke-width="2"/>
            <text x="78" y="114" fill="#ffffff" font-size="8" font-family="Impact" text-anchor="middle">SHA</text>
            <circle cx="142" cy="110" r="14" fill="#dc2626" stroke="#991b1b" stroke-width="2"/>
            <text x="142" y="114" fill="#ffffff" font-size="8" font-family="Impact" text-anchor="middle">SHA</text>
            <!-- Cryptographic chain link between pages -->
            <path d="M 92 110 L 128 110" stroke="#7c3aed" stroke-width="4" stroke-dasharray="3 2"/>
            <text x="110" y="185" fill="#f59e0b" font-size="8" font-family="monospace" font-weight="bold" text-anchor="middle">HASH(N) = SHA256(PREV + DATA)</text>
            <rect x="45" y="195" width="130" height="20" rx="4" fill="#059669"/>
            <text x="110" y="209" fill="#ffffff" font-size="8.5" font-family="monospace" font-weight="bold" text-anchor="middle">IMMUTABLE CAUSALITY</text>
            <text x="110" y="245" fill="#f59e0b" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">BRONZE SCRIBE (LEDGER)</text>
        </svg>'''

    elif svg_type == "detective_scoop":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- 3-Source Triangulation Radar Board -->
            <polygon points="110,50 60,135 160,135" fill="rgba(16,185,129,0.15)" stroke="#10b981" stroke-width="2.5"/>
            <!-- Top Node: S3 WORM -->
            <circle cx="110" cy="50" r="16" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>
            <text x="110" y="54" fill="#ffffff" font-size="8" font-family="Impact" text-anchor="middle">S3</text>
            <!-- Bottom Left Node: OpenSearch k-NN -->
            <circle cx="60" cy="135" r="16" fill="#f59e0b" stroke="#fbbf24" stroke-width="2"/>
            <text x="60" y="139" fill="#000000" font-size="8" font-family="Impact" text-anchor="middle">k-NN</text>
            <!-- Bottom Right Node: Neptune Graph -->
            <circle cx="160" cy="135" r="16" fill="#7c3aed" stroke="#c084fc" stroke-width="2"/>
            <text x="160" y="139" fill="#ffffff" font-size="8" font-family="Impact" text-anchor="middle">GRAPH</text>
            <!-- Center Verification Stamp -->
            <circle cx="110" cy="105" r="12" fill="#10b981"/>
            <text x="110" y="109" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">&#10003;</text>
            <!-- CERT_OK Stamped Document -->
            <rect x="50" y="170" width="120" height="28" rx="4" fill="#ecfdf5" stroke="#10b981" stroke-width="2"/>
            <text x="110" y="188" fill="#065f46" font-size="9.5" font-family="Impact" text-anchor="middle">CERT_OK STAMPED</text>
            <text x="110" y="210" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">ALL 3 MUST AGREE</text>
            <text x="110" y="245" fill="#10b981" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">DETECTIVE SCOOP (GROUNDING)</text>
        </svg>'''

    elif svg_type == "navigator":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- Watts-Strogatz Hubs -->
            <!-- Pod 1 Hub (Finance) -->
            <circle cx="70" cy="105" r="32" fill="rgba(124,58,237,0.2)" stroke="#8b5cf6" stroke-width="2.5"/>
            <circle cx="70" cy="105" r="10" fill="#7c3aed"/>
            <text x="70" y="109" fill="#fff" font-size="7.5" font-family="sans-serif" font-weight="bold" text-anchor="middle">POD A</text>
            <!-- Pod 2 Hub (Ops) -->
            <circle cx="150" cy="105" r="32" fill="rgba(37,99,235,0.2)" stroke="#3b82f6" stroke-width="2.5"/>
            <circle cx="150" cy="105" r="10" fill="#2563eb"/>
            <text x="150" y="109" fill="#fff" font-size="7.5" font-family="sans-serif" font-weight="bold" text-anchor="middle">POD B</text>
            <!-- Golden Shortcut Bridge -->
            <path d="M 80 105 Q 110 65 140 105" fill="none" stroke="#f59e0b" stroke-width="4"/>
            <rect x="95" y="60" width="30" height="14" rx="3" fill="#f59e0b"/>
            <text x="110" y="70" fill="#000" font-size="7" font-family="monospace" font-weight="bold" text-anchor="middle">p=0.15</text>
            <!-- Bounded Hops banner -->
            <rect x="45" y="170" width="130" height="24" rx="4" fill="#059669"/>
            <text x="110" y="186" fill="#fff" font-size="9" font-family="monospace" font-weight="bold" text-anchor="middle">&lt;= 3 HOPS ACROSS SWARM</text>
            <text x="110" y="208" fill="#c084fc" font-size="8" font-family="monospace" text-anchor="middle">CLUSTERING C = 0.68</text>
            <text x="110" y="245" fill="#a855f7" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">NAVIGATOR (TOPOLOGY BUILDER)</text>
        </svg>'''

    elif svg_type == "ambassador_leo":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- Embassy Desk & Boundary -->
            <line x1="110" y1="40" x2="110" y2="180" stroke="#f59e0b" stroke-width="3" stroke-dasharray="6 4"/>
            <!-- Left Country (Pod A) -->
            <rect x="35" y="70" width="55" height="40" rx="6" fill="#1e293b" stroke="#3b82f6" stroke-width="2"/>
            <text x="62" y="94" fill="#38bdf8" font-size="8" font-family="monospace" font-weight="bold" text-anchor="middle">POD A</text>
            <!-- Right Country (Pod B) -->
            <rect x="130" y="70" width="55" height="40" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
            <text x="157" y="94" fill="#34d399" font-size="8" font-family="monospace" font-weight="bold" text-anchor="middle">POD B</text>
            <!-- Ambassador Leo Diplomatic Pouch Crossing Bridge -->
            <g transform="translate(110, 90)">
              <rect x="-18" y="-12" width="36" height="24" rx="4" fill="#fef08a" stroke="#ca8a04" stroke-width="2"/>
              <text x="0" y="3" fill="#854d0e" font-size="12" text-anchor="middle">&#9993;</text>
              <circle cx="0" cy="-12" r="4" fill="#ef4444"/>
            </g>
            <rect x="40" y="165" width="140" height="26" rx="4" fill="#1e293b" stroke="#a855f7" stroke-width="2"/>
            <text x="110" y="182" fill="#c084fc" font-size="8.5" font-family="monospace" font-weight="bold" text-anchor="middle">VETTED VIA RING 0 KERNEL</text>
            <text x="110" y="245" fill="#a855f7" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">AMBASSADOR LEO (LIAISON)</text>
        </svg>'''

    elif svg_type == "ticket_puncher":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- Metal Ticket Puncher -->
            <g transform="translate(110, 70)">
              <rect x="-35" y="-14" width="70" height="28" rx="6" fill="#64748b" stroke="#cbd5e1" stroke-width="3"/>
              <circle cx="0" cy="0" r="8" fill="#0f172a"/>
              <text x="0" y="4" fill="#ef4444" font-size="9" font-family="Impact" text-anchor="middle">&#10005;</text>
            </g>
            <!-- 3 Ticket Punches -->
            <g transform="translate(110, 130)">
              <rect x="-65" y="-20" width="130" height="40" rx="8" fill="#fef3c7" stroke="#d97706" stroke-width="2.5"/>
              <circle cx="-35" cy="0" r="10" fill="#0284c7"/>
              <text x="-35" y="3" fill="#fff" font-size="7.5" font-family="monospace" font-weight="bold" text-anchor="middle">P1</text>
              <circle cx="0" cy="0" r="10" fill="#0284c7"/>
              <text x="0" y="3" fill="#fff" font-size="7.5" font-family="monospace" font-weight="bold" text-anchor="middle">P2</text>
              <circle cx="35" cy="0" r="10" fill="#dc2626"/>
              <text x="35" y="3" fill="#fff" font-size="7.5" font-family="monospace" font-weight="bold" text-anchor="middle">P3</text>
            </g>
            <rect x="45" y="180" width="130" height="24" rx="4" fill="#ef4444"/>
            <text x="110" y="196" fill="#fff" font-size="9" font-family="monospace" font-weight="bold" text-anchor="middle">TTL=0 • EXECUTE OR HALT!</text>
            <text x="110" y="245" fill="#a855f7" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">TICKET PUNCHER (HOP LIMITER)</text>
        </svg>'''

    elif svg_type == "whiteboard_master":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- Submarine Tactical Blackboard -->
            <rect x="35" y="45" width="150" height="95" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="3"/>
            <!-- 3 Partitioned Lanes -->
            <rect x="42" y="55" width="40" height="75" rx="4" fill="#0284c7" opacity="0.3"/>
            <text x="62" y="72" fill="#38bdf8" font-size="7" font-family="monospace" font-weight="bold" text-anchor="middle">DEMAND</text>
            <rect x="90" y="55" width="40" height="75" rx="4" fill="#10b981" opacity="0.3"/>
            <text x="110" y="72" fill="#34d399" font-size="7" font-family="monospace" font-weight="bold" text-anchor="middle">SUPPLY</text>
            <rect x="138" y="55" width="40" height="75" rx="4" fill="#f59e0b" opacity="0.3"/>
            <text x="158" y="72" fill="#fbbf24" font-size="7" font-family="monospace" font-weight="bold" text-anchor="middle">CTRL</text>
            <!-- The CAS Mutex Talking Stick -->
            <g transform="translate(110, 165)">
              <rect x="-55" y="-9" width="110" height="18" rx="9" fill="#d97706" stroke="#fef08a" stroke-width="2.5"/>
              <circle cx="-45" cy="0" r="5" fill="#fef08a"/>
              <circle cx="45" cy="0" r="5" fill="#fef08a"/>
              <text x="0" y="4" fill="#ffffff" font-size="7.5" font-family="Impact" text-anchor="middle">TALKING STICK MUTEX</text>
            </g>
            <rect x="45" y="195" width="130" height="20" rx="4" fill="#059669"/>
            <text x="110" y="209" fill="#ffffff" font-size="8.5" font-family="monospace" font-weight="bold" text-anchor="middle">O(N) ILLUMINATION</text>
            <text x="110" y="245" fill="#a855f7" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">QUARTERMASTER (WHITEBOARD)</text>
        </svg>'''

    elif svg_type == "quorum_director":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- 10/12 Quorum Voting Console -->
            <rect x="40" y="45" width="140" height="105" rx="10" fill="#1e293b" stroke="#10b981" stroke-width="3"/>
            <!-- 10 Green Valid Ballots -->
            <g transform="translate(52, 60)">
              <rect x="0" y="0" width="18" height="16" rx="3" fill="#10b981"/>
              <rect x="24" y="0" width="18" height="16" rx="3" fill="#10b981"/>
              <rect x="48" y="0" width="18" height="16" rx="3" fill="#10b981"/>
              <rect x="72" y="0" width="18" height="16" rx="3" fill="#10b981"/>
              <rect x="96" y="0" width="18" height="16" rx="3" fill="#10b981"/>
              <rect x="0" y="24" width="18" height="16" rx="3" fill="#10b981"/>
              <rect x="24" y="24" width="18" height="16" rx="3" fill="#10b981"/>
              <rect x="48" y="24" width="18" height="16" rx="3" fill="#10b981"/>
              <rect x="72" y="24" width="18" height="16" rx="3" fill="#10b981"/>
              <rect x="96" y="24" width="18" height="16" rx="3" fill="#10b981"/>
              <!-- 2 Glitching Nodes (Red) -->
              <rect x="0" y="48" width="18" height="16" rx="3" fill="#ef4444"/>
              <rect x="24" y="48" width="18" height="16" rx="3" fill="#ef4444"/>
            </g>
            <rect x="45" y="165" width="130" height="24" rx="4" fill="#059669"/>
            <text x="110" y="181" fill="#ffffff" font-size="8.5" font-family="monospace" font-weight="bold" text-anchor="middle">10/12 QUORUM LOCKED</text>
            <text x="110" y="205" fill="#10b981" font-size="8" font-family="monospace" text-anchor="middle">BYZANTINE TOLERANCE (2f+1)</text>
            <text x="110" y="245" fill="#a855f7" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">QUORUM DIRECTOR (ARBITER)</text>
        </svg>'''

    elif svg_type == "marshal_redcard":
        return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="{w}" height="{h}" rx="12" fill="#0f172a"/>
            <!-- Big Red Card Waved by Referee -->
            <g transform="translate(110, 85) rotate(-10)">
              <rect x="-24" y="-38" width="48" height="76" rx="6" fill="#ef4444" stroke="#b91c1c" stroke-width="3"/>
              <text x="0" y="5" fill="#ffffff" font-size="10" font-family="Impact" text-anchor="middle">RED</text>
              <text x="0" y="18" fill="#ffffff" font-size="10" font-family="Impact" text-anchor="middle">CARD</text>
            </g>
            <!-- Smoking Racecar in Pit Lane -->
            <g transform="translate(110, 160)">
              <rect x="-35" y="-10" width="70" height="20" rx="4" fill="#334155" stroke="#ef4444" stroke-width="2"/>
              <circle cx="-22" cy="10" r="7" fill="#0f172a"/>
              <circle cx="22" cy="10" r="7" fill="#0f172a"/>
              <!-- Black smoke clouds -->
              <circle cx="-35" cy="-18" r="8" fill="#64748b" opacity="0.6"/>
              <circle cx="-25" cy="-24" r="10" fill="#475569" opacity="0.7"/>
            </g>
            <rect x="45" y="195" width="130" height="20" rx="4" fill="#ef4444"/>
            <text x="110" y="209" fill="#ffffff" font-size="8.5" font-family="monospace" font-weight="bold" text-anchor="middle">BENCHED 5 MIN IN PIT LANE</text>
            <text x="110" y="245" fill="#ef4444" font-size="11" font-weight="bold" font-family="Impact" text-anchor="middle" letter-spacing="1">MARSHAL REDCARD (BREAKER)</text>
        </svg>'''

    return f'''<svg viewBox="0 0 {w} {h}" width="100%" height="100%"><rect width="{w}" height="{h}" fill="#1e293b"/></svg>'''

def build_dossier_html():
    cards_html = []

    for c in CHARACTERS:
        portrait_svg = get_character_portrait_svg(c["svg_type"], w=220, h=260)
        spec = c["spec"]

        trace_steps_html = ""
        for st_title, st_desc in spec["downward_trace"]:
            trace_steps_html += f"""
            <div class="trace-pill">
                <span class="trace-pill-title">{st_title}:</span>
                <span class="trace-pill-desc">{st_desc}</span>
            </div>
            """

        card_markup = f"""
        <div class="character-dossier-card" id="char-card-{c['id']}" data-tier="{c['tier'].split(':')[0].strip()}">
            <!-- LEFT: ILLUSTRATED CARTOON CHARACTER PROFILE -->
            <div class="char-portrait-col">
                <div class="portrait-header">
                    <span class="tier-badge-pill" style="background:{c['tier_color']}; color:#fff;">{c['tier'].split(':')[0]} • SKILL #{c['id']}</span>
                    <span class="ring-badge-pill">{c['ring'].split('(')[0].strip()}</span>
                </div>
                <div class="portrait-svg-container" style="border-color:{c['border_color']};">
                    {portrait_svg}
                </div>
                <div class="char-title-block">
                    <div class="char-codename">{c['icon']} {c['name']}</div>
                    <div class="char-service-tag">{c['service']}</div>
                    <div class="char-archetype">{c['archetype']}</div>
                </div>
                <div class="char-quote-box">
                    "{c['catchphrase']}"
                </div>
                <div class="char-superpower-tag">
                    ⚡ {c['superpower']}
                </div>
            </div>

            <!-- RIGHT: FORMAL ARCHITECTURAL SPECIFICATION & TIER 0 TRACE -->
            <div class="char-spec-col">
                <div class="spec-header-flex">
                    <div>
                        <div class="spec-title">Formal Engineering Contract &amp; Invariants</div>
                        <div class="spec-module-code">SKILL.md Module: <code>{spec['module']}</code></div>
                    </div>
                    <div class="sla-badge">
                        ⏱ SLA: {spec['latency_sla']}
                    </div>
                </div>

                <!-- Spec Grid -->
                <div class="spec-fields-grid">
                    <div class="spec-field">
                        <div class="field-label">System Role &amp; Responsibility</div>
                        <div class="field-val">{spec['role']}</div>
                    </div>
                    <div class="spec-field">
                        <div class="field-label">Input / Output Boundary Contract</div>
                        <div class="field-val">{spec['input_output']}</div>
                    </div>
                    <div class="spec-field">
                        <div class="field-label">IAM &amp; Privilege Ring Isolation</div>
                        <div class="field-val">{spec['iam_boundary']}</div>
                    </div>
                </div>

                <!-- Downward Traceability to Tier 0 -->
                <div class="spec-trace-box">
                    <div class="trace-box-header">
                        <span class="trace-box-tag">⬇️ DOWNWARD TRACEABILITY TO TIER 0 AWS INFRASTRUCTURE</span>
                        <span class="trace-box-sub">Root Cloud Primitives &amp; Hardware Proof</span>
                    </div>
                    <div class="trace-pills-list">
                        {trace_steps_html}
                    </div>
                </div>

                <!-- Failure Mode & Containment Protocol -->
                <div class="spec-failure-box">
                    <div class="failure-row">
                        <span class="failure-tag">⚠️ CATASTROPHIC FAILURE MODE:</span>
                        <span class="failure-desc">{spec['failure_mode']}</span>
                    </div>
                    <div class="containment-row">
                        <span class="containment-tag">🛡️ HARDWARE CONTAINMENT:</span>
                        <span class="containment-desc">{spec['containment']}</span>
                    </div>
                </div>
            </div>
        </div>
        """
        cards_html.append(card_markup)

    html_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>20 Enterprise Agent Characters • 3-Tier Citadel Field Manual</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-page: #f8fafc;
      --bg-card: #ffffff;
      --bg-card-subtle: #f1f5f9;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --border-color: #cbd5e1;
      --border-focus: #3b82f6;

      --tier0-green: #059669;
      --tier0-bg: #ecfdf5;
      --tier1-blue: #2563eb;
      --tier1-bg: #eff6ff;
      --tier2-purple: #7c3aed;
      --tier2-bg: #f5f3ff;

      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', 'Consolas', monospace;
      --font-display: 'Impact', 'Arial Black', sans-serif;
    }}

    [data-theme="dark"] {{
      --bg-page: #0b1120;
      --bg-card: #131d31;
      --bg-card-subtle: #1e293b;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --border-color: #334155;
      --border-focus: #38bdf8;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: var(--font-sans);
      background: var(--bg-page);
      color: var(--text-main);
      padding: 24px;
      line-height: 1.5;
    }}

    /* HEADER BANNER */
    .studio-header {{
      background: var(--bg-card);
      border: 2px solid var(--border-color);
      border-radius: 16px;
      padding: 24px 32px;
      margin-bottom: 24px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.05);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .studio-title-group {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}
    .studio-badge {{
      display: inline-block;
      background: #f59e0b;
      color: #000;
      font-weight: 900;
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      font-family: var(--font-mono);
      width: fit-content;
    }}
    .studio-main-title {{
      font-family: var(--font-display);
      font-size: 28px;
      letter-spacing: 0.5px;
      color: var(--text-main);
    }}
    .studio-subtext {{
      font-size: 13px;
      color: var(--text-muted);
      max-width: 650px;
    }}

    .studio-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}
    .btn {{
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 12.5px;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid transparent;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
      text-decoration: none;
      font-family: var(--font-sans);
    }}
    .btn-primary {{
      background: #f59e0b;
      color: #000;
    }}
    .btn-primary:hover {{
      background: #d97706;
    }}
    .btn-secondary {{
      background: var(--bg-card-subtle);
      color: var(--text-main);
      border-color: var(--border-color);
    }}
    .btn-secondary:hover {{
      background: var(--border-color);
    }}

    /* FILTER TOOLBAR */
    .filter-toolbar {{
      background: var(--bg-card);
      border: 1.5px solid var(--border-color);
      border-radius: 12px;
      padding: 12px 20px;
      margin-bottom: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .filter-btn-group {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .filter-chip {{
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid var(--border-color);
      background: var(--bg-card-subtle);
      color: var(--text-muted);
      transition: all 0.2s;
    }}
    .filter-chip.active {{
      background: var(--text-main);
      color: var(--bg-card);
      border-color: var(--text-main);
    }}
    .search-box {{
      padding: 6px 14px;
      border-radius: 8px;
      border: 1px solid var(--border-color);
      background: var(--bg-card-subtle);
      color: var(--text-main);
      font-size: 12.5px;
      font-family: var(--font-mono);
      min-width: 260px;
    }}

    /* DOSSIER CARDS CONTAINER */
    .dossier-list {{
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}

    /* DOSSIER CARD */
    .character-dossier-card {{
      background: var(--bg-card);
      border: 2px solid var(--border-color);
      border-radius: 16px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.06);
      display: grid;
      grid-template-columns: 310px 1fr;
      overflow: hidden;
      transition: all 0.25s ease;
    }}
    .character-dossier-card:hover {{
      border-color: var(--border-focus);
      box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }}

    @media (max-width: 900px) {{
      .character-dossier-card {{
        grid-template-columns: 1fr;
      }}
    }}

    /* LEFT: CHARACTER PROFILE */
    .char-portrait-col {{
      background: var(--bg-card-subtle);
      border-right: 2px solid var(--border-color);
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
    }}
    .portrait-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .tier-badge-pill {{
      font-size: 10px;
      font-weight: 900;
      padding: 2px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      font-family: var(--font-mono);
    }}
    .ring-badge-pill {{
      font-size: 9.5px;
      font-weight: 700;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }}

    .portrait-svg-container {{
      width: 100%;
      height: 230px;
      border-radius: 12px;
      overflow: hidden;
      border: 2px solid;
      background: #0f172a;
      box-shadow: inset 0 2px 6px rgba(0,0,0,0.2);
    }}

    .char-title-block {{
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    .char-codename {{
      font-family: var(--font-display);
      font-size: 20px;
      letter-spacing: 0.5px;
      color: var(--text-main);
    }}
    .char-service-tag {{
      font-size: 11px;
      font-weight: 800;
      color: var(--border-focus);
      font-family: var(--font-mono);
    }}
    .char-archetype {{
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      font-style: italic;
    }}

    .char-quote-box {{
      background: var(--bg-card);
      border: 1.5px solid var(--border-color);
      border-radius: 8px;
      padding: 8px 10px;
      font-size: 10.5px;
      font-style: italic;
      color: var(--text-main);
      line-height: 1.35;
    }}
    .char-superpower-tag {{
      background: #0f172a;
      border: 1.5px solid #38bdf8;
      color: #38bdf8;
      font-size: 10px;
      font-weight: 800;
      padding: 4px 8px;
      border-radius: 6px;
      text-align: center;
      line-height: 1.3;
    }}

    /* RIGHT: ARCHITECTURAL SPECIFICATION */
    .char-spec-col {{
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 14px;
    }}
    .spec-header-flex {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 1.5px solid var(--border-color);
      padding-bottom: 10px;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .spec-title {{
      font-size: 16px;
      font-weight: 800;
      color: var(--text-main);
    }}
    .spec-module-code {{
      font-size: 11.5px;
      color: var(--text-muted);
      font-family: var(--font-mono);
      margin-top: 2px;
    }}
    .spec-module-code code {{
      background: var(--bg-card-subtle);
      padding: 1px 5px;
      border-radius: 4px;
      border: 1px solid var(--border-color);
      color: var(--border-focus);
    }}
    .sla-badge {{
      background: #fef3c7;
      color: #92400e;
      border: 1px solid #fde68a;
      font-size: 10.5px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
      font-family: var(--font-mono);
    }}

    .spec-fields-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 10px;
    }}
    .spec-field {{
      background: var(--bg-card-subtle);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 8px 12px;
    }}
    .field-label {{
      font-size: 10px;
      font-weight: 800;
      color: var(--text-muted);
      text-transform: uppercase;
      font-family: var(--font-mono);
    }}
    .field-val {{
      font-size: 11.5px;
      color: var(--text-main);
      font-weight: 600;
      margin-top: 2px;
    }}

    /* DOWNWARD TRACE BOX */
    .spec-trace-box {{
      border: 1.5px solid var(--border-color);
      border-radius: 10px;
      padding: 12px 14px;
      background: var(--bg-card-subtle);
    }}
    .trace-box-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .trace-box-tag {{
      font-size: 10px;
      font-weight: 900;
      color: var(--text-main);
      font-family: var(--font-mono);
    }}
    .trace-box-sub {{
      font-size: 10px;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }}
    .trace-pills-list {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 8px;
    }}
    .trace-pill {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 6px 10px;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    .trace-pill-title {{
      font-size: 10px;
      font-weight: 800;
      color: var(--text-main);
    }}
    .trace-pill-desc {{
      font-size: 10px;
      color: var(--text-muted);
      font-family: var(--font-mono);
      line-height: 1.3;
    }}

    /* FAILURE & CONTAINMENT BOX */
    .spec-failure-box {{
      border: 1.5px solid var(--border-color);
      border-radius: 10px;
      padding: 10px 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      background: var(--bg-card);
    }}
    .failure-row, .containment-row {{
      font-size: 11px;
      display: flex;
      align-items: flex-start;
      gap: 6px;
      line-height: 1.35;
    }}
    .failure-tag {{
      font-weight: 800;
      color: #dc2626;
      font-family: var(--font-mono);
      white-space: nowrap;
    }}
    .failure-desc {{
      color: var(--text-main);
    }}
    .containment-tag {{
      font-weight: 800;
      color: #059669;
      font-family: var(--font-mono);
      white-space: nowrap;
    }}
    .containment-desc {{
      color: var(--text-main);
    }}
  </style>
</head>
<body>

  <!-- HEADER BANNER -->
  <header class="studio-header">
    <div class="studio-title-group">
      <span class="studio-badge">THE CITADEL FIELD MANUAL • OFFICIAL SPECIFICATION</span>
      <h1 class="studio-main-title">The 20 Enterprise Agent Characters &amp; Architecture Dossier</h1>
      <p class="studio-subtext">
        Every agent has an illustrated persona, formal privilege ring, production <code>SKILL.md</code> contract, 
        and downward traceability to Tier 0 AWS physical cloud primitives.
      </p>
    </div>
    <div class="studio-actions">
      <button class="btn btn-secondary" onclick="toggleTheme()">🌓 Dark / Light</button>
      <a href="https://github.com/cosmosanalytics/uat-copilot-local/raw/main/The_20_Enterprise_Agent_Characters_Field_Manual.pdf" class="btn btn-primary" download>
        ⬇️ Download Field Manual PDF
      </a>
    </div>
  </header>

  <!-- FILTER & SEARCH TOOLBAR -->
  <section class="filter-toolbar">
    <div class="filter-btn-group">
      <button class="filter-chip active" onclick="filterTier('all', this)">All 20 Agents</button>
      <button class="filter-chip" onclick="filterTier('Tier 0', this)">Tier 0: Cloud Primitives (7)</button>
      <button class="filter-chip" onclick="filterTier('Tier 1', this)">Tier 1: Agent OS Kernel (7)</button>
      <button class="filter-chip" onclick="filterTier('Tier 2', this)">Tier 2: Swarm Coordination (6)</button>
    </div>
    <input type="text" class="search-box" id="searchBox" placeholder="🔍 Search agent, AWS API, or role..." onkeyup="searchAgents(this.value)">
  </section>

  <!-- 20 AGENT CARDS LIST -->
  <main class="dossier-list" id="dossierList">
    {"".join(cards_html)}
  </main>

  <script>
    function toggleTheme() {{
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
    }}

    function filterTier(tier, btn) {{
      document.querySelectorAll('.filter-chip').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const cards = document.querySelectorAll('.character-dossier-card');
      cards.forEach(card => {{
        if (tier === 'all' || card.getAttribute('data-tier') === tier) {{
          card.style.display = 'grid';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    function searchAgents(query) {{
      const q = query.toLowerCase();
      const cards = document.querySelectorAll('.character-dossier-card');
      cards.forEach(card => {{
        const text = card.textContent.toLowerCase();
        if (text.includes(q)) {{
          card.style.display = 'grid';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}
  </script>
</body>
</html>
"""

    out_html = "agent_character_dossier_studio.html"
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html_page)
    print(f"Generated {out_html} ({len(html_page)} bytes)")

    # Compile to PDF
    out_pdf = "The_20_Enterprise_Agent_Characters_Field_Manual.pdf"
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    abs_html = os.path.abspath(out_html)
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={os.path.abspath(out_pdf)}",
        f"file:///{abs_html}"
    ]
    print(f"Compiling Field Manual PDF via {chrome_path}...")
    subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(out_pdf):
        print(f"SUCCESS: Generated Field Manual PDF at {out_pdf} ({os.path.getsize(out_pdf)/(1024*1024):.2f} MB)")
    else:
        print("WARNING: PDF generation failed.")

if __name__ == "__main__":
    build_dossier_html()
