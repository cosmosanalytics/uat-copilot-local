# -*- coding: utf-8 -*-
"""
update_aws_basics_studio.py
Embeds all 20 production-grade SKILL.md specification files across all 3 Tiers
(Level 0 AWS Cloud Basics, Level 1 Agent OS Kernel, Level 2 Small-World Multi-Agent Network)
directly into aws_basics_studio_app.html with interactive tier filtering, search, copy,
and export capabilities.
"""

import json
import re

# Define all 20 Skills in full SKILL.md format
SKILLS_DATA = [
    # LEVEL 0: AWS CLOUD PRIMITIVES & SIMULATOR BINDINGS (7 Skills)
    {
        "id": "aws-bedrock",
        "name": "aws-bedrock",
        "title": "Amazon Bedrock Proposal Synthesizer",
        "tier": "Level 0",
        "tierCode": "L0",
        "ring": "Ring 3 (Untrusted Proposal Space)",
        "service": "Amazon Bedrock",
        "category": "AWS Cloud Primitives",
        "description": "Foundation model inference engine generating strictly typed JSON proposals. Never executes mutations directly.",
        "content": """---
name: aws-bedrock
description: Foundation model inference engine generating strictly typed JSON proposals. Never executes mutations directly.
version: 1.0.0
tier: Level 0 (Physical Cloud Primitives)
ring: Ring 3 (Untrusted Proposal Space)
service: Amazon Bedrock
permissions:
  - bedrock:InvokeModel
  - bedrock:InvokeModelWithResponseStream
tools:
  - synthesize_proposal
  - evaluate_prompt_schema
---

# aws-bedrock: Foundation Model Proposal Engine

## 1. Purpose & Architectural Boundary
`aws-bedrock` operates strictly within **Ring 3 (Untrusted Proposal Space)**. Its sole role is to transform natural language user objectives and system contexts into deterministic, structured JSON schemas. Under the Ring 0 / Ring 3 segregation principle:
- `aws-bedrock` **proposes** state changes.
- It is **strictly forbidden** from holding IAM mutation credentials.
- All generated payloads are quarantined until verified by `aws-agentcore`.

## 2. Input JSON Schema
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["prompt", "modelId", "responseSchema"],
  "properties": {
    "prompt": { "type": "string", "description": "User intent or task description" },
    "systemPrompt": { "type": "string", "description": "Kernel-injected behavioral constraints" },
    "modelId": { "type": "string", "default": "anthropic.claude-3-5-sonnet-20241022-v2:0" },
    "temperature": { "type": "number", "minimum": 0.0, "maximum": 1.0, "default": 0.2 },
    "responseSchema": { "type": "object", "description": "Target JSON schema for structured output" }
  }
}
```

## 3. Output Schema & Guarantees
```json
{
  "type": "object",
  "required": ["proposalId", "structuredPayload", "modelId", "reasoningHash"],
  "properties": {
    "proposalId": { "type": "string", "format": "uuid" },
    "structuredPayload": { "type": "object" },
    "modelId": { "type": "string" },
    "reasoningHash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
    "latencyMs": { "type": "integer" }
  }
}
```

## 4. Deterministic Guardrails
1. **No Out-of-Band Calls:** Bedrock responses must never trigger network requests without kernel mediation.
2. **Schema Conformance:** If output violates `responseSchema`, the kernel triggers instant rejection without retry token bleed.
3. **Receipt Tagging:** Bedrock outputs are hashed (SHA-256) and passed to `aws-s3-vault` before execution.
"""
    },
    {
        "id": "aws-agentcore",
        "name": "aws-agentcore",
        "title": "AgentCore Cedar Guardrail Gatekeeper",
        "tier": "Level 0",
        "tierCode": "L0",
        "ring": "Ring 0 (Kernel Supervisor)",
        "service": "AWS Verified Permissions / IAM",
        "category": "AWS Cloud Primitives",
        "description": "Kernel-level gatekeeper validating agent tool proposals against Cedar policies and syscall boundaries.",
        "content": """---
name: aws-agentcore
description: Kernel-level gatekeeper validating agent tool proposals against Cedar policies and syscall boundaries.
version: 1.0.0
tier: Level 0 (Physical Cloud Primitives)
ring: Ring 0 (Kernel Gatekeeper)
service: AWS Verified Permissions
permissions:
  - verifiedpermissions:IsAuthorized
  - verifiedpermissions:GetPolicy
tools:
  - enforce_cedar_guardrails
  - validate_syscall_args
---

# aws-agentcore: Ring 0 Cedar Guardrail Engine

## 1. Purpose & Security Model
`aws-agentcore` forms the **unbypassable hardware-like boundary** between autonomous reasoning (Ring 3) and cloud infrastructure (Ring 0). Every action proposed by Bedrock must be submitted to `aws-agentcore` for authorization before any AWS SDK call occurs.

## 2. Cedar Policy Definition Example
```cedar
// Permit financial operations only if leased by agent and bounded below $10,000
permit(
    principal in AgentGroup::"FinanceWorkers",
    action in [Action::"TransferFunds", Action::"ReconcileBatch"],
    resource in ResourceType::"LedgerAccount"
) when {
    context.hasValidLease == true &&
    context.proposedAmount <= 10000 &&
    context.s3ReceiptHash != ""
};
```

## 3. Input JSON Schema
```json
{
  "type": "object",
  "required": ["agentId", "proposedAction", "targetResourceArn", "actionParameters"],
  "properties": {
    "agentId": { "type": "string" },
    "proposedAction": { "type": "string" },
    "targetResourceArn": { "type": "string" },
    "actionParameters": { "type": "object" },
    "contextReceipts": { "type": "array", "items": { "type": "string" } }
  }
}
```

## 4. Output Contract
```json
{
  "type": "object",
  "required": ["decision", "evaluatedPolicyId", "auditSignature"],
  "properties": {
    "decision": { "type": "string", "enum": ["ALLOW", "DENY"] },
    "evaluatedPolicyId": { "type": "string" },
    "denialReason": { "type": "string" },
    "auditSignature": { "type": "string" }
  }
}
```
"""
    },
    {
        "id": "aws-s3-vault",
        "name": "aws-s3-vault",
        "title": "Amazon S3 WORM Receipt Vault",
        "tier": "Level 0",
        "tierCode": "L0",
        "ring": "Ring 0 (Cryptographic Vault)",
        "service": "Amazon S3 (Object Lock Compliance)",
        "category": "AWS Cloud Primitives",
        "description": "Cryptographic WORM storage ensuring all agent facts, audit logs, and outputs have immutable SHA-256 receipts.",
        "content": """---
name: aws-s3-vault
description: Cryptographic WORM storage ensuring all agent facts, audit logs, and outputs have immutable SHA-256 receipts.
version: 1.0.0
tier: Level 0 (Physical Cloud Primitives)
ring: Ring 0 (Immutable Vault)
service: Amazon S3
permissions:
  - s3:PutObject
  - s3:GetObject
  - s3:PutObjectLegalHold
tools:
  - commit_worm_receipt
  - verify_receipt_hash
---

# aws-s3-vault: Write-Once-Read-Many Grounding Engine

## 1. Purpose & Guarantees
In autonomous multi-agent environments, hallucinations often stem from mutable state and ungrounded memories. `aws-s3-vault` guarantees **Zero Hallucination Amnesia** by persisting all perception records, state transitions, and completed jobs under S3 Object Lock (`COMPLIANCE` mode).

## 2. Invariants
- **Non-deletable:** Even root accounts cannot overwrite or delete receipts before retention period expiry.
- **SHA-256 Integrity:** Objects must be accompanied by an x-amz-checksum-sha256 header.
- **Auditable URIs:** Receipts are addressed via `s3://bucket/receipts/{agent_id}/{timestamp}_{hash}.json`.

## 3. Input Schema
```json
{
  "type": "object",
  "required": ["bucket", "receiptKey", "payload", "retentionDays"],
  "properties": {
    "bucket": { "type": "string" },
    "receiptKey": { "type": "string" },
    "payload": { "type": "object" },
    "retentionDays": { "type": "integer", "default": 365 },
    "legalHold": { "type": "boolean", "default": true }
  }
}
```

## 4. Output Contract
```json
{
  "type": "object",
  "required": ["s3Uri", "sha256Checksum", "versionId", "wormStatus"],
  "properties": {
    "s3Uri": { "type": "string" },
    "sha256Checksum": { "type": "string" },
    "versionId": { "type": "string" },
    "wormStatus": { "type": "string", "enum": ["COMPLIANT_LOCKED"] }
  }
}
```
"""
    },
    {
        "id": "aws-database",
        "name": "aws-database",
        "title": "Distributed State, Vector & Graph Database",
        "tier": "Level 0",
        "tierCode": "L0",
        "ring": "Ring 0 (State Store)",
        "service": "Amazon DynamoDB + OpenSearch + Neptune",
        "category": "AWS Cloud Primitives",
        "description": "Multi-engine grounding store managing DynamoDB CAS mutex locks, OpenSearch vectors, and Neptune graph triples.",
        "content": """---
name: aws-database
description: Multi-engine grounding store managing DynamoDB CAS mutex locks, OpenSearch vectors, and Neptune graph triples.
version: 1.0.0
tier: Level 0 (Physical Cloud Primitives)
ring: Ring 0 (Distributed State)
service: DynamoDB, OpenSearch Serverless, Amazon Neptune
permissions:
  - dynamodb:PutItem
  - dynamodb:UpdateItem
  - aoss:APIAccessAll
  - neptune-db:*
tools:
  - acquire_cas_mutex
  - release_cas_mutex
  - query_vector_embeddings
  - match_graph_knowledge
---

# aws-database: State Mutex & Grounding Engine

## 1. Capabilities
1. **DynamoDB CAS Mutex (Distributed Locking):** Prevents multi-agent race conditions using atomic conditional expressions (`attribute_not_exists(LockKey) OR expiresAt < :now`).
2. **OpenSearch Serverless (Vector Recall):** Cosine semantic similarity across high-dimensional agent memories ($k$-NN search).
3. **Amazon Neptune (Relational Graph):** Knowledge graph triple storage (Subject-Predicate-Object) for relational queries.

## 2. DynamoDB CAS Expression Reference
```python
dynamodb.put_item(
    TableName='DistributedAgentLocks',
    Item={
        'LockKey': {'S': 'batch-recon-eur-usd'},
        'OwnerAgentId': {'S': 'agent-fin-recon-01'},
        'AcquiredAt': {'N': str(int(time.time()))},
        'ExpiresAt': {'N': str(int(time.time() + 60))},
        'LeaseToken': {'S': str(uuid.uuid4())}
    },
    ConditionExpression='attribute_not_exists(LockKey) OR ExpiresAt < :now',
    ExpressionAttributeValues={':now': {'N': str(int(time.time()))}}
)
```

## 3. Output Schema
```json
{
  "type": "object",
  "required": ["success", "operation"],
  "properties": {
    "success": { "type": "boolean" },
    "operation": { "type": "string" },
    "leaseToken": { "type": "string" },
    "ttlRemaining": { "type": "integer" },
    "vectorHits": { "type": "array" },
    "graphTriples": { "type": "array" }
  }
}
```
"""
    },
    {
        "id": "aws-lambda",
        "name": "aws-lambda",
        "title": "AWS Lambda Firecracker MicroVM Sandbox",
        "tier": "Level 0",
        "tierCode": "L0",
        "ring": "Ring 1 (Isolated Sandbox)",
        "service": "AWS Lambda",
        "category": "AWS Cloud Primitives",
        "description": "Stateless, memory-capped compute execution in ephemeral Firecracker microVMs with strict execution budgets.",
        "content": """---
name: aws-lambda
description: Stateless, memory-capped compute execution in ephemeral Firecracker microVMs with strict execution budgets.
version: 1.0.0
tier: Level 0 (Physical Cloud Primitives)
ring: Ring 1 (Stateless Sandbox)
service: AWS Lambda
permissions:
  - lambda:InvokeFunction
tools:
  - execute_sandboxed_tool
  - run_ephemeral_compute
---

# aws-lambda: Ephemeral Compute Sandbox

## 1. Architectural Guardrails
- **Zero Host Mutation:** Code runs in isolated Firecracker microVMs.
- **Resource Hard Caps:** Default 512MB RAM, 10s execution timeout.
- **Idempotent Calling:** Must supply `ClientContext` hash for request de-duplication.
- **Stateless Lifecycle:** Memory and ephemeral disk (`/tmp`) are wiped immediately on completion.

## 2. Input JSON Schema
```json
{
  "type": "object",
  "required": ["functionName", "payload"],
  "properties": {
    "functionName": { "type": "string" },
    "payload": { "type": "object" },
    "timeoutSec": { "type": "integer", "maximum": 60, "default": 10 },
    "memoryMb": { "type": "integer", "maximum": 1024, "default": 512 }
  }
}
```

## 3. Output Schema
```json
{
  "type": "object",
  "required": ["statusCode", "outputPayload", "billedDurationMs"],
  "properties": {
    "statusCode": { "type": "integer" },
    "outputPayload": { "type": "object" },
    "billedDurationMs": { "type": "integer" },
    "memoryUsedMb": { "type": "integer" }
  }
}
```
"""
    },
    {
        "id": "aws-stepfunctions",
        "name": "aws-stepfunctions",
        "title": "AWS Step Functions HFSM Orchestrator",
        "tier": "Level 0",
        "tierCode": "L0",
        "ring": "Ring 0 (Deterministic State Machine)",
        "service": "AWS Step Functions",
        "category": "AWS Cloud Primitives",
        "description": "Hierarchical Finite State Machine workflow manager ensuring deterministic transitions and automatic rollback.",
        "content": """---
name: aws-stepfunctions
description: Hierarchical Finite State Machine workflow manager ensuring deterministic transitions and automatic rollback.
version: 1.0.0
tier: Level 0 (Physical Cloud Primitives)
ring: Ring 0 (Workflow HFSM)
service: AWS Step Functions
permissions:
  - states:StartExecution
  - states:DescribeExecution
  - states:StopExecution
tools:
  - execute_state_machine
  - trigger_rollback_compensation
---

# aws-stepfunctions: Deterministic Workflow Engine

## 1. Core Principles
Unconstrained LLM loops wander and hallucinate. `aws-stepfunctions` binds agent action into **Hierarchical Finite State Machines (HFSM)**:
1. Each state must finish with a deterministic status (`SUCCESS`, `RETRY`, `FAIL`).
2. Retries are strictly budget-capped (exponential backoff, max 3 attempts).
3. Any unrecoverable error branches to a **Compensation State** to undo distributed mutations (e.g. release locks, refund charges).

## 2. Execution Definition Example
```json
{
  "StartAt": "AcquireDynamoDBLock",
  "States": {
    "AcquireDynamoDBLock": {
      "Type": "Task",
      "Resource": "arn:aws:states:::dynamodb:putItem",
      "Next": "VerifyS3Receipts",
      "Catch": [{ "ErrorEquals": ["States.ALL"], "Next": "AbortWorkflow" }]
    },
    "VerifyS3Receipts": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:function:VerifyS3Receipts",
      "Next": "InvokeLambdaLedger",
      "Catch": [{ "ErrorEquals": ["States.ALL"], "Next": "ReleaseLockCompensation" }]
    },
    "InvokeLambdaLedger": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:function:ReconcileLedgerMicroVM",
      "Next": "ReleaseDynamoDBLock"
    },
    "ReleaseDynamoDBLock": {
      "Type": "Task",
      "Resource": "arn:aws:states:::dynamodb:deleteItem",
      "End": true
    },
    "ReleaseLockCompensation": {
      "Type": "Task",
      "Resource": "arn:aws:states:::dynamodb:deleteItem",
      "Next": "WorkflowFailed"
    },
    "AbortWorkflow": { "Type": "Fail" },
    "WorkflowFailed": { "Type": "Fail" }
  }
}
```
"""
    },
    {
        "id": "aws-client-api",
        "name": "aws-client-api",
        "title": "Amazon EventBridge & API Gateway Telemetry",
        "tier": "Level 0",
        "tierCode": "L0",
        "ring": "Ring 0 (Network Ingress/Egress)",
        "service": "Amazon EventBridge / API Gateway",
        "category": "AWS Cloud Primitives",
        "description": "Network ingress and telemetry gateway validating HTTP contracts and publishing inter-agent events.",
        "content": """---
name: aws-client-api
description: Network ingress and telemetry gateway validating HTTP contracts and publishing inter-agent events.
version: 1.0.0
tier: Level 0 (Physical Cloud Primitives)
ring: Ring 0 (Gateway & Ingress)
service: Amazon EventBridge & API Gateway
permissions:
  - events:PutEvents
  - apigateway:POST
tools:
  - publish_eventbridge_event
  - validate_api_ingress
---

# aws-client-api: Ingress & Egress Gateway

## 1. Capabilities
- **API Gateway Contract Validation:** Enforces OpenAPI v3 schema validation at the perimeter before payload reaches any agent.
- **EventBridge Inter-Cluster Pub/Sub:** Asynchronous, decoupled event broadcasting for multi-agent swarm updates.
- **Audit Stream Ingress:** Emits all state change events to CloudWatch Logs and S3 WORM archives.

## 2. EventBridge Event Envelope
```json
{
  "Source": "corp.agent.os",
  "DetailType": "AgentStateTransitionCompleted",
  "Detail": {
    "agentId": "agent-fin-recon-01",
    "step": "CommitAuditRecord",
    "receiptS3Uri": "s3://agent-grounding-receipts-vault-prod/receipts/rec-9872.json",
    "timestamp": "2026-10-10T21:40:00Z"
  },
  "EventBusName": "AgentCoordinationBus"
}
```
"""
    },

    # LEVEL 1: AGENT OS KERNEL (7 Skills)
    {
        "id": "kernel-propose-decide",
        "name": "kernel-propose-decide",
        "title": "Kernel Propose-Decide Arbiter",
        "tier": "Level 1",
        "tierCode": "L1",
        "ring": "Ring 0 (Executive Control)",
        "service": "Agent OS Core",
        "category": "Executive Control Suite",
        "description": "Prefrontal executive arbiter ensuring model outputs are treated as untrusted proposals subject to kernel verdict.",
        "content": """---
name: kernel-propose-decide
description: Prefrontal executive arbiter ensuring model outputs are treated as untrusted proposals subject to kernel verdict.
version: 1.0.0
tier: Level 1 (Individual Agent OS Kernel)
ring: Ring 0 (Executive Control)
category: Prefrontal Executive Suite
permissions:
  - kernel:EvaluateProposal
  - kernel:DispatchSyscall
tools:
  - evaluate_model_proposal
  - commit_kernel_verdict
---

# kernel-propose-decide: The Executive Gatekeeper

## 1. Axiom of Separation
An LLM is an **inference engine**, not a trustworthy operating system.
`kernel-propose-decide` enforces the fundamental invariant:
$$\\text{Action} = \\text{Verdict}_{\\text{Kernel}}(\\text{Proposal}_{\\text{Model}})$$

## 2. Decision Pipeline
1. Model generates proposed tool call and parameter JSON (Ring 3).
2. Kernel validates against JSON Schema and active goal invariants (Ring 0).
3. Kernel checks active CAS leases and Cedar authorization rules.
4. If valid, kernel issues syscall to Level 0 AWS skill.
5. If invalid, kernel writes denial to episodic memory and halts loop.
"""
    },
    {
        "id": "kernel-runbook-engine",
        "name": "kernel-runbook-engine",
        "title": "Kernel Procedural Runbook Engine",
        "tier": "Level 1",
        "tierCode": "L1",
        "ring": "Ring 0 (Procedural Memory)",
        "service": "Agent OS Core",
        "category": "Executive Control Suite",
        "description": "Procedural memory engine parsing and executing strictly typed DAG workflow runbooks.",
        "content": """---
name: kernel-runbook-engine
description: Procedural memory engine parsing and executing strictly typed DAG workflow runbooks.
version: 1.0.0
tier: Level 1 (Individual Agent OS Kernel)
ring: Ring 0 (Procedural Memory)
category: Prefrontal Executive Suite
permissions:
  - kernel:LoadRunbook
  - kernel:ExecuteStep
tools:
  - parse_runbook_dag
  - advance_step_barrier
---

# kernel-runbook-engine: Procedural DAG Dispatcher

## 1. Design Overview
Prevents erratic agent wandering by converting standard operating procedures into Directed Acyclic Graphs (DAGs). Each step must pass pre-condition checks before execution and post-condition checks before the barrier advances.
"""
    },
    {
        "id": "kernel-supervisor-circuit",
        "name": "kernel-supervisor-circuit",
        "title": "Kernel Supervisor Circuit Breaker",
        "tier": "Level 1",
        "tierCode": "L1",
        "ring": "Ring 0 (Supervisory Watchdog)",
        "service": "Agent OS Core",
        "category": "Executive Control Suite",
        "description": "Watchdog supervisor tracking token budgets, execution loops, and trip circuits on drift.",
        "content": """---
name: kernel-supervisor-circuit
description: Watchdog supervisor tracking token budgets, execution loops, and trip circuits on drift.
version: 1.0.0
tier: Level 1 (Individual Agent OS Kernel)
ring: Ring 0 (Supervisor)
category: Prefrontal Executive Suite
permissions:
  - kernel:MonitorHealth
  - kernel:TripBreaker
tools:
  - check_loop_divergence
  - emergency_kill_switch
---

# kernel-supervisor-circuit: Watchdog & Safety Loop

## 1. Trip Conditions
- **Loop Detection:** 3 consecutive identical proposals trip circuit instantly.
- **Token Budget:** Execution terminating if token burn exceeds $10\\times$ baseline.
- **Timeout Watchdog:** Kills hung microVMs after 15 seconds.
"""
    },
    {
        "id": "kernel-mutex-lease",
        "name": "kernel-mutex-lease",
        "title": "Kernel CAS Mutex Lease Coordinator",
        "tier": "Level 1",
        "tierCode": "L1",
        "ring": "Ring 0 (Concurrency)",
        "service": "Agent OS Core",
        "category": "Executive Control Suite",
        "description": "Distributed concurrency coordinator acquiring and renewing DynamoDB CAS leases with randomized jitter.",
        "content": """---
name: kernel-mutex-lease
description: Distributed concurrency coordinator acquiring and renewing DynamoDB CAS leases with randomized jitter.
version: 1.0.0
tier: Level 1 (Individual Agent OS Kernel)
ring: Ring 0 (Concurrency)
category: Prefrontal Executive Suite
permissions:
  - kernel:AcquireLease
  - kernel:HeartbeatLease
tools:
  - acquire_lease_with_retry
  - heartbeat_lease_renewal
---

# kernel-mutex-lease: CAS Mutex Coordinator

## 1. Guarantee
Guarantees strict single-agent exclusivity over shared business entities (e.g., bank accounts, flight seats, customer records) across distributed swarms.
"""
    },
    {
        "id": "kernel-context-pager",
        "name": "kernel-context-pager",
        "title": "Kernel Virtual Context Pager",
        "tier": "Level 1",
        "tierCode": "L1",
        "ring": "Ring 0 (Working Memory)",
        "service": "Agent OS Core",
        "category": "Multi-Store Memory Suite",
        "description": "Virtual working memory pager implementing O(1) active token window with LRU disk paging.",
        "content": """---
name: kernel-context-pager
description: Virtual working memory pager implementing O(1) active token window with LRU disk paging.
version: 1.0.0
tier: Level 1 (Individual Agent OS Kernel)
ring: Ring 0 (Working Memory)
category: Multi-Store Memory Suite
permissions:
  - kernel:PageContext
  - kernel:EvictColdFrames
tools:
  - page_in_hot_memory
  - page_out_cold_frames
---

# kernel-context-pager: Virtual Working Memory

## 1. Context Window Virtualization
Models suffer from "Lost in the Middle" attention degradation when contexts exceed 16k tokens. `kernel-context-pager` maintains a compact $O(1)$ active sliding window of relevant tokens, paging older context frames out to local disk and S3 vaults.
"""
    },
    {
        "id": "kernel-episodic-ledger",
        "name": "kernel-episodic-ledger",
        "title": "Kernel Episodic Hash-Chained Ledger",
        "tier": "Level 1",
        "tierCode": "L1",
        "ring": "Ring 0 (Episodic Memory)",
        "service": "Agent OS Core",
        "category": "Multi-Store Memory Suite",
        "description": "Append-only, SHA-256 hash-chained episodic memory ledger recording all perceptions, decisions, and outcomes.",
        "content": """---
name: kernel-episodic-ledger
description: Append-only, SHA-256 hash-chained episodic memory ledger recording all perceptions, decisions, and outcomes.
version: 1.0.0
tier: Level 1 (Individual Agent OS Kernel)
ring: Ring 0 (Episodic Memory)
category: Multi-Store Memory Suite
permissions:
  - kernel:AppendEpisodicRecord
  - kernel:VerifyChainIntegrity
tools:
  - append_episode_block
  - audit_ledger_chain
---

# kernel-episodic-ledger: Hash-Chained Episodic Memory

## 1. Blockchain-Style Ledger
Every perception, proposal, and syscall is stamped into an append-only block:
$$\\text{Hash}_i = \\text{SHA-256}(\\text{Hash}_{i-1} \\parallel \\text{Timestamp} \\parallel \\text{Payload})$$
Provides complete mathematical auditability of agent reasoning over time.
"""
    },
    {
        "id": "kernel-grounding-certifier",
        "name": "kernel-grounding-certifier",
        "title": "Kernel Hybrid Grounding Certifier",
        "tier": "Level 1",
        "tierCode": "L1",
        "ring": "Ring 0 (Semantic Grounding)",
        "service": "Agent OS Core",
        "category": "Multi-Store Memory Suite",
        "description": "Triangulates model assertions against S3 WORM receipts, OpenSearch vector cosine distance, and Neptune graph entities.",
        "content": """---
name: kernel-grounding-certifier
description: Triangulates model assertions against S3 WORM receipts, OpenSearch vector cosine distance, and Neptune graph entities.
version: 1.0.0
tier: Level 1 (Individual Agent OS Kernel)
ring: Ring 0 (Semantic Grounding)
category: Multi-Store Memory Suite
permissions:
  - kernel:CertifyGrounding
tools:
  - certify_factual_claim
  - triangulate_evidence
---

# kernel-grounding-certifier: Factual Truth Verifier

## 1. Multi-Store Triangulation
An agent assertion is certified as grounded **only if**:
1. It matches an S3 WORM receipt with verified SHA-256 checksum.
2. It has vector similarity $\\ge 0.82$ in OpenSearch embeddings.
3. It resolves to a valid entity-relationship node in Amazon Neptune.
"""
    },

    # LEVEL 2: SMALL-WORLD MULTI-AGENT NETWORK (6 Skills)
    {
        "id": "swarm-topology-builder",
        "name": "swarm-topology-builder",
        "title": "Swarm Watts-Strogatz Topology Builder",
        "tier": "Level 2",
        "tierCode": "L2",
        "ring": "Ring 0 (Network Topology)",
        "service": "Swarm Coordinator",
        "category": "Multi-Agent Swarm Suite",
        "description": "Builds small-world agent networks with high clustering and short characteristic path length (rewiring probability p=0.15).",
        "content": """---
name: swarm-topology-builder
description: Builds small-world agent networks with high clustering and short characteristic path length (rewiring probability p=0.15).
version: 1.0.0
tier: Level 2 (Small-World Multi-Agent Network)
ring: Ring 0 (Topology Architecture)
category: Swarm Coordination Suite
permissions:
  - swarm:BuildLattice
  - swarm:RewireBridges
tools:
  - generate_small_world_mesh
  - calculate_clustering_coefficient
---

# swarm-topology-builder: Watts-Strogatz Lattice

## 1. Mathematical Foundation
Avoids both chaotic fully-connected $O(N^2)$ chatter and fragile linear chains.
Generates small-world graphs:
- High local clustering coefficient ($C \\gg C_{\\text{random}}$)
- Short average path length ($L \\approx L_{\\text{random}} \\propto \\ln N$)
- Rewiring probability: $p = 0.15$
"""
    },
    {
        "id": "swarm-liaison-router",
        "name": "swarm-liaison-router",
        "title": "Swarm Inter-Cluster Liaison Router",
        "tier": "Level 2",
        "tierCode": "L2",
        "ring": "Ring 0 (Inter-Cluster Routing)",
        "service": "Swarm Coordinator",
        "category": "Multi-Agent Swarm Suite",
        "description": "Dedicated bridge router mediating communication between dense specialist clusters without message flooding.",
        "content": """---
name: swarm-liaison-router
description: Dedicated bridge router mediating communication between dense specialist clusters without message flooding.
version: 1.0.0
tier: Level 2 (Small-World Multi-Agent Network)
ring: Ring 0 (Inter-Cluster Routing)
category: Swarm Coordination Suite
permissions:
  - swarm:RouteCrossCluster
tools:
  - dispatch_liaison_message
  - resolve_cluster_boundary
---

# swarm-liaison-router: Bridge Router

## 1. Isolation & Efficiency
Specialist agent teams (e.g., Coding Pod, Finance Pod, Compliance Pod) communicate internally with high bandwidth. All cross-pod requests must traverse designated **Liaison Nodes**, preventing network pollution and cross-domain hallucination cascades.
"""
    },
    {
        "id": "swarm-hop-limiter",
        "name": "swarm-hop-limiter",
        "title": "Swarm Gossip & Delegation Hop Limiter",
        "tier": "Level 2",
        "tierCode": "L2",
        "ring": "Ring 0 (Gossip Control)",
        "service": "Swarm Coordinator",
        "category": "Multi-Agent Swarm Suite",
        "description": "Enforces strict TTL and hop budgets (max 3 hops) on inter-agent task delegation to stop infinite loops.",
        "content": """---
name: swarm-hop-limiter
description: Enforces strict TTL and hop budgets (max 3 hops) on inter-agent task delegation to stop infinite loops.
version: 1.0.0
tier: Level 2 (Small-World Multi-Agent Network)
ring: Ring 0 (Gossip Protocol)
category: Swarm Coordination Suite
permissions:
  - swarm:EnforceHopLimit
tools:
  - decrement_hop_budget
  - drop_expired_messages
---

# swarm-hop-limiter: Delegation Guardrails

## 1. Hop Budget Rule
Every inter-agent message carries a `MaxHops = 3` header.
Upon receipt, the router decrements the counter:
- If `Hops == 0`: Packet dropped immediately; notification sent to consensus arbiter.
- Prevents infinite ping-pong delegation cascades across autonomous agents.
"""
    },
    {
        "id": "swarm-shared-whiteboard",
        "name": "swarm-shared-whiteboard",
        "title": "Swarm O(N) Shared Whiteboard Memory",
        "tier": "Level 2",
        "tierCode": "L2",
        "ring": "Ring 0 (Global Shared State)",
        "service": "Swarm Coordinator",
        "category": "Multi-Agent Swarm Suite",
        "description": "Append-only global state blackboard providing O(N) linear coordination without O(N²) peer-to-peer chat overhead.",
        "content": """---
name: swarm-shared-whiteboard
description: Append-only global state blackboard providing O(N) linear coordination without O(N²) peer-to-peer chat overhead.
version: 1.0.0
tier: Level 2 (Small-World Multi-Agent Network)
ring: Ring 0 (Shared State)
category: Swarm Coordination Suite
permissions:
  - swarm:WriteWhiteboard
  - swarm:SubscribeWhiteboard
tools:
  - post_blackboard_update
  - query_blackboard_state
---

# swarm-shared-whiteboard: The Blackboard Pattern

## 1. Complexity Comparison
- **Point-to-Point Mesh:** $N \\times (N-1) / 2 = O(N^2)$ message complexity. Unsustainable for $N > 10$.
- **Shared Whiteboard:** $O(N)$ linear updates. Agents read and write to partitioned topic lanes with immutable receipts.
"""
    },
    {
        "id": "swarm-consensus-arbiter",
        "name": "swarm-consensus-arbiter",
        "title": "Swarm Byzantine Quorum Consensus Arbiter",
        "tier": "Level 2",
        "tierCode": "L2",
        "ring": "Ring 0 (Consensus Engine)",
        "service": "Swarm Coordinator",
        "category": "Multi-Agent Swarm Suite",
        "description": "Byzantine fault-tolerant voting arbiter requiring 2/3+1 quorum for high-stakes actions.",
        "content": """---
name: swarm-consensus-arbiter
description: Byzantine fault-tolerant voting arbiter requiring 2/3+1 quorum for high-stakes actions.
version: 1.0.0
tier: Level 2 (Small-World Multi-Agent Network)
ring: Ring 0 (Consensus Engine)
category: Swarm Coordination Suite
permissions:
  - swarm:GatherQuorum
  - swarm:CommitConsensus
tools:
  - solicit_agent_votes
  - certify_byzantine_quorum
---

# swarm-consensus-arbiter: High-Stakes Quorum

## 1. Byzantine Fault Tolerance (BFT)
For actions exceeding a predetermined risk threshold (e.g. fund transfers, production schema migrations), a supermajority quorum is mandatory:
$$Q = \\left\\lfloor \\frac{2N}{3} \\right\\rfloor + 1$$
Independent agents cast cryptographic votes verified by SHA-256 signatures.
"""
    },
    {
        "id": "swarm-circuit-breaker",
        "name": "swarm-circuit-breaker",
        "title": "Swarm Distributed Cascading Circuit Breaker",
        "tier": "Level 2",
        "tierCode": "L2",
        "ring": "Ring 0 (Cascade Isolation)",
        "service": "Swarm Coordinator",
        "category": "Multi-Agent Swarm Suite",
        "description": "Network partitioner isolating malfunctioning or hallucinating agent nodes before systemic contamination occurs.",
        "content": """---
name: swarm-circuit-breaker
description: Network partitioner isolating malfunctioning or hallucinating agent nodes before systemic contamination occurs.
version: 1.0.0
tier: Level 2 (Small-World Multi-Agent Network)
ring: Ring 0 (Cascade Isolation)
category: Swarm Coordination Suite
permissions:
  - swarm:QuarantineNode
  - swarm:RestoreCluster
tools:
  - isolate_rogue_agent
  - trigger_network_partition
---

# swarm-circuit-breaker: Epidemic Cascade Prevention

## 1. Automated Quarantine
If an agent repeatedly fails grounding certification or generates rejected syscall proposals ($k \\ge 3$), `swarm-circuit-breaker` immediately revokes its lease tokens and severs its edges in the Watts-Strogatz graph.
"""
    }
]

