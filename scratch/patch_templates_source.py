# -*- coding: utf-8 -*-
"""
Updates App 08 and App 09 to:
1. Use the EXACT same 3 examples as App 06 and App 07:
   - it_security: Enterprise IT SSO & Privilege Escalation Policy
   - fintech_dispute: FinTech Dispute Intake & AML Hold
   - cloud_devops: Cloud Canary Release & DB Lock Runbook
2. Render the EXACT same 3 domain-specific flowcharts as App 06 and App 07:
   - it_security: FIDO2 MFA Check -> Portal Dashboard -> Request Type -> Director Approval / 4h Lease / Break-Glass 2h Revoke
   - fintech_dispute: Dispute Ingest -> Risk Scoring -> Instant $150 Credit / SAR AML Freeze / Merchant Evidence -> Valid / Forfeit
   - cloud_devops: Deploy Canary -> 5% Traffic -> DDL Lock < 200ms? -> Abort Rollback / 15-min Error Rate -> Promote 100%
3. Ensure App 08 and App 09 dynamically switch flowcharts when each example is selected.
"""
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# The exact 3 DAGs from App 06
DAG_IT_SECURITY = """flowchart TD
  A["👤 Employee Login"] --> B{"🔑 Hardware MFA Check"}
  B -->|"FIDO2 Token OK"| C["📄 Portal Dashboard (/overview)"]
  B -->|"Token Missing"| D["⚠️ Register Hardware Token (/mfa-setup)"]
  C --> E{"Request Type"}
  E -->|"Standard Access"| F["✅ Auto-Approved (/status)"]
  E -->|"Production DB Root"| G["✍️ Director Approval Gate (/privilege-escalation)"]
  G -->|"Approved"| H["🟢 4-Hour Temporary Lease"]
  G -->|"Denied"| I["❌ Access Denied"]
  E -->|"Break-Glass"| J["🚨 Emergency Break-Glass Form (/break-glass)"]
  J --> K["🔒 2-Hour Auto-Revoke + SOC2 Alert"]
  style B fill:#e0f2fe,stroke:#0284c7,stroke-width:2px
  style G fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
  style K fill:#fee2e2,stroke:#ef4444,stroke-width:2px"""

DAG_FINTECH_DISPUTE = """flowchart TD
  A["📥 Dispute Ingest (/disputes)"] --> B{"Risk Scoring"}
  B -->|"< $150 & Low Risk"| C["⚡ Instant Tier 1 Credit (/tier1-refund)"]
  B -->|"Velocity Flag > $5k"| D["🚨 SAR / AML Freeze Gate (/aml-hold)"]
  B -->|"Standard Dispute"| E["📄 Merchant Evidence Intake (/merchant-evidence)"]
  E --> F{"Merchant Proof"}
  F -->|"Valid Delivery"| G["❌ Chargeback Denied"]
  F -->|"No Delivery in 5 Days"| H["✅ Merchant Forfeits / Refunded"]
  style C fill:#d1fae5,stroke:#10b981,stroke-width:2px
  style D fill:#fee2e2,stroke:#ef4444,stroke-width:2px"""

DAG_CLOUD_DEVOPS = """flowchart TD
  A["🚀 Deploy Canary (/release-console)"] --> B["⚖️ Route 5% Traffic (/canary-traffic)"]
  B --> C{"DDL Table Lock < 200ms?"}
  C -->|"Lock Timeout Exceeded"| D["🚨 Abort Migration & Rollback (/rollback-trigger)"]
  C -->|"Safe Lock"| E{"15-Min Error Rate"}
  E -->|"5xx > 0.05%"| D
  E -->|"Healthy"| F["🟢 Promote to 100% Production"]
  style D fill:#fee2e2,stroke:#ef4444,stroke-width:2px
  style F fill:#d1fae5,stroke:#10b981,stroke-width:2px"""

