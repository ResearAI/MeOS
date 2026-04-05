# 10 Applying MeOS

## Core idea

MeOS should not only create or refresh assets.
Its real value is applying those assets in future tasks.

## What `apply` should do

When MeOS is used in `apply` mode, the agent should:

1. identify the current task type
2. read only the minimum relevant assets
3. let those assets shape:
   - reasoning
   - workflow
   - output
   - correction handling
4. avoid rewriting the asset store unless genuinely stable new information appears

## Which assets matter for which tasks

### Technical implementation

Read:

- `assets/live/work/`
- `assets/live/thought-style/`
- `assets/live/workflow/`
- `assets/live/principles/`

### UI / product work

Read:

- `assets/live/taste/`
- `assets/live/work/`
- `assets/live/workflow/`
- `assets/live/corrections/`

### Research or writing work

Read:

- `assets/live/work/`
- `assets/live/thought-style/`
- `assets/live/principles/`
- `assets/live/knowledge/`
- `assets/live/workflow/`

### Style-sensitive replies

Read:

- `assets/live/preferences/`
- `assets/live/corrections/`

## Highest-priority layer

If a rule in `assets/live/corrections/` conflicts with another layer, the correction wins.