print(f"Loaded {len(SKILLS_DATA)} skills across 3 Tiers.")

# Now read existing aws_basics_studio_app.html
with open('aws_basics_studio_app.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's inspect the tabs in html:
# We have:
# <button class="tab-btn" id="tabBtnRunbook" onclick="switchStage('runbook')">📜 Level 0 Skill Directives</button>
# Let's add:
# <button class="tab-btn" id="tabBtnSkills" onclick="switchStage('skills')">📚 SKILL.md Library (All 20 Skills)</button>

old_tab_buttons = '<button class="tab-btn" id="tabBtnRunbook" onclick="switchStage(\'runbook\')">📜 Level 0 Skill Directives</button>'
new_tab_buttons = '''<button class="tab-btn" id="tabBtnRunbook" onclick="switchStage('runbook')">📜 Level 0 Directives</button>
        <button class="tab-btn" id="tabBtnSkills" onclick="switchStage('skills')">📚 SKILL.md Library (All 20 Skills)</button>'''

if 'id="tabBtnSkills"' not in html:
    html = html.replace(old_tab_buttons, new_tab_buttons)

# Now add the stageSkills container after stageRunbook
skills_stage_html = '''
      <!-- TAB 6: COMPLETE SKILL.MD LIBRARY (ALL 20 SKILLS) -->
      <div class="stage-content" id="stageSkills" style="display: none;">
        <div style="background: var(--bg-panel); border: 1px solid var(--border-subtle); border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; height: 600px;">
          <!-- SKILL LIBRARY TOP TOOLBAR -->
          <div style="padding: 12px 16px; background: var(--bg-panel-subtle); border-bottom: 1px solid var(--border-subtle); display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px;">
            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
              <span style="font-weight: 800; font-size: 0.85rem; font-family: var(--font-display);">Filter Tier:</span>
              <button class="theme-toggle-btn active-skill-filter" id="filterAll" onclick="filterSkills('all')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">All (20)</button>
              <button class="theme-toggle-btn" id="filterL0" onclick="filterSkills('L0')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Level 0: AWS Basics (7)</button>
              <button class="theme-toggle-btn" id="filterL1" onclick="filterSkills('L1')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Level 1: Agent Kernel (7)</button>
              <button class="theme-toggle-btn" id="filterL2" onclick="filterSkills('L2')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Level 2: Swarm Network (6)</button>
            </div>
            <div style="display: flex; gap: 8px; align-items: center;">
              <input type="text" id="skillSearchInput" placeholder="🔍 Search skills..." oninput="searchSkills()" style="padding: 5px 10px; border-radius: 6px; border: 1px solid var(--border-subtle); background: var(--bg-panel); font-size: 0.75rem; color: var(--text-primary); width: 160px;">
              <button class="theme-toggle-btn" onclick="copyCurrentSkillMd()" title="Copy active SKILL.md to clipboard" style="padding: 5px 10px; font-size: 0.72rem;">📋 Copy SKILL.md</button>
              <button class="theme-toggle-btn" onclick="downloadCurrentSkillMd()" title="Download active SKILL.md" style="padding: 5px 10px; font-size: 0.72rem;">⬇️ Download</button>
              <button class="btn-action" onclick="downloadAllSkillsBundle()" style="padding: 5px 12px; font-size: 0.72rem;"><span>📦 Export All (JSON)</span></button>
            </div>
          </div>

          <!-- SKILL EXPLORER SPLIT VIEW -->
          <div style="display: flex; flex: 1; overflow: hidden;">
            <!-- LEFT LIST -->
            <div id="skillsListPane" style="width: 280px; border-right: 1px solid var(--border-subtle); overflow-y: auto; background: var(--bg-canvas); padding: 8px; display: flex; flex-direction: column; gap: 6px;">
              <!-- Rendered dynamically -->
            </div>

            <!-- RIGHT DETAIL VIEW -->
            <div style="flex: 1; display: flex; flex-direction: column; overflow: hidden; background: var(--bg-panel);">
              <div id="skillDetailHeader" style="padding: 10px 16px; border-bottom: 1px solid var(--border-subtle); background: var(--bg-panel-subtle); display: flex; justify-content: space-between; align-items: center;">
                <div>
                  <div id="skillHeaderTitle" style="font-weight: 800; font-size: 0.95rem; font-family: var(--font-display);">aws-bedrock/SKILL.md</div>
                  <div id="skillHeaderMeta" style="font-size: 0.72rem; color: var(--text-muted);">Level 0 &bull; Ring 3 &bull; Amazon Bedrock</div>
                </div>
                <div id="skillBadgeTier" class="badge-skill" style="font-size: 0.7rem;">LEVEL 0</div>
              </div>
              <div style="flex: 1; overflow-y: auto; padding: 14px;">
                <pre class="code-view" id="skillContentPre" style="margin: 0; min-height: 100%; font-size: 0.76rem; line-height: 1.45;"></pre>
              </div>
            </div>
          </div>
        </div>
      </div>
'''

if 'id="stageSkills"' not in html:
    # insert before </div> </main> (end of stage-pane)
    html = html.replace('<!-- TAB 5: RUNBOOK -->', skills_stage_html + '\n      <!-- TAB 5: RUNBOOK -->')

# Now add JavaScript for the Skills Library
js_skills_data = json.dumps(SKILLS_DATA, indent=2)

js_logic = f'''
    // ==========================================
    // EMBEDDED 3-TIER SKILL.MD LIBRARY (20 SKILLS)
    // ==========================================
    const SKILLS_LIBRARY = {js_skills_data};
    let currentSelectedSkillId = "aws-bedrock";
    let activeTierFilter = "all";

    function initSkillsLibrary() {{
      renderSkillsList();
      selectSkill(currentSelectedSkillId);
    }}

    function filterSkills(tier) {{
      activeTierFilter = tier;
      document.querySelectorAll('#stageSkills .theme-toggle-btn').forEach(b => {{
        if (b.id && b.id.startsWith('filter')) b.style.borderColor = 'var(--border-subtle)';
      }});
      const activeBtn = document.getElementById(tier === 'all' ? 'filterAll' : 'filter' + tier);
      if (activeBtn) activeBtn.style.borderColor = 'var(--aws-orange)';
      renderSkillsList();
    }}

    function searchSkills() {{
      renderSkillsList();
    }}

    function renderSkillsList() {{
      const pane = document.getElementById('skillsListPane');
      if (!pane) return;
      const query = (document.getElementById('skillSearchInput')?.value || '').toLowerCase();

      let filtered = SKILLS_LIBRARY.filter(s => {{
        const matchesTier = activeTierFilter === 'all' || s.tierCode === activeTierFilter;
        const matchesQuery = s.name.toLowerCase().includes(query) ||
                             s.title.toLowerCase().includes(query) ||
                             s.service.toLowerCase().includes(query) ||
                             s.description.toLowerCase().includes(query);
        return matchesTier && matchesQuery;
      }});

      if (filtered.length === 0) {{
        pane.innerHTML = '<div style="padding: 12px; font-size: 0.75rem; color: var(--text-muted); text-align: center;">No matching skills found.</div>';
        return;
      }}

      pane.innerHTML = filtered.map(s => {{
        const isSelected = s.id === currentSelectedSkillId;
        const bgStyle = isSelected ? 'background: #fff7ed; border-color: var(--aws-orange);' : 'background: var(--bg-panel); border-color: var(--border-subtle);';
        const tierColor = s.tierCode === 'L0' ? '#ea580c' : (s.tierCode === 'L1' ? '#2563eb' : '#7c3aed');
        return `
          <div onclick="selectSkill('${{s.id}}')" style="cursor: pointer; padding: 8px 10px; border-radius: 8px; border: 1.5px solid; ${{bgStyle}} display: flex; flex-direction: column; gap: 3px; transition: all 0.15s ease;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span style="font-family: var(--font-mono); font-weight: 700; font-size: 0.76rem; color: var(--text-primary);">${{s.name}}</span>
              <span style="font-size: 0.62rem; font-weight: 800; padding: 1px 5px; border-radius: 4px; background: ${{tierColor}}15; color: ${{tierColor}};">${{s.tierCode}}</span>
            </div>
            <div style="font-size: 0.68rem; color: var(--text-secondary); line-height: 1.25;">${{s.title}}</div>
            <div style="font-size: 0.62rem; color: var(--text-muted); font-family: var(--font-mono);">${{s.ring.split(' ')[0]}}</div>
          </div>
        `;
      }}).join('');
    }}

    function selectSkill(skillId) {{
      const skill = SKILLS_LIBRARY.find(s => s.id === skillId);
      if (!skill) return;
      currentSelectedSkillId = skillId;

      document.getElementById('skillHeaderTitle').textContent = `${{skill.name}}/SKILL.md`;
      document.getElementById('skillHeaderMeta').textContent = `${{skill.tier}} • ${{skill.ring}} • ${{skill.service}}`;
      document.getElementById('skillBadgeTier').textContent = skill.tier.toUpperCase();
      document.getElementById('skillContentPre').textContent = skill.content.trim();

      renderSkillsList();
    }}

    function copyCurrentSkillMd() {{
      const skill = SKILLS_LIBRARY.find(s => s.id === currentSelectedSkillId);
      if (!skill) return;
      navigator.clipboard.writeText(skill.content.trim()).then(() => {{
        showToast(`✅ Copied ${{skill.name}}/SKILL.md to clipboard!`);
      }});
    }}

    function downloadCurrentSkillMd() {{
      const skill = SKILLS_LIBRARY.find(s => s.id === currentSelectedSkillId);
      if (!skill) return;
      const blob = new Blob([skill.content.trim()], {{ type: 'text/markdown' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${{skill.name}}.SKILL.md`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast(`💾 Downloaded ${{skill.name}}.SKILL.md`);
    }}

    function downloadAllSkillsBundle() {{
      const bundle = {{
        title: "The 3-Tier Enterprise Agent Skills Bundle",
        count: SKILLS_LIBRARY.length,
        exportedAt: new Date().toISOString(),
        skills: SKILLS_LIBRARY
      }};
      const blob = new Blob([JSON.stringify(bundle, null, 2)], {{ type: 'application/json' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'three_tier_agent_skills_manifest.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast(`📦 Exported all 20 SKILL.md specifications in JSON manifest!`);
    }}
'''

# Update switchStage in html to handle 'skills'
if "if (tab === 'skills')" not in html:
    old_switch = "if (tab === 'runbook') document.getElementById('stageRunbook').style.display = 'block';"
    new_switch = """if (tab === 'runbook') document.getElementById('stageRunbook').style.display = 'block';
      if (tab === 'skills') {
        document.getElementById('stageSkills').style.display = 'block';
        if (typeof initSkillsLibrary === 'function') initSkillsLibrary();
      }"""
    html = html.replace(old_switch, new_switch)

# Also ensure active button class handles 'tabBtnSkills'
if "'tabBtnSkills'" not in html:
    old_tabs_reset = "['tabBtnArch', 'tabBtnLocks', 'tabBtnHfsm', 'tabBtnCode', 'tabBtnRunbook'].forEach(id => {"
    new_tabs_reset = "['tabBtnArch', 'tabBtnLocks', 'tabBtnHfsm', 'tabBtnCode', 'tabBtnRunbook', 'tabBtnSkills'].forEach(id => {"
    html = html.replace(old_tabs_reset, new_tabs_reset)

# Inject JS Logic before </script>
if "const SKILLS_LIBRARY" not in html:
    html = html.replace("window.onload = function() {", js_logic + "\n    window.onload = function() {")
    html = html.replace("selectPreset(0);", "selectPreset(0);\n      initSkillsLibrary();")

with open('aws_basics_studio_app.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated aws_basics_studio_app.html with all 20 SKILL.md specifications successfully!")
