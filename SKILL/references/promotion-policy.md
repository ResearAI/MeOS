# Promotion Policy

## Core principle

Not every observed behavior should become a durable operating rule.
Not every observed behavior should become a stable person-level claim either.

## Promotion ladder

### Stay in `evidence/`

Keep a candidate in `evidence/` when:

- it appears only once
- it conflicts with later corrections
- it depends on one narrow project context
- it contains sensitive details that are not yet sanitized
- the pattern is plausible but not yet stable
- it sounds like a psychological label rather than a collaboration-relevant rule

### Promote to a stable claim

Promote to a stable person-graph claim when at least one of these is true:

- the user stated the rule or preference explicitly
- the user issued a strong correction or reversal
- the same pattern appears repeatedly across time
- the same pattern appears across independent contexts
- the pattern would materially change future agent behavior

Scope-limited claims may still be promoted if the scope is explicit.

### Promote to `assets/`

Promote when at least one of these is true:

- the user stated the rule explicitly
- the same pattern appears repeatedly across independent contexts
- the user later reinforced the same rule by correction or acceptance
- the claim is stable and benefits from a human-readable prose form

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
5. prefer narrower scoped truths over false global summaries
