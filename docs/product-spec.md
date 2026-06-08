# Delphi Product Spec

## Summary

Delphi is a Kubernetes-native internal platform for data observability and trust. It helps engineers, data stewards, and stakeholders define data contracts, evaluate datasets against those contracts, track violations, and understand dataset health through both an operational UI and grounded natural language queries.

The proof of concept focuses on PostgreSQL-backed datasets and operational metadata managed inside Delphi itself.

## Problem

Teams need a trustworthy way to answer:

- Is this dataset healthy right now?
- What are the current contract expectations?
- What changed in the contract over time?
- Which issues are still unresolved?
- Which datasets are behind on freshness or failing core validation checks?

Today, that information often lives across runbooks, SQL queries, dashboards, and tribal knowledge. Delphi centralizes it into one platform.

## Goals

- Provide a durable contract model with meaningful version history.
- Support API-triggered evaluations from the UI.
- Detect violations for freshness, row count, and custom SQL rules.
- Keep a single open violation per failing rule until it is resolved.
- Give users an operational dashboard optimized for dense workflows.
- Support natural language Q&A over Delphi metadata with evidence.

## Non-Goals

- Enterprise authentication and RBAC
- Automated remediation or downstream actions
- Multi-tenant or multi-cluster deployment complexity
- Broad warehouse support beyond PostgreSQL in the first POC
- Freeform LLM access to raw source data

## Users

### Data Platform Engineers

Need to define rules, trigger evaluations, and inspect failures quickly.

### Data Stewards

Need contract visibility, change history, and issue lifecycle tracking.

### Stakeholders

Need a trustworthy high-level view of dataset health and SLA posture.

## Product Principles

- Operational density over presentation polish
- Evidence attached to every system answer
- Current state and historical context visible together
- Versioning only when rule or SLA semantics change
- Platform metadata remains the system of record

## Dataset Model

Datasets are identified by `database.schema.table`.

Each dataset contains:

- identity fields
- owner metadata
- descriptive metadata
- current health summary

The POC stays lean and does not introduce team or domain models yet.

## Contract Model

Contracts are managed in the UI and stored as application state.

Each contract:

- belongs to one dataset
- contains one or more rules
- supports severity per rule
- includes SLA expectations
- requires a change reason when versioned

Contract versions are created only when SLA or rule definitions change.

## Rule Types

### Freshness

Freshness is configurable per rule. It may evaluate:

- a dataset timestamp column
- a source metadata timestamp
- another configured freshness expression later

### Row Count

The POC supports:

- minimum and maximum thresholds
- expected range
- comparison to prior run

### Custom SQL

Users author raw SQL in a text box.

The SQL must resolve to a pass/fail outcome through a standard pattern, such as an aggregate with a `HAVING` clause or another boolean-compatible query result. Delphi stores the SQL text and evaluation result metadata.

## Evaluation Model

Evaluations are triggered through an API and may be initiated from the UI. Scheduled execution can be layered on later using the same API.

An evaluation:

- targets a dataset and current contract version
- runs all active rules in the contract
- records per-rule results
- writes a dataset-level summary
- opens or updates violations based on failures

## Violation Model

Violations are persistent operational records.

Workflow:

- `open`
- `acknowledged`
- `resolved`

Behavior:

- one open violation per rule per dataset/contract context
- repeated failures update the existing open violation
- resolution requires explicit user action

Violations also store:

- severity
- timestamps
- resolution notes
- supporting evaluation references

## Natural Language Experience

The natural language interface answers operational questions over Delphi metadata only.

Examples:

- Which datasets are unhealthy right now?
- Which datasets have critical open violations?
- Show datasets behind schedule.
- What changed in the latest contract version for `database.schema.table`?

Every answer must include evidence, such as matching datasets, evaluations, violations, or contract versions.

## UX Requirements

### Overview Dashboard

Top priorities:

- healthy versus unhealthy dataset counts
- open violations by severity and status
- dense scan-friendly dataset inventory

### Dataset Detail

Essential tabs:

- Overview
- Current Contract
- Contract History
- Evaluations
- Violations
- Ask Delphi

Each dataset page should include both current operational state and drill-down access to full history.

## Functional Requirements

### FR-1 Dataset Registration

Users can register a PostgreSQL dataset using its `database.schema.table` identity.

### FR-2 Contract Authoring

Users can create and edit contracts in the UI with:

- SLA fields
- freshness rules
- row count rules
- custom SQL rules
- severity per rule

### FR-3 Contract Versioning

The system creates a new contract version only when rules or SLA fields change and requires a change reason.

### FR-4 Evaluation Execution

Users can trigger an evaluation through the API or UI.

### FR-5 Rule Result Persistence

The system stores full evaluation history with dataset summary and per-rule drill-down.

### FR-6 Violation Lifecycle

The system opens, acknowledges, and resolves violations while preserving history.

### FR-7 Single Open Violation Rule

The system maintains one open violation per failing rule until resolved.

### FR-8 Dashboard Visibility

Users can view aggregate health and dataset-level operational detail.

### FR-9 Natural Language Querying

Users can submit operational questions and receive grounded answers with evidence.

## Non-Functional Requirements

- Kubernetes deployable
- PostgreSQL-backed metadata persistence
- Structured logs and metrics
- API-first service design
- Extensible rule model for future checks and actions

## Success Criteria

The POC succeeds when a user can:

1. register a dataset
2. define a contract with multiple rule types
3. update the contract and see version history
4. trigger an evaluation
5. inspect pass/fail results and evidence
6. review an open violation
7. acknowledge and resolve that violation
8. ask an operational question in natural language and see evidence-backed results

## Release Shape

The first release should feel like an internal platform tool:

- practical
- dense
- trustworthy
- explainable

It does not need enterprise surface area yet, but it does need strong information architecture and clean operator workflows.
