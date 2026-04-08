# Person Graph SOP

## Goal

Build and maintain an owner-centric graph that helps agents understand:

- who the owner is in work
- what the owner prefers
- how the owner usually behaves
- what the owner values or rejects
- how the owner wants future collaboration to feel

The output is not a transcript replay.
It is a structured operating model of the owner.

## Shared pipeline

### 1. Source triage

Select high-signal sources first:

- explicit user self-description
- explicit corrections
- repeated choices across tasks
- long-running project and decision history
- durable docs written or approved by the owner

Optimize for owner signal density, not transcript coverage.

### 2. Evidence slicing

Split raw material into minimal evidence units.

Each evidence unit should ideally support one claim candidate.

Do not dump whole sessions into the graph.

### 3. Candidate claim extraction

For each evidence unit, ask:

1. what does this reveal about the owner?
2. is it `role`, `interest`, `preference`, `behavior`, `workflow`, `principle`, `constraint`, `knowledge`, or `taste`?
3. is it explicit or inferred?
4. is it global or scoped?
5. would this change how a future agent should work?

### 4. Normalization

Normalize evidence into reusable claims.

Example:

- raw: `Do not give me a long preface. Just tell me what to do.`
- normalized:
  - `owner --prefers--> concise_actionable_output`
  - `owner --avoids--> long_prefatory_explanations`

### 5. Scoring

Score each claim with `references/claim-scoring-policy.md`.

### 6. Scope assignment

Assign one of:

- `global`
- `domain:*`
- `project:*`
- `task_family:*`

### 7. Conflict review

Check whether new material:

- supports an existing claim
- narrows an existing claim
- overrides an existing claim
- truly conflicts with an existing claim

Different scopes are often the right answer.

### 8. Promotion

Route by stability:

- weak -> evidence only
- candidate -> keep in evidence and wait
- stable -> promote to stable claim and optionally to assets

### 9. Apply packet compilation

From the stable graph slice, compile a concise alignment packet for live use.

## Init mode

Use `init` when no usable graph exists yet.

Required behavior:

- build from the highest-signal local sources first
- prefer conservative extraction
- avoid overfitting one-off phrasing
- create an initial stable claim set plus evidence ledger

Expected outputs:

- initial claim ledger
- initial conflict ledger if needed
- initial graph projection
- initial alignment packet

## Refresh mode

Use `refresh` when a graph already exists.

Required behavior:

- read the current stable claims first
- process only new high-signal material
- merge instead of duplicating
- narrow scope or create overrides when newer evidence changes older assumptions

Expected outputs:

- merged claims
- updated evidence links
- updated graph projection
- updated alignment packet

## Apply mode

Use `apply` to actively work in the owner's style.

Required behavior:

1. type the current task
2. retrieve only the relevant graph slice
3. retrieve only the relevant assets
4. compile or read the alignment packet
5. let it shape tone, reasoning, workflow, output, and correction handling

Do not roleplay.
Do not exaggerate.
Do align to the owner's stable working personality.

## Anti-patterns

Do not:

- build a raw message-flow graph and call it a person graph
- create deep personality labels from weak evidence
- mistake temporary urgency for a stable trait
- promote a scoped preference as a global identity rule
- let graph alignment override accuracy, safety, or the owner's latest explicit instruction
