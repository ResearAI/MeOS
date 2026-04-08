# Writeback Policy

## Goal

Keep MeOS assets and person-graph state current without turning every run into noisy profile churn.

## When to write back

Write back only when the new information is:

- stable
- reusable
- task-relevant beyond the current moment

## Where to write back

- stable operating pattern -> `assets/`
- stable person-level claim -> `evidence/claims.jsonl` and local graph outputs
- explicit override -> `assets/corrections/`
- uncertain fact -> `evidence/`
- raw source material -> `private/`

## Writeback steps

1. identify the correct asset category
2. identify the correct claim dimension and scope
3. sanitize the content
4. record source linkage in `evidence/source-map.json`
5. append fact, claim, or conflict records when needed
6. update graph outputs or alignment packets if the local runtime uses them
7. only then update the asset file when a prose asset is warranted

## Anti-pattern

Do not dump session summaries directly into assets.
Assets should hold durable rules, not raw narrative.
Graphs should hold structured indexes, not raw narrative either.
