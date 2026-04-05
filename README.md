<h1 align="center">
  <img src="assets/branding/logo.svg" alt="MeOS logo" width="92" />
  MeOS
</h1>

<p align="center">
  MeOS is a local-first operating layer for turning your workflows, standards, preferences, and corrections into reusable agent assets.
</p>

<p align="center">
  It helps agents learn how you work across Codex, Claude Code, OpenClaw, and OpenCode, without turning private raw history into a public leak.
</p>

<p align="center">
  <a href="docs/en/README.md">English Docs</a> |
  <a href="docs/zh/README.md">中文文档</a> |
  <a href="#quick-start">Quick Start</a> |
  <a href="#how-meos-works">How It Works</a> |
  <a href="#verified-runtimes">Verified Runtimes</a> |
  <a href="#privacy-boundary">Privacy Boundary</a>
</p>

<p align="center">
  <img alt="License MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" />
  <img alt="Format Agent Skill" src="https://img.shields.io/badge/Format-Agent%20Skill-green?style=for-the-badge" />
  <img alt="Scope local-first" src="https://img.shields.io/badge/Scope-local--first-blue?style=for-the-badge" />
  <img alt="Mode privacy-aware" src="https://img.shields.io/badge/Mode-privacy--aware-purple?style=for-the-badge" />
</p>

<p align="center">
  <strong>Apply, not just store</strong> ·
  <strong>Public core, private local layer</strong> ·
  <strong>Editable assets, not black-box memory</strong> ·
  <strong>Works across multiple agent runtimes</strong>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#what-you-actually-get">What You Get</a> •
  <a href="#verified-runtimes">Runtime Status</a> •
  <a href="#important-docs">Important Docs</a>
</p>

![MeOS overview](assets/readme/00-overview.svg)

MeOS is not a memory dump.  
It is not a roleplay profile pack.  
It is not just a pile of prompts.

It is a file-first system for turning a person's stable way of working into assets that future agents can actually use.

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
git clone <your-meos-repo-url>
cd MeOS
```

### 2. Install into one runtime

`--mode auto` is the default.
It uses a runtime-safe install strategy: `copy` for OpenClaw, `symlink` for the others.

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

## ✅ Verified Runtimes

Manual verification completed on 2026-04-04.

| Runtime | Status | What was verified | Important note |
|---|---|---|---|
| Codex | `✅ verified` | MeOS was discovered and used in an `apply` task | standard skill install works |
| Claude Code | `✅ verified` | MeOS was discovered and used via `/meos` | separate MiniMax guide is available |
| OpenClaw | `✅ verified` | MeOS was loaded from a workspace copy and completed an `apply` turn | avoid external symlink installs |
| OpenCode | `✅ verified` | MeOS was loaded through the `skill` tool and completed a turn | `small_model` may need explicit config |

## 🔒 Privacy Boundary

This split is one of the most important parts of MeOS.

| Safe to publish | Keep local by default |
|---|---|
| `🌐 SKILL.md` | `🔒 private/` |
| `🌐 references/` | `🔒 evidence/` |
| `🌐 schemas/` | `🔒 runtime/` |
| `🌐 assets/templates/` | `🔒 assets/live/` |
| `🌐 assets/examples/` | `🔒 raw imported material` |

Rules:

- do not commit secrets, tokens, or private raw transcripts
- do not promote one-off behavior into stable assets
- do not confuse evidence with reusable assets
- do not store unnecessary personal identifiers in reusable files

![MeOS privacy boundary](assets/readme/03-privacy-boundary.svg)

## 🏗 Repository Layout

```text
MeOS/
├── SKILL.md
├── README.md
├── LICENSE
├── references/
├── schemas/
├── assets/
│   ├── branding/
│   ├── readme/
│   ├── templates/
│   ├── examples/
│   └── live/         # local-only by default
├── evidence/         # local-only by default
├── runtime/          # local-only by default
└── private/          # local-only by default
```

The important pattern is:

- public method in `references/`, `schemas/`, `assets/templates/`, `assets/examples/`
- real owner calibration in `assets/live/`
- weak or conflicting facts in `evidence/`
- raw imported history in `private/`

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

- a cross-tool `SKILL.md`
- extraction, promotion, privacy, and writeback references
- JSON schemas for durable entries
- example and template asset trees
- verified install and load paths for four runtimes

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
