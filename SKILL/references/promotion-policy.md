# Promotion Policy

## Core principle

Not every observed behavior should become a durable operating rule.

## Promotion ladder

### Stay in `evidence/`

Keep a candidate in `evidence/` when:

- it appears only once
- it conflicts with later corrections
- it depends on one narrow project context
- it contains sensitive details that are not yet sanitized
- the pattern is plausible but not yet stable

### Promote to `assets/`

Promote when at least one of these is true:

- the user stated the rule explicitly
- the same pattern appears repeatedly across independent contexts
- the user later reinforced the same rule by correction or acceptance

### Promote to `assets/corrections/`

Use `corrections/` for:

- explicit user reversals
- explicit "not this, use that instead"
- strong overrides that should outrank older inferences

## Conflict handling

When old and new evidence conflict:

1. do not overwrite silently
2. append a conflict record to `evidence/conflicts.jsonl`
3. prefer explicit correction over implicit inference
4. downgrade stale rules if needed
