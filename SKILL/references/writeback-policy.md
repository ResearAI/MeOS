# Writeback Policy

## Goal

Keep MeOS assets current without turning every run into noisy profile churn.

## When to write back

Write back only when the new information is:

- stable
- reusable
- task-relevant beyond the current moment

## Where to write back

- stable operating pattern -> `assets/`
- explicit override -> `assets/corrections/`
- uncertain fact -> `evidence/`
- raw source material -> `private/`

## Writeback steps

1. identify the correct asset category
2. sanitize the content
3. record source linkage in `evidence/source-map.json`
4. append fact or conflict records when needed
5. only then update the asset file

## Anti-pattern

Do not dump session summaries directly into assets.
Assets should hold durable rules, not raw narrative.
