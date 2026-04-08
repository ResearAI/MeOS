---
name: meos
description: Read the owner's local history, assets, and person-graph evidence; extract stable workflows, preferences, and personality-level claims; keep them updated; and align future tasks to the owner's style. Use when explicitly asked to initialize, refresh, or apply MeOS.
license: MIT
---

# MeOS

MeOS is a local-first operating-layer skill.

It is not a chat memory dump.
It is not literal roleplay.
It is not a one-shot profile summary.

It exists to keep the owner's long-lived working assets and person-level operating traits readable, editable, and reusable.

## Modes

- `init`
- `refresh`
- `apply`

### `init`

Use when MeOS has not been built yet and the agent must create the first durable asset set from local history sources.

### `refresh`

Use when new history or new corrections exist and the agent must update existing assets without duplicating or overwriting them blindly.

### `apply`

Use when the current task should be executed with MeOS calibration and only stable new information should be written back.

`apply` is the most important mode in real usage.
It is what makes MeOS useful in later tasks instead of becoming an archive-only system.

## Hard rules

1. Do not treat one-off behavior as a stable rule.
2. Prefer explicit user statements over inferred patterns.
3. Prefer correction signals over older assumptions.
4. Do not promote a fact into `assets/` unless its evidence is strong enough.
5. Keep private raw material out of git by default.
6. Do not store secrets, tokens, or unnecessary personal identifiers in reusable assets.
7. If evidence is weak or conflicting, store it in `evidence/` instead of pretending certainty.
8. Align to the owner's stable working personality, but do not invent a theatrical persona or psychologize beyond the evidence.

## Repository layout

- `references/`
  - operating manuals for extraction, promotion, privacy, and writeback
- `schemas/`
  - JSON schemas for durable entries
- `assets/`
  - stable, reusable owner assets
- `evidence/`
  - raw promoted facts, claim records, conflict records, and source maps
- `runtime/`
  - local run state, graph outputs, and alignment packets
- `private/`
  - imported raw history and local-only material

## Reading order

### For `init`

1. Read `references/source-locations.md`
2. Read `references/extraction-sop.md`
3. Read `references/graph-ontology.md`
4. Read `references/claim-scoring-policy.md`
5. Read `references/promotion-policy.md`
6. Read `references/privacy-policy.md`
7. Read `references/writeback-policy.md`

### For `refresh`

1. Read `references/source-locations.md`
2. Read `references/extraction-sop.md`
3. Read `references/graph-ontology.md`
4. Read `references/claim-scoring-policy.md`
5. Read `references/promotion-policy.md`
6. Read `references/correction-policy.md`
7. Read `references/writeback-policy.md`

### For `apply`

1. Read `runtime/graph/alignment-packet.json` first when it exists
2. Read only the minimum relevant files under `assets/`
3. Read `references/style-alignment-policy.md`
4. Read `references/apply-task-map.md` when you need the task-to-asset and task-to-graph mapping
5. Read `references/writeback-policy.md` before writing back any new durable update

## Promotion rule

Use this promotion ladder:

- weak or one-off evidence -> `evidence/`
- repeated or explicit stable rule -> stable claim plus `assets/` when prose representation is useful
- direct user correction -> `assets/corrections/` plus override claim

Never skip `evidence/` when uncertainty is real.

## Write-back rule

When stable new information appears:

- normalize it into a structured claim
- update the appropriate file under `assets/` when a human-readable durable rule is useful
- append a matching source record under `evidence/`
- append or merge a matching claim record under `evidence/claims.jsonl`
- if a conflict exists, append it to `evidence/conflicts.jsonl`
- if the new information is a correction, prefer updating `assets/corrections/overrides.md`
- if local graph generation is enabled, update `runtime/graph/` outputs and the alignment packet

When graph outputs are generated or refreshed:

- write `runtime/graph/owner-graph.json`
- write `runtime/graph/alignment-packet.json`
- write `runtime/graph/owner-graph.html`
- tell the user the exact local preview command and URL, defaulting to `meos graph serve --host 127.0.0.1 --port 20998`

## Apply behavior

When MeOS is used during a real task, do not load the whole asset tree by default.
Do not load the whole person graph by default either.

Instead:

1. identify the task type
2. retrieve only the relevant graph slice and live assets
3. let those materials shape:
   - reasoning
   - workflow
   - output
   - tone
   - correction handling
4. only write back stable new information

## Expected outputs

Good MeOS work usually leaves behind:

- one or more updated asset files
- one or more evidence records
- one or more claim records when person-level traits were updated
- an updated alignment packet or graph slice when local graph generation is enabled
- a rendered graph preview when local graph generation is enabled
- conflict records when needed
- no private-secret leakage into reusable assets

MeOS should make the owner more reusable, not more exposed.
