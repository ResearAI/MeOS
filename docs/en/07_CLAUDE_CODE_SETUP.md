# 07 Claude Code Setup

## Official skill locations

Claude Code supports:

- personal skills: `~/.claude/skills/<skill-name>/SKILL.md`
- project skills: `.claude/skills/<skill-name>/SKILL.md`
- plugin skills

Claude can use a skill automatically when the task matches the `description`, or directly via `/<skill-name>`.

## Recommended install for MeOS

Install into a lowercase directory named `meos`.

### Personal

```bash
mkdir -p ~/.claude/skills
ln -s /path/to/MeOS/SKILL ~/.claude/skills/meos
```

### Project-local

```bash
mkdir -p .claude/skills
ln -s /path/to/MeOS/SKILL .claude/skills/meos
```

Claude also supports nested project discovery under subdirectories.

## How to use

### Initialize

```text
/meos
```

Then instruct it to run in `init` mode:

```text
Initialize MeOS from the available local history sources and create the first sanitized asset set.
```

### Refresh

```text
/meos
```

```text
Refresh the MeOS assets from new local material, but only promote stable rules.
```

### Apply

```text
/meos
```

```text
Apply MeOS for this task. Read only the minimum relevant assets and use them to shape reasoning, workflow, and output.
```

## Verify

```bash
cd /path/to/MeOS
claude -p '/meos
Use meos in apply mode for this task. In 3 short bullets, say what you would read first and why.'
```

## Notes

- Claude discovers project-local skills automatically from nested `.claude/skills/` directories.
- Supporting files referenced from `SKILL.md` can be loaded on demand.
- If you want MiniMax specifically, use the separate guide: [12 Claude Code With MiniMax](12_CLAUDE_CODE_MINIMAX.md).
