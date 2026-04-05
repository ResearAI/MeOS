<h1 align="center">
  <img src="assets/branding/logo.svg" alt="MeOS logo" width="92" />
  MeOS
</h1>

<p align="center">
  MeOS 是一个本地优先的操作层，用来把你的工作流、技术标准、偏好和纠偏规则整理成可复用的 agent 资产。
</p>

<p align="center">
  它让 Codex、Claude Code、OpenCode 和 OpenClaw 更像“学会了你怎么工作”，同时默认把私有原始历史保留在本地。
</p>

<p align="center">
  <a href="https://github.com/ResearAI/MeOS">https://github.com/ResearAI/MeOS</a>
</p>

<p align="center">
  <a href="https://github.com/ResearAI/MeOS">GitHub</a> |
  <a href="README.md">English README</a> |
  <a href="docs/zh/README.md">中文文档</a> |
  <a href="#quick-start">快速开始</a> |
  <a href="#important-docs">重要文档</a>
</p>

<p align="center">
  <a href="https://github.com/ResearAI/MeOS"><img alt="GitHub stars" src="https://img.shields.io/github/stars/ResearAI/MeOS?style=for-the-badge&logo=github"></a>
  <a href="LICENSE"><img alt="License MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge"></a>
  <img alt="Format Agent Skill" src="https://img.shields.io/badge/Format-Agent%20Skill-green?style=for-the-badge" />
  <img alt="Scope local-first" src="https://img.shields.io/badge/Scope-local--first-blue?style=for-the-badge" />
</p>

<p align="center">
  <strong>不只是存储，而是实际应用</strong> ·
  <strong>公开仓库，私有本地层</strong> ·
  <strong>可编辑资产，不是黑箱记忆</strong> ·
  <strong>一套安装器覆盖多个运行时</strong>
</p>

<p align="center">
  <a href="#what-you-actually-get">能得到什么</a> •
  <a href="#how-meos-works">工作方式</a> •
  <a href="#privacy-boundary">隐私边界</a> •
  <a href="#repository-layout">仓库结构</a>
</p>

![MeOS overview](assets/readme/00-overview.svg)

MeOS 不是 memory dump。  
不是角色扮演 prompt 包。  
也不是一堆零散提示词。

它是一个文件优先的系统，用来把“一个人的稳定工作方式”沉淀成未来 agent 真能用起来的资产。

支持 Codex、Claude Code、OpenCode 和 OpenClaw。

如果你已经厌倦了在每个新 agent 会话里重复解释同一套标准、同一种审美、同一类纠偏规则，MeOS 就是把这些重复劳动变成长期本地资产的那一层。

## ✨ 为什么是 MeOS

这一类系统通常各自只擅长一个点：

- 把一个人蒸馏成一段 prompt
- 从历史交互里抽技能
- 保留一批可复用的说明文档

MeOS 关注的是中间那层更长期、更稳定的“操作层”。

| 常见做法 | 常见问题 | MeOS 的做法 |
|---|---|---|
| Memory dump | 噪声太多，复用性弱 | 只把稳定模式晋升成资产 |
| Persona prompt | 听起来像你，但工作层很浅 | 直接存工作流、标准、原则和纠偏 |
| 一次性画像总结 | 很快过时 | 把 `init`、`refresh`、`apply` 做成长期生命周期 |
| 本地私人笔记 | 难以跨工具复用 | 用通用 `SKILL.md` 结构让多个运行时可加载 |

核心思想很简单：

> 不只是记住这个人，而是让这个人变得可复用

## 🧩 你实际会得到什么

| 资产类型 | 例子 | 改善什么 |
|---|---|---|
| `🛠` 工作标准 | 编码规则、review 标准、验收线 | 技术质量与一致性 |
| `🧭` 工作流资产 | debug 顺序、架构评审顺序、交付清单 | agent 处理任务的方式 |
| `🧠` 思维风格 | 推理模式、权衡习惯、决策风格 | 规划与判断质量 |
| `🎨` 审美与偏好 | 输出结构、UI 审美、表达风格 | 最终结果的样子 |
| `✍️` 纠偏规则 | 明确 override、历史否定过的东西 | 减少重复偏航 |
| `📚` 知识资产 | 稳定事实、领域理解、可复用经验 | 超出单次聊天的上下文积累 |

## ⚙️ MeOS 如何工作

| 模式 | 目的 | 先读什么 | 会写回什么 |
|---|---|---|---|
| `🧱 init` | 从批准过的本地材料建立第一版资产 | source policy、extraction SOP、promotion policy、privacy policy | 初始资产和 evidence |
| `🔁 refresh` | 用新增材料更新已有资产 | extraction SOP、promotion policy、correction policy | merge 后的更新、冲突、纠偏 |
| `🎯 apply` | 在真实任务里使用已有资产 | 只读取最相关的资产 | 只有稳定新信息才写回 |

`apply` 是最关键的模式。  
这也是 MeOS 从“档案”变成“真正有用”的地方。

## 🗂 `apply` 模式下 agent 会读什么

