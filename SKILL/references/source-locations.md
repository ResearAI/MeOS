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

## Person-graph signal priority

When building owner-centric claims, prefer sources with the highest signal about the owner as an individual.

Prefer, in order:

1. explicit self-description
2. explicit corrections and reversals
3. repeated choices or repeated rejections
4. long-running project and decision history
5. assistant-visible repeated behavior with clear evidence

Do not optimize for transcript volume.
Optimize for stable owner signal.

## Recommended source families

### A. Codex-style local sessions

Typical location shape:

- `$HOME/.codex/sessions/`

Use these mainly for:

- direct user instructions
- durable preference and correction signals
- accepted or rejected answer patterns
- stable tone and structure preferences when reinforced repeatedly

### B. Claude Code local history

Typical location shapes:

- `$HOME/.claude/history.jsonl`
- `$HOME/.claude/projects/**/*.jsonl`

Use these mainly for:

- user-side workflow and planning signals
- structured audit expectations
- implementation and verification habits
- full `user` / `assistant` transcript pairs when available in project session logs
- repeated collaboration style patterns

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
- long-horizon interest and role signals

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
- what that pattern reveals about the owner's preferences, principles, and working style

over:

- generic progress chatter
- one-off casual messages
- low-signal acknowledgements

## Privacy rule

Raw imports and sensitive source material belong under `private/` and should not be committed by default.
