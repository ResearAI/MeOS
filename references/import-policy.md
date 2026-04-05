# Import Policy

## Goal

Allow offline history import without forcing replay of the original interaction.

## Supported import classes

- archived agent conversations
- local quest histories
- local coding-assistant transcripts
- user-provided document bundles
- future communication exports explicitly approved by the owner

## Import stages

1. `discover`
   - locate candidate source files
2. `classify`
   - identify source type and expected signal density
3. `sanitize`
   - remove or mask private secrets and unnecessary identifiers
4. `stage`
   - copy into `private/imported/` or `private/raw/`
5. `extract`
   - produce evidence candidates
6. `promote`
   - move only stable rules into `assets/`

## Import rules

- Do not promote directly from a raw import into `assets/`.
- Keep original imported material local-only by default.
- Record source provenance in `evidence/source-map.json`.
- When two imports disagree, create a conflict record instead of forcing a merge.
