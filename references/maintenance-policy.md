# Maintenance Policy

## Goal

Keep MeOS evolving without turning it into a pile of duplicated prompts.

## Maintenance actions

- `add`
- `merge`
- `downgrade`
- `discard`

## Action rules

### `add`

Use when:

- a truly new stable capability or rule appears
- it does not overlap strongly with an existing asset

### `merge`

Use when:

- new evidence strengthens or refines an existing asset
- creating a second asset would cause duplication

### `downgrade`

Use when:

- a formerly strong rule becomes uncertain
- a newer correction weakens confidence

Downgraded content should move back toward `evidence/` or be clearly marked as lower-confidence.

### `discard`

Use when:

- the content was one-off noise
- the content was superseded by correction
- the content is too private or too context-specific to remain reusable

## Versioning rule

MeOS assets should evolve as maintained files, not as a growing pile of similar prompts.

Preferred behavior:

- revise the existing asset
- preserve important evidence
- append conflict history when needed
- update timestamps and confidence
