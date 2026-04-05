# 09 OpenCode 配置

## 官方技能目录

OpenCode 会搜索这些位置：

- `.opencode/skills/<name>/SKILL.md`
- `~/.config/opencode/skills/<name>/SKILL.md`
- `.claude/skills/<name>/SKILL.md`
- `~/.claude/skills/<name>/SKILL.md`
- `.agents/skills/<name>/SKILL.md`
- `~/.agents/skills/<name>/SKILL.md`

OpenCode 通过原生 `skill` 工具按需加载技能。

## 手动测试后确认的重要行为

- OpenCode 对 skill 命名很严格。
- 它会同时搜索多个兼容目录，所以如果你把 `meos` 装进所有目录，会出现 duplicate-skill warning。
- 某些 OpenAI 兼容 provider 还需要显式设置 `small_model`，否则 OpenCode 可能会在正式回合开始前就失败，例如在生成 session title 时失败。

## 命名规则

OpenCode 要求：

- `name` 必须是小写
- skill 所在目录名也必须与 `name` 一致

所以 MeOS 在运行时应安装到 `meos/` 目录中。

## 推荐安装方式

三种目录里选一种即可，不要全装。

### OpenCode 原生目录

```bash
mkdir -p ~/.config/opencode/skills
ln -s /path/to/MeOS/SKILL ~/.config/opencode/skills/meos
```

### Claude 兼容目录

```bash
mkdir -p ~/.claude/skills
ln -s /path/to/MeOS/SKILL ~/.claude/skills/meos
```

### Agent 兼容目录

```bash
mkdir -p ~/.agents/skills
ln -s /path/to/MeOS/SKILL ~/.agents/skills/meos
```

## Provider 兼容性说明

如果你的 provider 或代理不支持 OpenCode 默认用来生成标题的副模型，请显式设置 `small_model`：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "openai/gpt-5.4",
  "small_model": "openai/gpt-5.4"
}
```

如果你的 provider 支持更便宜但同样稳定的模型，也可以把 `small_model` 设成那个。

## 验证安装与 skill 加载

```bash
opencode run --model openai/gpt-5.4 --format json \
  'Use meos in apply mode for this task. In 3 short bullets, say what you would read first and why.'
```

如果 JSON 输出里出现 `tool_use` 且 `tool` 是 `skill`、`name` 是 `meos`，说明技能已被成功加载。

## 如何使用

OpenCode agent 会发现 skill，并在需要时按需加载。

MeOS 主要有三种用法：

- 初始化第一版资产
- 刷新已有资产
- 在当前任务中应用已有资产

## 备注

- OpenCode 会忽略未知 frontmatter 字段，所以 MeOS 的核心 frontmatter 应保持极简。
- 如果启用了 per-agent permissions，需要确保 `meos` 对对应 agent 是允许的。
- 如果你已经通过 `~/.claude/skills` 或 `~/.agents/skills` 安装了 MeOS，就不要再额外装到 `~/.config/opencode/skills`，除非你能接受重复告警。
