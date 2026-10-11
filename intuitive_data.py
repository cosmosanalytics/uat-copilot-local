# -*- coding: utf-8 -*-
"""
intuitive_data.py
Contains the 20 simple, intuitive, graphical & fun architectural mental models,
metaphors, diagrams, and rules of thumb for the 20 skills.
"""

INTUITIVE_DATA = [
    # 1: aws-bedrock
    {
        "hook": "The Dreamer with No Hands",
        "concept": "Separating Creative Inference from Physical State Mutation",
        "metaphor": (
            "Think of Bedrock as an eccentric, brilliant architect who sketches incredible blueprints on restaurant napkins. "
            "He has endless imagination, but he is strictly banned from holding a sledgehammer or construction crane! "
            "He creates typed JSON blueprints, but possesses zero IAM credentials to touch your databases or APIs. "
            "His ideas remain pure proposals until the Prefrontal Kernel approves them."
        ),
        "diagram": [
            ("User Task", "Raw prompt intent"),
            ("Bedrock Engine", "Ring 3 proposal space"),
            ("JSON Blueprint", "Quarantined typed contract")
        ],
        "diagram_caption": "Creative Inference (Ring 3)  ──►  Structured Schema  ──►  Gated by Kernel (Ring 0)",
        "wire_expl": "Blue wire feeds proposed JSON contracts up into Kernel Propose-Decide (#8). Nothing executes until the Brain Judge issues a formal verdict.",
        "wire_target": "Kernel Propose-Decide (#8)",
        "superpower": "Sub-second multi-model reasoning without the danger of rogue tool execution.",
        "rule_of_thumb": "Never give IAM mutation keys to an LLM. Treat all model outputs as unverified proposals."
    },
    # 2: aws-agentcore
    {
        "hook": "The Cryptographic Bouncer",
        "concept": "Deterministic AST Guardrails over Fuzzy System Prompts",
        "metaphor": (
            "Imagine an elite VIP lounge with a robotic bouncer holding a cryptographic rulebook. "
            "Even if a smooth-talking AI agent shows up in a tuxedo claiming a national emergency, the bouncer doesn't negotiate. "
            "In 2 milliseconds, it compiles the request into a Cedar Abstract Syntax Tree (AST): Principal, Action, Resource. "
            "If the policy returns FORBID, the steel door remains bolted. Zero social engineering allowed."
        ),
        "diagram": [
            ("Proposed Syscall", "Agent requests mutation"),
            ("Cedar AST Engine", "Sub-10ms policy check"),
            ("Permit / Deny Token", "Cryptographic authorization")
        ],
        "diagram_caption": "Agent Mutation Request  ──►  Cedar AST Evaluation  ──►  Deterministic Access Token",
        "wire_expl": "Blue wire connects directly to Kernel Propose-Decide (#8). Every proposed syscall is validated against compiled Cedar policies before hitting AWS hardware.",
        "wire_target": "Kernel Propose-Decide (#8)",
        "superpower": "Sub-10ms deterministic authorization that is mathematically immune to prompt injection.",
        "rule_of_thumb": "Security guardrails belong in formal AST rulebooks (Cedar), never in prompt text."
    },
    # 3: aws-s3-vault
    {
        "hook": "The Titanium Time Capsule",
        "concept": "Cryptographic WORM Compliance (Write Once, Read Many)",
        "metaphor": (
            "Picture dropping a wax-sealed, signed legal treaty into a titanium safe through a one-way mail slot. "
            "Once inside, a mechanical lock freezes the door for exactly 7 years. "
            "Even the CEO, company root administrator, or AWS account owner cannot alter a single comma or delete the record. "
            "Every agent perception and tool result gets an immutable SHA-256 fingerprint."
        ),
        "diagram": [
            ("Execution Receipt", "SHA-256 digested payload"),
            ("S3 Object Lock", "Compliance WORM mode"),
            ("7-Year Anchor", "Zero tampering possible")
        ],
        "diagram_caption": "Payload Digest  ──►  S3 Object Lock Enforcement  ──►  Immutable Legal Audit Proof",
        "wire_expl": "Three blue wires plug into this vault from Context Pager (#12), Episodic Ledger (#13), and Grounding Certifier (#14) to permanently seal audit receipts.",
        "wire_target": "Context Pager (#12), Ledger (#13), & Grounding (#14)",
        "superpower": "Guarantees 100% forensic honesty—past execution history cannot be rewritten or erased.",
        "rule_of_thumb": "Audit logs that can be overwritten are just suggestions. Real enterprise audit is immutable WORM."
    },
    # 4: aws-database
    {
        "hook": "The Multi-Tool Precision Locker",
        "concept": "Tri-Store State: Atomic Locks, Vector Similarity & Graph Ontologies",
        "metaphor": (
            "Why force one database to do three completely different jobs? This locker has three specialized drawers: "
            "Drawer 1 holds atomic CAS locks (DynamoDB) so multiple workers never collide on the same row; "
            "Drawer 2 holds a high-speed semantic searchlight (OpenSearch vectors) to match concepts; "
            "Drawer 3 holds a relational spiderweb (Neptune graph) mapping deep corporate entity connections."
        ),
        "diagram": [
            ("DynamoDB CAS", "Atomic concurrency lock"),
            ("OpenSearch k-NN", "Semantic cosine match"),
            ("Neptune Graph", "Entity-relationship triples")
        ],
        "diagram_caption": "Atomic Concurrency  |  Semantic Vector Proximity  |  Knowledge Graph Relations",
        "wire_expl": "Blue wires provide conditional atomic locks to Kernel Mutex (#11) and feed multi-modal facts into Detective Triangulator (#14).",
        "wire_target": "Kernel Mutex (#11) & Grounding Certifier (#14)",
        "superpower": "Zero race conditions combined with rich multi-source semantic and relational retrieval.",
        "rule_of_thumb": "Never rely on a single database type. Separate concurrency locks from vector embeddings and graphs."
    },
    # 5: aws-lambda
    {
        "hook": "The Ephemeral Pop-Up Lab",
        "concept": "Stateless MicroVM Sandboxing with Zero Residue",
        "metaphor": (
            "Imagine an inflatable high-tech cleanroom that pops up in 50 milliseconds, performs a delicate calculation or "
            "code execution, and instantly vanishes into thin air without leaving a single molecule on the floor. "
            "Yesterday's crumbs, memory leaks, or poisoned variables can never contaminate today's execution. "
            "Everything is strictly memory-capped (512MB) and bounded by a 15-second wall clock."
        ),
        "diagram": [
            ("Stateless Payload", "Pure function invocation"),
            ("Firecracker MicroVM", "Isolated hardware sandbox"),
            ("Instant Dissolution", "Zero residual state left")
        ],
        "diagram_caption": "Stateless Task  ──►  Isolated Firecracker Container  ──►  Result Returned & Destroyed",
        "wire_expl": "Plugs into Kernel Runbook Engine (#9) for discrete execution stages and Watchdog Supervisor (#10) for strict timeout enforcement.",
        "wire_target": "Runbook Engine (#9) & Watchdog Supervisor (#10)",
        "superpower": "Fresh, pristine compute environments on every call with zero persistent attack surface.",
        "rule_of_thumb": "Treat compute runtimes like paper napkins, not pets. Execute, collect results, and destroy."
    },
    # 6: aws-stepfunctions
    {
        "hook": "The Unskippable Rail System",
        "concept": "Hierarchical Finite State Machine (HFSM) with Guaranteed Checkpoints",
        "metaphor": (
            "Think of an automated roller coaster on a fixed steel rail with ratchet safety brakes. "
            "You cannot jump from loop #1 straight to loop #5. Every transition requires satisfying strict checkpoint criteria. "
            "If a mechanical fault happens on step #3, the reverse ratchet catches the cart and glides it backwards into a "
            "registered compensatory safe state—never derailing."
        ),
        "diagram": [
            ("State 1: Validate", "Prerequisites verified"),
            ("State 2: Execute", "Task deployed in sandbox"),
            ("State 3: Commit", "Atomic state confirmed")
        ],
        "diagram_caption": "Strict Sequential DAG  ──►  Deterministic Transition  ──►  Automatic Rollback on Error",
        "wire_expl": "Blue wire anchors the Kernel Runbook Engine (#9), providing strict state machine checkpoints and automated compensatory rollbacks.",
        "wire_target": "Kernel Runbook Engine (#9)",
        "superpower": "Guarantees workflows never skip prerequisites, drop transactions, or lose execution state.",
        "rule_of_thumb": "Never let agents 'wing it' through complex multi-step processes. Model workflows as explicit state machines."
    },
    # 7: aws-client-api
    {
        "hook": "The Targeted Airport Pager",
        "concept": "Declarative Pub/Sub Event Routing without Broadcast Noise",
        "metaphor": (
            "Instead of a blaring loudspeaker screaming every single flight update across the entire terminal, "
            "passengers hold smart pagers that buzz only when their specific flight group boards. "
            "EventBridge routes high-throughput asynchronous signals across specialist pods with declarative pattern matching. "
            "Pods stay quiet and focused on their domain work until an event tagged specifically for them arrives."
        ),
        "diagram": [
            ("Event Ingested", "OpenAPI validated ingress"),
            ("EventBridge Filter", "Declarative pattern match"),
            ("Subscriber Queue", "Delivered only to target pod")
        ],
        "diagram_caption": "Ingress Event  ──►  Declarative Pattern Evaluation  ──►  Direct Consumer Delivery",
        "wire_expl": "Connects to Kernel Supervisor Watchdog (#10) to broadcast emergency circuit breaker alerts instantly across the entire swarm.",
        "wire_target": "Kernel Supervisor Watchdog (#10)",
        "superpower": "High-throughput asynchronous communication with zero broadcast chatter or message storms.",
        "rule_of_thumb": "Whisper to specific subscribers; never broadcast raw messages across a multi-agent mesh."
    },
    # 8: kernel-propose-decide
    {
        "hook": "The Prefrontal Cortex Firewall",
        "concept": "The Fundamental Invariant: Action = Kernel_Verdict( Model_Proposal )",
        "metaphor": (
            "When you smell freshly baked cookies, your primal brain impulsively shouts: 'Eat all 12 right now!' "
            "Your prefrontal cortex steps in: 'Wait, dinner is in 10 minutes. Eat one.' "
            "In modern AI architecture, LLMs are that impulsive imagination engine (Ring 3). "
            "The Prefrontal Kernel (Ring 0) is the rational executive gate that evaluates proposals against security policies before any real action occurs."
        ),
        "diagram": [
            ("Model Proposal", "Untrusted Ring 3 JSON"),
            ("Prefrontal Filter", "Ring 0 invariant check"),
            ("Action Verdict", "Approved physical execution")
        ],
        "diagram_caption": "Untrusted Model Idea  ──►  Executive Policy Evaluation  ──►  Authorized Syscall Execution",
        "wire_expl": "Centrally connected to Bedrock (#1) and Cedar (#2) below, while intercepting cross-pod messages from Ambassador Leo (#16) above.",
        "wire_target": "Bedrock (#1), Cedar (#2), & Liaison Router (#16)",
        "superpower": "Eliminates rogue AI hallucinations by mathematically separating proposal generation from execution authority.",
        "rule_of_thumb": "Action = Verdict(Proposal). An LLM is an inference engine, not a trustworthy operating system."
    },
    # 9: kernel-runbook-engine
    {
        "hook": "The Mission Flight Checklist",
        "concept": "Compiling Swarm Intent into Directed Acyclic Graph (DAG) Checkpoints",
        "metaphor": (
            "NASA astronauts don't launch rockets by improvising. They execute pre-flight checklists where task B cannot "
            "begin until task A passes telemetry checks. "
            "The Runbook Engine compiles high-level swarm directives into a mathematical Directed Acyclic Graph (DAG) with "
            "step barriers. If any milestone fails validation, the engine halts the branch before damage spreads."
        ),
        "diagram": [
            ("Mission Goal", "Decomposed into steps"),
            ("DAG Execution", "Dependency barrier gates"),
            ("Milestone Sealed", "WORM hash committed")
        ],
        "diagram_caption": "Decomposed DAG  ──►  Step Barrier Telemetry Verification  ──►  Idempotent State Commit",
        "wire_expl": "Takes high-level mission layouts from Swarm Topology (#15) and compiles them into Step Functions (#6) and Lambda (#5) executions.",
        "wire_target": "Topology (#15), Step Functions (#6), & Lambda (#5)",
        "superpower": "Transforms chaotic multi-agent goals into deterministic, reproducible engineering pipelines.",
        "rule_of_thumb": "Replace monolithic agent prompt loops with explicit DAG runbooks and verifiable step barriers."
    },
    # 10: kernel-supervisor-circuit
    {
        "hook": "The Deadlock Watchdog & Kill Switch",
        "concept": "Out-of-Band Hardware Timer Overriding Rogue Execution Threads",
        "metaphor": (
            "Think of the industrial circuit breaker in your house's electrical panel. "
            "If a faulty appliance draws dangerous current, the physical switch trips in 5 milliseconds—independent of what "
            "the appliance wants. "
            "Watchdog Sparky monitors agent threads with an external egg timer. If an agent loops 3 times or exceeds 15 seconds, "
            "the supervisor kills the process and resets state."
        ),
        "diagram": [
            ("Active Thread", "Agent processing task"),
            ("Watchdog Timer", "15s countdown ceiling"),
            ("Normal OR Trip", "Reset state on deadlock")
        ],
        "diagram_caption": "Monitored Agent Thread  ──►  External Countdown Watchdog  ──►  Immediate Thread Termination on Loop",
        "wire_expl": "Accepts trip signals from Hop Limiter (#17) and Circuit Breaker (#20); radios emergency shutdown events via EventBridge (#7).",
        "wire_target": "Hop Limiter (#17), Circuit Breaker (#20), & EventBridge (#7)",
        "superpower": "Prevents runaway LLM loops and runaway token burns before they consume system resources.",
        "rule_of_thumb": "Every autonomous agent must have an external, non-bypassable supervisor kill switch."
    },
    # 11: kernel-mutex-lease
    {
        "hook": "The Traffic Light & Fenced Token",
        "concept": "Distributed Atomic Locks with Monotonic Fencing Tokens & TTL Auto-Expiry",
        "metaphor": (
            "When 4 self-driving cars enter a busy intersection, they don't negotiate by honking at each other. "
            "The traffic light grants an exclusive 15-second green signal paired with a monotonic ticket number. "
            "If a car stalls mid-intersection, its lease expires automatically, dissolving the lock so traffic resumes. "
            "Stale out-of-order writes are rejected by the fence token."
        ),
        "diagram": [
            ("Acquire Request", "Agent requests write lease"),
            ("DynamoDB CAS", "Atomic conditional write"),
            ("Fence Token Granted", "15-second TTL countdown")
        ],
        "diagram_caption": "Acquire Request  ──►  Atomic Compare-and-Swap (CAS)  ──►  Monotonic Fenced Execution Lease",
        "wire_expl": "Plugs into DynamoDB Locker (#4) for atomic CAS operations. Leased by Shared Whiteboard (#18) and forcefully revoked by Red Card (#20).",
        "wire_target": "AWS Database (#4), Whiteboard (#18), & Circuit Breaker (#20)",
        "superpower": "Eliminates race conditions, write collisions, and deadlocks across concurrent agent clusters.",
        "rule_of_thumb": "Always pair distributed locks with TTL expiration and monotonic fencing tokens to reject zombie writes."
    },
    # 12: kernel-context-pager
    {
        "hook": "The Virtual RAM Desk Organizer",
        "concept": "Virtual Memory Management: Keeping Active Attention Bounded at 8k Tokens",
        "metaphor": (
            "A financial trader doesn't keep 500 open paper folders spread across their physical desk. "
            "They keep 3 active sheets within arm's reach and file older charts into a motorized archive cabinet. "
            "If they need last week's chart, an automated retriever fetches it in 20 milliseconds. "
            "The Context Pager prevents context dilution by paging cold frames out to S3 WORM storage."
        ),
        "diagram": [
            ("Active Working RAM", "8,192 token attention ceiling"),
            ("Context Pager", "Evicts cold reasoning frames"),
            ("S3 Vault Archive", "Immutable retrieval by key")
        ],
        "diagram_caption": "Bounded Active RAM (8k)  ◄── Evict / Hydrate Frames ──►  Immutable S3 Storage Vault",
        "wire_expl": "Blue wire evicts cold reasoning frames down into the 7-year S3 WORM safe (#3), maintaining high model attention accuracy.",
        "wire_target": "Amazon S3 Vault (#3)",
        "superpower": "Maintains sharp, hallucination-free reasoning by keeping working context small while preserving infinite memory.",
        "rule_of_thumb": "Do not stuff massive context into active prompts. Keep working RAM tiny (8k) and page out history."
    },
    # 13: kernel-episodic-ledger
    {
        "hook": "The Blockchain of Agent Cognition",
        "concept": "Append-Only SHA-256 Hash-Chaining: Block(n) = Hash(Block(n-1) + Data)",
        "metaphor": (
            "Imagine an unbreakable digital diary where every page incorporates the cryptographic hash of the page before it. "
            "If a malicious actor or buggy model attempts to retroactively alter a past perception or delete an erroneous decision, "
            "the hash equation breaks down the entire chain. "
            "It provides tamper-evident proof linking perception directly to action."
        ),
        "diagram": [
            ("Perception & Action", "Structured event payload"),
            ("SHA-256 Hash Chaining", "Block_n embeds Block_n-1"),
            ("WORM Audit Vault", "Immutable append-only record")
        ],
        "diagram_caption": "Decision Payload  ──►  Cryptographic Hash Chaining  ──►  Append-Only S3 WORM Commitment",
        "wire_expl": "Collects verified team findings from Shared Whiteboard (#18), chains them with SHA-256 digests, and locks them into S3 Vault (#3).",
        "wire_target": "Whiteboard (#18) & Amazon S3 Vault (#3)",
        "superpower": "Mathematically guarantees that agent decision history can never be rewritten or falsified.",
        "rule_of_thumb": "Auditability requires cryptographic causality. Chain perceptions to actions with append-only hashes."
    },
    # 14: kernel-grounding-certifier
    {
        "hook": "The 3-Source Investigative Reporter",
        "concept": "Multi-Modal Triangulation: S3 Object Receipt + Vector Match + Graph Triple",
        "metaphor": (
            "An award-winning investigative journalist never publishes a breaking story based on an unverified rumor. "
            "They demand 3 independent pieces of physical corroboration: "
            "Proof 1 is a signed photo receipt in S3 (#3); "
            "Proof 2 is a high-confidence semantic vector match (>0.82) in OpenSearch (#4); "
            "Proof 3 is a validated relational entity triple in Neptune (#4). All 3 must agree."
        ),
        "diagram": [
            ("Candidate Assertion", "Model proposes claim"),
            ("3-Source Triangulator", "S3 Photo + Vector + Graph"),
            ("Grounding Token", "CERT_OK cryptographic proof")
        ],
        "diagram_caption": "Candidate Claim  ──►  Tri-Store Verification (Receipt + Embedding + Graph)  ──►  Certified Fact",
        "wire_expl": "Supplies certified facts up to Byzantine Ballot Box (#19) by cross-checking receipts in S3 (#3) and graph relations in DB (#4).",
        "wire_target": "Quorum Arbiter (#19), S3 Vault (#3), & Database (#4)",
        "superpower": "Completely annihilates hallucinated assertions before they enter the swarm decision pipeline.",
        "rule_of_thumb": "Grounding is not prompt engineering. It is a tri-store cryptographic consensus verification protocol."
    },
    # 15: swarm-topology-builder
    {
        "hook": "The Small-World Airport Hub Network",
        "concept": "Watts-Strogatz Lattice (p=0.15): High Clustering (C=0.68) with Short Paths (L=1.8)",
        "metaphor": (
            "A global airline doesn't run non-stop flights between every single pair of 10,000 cities—that would create $O(N^2)$ chaos. "
            "Instead, they cluster regional flights within cities and connect regions through long-range express hub flights. "
            "Agents work in dense specialist pods (Finance, Compliance, Ops) with long-range shortcut bridges, "
            "enabling any agent to reach any other in <= 3 hops without message explosions."
        ),
        "diagram": [
            ("Finance Pod", "4 local nodes (dense)"),
            ("Gold Liaison Bridges", "p=0.15 shortcut links"),
            ("Operations Pod", "4 local nodes (dense)")
        ],
        "diagram_caption": "High Local Clustering (C=0.68)  ──►  Long-Range Shortcut Bridges  ──►  Bounded Diameter (L <= 3)",
        "wire_expl": "Translates the small-world clubhouse cluster map into step-by-step DAG runbook stages in Kernel Runbook Engine (#9).",
        "wire_target": "Kernel Runbook Engine (#9)",
        "superpower": "Connects large swarms of agents with ultra-short communication paths while eliminating O(N^2) message storms.",
        "rule_of_thumb": "Structure multi-agent swarms as Watts-Strogatz small worlds with high clustering and bounded shortcuts."
    },
    # 16: swarm-liaison-router
    {
        "hook": "The Diplomatic Embassy Channel",
        "concept": "Cross-Pod Boundary Isolation via Designated Ambassador Leaders",
        "metaphor": (
            "When the government of France communicates with Japan, 67 million French citizens don't send individual chat "
            "messages to 125 million Japanese citizens. "
            "Communication flows strictly through designated ambassadors who review every diplomatic memo with their cabinet. "
            "Liaison agents funnel inquiries across pods, ensuring internal discussions remain isolated and noise-free."
        ),
        "diagram": [
            ("Pod A Internal", "Domain debate isolated"),
            ("Liaison Ambassador", "Structured cross-pod query"),
            ("Pod B Receiver", "Vetted through Ring 0 gate")
        ],
        "diagram_caption": "Internal Pod Deliberation  ──►  Designated Liaison Ambassador  ──►  Kernel-Vetted Cross-Pod Transit",
        "wire_expl": "Routes inter-pod messages down through Kernel Propose-Decide (#8). No message enters a pod without kernel arbitration.",
        "wire_target": "Kernel Propose-Decide (#8)",
        "superpower": "Maintains strict modularity across agent domains, preventing communication leaks and cross-pod confusion.",
        "rule_of_thumb": "Confine intra-domain chatter to specialist pods; route cross-domain queries via designated ambassadors."
    },
    # 17: swarm-hop-limiter
    {
        "hook": "The 3-Hop Game of Hot Potato",
        "concept": "Monotonic TTL Delegation Budgets & Cycle-Free Loop Prevention",
        "metaphor": (
            "We've all suffered through workplace email chains where person A forwards a question to B, B forwards to C, "
            "and C forwards it right back to A without anyone doing the work! "
            "The Hop Limiter punches a strict 3-ticket budget on every message. "
            "Hop 1 uses ticket #1; Hop 2 uses ticket #2; Hop 3 is the final stop. If anyone tries a 4th hop, the referee halts the loop!"
        ),
        "diagram": [
            ("Delegation 1", "Ticket #1 punched (TTL=2)"),
            ("Delegation 2", "Ticket #2 punched (TTL=1)"),
            ("Final Hop 3", "Ticket #3: MUST EXECUTE")
        ],
        "diagram_caption": "Monotonic Ticket Decrement  ──►  Cycle Detection Visited Hash  ──►  Loop Interrupt on Expiry",
        "wire_expl": "Signals Watchdog Sparky (#10). If the 3-ticket hop limit is exhausted without task resolution, the supervisor terminates the cycle.",
        "wire_target": "Kernel Supervisor Watchdog (#10)",
        "superpower": "Permanently terminates infinite delegation loops and circular gossip tag games in multi-agent networks.",
        "rule_of_thumb": "Enforce monotonic TTL budgets and visited-node history on every multi-agent delegation packet."
    },
    # 18: swarm-shared-whiteboard
    {
        "hook": "The Tactical Combat Blackboard",
        "concept": "The Blackboard Pattern: O(N) Shared Memory Replacing O(N^2) Point-to-Point Messaging",
        "metaphor": (
            "On a naval submarine during combat, crew members don't send 500 individual radio messages to each other. "
            "They write radar positions, sonar depths, and weapons status on a central illuminated tactical blackboard. "
            "Everyone reads the same shared truth in real time with zero messaging overhead. "
            "Each domain owns its own lane, governed by atomic mutex locks."
        ),
        "diagram": [
            ("Finance Lane", "Liquidity & balance state"),
            ("Compliance Lane", "Cedar passes & proofs"),
            ("Operations Lane", "Build tasks & progress")
        ],
        "diagram_caption": "Global Read Visibility (O(1))  ──►  Partitioned Write Ownership  ──►  Atomic Mutex Commit (O(N))",
        "wire_expl": "Drops two purple wires down: one borrows Talking Stick (#11) for atomic lane writes, and the other commits snapshots to Wax Diary (#13).",
        "wire_target": "Kernel Mutex (#11) & Episodic Ledger (#13)",
        "superpower": "Enables dozens of agents to collaborate with O(N) write complexity instead of O(N^2) communication explosion.",
        "rule_of_thumb": "Replace peer-to-peer message storms with partitioned blackboard lanes and atomic mutex locks."
    },
    # 19: swarm-consensus-arbiter
    {
        "hook": "The Byzantine Spaceflight Quorum",
        "concept": "Byzantine Fault Tolerance: Unstoppable Decisions with >= 2/3 + 1 Supermajority",
        "metaphor": (
            "NASA space shuttles fly with redundant flight computers voting on thruster burns. "
            "If cosmic radiation scrambles 1 computer and it starts voting crazy numbers, the remaining computers outvote it "
            "in milliseconds and maintain trajectory. "
            "The Byzantine Arbiter requires a >= 2/3 + 1 supermajority (>= 10 of 12 votes), with each ballot backed by "
            "cryptographic grounding receipts from Detective Triangulator."
        ),
        "diagram": [
            ("10 Verified Votes", "Valid Grounding receipts"),
            ("2 Faulty Nodes", "Glitching or ungrounded"),
            ("Binding Quorum", "Supermajority verdict committed")
        ],
        "diagram_caption": "Cryptographic Ballot Ingest  ──►  Supermajority Threshold (>= 10/12)  ──►  Binding S3 WORM Commit",
        "wire_expl": "Verifies all voting ballots with Detective Triangulator (#14). No vote counts unless backed by S3 receipts and vector similarity proofs.",
        "wire_target": "Grounding Certifier (#14)",
        "superpower": "Reaches deterministic, tamper-proof consensus even when up to 3 agent nodes glitch, crash, or hallucinate.",
        "rule_of_thumb": "High-stakes autonomous actions must require Byzantine fault-tolerant quorums with cryptographic grounding."
    },
    # 20: swarm-circuit-breaker
    {
        "hook": "The Formula 1 Red Card & Pit Stop",
        "concept": "Automated Cascade Quarantine & Immediate Mutex Lease Revocation",
        "metaphor": (
            "In high-speed auto racing, if a car gets a flat tire or spews smoke, race marshals immediately wave the black flag. "
            "The driver must pull into the pit stop before causing a multi-car collision. "
            "The Circuit Breaker detects hallucinating or spinning agents, pulls them off the active network for a 5-minute cool down, "
            "and immediately snatches their active mutex write lease so they cannot corrupt shared memory."
        ),
        "diagram": [
            ("Anomaly Detected", "3 strikes / error threshold"),
            ("Referee Whistle", "Agent benched to pit lane"),
            ("Mutex Revoked", "Locks released immediately")
        ],
        "diagram_caption": "Error Spike Detected  ──►  Immediate Thread Quarantine  ──►  Active Lock Revocation & Rerouting",
        "wire_expl": "Two purple wires: one trips Watchdog Sparky (#10) to pause execution, and the other instantly revokes the DynamoDB mutex lease (#11).",
        "wire_target": "Watchdog Sparky (#10) & Kernel Mutex (#11)",
        "superpower": "Prevents a single malfunctioning agent from creating a domino effect that crashes the entire swarm.",
        "rule_of_thumb": "When an agent fails, don't just log it. Immediately bench the node and forcefully revoke its active write locks."
    }
]
