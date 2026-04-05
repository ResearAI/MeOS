# 08 OpenClaw Setup

## Official skill locations

OpenClaw loads skills from several locations, including:

- `~/.openclaw/skills`
- `~/.agents/skills`
- `<workspace>/.agents/skills`
- `<workspace>/skills`

It also supports watcher-based auto-refresh for changed `SKILL.md` files.

## Important behavior from manual testing

- OpenClaw skips symlinked skill roots whose resolved realpath escapes the configured root.
- In practice, `ln -s /path/to/MeOS ~/.openclaw/skills/meos` is not reliable.
- The safest install is a real copied directory under `<workspace>/skills/meos` or `~/.openclaw/skills/meos`.
- If you create a new profile or agent, auth is isolated. A skill can be visible while model auth is still missing.

## Recommended install for MeOS

Install into a lowercase directory named `meos`.

### Workspace-local copy (recommended)

```bash
mkdir -p <workspace>/skills
cp -a /path/to/MeOS <workspace>/skills/meos
```

### Shared managed copy

```bash
mkdir -p ~/.openclaw/skills
cp -a /path/to/MeOS ~/.openclaw/skills/meos
```

### External shared skill root

```bash
openclaw config set skills.load.extraDirs '["/absolute/path/to/skills-root"]' --strict-json
```

If you use `skills.load.extraDirs`, point it at the parent directory that contains `meos/`.

## Verify installation

```bash
openclaw skills info meos
openclaw skills list | rg meos
```

If the skill is loaded correctly, `skills info` should show `Path: .../meos/SKILL.md`.

## Use MeOS in a local agent turn

OpenClaw requires `--agent`, `--to`, or `--session-id` to choose a session.

```bash
openclaw agent --local --agent main --json \
  --thinking minimal \
  --timeout 180 \
  --message 'Use meos in apply mode for this task. In 3 short bullets, say what you would read first and why.'
```

## Fully isolated manual test example

This is a tested pattern that does not depend on your main OpenClaw profile:

```bash
mkdir -p /tmp/openclaw-meos-test/skills
cp -a /path/to/MeOS /tmp/openclaw-meos-test/skills/meos

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

## Usage modes

Recommended task modes:

- `init`: first-time asset creation from local owner-approved source material
- `refresh`: update maintained assets from new material
- `apply`: use existing assets to guide the current agent task

## Notes

- Workspace `skills/` has the highest precedence.
- If agent skill allowlists are enabled, make sure `meos` is allowed for the relevant agent.
- OpenClaw can auto-refresh skills when `SKILL.md` changes if watcher support is enabled.
- If a new profile or agent reports missing auth, configure that profile first; skill discovery and provider auth are separate.
