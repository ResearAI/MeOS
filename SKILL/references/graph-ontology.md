# Graph Ontology

## Goal

Define the owner-centric graph model used by MeOS.

The graph is not a raw conversation graph.
It is a structured model of the owner as a working individual.

## Core modeling rule

The center of the graph is `owner`, not `session`, `turn`, or `prompt`.

Sessions, documents, tasks, and artifacts are evidence and context layers.
They support person-level claims instead of replacing them.

## Layers

### 1. Person layer

Stable traits that matter for future collaboration:

- `owner`
- `role`
- `interest`
- `preference`
- `behavior`
- `workflow`
- `principle`
- `constraint`
- `knowledge`
- `taste`

### 2. Context layer

Where a claim applies:

- `domain`
- `project`
- `task_family`
- `tool`
- `artifact_type`
- `time_period`

### 3. Evidence layer

Why a claim exists:

- `session`
- `turn_excerpt`
- `document`
- `decision_note`
- `artifact_snapshot`
- `correction_record`

## Canonical claim dimensions

Use one primary dimension per claim:

- `role`
  - how the owner stably identifies in work
- `interest`
  - themes the owner repeatedly returns to
- `preference`
  - how the owner prefers to be served or responded to
- `behavior`
  - repeated actions or habits visible in real work
- `workflow`
  - repeatable task sequences or routines
- `principle`
  - stable judgment rules or trade-off boundaries
- `constraint`
  - explicit dislikes, refusals, or hard limits
- `knowledge`
  - stable domain understanding or reusable experience
- `taste`
  - stable presentation, UI, or expression preferences

## Canonical predicates

Prefer normalized predicates such as:

- `prefers`
- `avoids`
- `values`
- `tends_to`
- `uses_workflow`
- `interested_in`
- `identifies_as`
- `knows`
- `likes`
- `overrides`
- `conflicts_with`
- `supported_by`

Do not store raw sentence fragments as predicates.

## Scope model

Every non-trivial claim must be scoped.

Supported scope levels:

- `global`
- `domain:*`
- `project:*`
- `task_family:*`

Different scopes are not automatically conflicts.

Example:

- `owner --prefers--> concise_actionable_output` scoped to `task_family:coding`
- `owner --prefers--> detailed_audit_findings` scoped to `task_family:review`

These can both be true.

## Claim-first modeling rule

The graph should be grounded in structured claims.

Recommended normalized shape:

```json
{
  "id": "claim_xxx",
  "subject": "owner",
  "dimension": "preference",
  "predicate": "prefers",
  "object": "concise_actionable_output",
  "scope": "task_family:coding",
  "explicitness": "explicit",
  "stability": "stable",
  "confidence": 0.9,
  "evidence_ids": ["ev_12"]
}
```

Human-facing graph views may project this into a simpler edge:

- `owner --prefers--> concise_actionable_output`

## Asset relation

Assets and graph claims are related but not identical.

- `assets/` holds human-readable durable prose
- `evidence/` holds the claim ledger and proof chain
- `runtime/graph/` holds local graph projections and alignment packets

Use the graph as a structural index, not as a replacement for curated assets.

## Anti-patterns

Do not:

- model the whole chat transcript as the graph itself
- invent psychological labels with weak evidence
- flatten all scoped traits into one global persona
- let one dramatic message outweigh repeated behavior
- treat inferred claims as stronger than explicit user corrections
