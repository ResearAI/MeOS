# 06 Codex Setup

## Official skill locations

Codex documents these skill locations:

- repo-local: `.agents/skills/`
- user-global: `~/.agents/skills/`
- admin: `/etc/codex/skills`

Codex can activate skills:

- explicitly, by mentioning a skill in the prompt or via `/skills`
- implicitly, when the task matches the skill `description`

## Recommended install for MeOS

Because the skill name is `meos`, install it into a lowercase directory:

### User-global

```bash
mkdir -p ~/.agents/skills
ln -s /path/to/MeOS/SKILL ~/.agents/skills/meos
```

### Repo-local

```bash
mkdir -p .agents/skills
ln -s /path/to/MeOS/SKILL .agents/skills/meos
```

If symlinks are inconvenient, copy the contents of `MeOS/SKILL` into a folder named `meos`.

## How to use

### Initialize

Ask Codex to initialize MeOS from local source material:

```text
Use meos in init mode. Build the first sanitized operating-layer assets from the local history sources.
```

### Refresh

```text
Use meos in refresh mode. Update the existing MeOS assets from newly added local history without duplicating stale rules.
```

### Apply

```text
Use meos in apply mode for this task. Read only the minimum relevant assets and follow the owner's SOP, preferences, and correction rules while you work.
```

## Notes

- Keep the `description` specific so Codex can invoke it implicitly when appropriate.
- If a newly edited skill does not appear immediately, restarting Codex is the safest fallback.