下面这些路径都相对于安装后的 skill 根目录。  
在当前仓库里，它们实际位于 `SKILL/` 下。

| 任务类型 | 优先读什么 | 会带来什么 |
|---|---|---|
| `🛠` 技术实现 | `assets/live/work/`、`assets/live/thought-style/`、`assets/live/workflow/`、`assets/live/principles/` | 更贴近你的技术标准和执行顺序 |
| `🎨` UI / 产品 | `assets/live/taste/`、`assets/live/work/`、`assets/live/workflow/`、`assets/live/corrections/` | 更贴近你的审美和呈现要求 |
| `🔬` 研究 / 写作 | `assets/live/work/`、`assets/live/thought-style/`、`assets/live/principles/`、`assets/live/knowledge/`、`assets/live/workflow/` | 更贴近你的结构、推理和知识组织方式 |
| `💬` 风格敏感回复 | `assets/live/preferences/`、`assets/live/corrections/` | 更贴近你的表达形态和措辞习惯 |

如果 `assets/live/corrections/` 和其他层冲突，以 correction 为准。

## 🚀 Quick Start

### 1. 克隆仓库

```bash
git clone https://github.com/ResearAI/MeOS.git
cd MeOS
```

### 2. 安装到一个运行时

安装器不会把整个仓库塞进运行时。  
它真正安装的是 `./SKILL/` 的内容，目标目录是运行时里的 `meos/`。

默认模式是 `--mode auto`。  
它会用更安全的运行时策略：OpenClaw 用 `copy`，其他运行时默认 `symlink`。

| 运行时 | 推荐命令 | 说明 |
|---|---|---|
| Codex | `bash install.sh --runtime codex` | 最简单的本地 skill 使用路径 |
| Claude Code | `bash install.sh --runtime claude` | 注意 skill 目录名必须是小写 `meos` |
| OpenClaw | `bash install.sh --runtime openclaw --force` | 更推荐复制目录 |
| OpenCode | `bash install.sh --runtime opencode` | 只安装到一个兼容路径即可 |

也可以使用 npm 包装器：

```bash
npm install -g .
meos install --runtime codex
```

### 3. 直接开始用

```text
Use meos in apply mode for this task. Read only the minimum relevant assets and use them to shape reasoning, workflow, and output.
```

常用 prompt：

```text
Use meos in init mode. Build the first sanitized operating-layer assets from the available local source material.
```

```text
Use meos in refresh mode. Refresh the existing MeOS assets from new local material and only promote stable rules.
```

```text
Use meos in apply mode for this task. Read only the minimum relevant assets and write back only stable new information.
```

## 🔒 隐私边界

这一层拆分是 MeOS 最重要的设计之一。

| 可公开内容 | 默认保留在本地 |
|---|---|
| `README.md` | `SKILL/private/` |
| `docs/` | `SKILL/evidence/` |
| `assets/branding/` | `SKILL/runtime/` |
| `assets/readme/` | `SKILL/assets/live/` |
| `SKILL/references/` | 原始导入材料 |
| `SKILL/schemas/` | secrets 和 tokens |
| `SKILL/assets/templates/` | 工作站本地备注 |
| `SKILL/assets/examples/` | 私有原始对话 |

基本规则：

- 不要提交 secrets、tokens 或私有原始对话
- 不要把一次性行为直接晋升成长期资产
- 不要把 evidence 和正式资产混为一谈
- 不要把没必要的个人标识写进可复用文件

![MeOS privacy boundary](assets/readme/03-privacy-boundary.svg)

## 🏗 仓库结构

```text
MeOS/
├── README.md
├── README_ZH.md
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

关键结构就是：

- 仓库根目录放公开项目材料
- 运行时真正需要的 skill 内容都放在 `SKILL/`
- 安装器负责把 `SKILL/` 安装进运行时 skill 目录
- 本地 owner 校准层保留在 `SKILL/assets/live/`、`SKILL/evidence/`、`SKILL/private/` 和 `SKILL/runtime/`

## 📎 重要文档

最值得先看的几个文档：

- [快速开始](docs/zh/00_QUICK_START.md)
- [如何应用 MeOS](docs/zh/10_APPLYING_MEOS.md)
- [安装方式](docs/zh/11_INSTALLATION.md)
- [OpenClaw 配置](docs/zh/08_OPENCLAW_SETUP.md)
- [OpenCode 配置](docs/zh/09_OPENCODE_SETUP.md)
- [Claude Code + MiniMax](docs/zh/12_CLAUDE_CODE_MINIMAX.md)

## 🛤 当前方向

MeOS 现在已经有：

- 一套跨运行时的 `SKILL/` 包布局
- extraction、promotion、privacy、writeback 参考文档
- durable entry 的 JSON schema
- example 和 template 资产树
- 面向 Codex、Claude Code、OpenCode、OpenClaw 的安装路径

下一步不应该是“继续堆 prompt 文本”。  
而是继续完善资产、示例和公开展示，同时不泄露任何私有历史。

## 📚 引用

如果 MeOS 被用于人格对齐、风格蒸馏或长期操作层资产维护相关工作，也可以考虑引用：

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
