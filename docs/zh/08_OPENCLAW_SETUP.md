# 08 OpenClaw 配置

## 官方技能目录

OpenClaw 支持的主要技能目录包括：

- `~/.openclaw/skills`
- `~/.agents/skills`
- `<workspace>/.agents/skills`
- `<workspace>/skills`

并且支持对 `SKILL.md` 变更进行自动刷新。

## 手动测试后确认的重要行为

- OpenClaw 会跳过“真实路径跑到根目录之外”的 symlink skill。
- 实际上，`ln -s /path/to/MeOS/SKILL ~/.openclaw/skills/meos` 这类装法并不稳。
- 最稳妥的是把 MeOS 作为真实目录复制到 `<workspace>/skills/meos` 或 `~/.openclaw/skills/meos`。
- 即使 skill 已经可见，新的 profile 或 agent 仍然可能因为缺少模型 auth 而无法真正跑回合。

## MeOS 推荐安装方式

建议安装到小写目录 `meos`。

### 工作区本地 copy

```bash
mkdir -p <workspace>/skills
cp -a /path/to/MeOS/SKILL <workspace>/skills/meos
```

### 共享 managed copy

```bash
mkdir -p ~/.openclaw/skills
cp -a /path/to/MeOS/SKILL ~/.openclaw/skills/meos
```

### 外部共享 skill 根目录

```bash
openclaw config set skills.load.extraDirs '["/absolute/path/to/skills-root"]' --strict-json
```

如果你用 `skills.load.extraDirs`，请把它指向包含 `meos/` 的父目录。

## 验证安装

```bash
openclaw skills info meos
openclaw skills list | rg meos
```

如果安装正确，`skills info` 会显示 `Path: .../meos/SKILL.md`。

## 在本地 agent 回合中使用 MeOS

OpenClaw 必须通过 `--agent`、`--to` 或 `--session-id` 明确选择一个 session。

```bash
openclaw agent --local --agent main --json \
  --thinking minimal \
  --timeout 180 \
  --message 'Use meos in apply mode for this task. In 3 short bullets, say what you would read first and why.'
```

## 完整隔离的手动测试示例

下面这条链路已经实际验证过，不依赖你当前主 profile：

```bash
mkdir -p /tmp/openclaw-meos-test/skills
cp -a /path/to/MeOS/SKILL /tmp/openclaw-meos-test/skills/meos

export CUSTOM_API_KEY=your_minimaxi_or_other_compatible_key

openclaw --profile meosrun onboard --non-interactive \
  --accept-risk \
  --mode local \
  --auth-choice custom-api-key \
  --custom-provider-id minimaxi \
  --custom-base-url https://api.minimaxi.com/anthropic \
  --custom-model-id MiniMax-M2.7 \
  --custom-compatibility anthropic \
  --secret-input-mode ref \
  --workspace /tmp/openclaw-meos-test \
  --skip-channels --skip-daemon --skip-search --skip-skills --skip-ui --skip-health

openclaw --profile meosrun skills info meos

openclaw --profile meosrun agent --local --agent main --json \
  --thinking minimal \
  --timeout 180 \
  --message 'Use meos in apply mode for this task. In 3 short bullets, say what you would read first and why.'
```

## 如何使用

推荐的使用模式：

- `init`：第一次从本地材料创建资产
- `refresh`：用新增材料刷新资产
- `apply`：在当前任务中使用已有资产

## 备注

- `<workspace>/skills` 的优先级最高。
- 如果启用了 agent skill allowlist，需要确保 `meos` 对对应 agent 是可用的。
- 如果开启了 watcher，`SKILL.md` 修改后可自动刷新。
- 如果新 profile 或新 agent 报缺少 auth，需要单独为它配置 provider；skill 可见不等于模型可用。
