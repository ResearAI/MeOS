# 07 Claude Code 配置

## 官方技能目录

Claude Code 支持：

- 用户级 skills：`~/.claude/skills/<skill-name>/SKILL.md`
- 项目级 skills：`.claude/skills/<skill-name>/SKILL.md`
- 插件级 skills

Claude 会根据 `description` 自动触发 skill，也可以通过 `/<skill-name>` 显式调用。

## MeOS 推荐安装方式

建议安装到小写目录 `meos` 中。

### 用户级

```bash
mkdir -p ~/.claude/skills
ln -s /path/to/MeOS/SKILL ~/.claude/skills/meos
```

### 项目级

```bash
mkdir -p .claude/skills
ln -s /path/to/MeOS/SKILL .claude/skills/meos
```

## 如何使用

### 初始化

```text
/meos
```

然后输入：

```text
Initialize MeOS from the available local history sources and create the first sanitized asset set.
```

### 刷新

```text
/meos
```

```text
Refresh the MeOS assets from new local material, but only promote stable rules.
```

### 应用

```text
/meos
```

```text
Apply MeOS for this task. Read only the minimum relevant assets and use them to shape reasoning, workflow, and output.
```

## 验证

```bash
cd /path/to/MeOS
claude -p '/meos
Use meos in apply mode for this task. In 3 short bullets, say what you would read first and why.'
```

## 备注

- Claude Code 会自动发现嵌套目录下的 `.claude/skills/`。
- `SKILL.md` 里引用的 supporting files 可以按需加载。
- 如果你想专门使用 MiniMax，请看单独文档：[12 Claude Code + MiniMax](12_CLAUDE_CODE_MINIMAX.md)。
