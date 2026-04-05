# 01 仓库结构

## 顶层结构

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

## 可公开层

- `SKILL/SKILL.md`
- `SKILL/references/`
- `SKILL/schemas/`
- `SKILL/assets/templates/`
- `SKILL/assets/examples/`
- `docs/`

## 本地优先层

- `SKILL/assets/live/`
- `SKILL/evidence/`
- `SKILL/runtime/`
- `SKILL/private/`

这样划分的目的，是把“方法框架”公开出去，而不是把你的私有原始材料一起公开。
