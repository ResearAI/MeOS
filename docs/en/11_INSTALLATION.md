# 11 Installation

MeOS supports two installation styles:

- local shell install
- npm wrapper install

## Option A: local shell install

From the repository root:

```bash
bash install.sh --runtime codex
```

Important defaults:

- `--mode auto` is the default
- `auto` uses `copy` for OpenClaw and `symlink` for the other runtimes
- installing `--runtime all` is possible, but explicit per-runtime installs are cleaner

Useful flags:

```bash
bash install.sh --runtime codex
bash install.sh --runtime claude
bash install.sh --runtime openclaw
bash install.sh --runtime openclaw --mode copy --force
bash install.sh --runtime opencode
bash install.sh --runtime all --dry-run
bash install.sh --runtime codex --scope project --project-dir /path/to/project
```

## Option B: direct Python installer

```bash
python3 installer.py install --runtime codex
python3 installer.py doctor
python3 installer.py print-prompts --lang en
python3 installer.py print-prompts --lang zh
```

## Option C: npm wrapper

From the repository root:

```bash
npm install -g .
meos install --runtime codex
```

Useful commands:

```bash
meos install --runtime claude
meos install --runtime openclaw --force
meos install --runtime opencode
meos doctor
meos print-prompts --lang zh
```

## Notes

- The installed skill directory name should be lowercase: `meos`
- `install` creates local private directories by default unless `--skip-private-layout` is used
- `doctor` checks repository layout and target install locations
- OpenClaw should usually use `copy` mode, because external symlink roots are skipped
- OpenCode should usually use one compatible skill directory only, otherwise duplicate warnings are expected
- If you are replacing an older symlink install with a copied install, add `--force`
