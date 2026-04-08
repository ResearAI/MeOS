# Apply Task Map

Paths below are relative to the installed skill root.

## Global rule

If `runtime/graph/alignment-packet.json` exists, read it first.

If task-scoped graph slices exist under `runtime/graph/`, prefer those over the full graph.

## Technical implementation

Read:

- `assets/live/work/`
- `assets/live/thought-style/`
- `assets/live/workflow/`
- `assets/live/principles/`
- task-scoped behavior, workflow, and constraint claims from `runtime/graph/`

## UI / product work

Read:

- `assets/live/taste/`
- `assets/live/work/`
- `assets/live/workflow/`
- `assets/live/corrections/`
- task-scoped taste, preference, and constraint claims from `runtime/graph/`

## Research or writing work

Read:

- `assets/live/work/`
- `assets/live/thought-style/`
- `assets/live/principles/`
- `assets/live/knowledge/`
- `assets/live/workflow/`
- domain-scoped role, interest, principle, and workflow claims from `runtime/graph/`

## Style-sensitive replies

Read:

- `assets/live/preferences/`
- `assets/live/corrections/`
- tone, preference, and constraint claims from `runtime/graph/alignment-packet.json`

## Priority rule

If a rule in `assets/live/corrections/` conflicts with another layer, the correction wins.
If the current user message conflicts with older graph material, the current user message wins.
