# 09 OpenCode Setup

## Official skill locations

OpenCode searches these locations:

- `.opencode/skills/<name>/SKILL.md`
- `~/.config/opencode/skills/<name>/SKILL.md`
- `.claude/skills/<name>/SKILL.md`
- `~/.claude/skills/<name>/SKILL.md`
- `.agents/skills/<name>/SKILL.md`
- `~/.agents/skills/<name>/SKILL.md`

OpenCode loads skills on demand via its native `skill` tool.

## Important behavior from manual testing

- OpenCode is strict about skill naming.
- OpenCode searches several compatible skill directories, so installing `meos` into all of them at once causes duplicate-skill warnings.
- OpenAI-compatible providers may also need `small_model` set explicitly. Otherwise OpenCode can fail before the main turn, for example while generating a session title.

## Naming rules

OpenCode requires:

- `name` must be lowercase
- the containing directory must match the skill name

So MeOS should be installed into a directory named `meos`.

## Recommended install options

Choose one install path, not all of them.

### OpenCode-native

```bash
mkdir -p ~/.config/opencode/skills
ln -s /path/to/MeOS ~/.config/opencode/skills/meos
```

### Claude-compatible

```bash
mkdir -p ~/.claude/skills
ln -s /path/to/MeOS ~/.claude/skills/meos
```

### Agent-compatible

```bash
mkdir -p ~/.agents/skills
ln -s /path/to/MeOS ~/.agents/skills/meos
```

## Provider compatibility note

If your provider or proxy does not support OpenCode's default secondary title model, set `small_model` to something your provider supports:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "openai/gpt-5.4",
  "small_model": "openai/gpt-5.4"
}
```

Use a cheaper compatible model if your provider supports one reliably.

## Verify installation and skill loading

```bash
opencode run --model openai/gpt-5.4 --format json \
  'Use meos in apply mode for this task. In 3 short bullets, say what you would read first and why.'
```

In JSON output, a successful skill load looks like a `tool_use` event for `skill` with `name: "meos"`.

## Usage modes

OpenCode agents discover skills and can load them on demand.

Use MeOS in three ways:

- initialize the first asset set
- refresh the existing asset set
- apply the current asset set to a live task

## Notes

- Unknown frontmatter fields are ignored by OpenCode, so keep the core frontmatter minimal and standards-compliant.
- If you use per-agent permissions, ensure `meos` is allowed for the agent that should use it.
- If you already install MeOS via `~/.claude/skills` or `~/.agents/skills`, do not also install it into `~/.config/opencode/skills` unless you accept duplicate warnings.
