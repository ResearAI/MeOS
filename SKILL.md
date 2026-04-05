---
name: meos
description: Read the owner's local history and profile assets, extract stable workflows and preferences, and keep those assets updated for future tasks. Use when explicitly asked to initialize, refresh, or apply MeOS.
license: MIT
---

# MeOS

MeOS is a local-first operating-layer skill.

It is not a chat memory dump.
It is not literal roleplay.
It is not a one-shot profile summary.

It exists to keep the owner's long-lived working assets readable, editable, and reusable.

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

## Repository layout

- `references/`
  - operating manuals for extraction, promotion, privacy, and writeback
- `schemas/`
  - JSON schemas for durable entries
- `assets/`
  - stable, reusable owner assets
- `evidence/`
  - raw promoted facts, conflict records, and source maps
- `runtime/`
  - local run state
- `private/`
  - imported raw history and local-only material

## Reading order

### For `init`

1. Read `references/source-locations.md`
2. Read `references/extraction-sop.md`
3. Read `references/promotion-policy.md`
4. Read `references/privacy-policy.md`
5. Read `references/writeback-policy.md`

### For `refresh`

1. Read `references/source-locations.md`
2. Read `references/extraction-sop.md`
3. Read `references/promotion-policy.md`
4. Read `references/correction-policy.md`
5. Read `references/writeback-policy.md`

### For `apply`

1. Read only the minimum relevant files under `assets/`
2. Read `references/writeback-policy.md` before writing back any new durable update
3. Read `docs/en/10_APPLYING_MEOS.md` or `docs/zh/10_APPLYING_MEOS.md` when you need the task-to-asset mapping

## Promotion rule

Use this promotion ladder:

- weak or one-off evidence -> `evidence/`
- repeated or explicit stable rule -> `assets/`
- direct user correction -> `assets/corrections/`

Never skip `evidence/` when uncertainty is real.

## Write-back rule

When stable new information appears:

- update the appropriate file under `assets/`
- append a matching source record under `evidence/`
- if a conflict exists, append it to `evidence/conflicts.jsonl`
- if the new information is a correction, prefer updating `assets/corrections/overrides.md`

## Apply behavior

When MeOS is used during a real task, do not load the whole asset tree by default.

Instead:

1. identify the task type
2. read only the relevant live assets
3. let those assets shape:
   - reasoning
   - workflow
   - output
   - correction handling
4. only write back stable new information

## Expected outputs

Good MeOS work usually leaves behind:

- one or more updated asset files
- one or more evidence records
- conflict records when needed
- no private-secret leakage into reusable assets

MeOS should make the owner more reusable, not more exposed.
