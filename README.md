<h1 align="center">
  <img src="assets/branding/logo.svg" alt="MeOS logo" width="92" />
  MeOS
</h1>

<p align="center">
  MeOS is a local-first operating layer for turning your workflows, standards, preferences, and corrections into reusable agent assets.
</p>

<p align="center">
  It helps agents learn how you work across Codex, Claude Code, OpenCode, and OpenClaw, while keeping private raw history local by default.
</p>

<p align="center">
  <a href="https://github.com/ResearAI/MeOS">https://github.com/ResearAI/MeOS</a>
</p>

<p align="center">
  <a href="https://github.com/ResearAI/MeOS">GitHub</a> |
  <a href="docs/en/README.md">English Docs</a> |
  <a href="README_ZH.md">中文 README</a> |
  <a href="#quick-start">Quick Start</a> |
  <a href="#important-docs">Important Docs</a>
</p>

<p align="center">
  <a href="https://github.com/ResearAI/MeOS"><img alt="GitHub stars" src="https://img.shields.io/github/stars/ResearAI/MeOS?style=for-the-badge&logo=github"></a>
  <a href="LICENSE"><img alt="License MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge"></a>
  <img alt="Format Agent Skill" src="https://img.shields.io/badge/Format-Agent%20Skill-green?style=for-the-badge" />
  <img alt="Scope local-first" src="https://img.shields.io/badge/Scope-local--first-blue?style=for-the-badge" />
</p>

<p align="center">
  <strong>Apply, not just store</strong> ·
  <strong>Public repository, private local layer</strong> ·
  <strong>Editable assets, not black-box memory</strong> ·
  <strong>One installer for multiple runtimes</strong>
</p>

<p align="center">
  <a href="#what-you-actually-get">What You Get</a> •
  <a href="#how-meos-works">How It Works</a> •
  <a href="#privacy-boundary">Privacy Boundary</a> •
  <a href="#repository-layout">Repository Layout</a>
</p>

![MeOS overview](assets/readme/00-overview.svg)

MeOS is not a memory dump.  
It is not a roleplay profile pack.  
It is not just a pile of prompts.

It is a file-first system for making a person reusable to future agents.

Supports Codex, Claude Code, OpenCode, and OpenClaw.

If you are tired of repeating the same standards, the same taste, and the same corrections in every new agent session, MeOS is the layer that turns that repetition into reusable local assets.

## ✨ Why MeOS

Most systems in this space do one part well:

- distill a person into a prompt
- extract reusable skills from interaction logs
- keep reusable instructions around

MeOS focuses on the layer in between: the long-lived operating layer.

| Typical approach | What it usually misses | What MeOS does instead |
|---|---|---|
| Memory dump | Too much noise, weak reuse | Promotes only stable patterns into assets |
| Persona prompt | Sounds similar, works shallowly | Stores workflows, standards, principles, and corrections |
| One-shot profile summary | Becomes stale quickly | Supports `init`, `refresh`, and `apply` as an ongoing lifecycle |
| Private local notebook | Hard to reuse across tools | Uses a shared `SKILL.md` shape that multiple runtimes can load |

The core idea is simple:

> do not merely remember the owner, make the owner reusable

## 🧩 What You Actually Get

| Asset type | Examples | What it improves |
|---|---|---|
| `🛠` Work standards | coding rules, review bar, acceptance lines | technical quality and consistency |
| `🧭` Workflow assets | debug order, architecture review sequence, delivery checklist | how the agent approaches the task |
| `🧠` Thought style | reasoning patterns, trade-off habits, decision style | planning and judgment quality |
| `🎨` Taste and preferences | output structure, UI taste, response style | how results look and read |
| `✍️` Corrections | explicit overrides, things the owner rejected before | prevents repeated misalignment |
| `📚` Knowledge assets | stable facts, domain understanding, reusable experience | task context that survives beyond one chat |

## ⚙️ How MeOS Works

| Mode | Purpose | Reads first | Writes back |
|---|---|---|---|
| `🧱 init` | Build the first asset set from approved local material | source policy, extraction SOP, promotion policy, privacy policy | initial assets plus evidence |
| `🔁 refresh` | Update existing assets with new material | extraction SOP, promotion policy, correction policy | merged updates, conflicts, corrections |
| `🎯 apply` | Use existing assets during a live task | only the minimum relevant assets | only stable new information |

`apply` is the most important mode.
That is where MeOS stops being an archive and starts becoming useful.

## 🗂 What The Agent Reads In `apply` Mode

Paths below are relative to the installed skill root.
Inside this repository, they live under `SKILL/`.