# The exact 3 templates with cascade tiers
TEMPLATES_JS = f"""    const TEMPLATES = {{
      it_security: {{
        key: 'it_security',
        title: 'SEC-POL-402_Rev4: Enterprise IT SSO & Privilege Escalation Policy',
        url: 'https://internal.corp.local/overview',
        text: `§ 1.0 Multi-Factor Authentication (MFA) Mandate: All engineers, contractor personnel, and automated system accounts accessing production VPCs, Kubernetes clusters, and database enclaves must authenticate using physical, hardware-backed FIDO2 WebAuthn cryptographic keys (e.g. YubiKey 5 Series). Legacy SMS OTP and voice-call telephone verifications are STRICTLY PROHIBITED.
§ 2.0 Elevated Database Write Leases & Authorization Ceilings: Direct write access to customer relational databases (PostgreSQL/Aurora) requires an active JIRA Change Reference ticket and mandatory sign-off from an L2 Engineering Director or VP. Elevated access leases are strictly ephemeral: TTL SHALL NOT EXCEED 4 HOURS (240 minutes).
§ 3.0 Emergency Break-Glass Exception Protocol: In the extraordinary circumstance of an active Sev-1 / P0 outage where designated approvers are unreachable, an on-call SRE may trigger the automated Emergency Break-Glass procedure. Break-Glass tokens are hard-capped at 2 HOURS (7,200 SECONDS). A non-dismissible audit event is dispatched instantly to SIRT.`,
        dagMermaid: `{DAG_IT_SECURITY}`,
        cascadeTiers: [
          {{
            tier: 'Tier 0: Root Invariant',
            desc: 'Constitutional Identity & Authentication Gate',
            badge: 'root-invariant',
            rules: [
              'RULE_ROOT_MFA: Hardware FIDO2 WebAuthn cryptographic challenge required across all internal systems without exception.',
              'STRICT NEGATION: Legacy SMS OTP and voice telephone MFA are STRICTLY PROHIBITED.'
            ]
          }},
          {{
            tier: 'Tier 1: Scoped Directive',
            desc: 'Privileged Infrastructure Access Boundaries',
            badge: 'directive',
            rules: [
              'DIRECTIVE (https://internal.corp.local/overview): Standard employee SSO grants read-only staging access.',
              'DIRECTIVE: Any elevated write or production access requires passing the L2 Director Gate.'
            ]
          }},
          {{
            tier: 'Tier 2: Execution Rules',
            desc: 'L2 Director Dual-Key Approval Gate',
            badge: 'execution',
            rules: [
              'RULE: Production database lease requests must submit a valid JIRA ticket number (INFRA-XXXX).',
              'RULE: Must obtain cryptographic co-signature from an active Engineering Director or VP.'
            ]
          }},
          {{
            tier: 'Tier 3: Parameter Bounds',
            desc: 'Time-Bound Lease Constraint (Max 4 Hours)',
            badge: 'param-bound',
            rules: [
              'BOUND: Lease expiration timestamp is hard-capped at now() + 4 HOURS (240 minutes).',
              'BOUND: Break-Glass tokens are hard-capped at exactly 2 HOURS (7,200 seconds).'
            ]
          }},
          {{
            tier: 'Tier 4: Dead Ends & Aborts',
            desc: 'Emergency Revocation & Audit Tripwires',
            badge: 'dead-end',
            rules: [
              'DEAD END: If Break-Glass token expires -> Instant session termination and alert SIRT.',
              'DEAD END: If SMS OTP attempted -> Immediate account lock.'
            ]
          }}
        ]
      }},
      fintech_dispute: {{
        key: 'fintech_dispute',
        title: 'POL-OPS-AML-2026-015: FinTech Dispute Intake & AML Hold',
        url: 'https://internal.corp.local/disputes',
        text: `§ 1.0 Tier-1 Instant Provisional Refund Guidelines: Cardholder disputes for unauthorized transactions with an aggregate claim amount EQUAL TO OR LESS THAN $150.00 and a machine risk score under 25 may be provisionally credited within 60 seconds without supervisor override.
§ 2.0 AML Velocity & SAR Filing Mandatory Freeze: Automated rule processors detecting transaction velocities exceeding $5,000.00 within a 24-hour window on newly provisioned cards MUST IMMEDIATELY PLACE A 72-HOUR RESTRICTIVE HOLD. Under Federal Non-Tipping Invariants (31 U.S.C. § 5318(g)), agents and customer support are STRICTLY PROHIBITED from disclosing SAR investigations.
§ 3.0 Merchant Evidence Rebuttal Protocol: Merchants have strictly 5 business days to submit signed carrier proof of delivery. Failure to supply valid carrier tracking results in automatic merchant forfeiture.`,
        dagMermaid: `{DAG_FINTECH_DISPUTE}`,
        cascadeTiers: [
          {{
            tier: 'Tier 0: Root Invariant',
            desc: 'Federal AML Compliance & Non-Tipping Invariant',
            badge: 'root-invariant',
            rules: [
              'RULE_ROOT_AML: Agents are strictly prohibited under federal regulations from disclosing SAR filings to customers.',
              'STRICT NEGATION: Tipping off a customer regarding a 72-hour AML hold is STRICTLY PROHIBITED.'
            ]
          }},
          {{
            tier: 'Tier 1: Scoped Directive',
            desc: 'Dispute Classification & Threshold Routing',
            badge: 'directive',
            rules: [
              'DIRECTIVE (https://internal.corp.local/disputes): Disputes under $150 route to instant automated reversal.',
              'DIRECTIVE: Disputes over $5,000 cross-check FinCEN anti-money laundering velocity thresholds.'
            ]
          }},
          {{
            tier: 'Tier 2: Execution Rules',
            desc: 'Tier 1 Automated Credit Reversal Gate',
            badge: 'execution',
            rules: [
              'RULE: Disputes meeting the $150 threshold and low risk score (< 25) disburse provisional credits within 60s.',
              'RULE: Complex disputes require signed merchant delivery rebuttals within 5 business days.'
            ]
          }},
          {{
            tier: 'Tier 3: Parameter Bounds',
            desc: 'Mandatory 72-Hour AML Compliance Hold',
            badge: 'param-bound',
            rules: [
              'BOUND: Instant credit ceiling: EQUAL TO OR LESS THAN $150.00.',
              'BOUND: High-velocity transactions are held for exactly 72 HOURS without exception.'
            ]
          }},
          {{
            tier: 'Tier 4: Dead Ends & Aborts',
            desc: 'Forfeiture & Suspicious Activity Tripwires',
            badge: 'dead-end',
            rules: [
              'DEAD END: If merchant fails to supply tracking proof in 5 days -> Automatic forfeiture.',
              'DEAD END: If transaction velocity > $5,000 -> Immediate 72-hour freeze.'
            ]
          }}
        ]
      }},
      cloud_devops: {{
        key: 'cloud_devops',
        title: 'SRE-RUN-DB-MIG-2026: Cloud Canary Release & DB Lock Runbook',
        url: 'https://internal.corp.local/release-console',
        text: `§ 1.0 Production Canary Deployment Gate: New microservice artifact builds MUST FIRST route strictly 5% of live production traffic to isolated canary container pods. Canary evaluation duration MUST NOT BE LESS THAN 15 MINUTES (900 seconds) prior to promotion.
§ 2.0 Database Schema Lock Mitigation: DDL migrations (ALTER TABLE, CREATE INDEX) executing against primary transactional relational tables MUST ACQUIRE EXCLUSIVE METADATA LOCKS IN LESS THAN 200 MILLISECONDS. If lock acquisition exceeds 200ms, the migration script MUST IMMEDIATELY ABORT and yield lock queues.
§ 3.0 Automated SRE Rollback Tripwires: If Canary 5xx HTTP error rates exceed 0.05% or P99 request latency degrades by > 20%, automated deployment orchestrators MUST TRIGGER AN INSTANT ROLLBACK to previous stable image tags.`,
        dagMermaid: `{DAG_CLOUD_DEVOPS}`,
        cascadeTiers: [
          {{
            tier: 'Tier 0: Root Invariant',
            desc: 'Production Availability & Error Budget Invariant',
            badge: 'root-invariant',
            rules: [
              'RULE_ROOT_AVAILABILITY: Production service SLA requires 99.99% uptime.',
              'STRICT NEGATION: Automated rollbacks supersede manual operator decisions whenever error budgets drain.'
            ]
          }},
          {{
            tier: 'Tier 1: Scoped Directive',
            desc: 'Canary Progressive Rollout Protocol',
            badge: 'directive',
            rules: [
              'DIRECTIVE (https://internal.corp.local/release-console): Releases must proceed in staged gates: 5% Canary ➔ 100% Production.',
              'DIRECTIVE: Traffic must remain clamped at 5% for not less than 15 minutes.'
            ]
          }},
          {{
            tier: 'Tier 2: Execution Rules',
            desc: '15-Minute Minimum Observation Interval',
            badge: 'execution',
            rules: [
              'RULE: Monitor HTTP 5xx error rate and p99 response times throughout the 15-minute soak.',
              'RULE: DDL migration must acquire locks safely or abort immediately.'
            ]
          }},
          {{
            tier: 'Tier 3: Parameter Bounds',
            desc: 'Database DDL Table Lock Abort (200ms Max)',
            badge: 'param-bound',
            rules: [
              'BOUND: Any database migration holding an exclusive table lock longer than 200ms is terminated.',
              'BOUND: Canary traffic proportion: Strictly 5% (15-minute minimum soak).'
            ]
          }},
          {{
            tier: 'Tier 4: Dead Ends & Aborts',
            desc: 'Automated Instant Rollback Tripwire',
            badge: 'dead-end',
            rules: [
              'DEAD END: If 5xx error rate > 0.05% -> Automated instantaneous rollback to previous stable tag.',
              'DEAD END: If DDL metadata lock wait > 200ms -> Abort migration and release lock queue.'
            ]
          }}
        ]
      }}
    }};"""

print("TEMPLATES_JS defined.")
