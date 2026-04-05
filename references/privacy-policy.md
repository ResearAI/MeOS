# Privacy Policy

## Core rule

MeOS should preserve reusable working knowledge without leaking unnecessary private detail.

## Do not promote by default

- tokens
- API keys
- raw connector ids
- personal contact ids
- workstation-specific private paths when a semantic path is enough
- copied private messages that are not required for the reusable rule

## Safe defaults

- prefer semantic labels over personal identifiers
- prefer relative paths over personal absolute paths when possible
- prefer summarized evidence over raw sensitive content

## Commit boundary

Default git-safe content:

- `SKILL.md`
- `references/`
- `schemas/`
- sanitized assets

Default local-only content:

- `private/`
- `evidence/`
- `runtime/`

## Escalation rule

If a detail is both sensitive and not essential to future reuse, exclude it.
