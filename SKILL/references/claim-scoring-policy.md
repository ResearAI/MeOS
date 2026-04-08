# Claim Scoring Policy

## Goal

Score person-level claims conservatively so MeOS promotes stable traits instead of noisy impressions.

## Scoring dimensions

### Explicitness

- explicit self-statement: `+3`
- explicit correction or override: `+3`
- repeated behavior with no explicit wording: `+1`
- assistant-only speculation: `0`

### Repetition

- seen across 3 or more independent moments: `+3`
- seen across 2 moments: `+2`
- single moment only: `0`

### Cross-context support

- appears across different projects, domains, or task families: `+2`
- appears across different tasks within one context: `+1`
- one narrow context only: `0`

### Recency

- still reinforced by recent material: `+1`
- not recently observed: `0`

### Scope clarity

- scope is explicit and coherent: `+1`
- scope is unclear: `0`

### Penalties

- unresolved conflicting evidence: `-2`
- sensitive or unsanitized detail still embedded in the claim: `-1`
- over-interpreted psychological label: `-2`

## Promotion thresholds

- `<= 2`
  - evidence only
- `3 - 5`
  - candidate claim
- `>= 6`
  - stable claim

## Special rule for corrections

Explicit user corrections have the highest priority.

If a correction is:

- clearly phrased
- collaboration-relevant
- safe to store

it may be promoted immediately as a stable override claim even before repetition.

## Scope rule

Scope-limited claims can still be stable.

Do not penalize a claim merely because it is scoped to:

- one domain
- one project
- one task family

Penalize only when the scope is unclear or misleading.

## Prohibited shortcuts

Do not promote a claim because:

- it sounds plausible
- it feels stylistically true
- the owner used emotional wording once
- the assistant prefers that interpretation

## Review questions

Before promotion, ask:

1. would I still believe this if the most dramatic example disappeared?
2. does this change how a future agent should work?
3. is the scope precise enough to avoid flattening the owner?
4. can I point to concrete evidence IDs that support it?
