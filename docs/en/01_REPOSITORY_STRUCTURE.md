# 01 Repository Structure

## Top-level layout

```text
MeOS/
├── README.md
├── docs/
├── assets/
│   ├── branding/
│   └── readme/
├── SKILL/
│   ├── SKILL.md
│   ├── references/
│   ├── schemas/
│   ├── assets/
│   │   ├── templates/
│   │   ├── examples/
│   │   └── live/
│   ├── evidence/
│   ├── runtime/
│   └── private/
├── installer.py
├── install.sh
└── package.json
```

## Public zones

- `SKILL/SKILL.md`
- `SKILL/references/`
- `SKILL/schemas/`
- `SKILL/assets/templates/`
- `SKILL/assets/examples/`
- `docs/`

## Local-first zones

- `SKILL/assets/live/`
- `SKILL/evidence/`
- `SKILL/runtime/`
- `SKILL/private/`

These are separated because MeOS should expose the method, not your private raw material.
