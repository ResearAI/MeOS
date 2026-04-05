# Source Locations

Use this file to decide where MeOS may read from.

## Priority order

1. Existing MeOS assets and corrections
2. Durable local project history and quest history
3. Agent transcript history
4. User-provided local documents
5. Additional communication exports explicitly provided by the user

## Default local source classes

- local quest conversations
- local agent transcripts
- local project documentation
- local correction notes

## Recommended source families

### A. Codex-style local sessions

Typical location shape:

- `$HOME/.codex/sessions/`

Use these mainly for:

- direct user instructions
- durable preference and correction signals
- accepted or rejected answer patterns

### B. Claude Code local history

Typical location shapes:

- `$HOME/.claude/history.jsonl`
- `$HOME/.claude/projects/**/*.jsonl`

Use these mainly for:

- user-side workflow and planning signals
- structured audit expectations
- implementation and verification habits
- full `user` / `assistant` transcript pairs when available in project session logs

### C. DeepScientist quest history

Typical location shape:

- `<DEEPSCIENTIST_HOME>/quests/*/.ds/`

High-value files often include:

- `conversations/main.jsonl`
- `events.jsonl`
- `interaction_journal.jsonl`
- local run or history folders

Use these mainly for:

- research workflow patterns
- continuation and interruption behavior
- what kinds of progress updates the owner accepts or rejects
- paper and experiment evidence-management habits

## Reading rule

Prefer owner-authored or owner-corrected material over generic assistant narration when both exist.

Prefer:

- explicit instructions
- corrections
- planning documents
- review / decision notes

When transcript pairs are available, distinguish:

- what the user asked for
- how the assistant responded
- whether the user accepted, corrected, or redirected that response

over:

- generic progress chatter
- one-off casual messages
- low-signal acknowledgements

## Privacy rule

Raw imports and sensitive source material belong under `private/` and should not be committed by default.
