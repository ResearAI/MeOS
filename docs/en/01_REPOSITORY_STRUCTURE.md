# 01 Repository Structure

## Top-level layout

```text
MeOS/
├── SKILL.md
├── README.md
├── docs/
├── references/
├── schemas/
├── assets/
│   ├── templates/
│   ├── examples/
│   └── live/
├── evidence/
├── runtime/
└── private/
```

## Public zones

- `SKILL.md`
- `references/`
- `schemas/`
- `assets/templates/`
- `assets/examples/`
- `docs/`

## Local-first zones

- `assets/live/`
- `evidence/`
- `runtime/`
- `private/`

These are separated because MeOS should expose the method, not your private raw material.