| Task type | Read first | Outcome |
|---|---|---|
| `🛠` Technical implementation | `assets/live/work/`, `assets/live/thought-style/`, `assets/live/workflow/`, `assets/live/principles/` | follows your technical standards and execution order |
| `🎨` UI / product work | `assets/live/taste/`, `assets/live/work/`, `assets/live/workflow/`, `assets/live/corrections/` | preserves your taste and presentation bar |
| `🔬` Research / writing | `assets/live/work/`, `assets/live/thought-style/`, `assets/live/principles/`, `assets/live/knowledge/`, `assets/live/workflow/` | uses your structure, reasoning, and domain framing |
| `💬` Style-sensitive replies | `assets/live/preferences/`, `assets/live/corrections/` | matches preferred response shape and wording |

If `assets/live/corrections/` conflicts with another layer, correction wins.

## 🚀 Quick Start

### 1. Clone

```bash
git clone https://github.com/ResearAI/MeOS.git
cd MeOS
```

### 2. Install into one runtime

The installer does not publish the whole repository.
It installs the contents of `./SKILL/` into the runtime skill directory `meos/`.

`--mode auto` is the default.
It uses a runtime-safe install strategy: `copy` for OpenClaw, `symlink` for the other runtimes.

| Runtime | Recommended command | Note |
|---|---|---|
| Codex | `bash install.sh --runtime codex` | simplest path for local skill use |
| Claude Code | `bash install.sh --runtime claude` | use lowercase `meos` skill dir |
| OpenClaw | `bash install.sh --runtime openclaw --force` | prefers copied skill directories |
| OpenCode | `bash install.sh --runtime opencode` | install into one compatible path only |

You can also use the npm wrapper:

```bash
npm install -g .
meos install --runtime codex
```

### 3. Use it immediately

```text
Use meos in apply mode for this task. Read only the minimum relevant assets and use them to shape reasoning, workflow, and output.
```

Useful prompts:

```text
Use meos in init mode. Build the first sanitized operating-layer assets from the available local source material.
```

```text
Use meos in refresh mode. Refresh the existing MeOS assets from new local material and only promote stable rules.
```

```text
Use meos in apply mode for this task. Read only the minimum relevant assets and write back only stable new information.
```

## 🔒 Privacy Boundary

This split is one of the most important parts of MeOS.

| Safe to publish | Keep local by default |
|---|---|
| `README.md` | `SKILL/private/` |
| `docs/` | `SKILL/evidence/` |
| `assets/branding/` | `SKILL/runtime/` |
| `assets/readme/` | `SKILL/assets/live/` |
| `SKILL/references/` | raw imported material |
| `SKILL/schemas/` | secrets and tokens |
| `SKILL/assets/templates/` | workstation-specific notes |
| `SKILL/assets/examples/` | private raw transcripts |

Rules:

- do not commit secrets, tokens, or private raw transcripts
- do not promote one-off behavior into stable assets
- do not confuse evidence with reusable assets
- do not store unnecessary personal identifiers in reusable files

![MeOS privacy boundary](assets/readme/03-privacy-boundary.svg)

## 🏗 Repository Layout

```text
MeOS/
├── README.md
├── LICENSE
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
├── install.sh
├── installer.py
├── package.json
└── bin/
```

The important pattern is:

- public project materials stay at the repository root
- everything the runtime skill needs lives under `SKILL/`
- the installer publishes `SKILL/` into runtime skill directories
- local-only owner calibration stays in `SKILL/assets/live/`, `SKILL/evidence/`, `SKILL/private/`, and `SKILL/runtime/`

## 📎 Important Docs

Only a few docs are worth opening first:

- [Quick Start](docs/en/00_QUICK_START.md)
- [Applying MeOS](docs/en/10_APPLYING_MEOS.md)
- [Installation](docs/en/11_INSTALLATION.md)
- [OpenClaw Setup](docs/en/08_OPENCLAW_SETUP.md)
- [OpenCode Setup](docs/en/09_OPENCODE_SETUP.md)
- [Claude Code + MiniMax](docs/en/12_CLAUDE_CODE_MINIMAX.md)

## 🛤 Current Direction

MeOS already has:

- a cross-tool `SKILL/` package layout
- extraction, promotion, privacy, and writeback references
- JSON schemas for durable entries
- example and template asset trees
- installer paths for Codex, Claude Code, OpenCode, and OpenClaw

The next step is not "add more prompt text".
It is to keep improving the assets, examples, and public presentation without leaking private local history.

## 📚 Citation

If MeOS is used in work related to personal alignment, style distillation, or operating-layer asset maintenance, you may also want to cite:

```bibtex
@inproceedings{
zhu2025personality,
title={Personality Alignment of Large Language Models},
author={Minjun Zhu and Yixuan Weng and Linyi Yang and Yue Zhang},
booktitle={The Thirteenth International Conference on Learning Representations},
year={2025},
url={https://openreview.net/forum?id=0DZEs8NpUH}
}
```
