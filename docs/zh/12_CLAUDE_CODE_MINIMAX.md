# 12 Claude Code + MiniMax

这个文档单独拆出来，是为了让主 `Claude Code` 配置文档保持简单，不把 MiniMax 的细节塞进主流程。

## 已手动验证的结果

下面这条链路已经实际跑通：

- Claude Code 能通过 Anthropic 兼容端点访问 MiniMax
- MeOS 能从 `~/.claude/skills/meos` 被发现
- Claude 能通过 `/meos` 正常响应 `apply` 模式请求

## 最小配置

先安装 MeOS：

```bash
mkdir -p ~/.claude/skills
ln -s /path/to/MeOS ~/.claude/skills/meos
```

然后在 `~/.claude/settings.json` 中配置 MiniMax 的 Anthropic 兼容端点：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.minimaxi.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "${MINIMAX_API_KEY}",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

真实 API Key 请放在本地环境变量或你自己的 secret 管理方式里，不要提交进 git。

## 验证模型链路

```bash
claude -p --model MiniMax-M2.7 'Respond with exactly CLAUDE_MINIMAX_OK.'
```

预期输出：

```text
CLAUDE_MINIMAX_OK
```

## 验证 MeOS 是否被加载

```bash
cd /path/to/MeOS
claude -p --model MiniMax-M2.7 '/meos
Use meos in apply mode for this task. In 3 short bullets, say what you would read first and why.'
```

如果 MeOS 生效，Claude 会根据这个 skill 回答，而不是把它当普通文本忽略掉。

## 可选：用 cc-switch 管理 Claude 配置档

如果你希望单独维护一个 MiniMax 配置档：

```bash
npm install -g @hobeeliu/cc-switch
cc-switch current
cc-switch cp default minimax
cc-switch use minimax
```

如果 `cc-switch` 在新机器上没有初始化 profile，需要先让 Claude 默认配置存在，再去复制。

## 备注

- 主 `Claude Code` 文档保持通用，这里的内容只处理 MiniMax。
- 如果 Claude 正常回复但没有使用 `/meos`，优先检查安装目录和 skill 名是否是小写 `meos`。
- 如果端点响应慢，优先调大 `API_TIMEOUT_MS`，不要去改 MeOS 本身。
