# 02 Extraction And Promotion

## Core idea

MeOS separates:

- raw evidence
- promoted reusable assets

## Default flow

1. collect local material
2. classify the source
3. extract high-signal candidate facts
4. store uncertain items in `evidence/`
5. promote only stable items into `assets/live/`

## Promotion rule

Promote when one of these is true:

- explicit user statement
- repeated pattern across contexts
- explicit user correction or reinforcement

Keep in `evidence/` when:

- one-off
- noisy
- too context-specific
- too sensitive
