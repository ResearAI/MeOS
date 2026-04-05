# 12 Claude Code With MiniMax

This guide is intentionally separate from the main Claude Code setup so the normal MeOS install path stays simple.

## What was manually verified

The following flow was tested successfully:

- Claude Code reached MiniMax through an Anthropic-compatible endpoint
- MeOS was discovered from `~/.claude/skills/meos`
- Claude could answer a MeOS `apply` prompt with `/meos`

## Minimal configuration

Install MeOS first:

```bash
mkdir -p ~/.claude/skills
ln -s /path/to/MeOS/SKILL ~/.claude/skills/meos
```

Then configure Claude Code to use the MiniMax Anthropic-compatible endpoint in `~/.claude/settings.json`:

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

Keep the actual API key in your shell environment or another local secret store.
Do not commit it.

## Verify the model path

```bash
claude -p --model MiniMax-M2.7 'Respond with exactly CLAUDE_MINIMAX_OK.'
```

Expected result:

```text
CLAUDE_MINIMAX_OK
```

## Verify MeOS loading

```bash
cd /path/to/MeOS
claude -p --model MiniMax-M2.7 '/meos
Use meos in apply mode for this task. In 3 short bullets, say what you would read first and why.'
```

If MeOS is loaded correctly, Claude should answer from the skill instead of ignoring it.

## Optional: manage Claude profiles with cc-switch

If you want a separate MiniMax profile:

```bash
npm install -g @hobeeliu/cc-switch
cc-switch current
cc-switch cp default minimax
cc-switch use minimax
```

If `cc-switch` starts with an empty profile store on a fresh machine, bootstrap the default Claude profile first, then copy it.

## Notes

- Keep the main MeOS Claude guide generic; put MiniMax-specific details here.
- If Claude responds normally without using `/meos`, re-check the install path and skill directory name.
- If the endpoint is slow, increase `API_TIMEOUT_MS` rather than editing MeOS.
