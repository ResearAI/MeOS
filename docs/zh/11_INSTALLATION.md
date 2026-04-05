# 11 安装方式

MeOS 目前支持两种安装风格：

- 本地 shell 安装
- npm 包装安装

## 方式 A：本地 shell 安装

在仓库根目录执行：

```bash
bash install.sh --runtime codex
```

默认行为说明：

- 默认模式是 `--mode auto`
- `auto` 会对 OpenClaw 使用 `copy`，对其它运行时使用 `symlink`
- 可以安装 `--runtime all`，但更推荐按运行时分别安装

常用参数：

```bash
bash install.sh --runtime codex
bash install.sh --runtime claude
bash install.sh --runtime openclaw
bash install.sh --runtime openclaw --mode copy --force
bash install.sh --runtime opencode
bash install.sh --runtime all --dry-run
bash install.sh --runtime codex --scope project --project-dir /path/to/project
```

## 方式 B：直接用 Python 安装器

```bash
python3 installer.py install --runtime codex
python3 installer.py doctor
python3 installer.py print-prompts --lang en
python3 installer.py print-prompts --lang zh
```

## 方式 C：npm 包装安装

在仓库根目录执行：

```bash
npm install -g .
meos install --runtime codex
```

常用命令：

```bash
meos install --runtime claude
meos install --runtime openclaw --force
meos install --runtime opencode
meos doctor
meos print-prompts --lang zh
```

## 备注

- 安装到运行时时，目录名建议统一使用小写 `meos`
- `install` 默认会创建本地私有层目录，除非使用 `--skip-private-layout`
- `doctor` 会检查仓库布局和目标安装位置
- OpenClaw 通常应使用 `copy` 模式，因为它会跳过真实路径跑到根目录外的 symlink skill
- OpenCode 通常只应选择一个兼容目录安装，否则会出现 duplicate warning
- 如果你要把旧的 symlink 安装替换成 copy 安装，请加 `--force`
