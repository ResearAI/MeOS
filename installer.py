#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
SKILL_ROOT = REPO_ROOT / "SKILL"
SKILL_DIRNAME = "meos"
SKIP_COPY_NAMES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
}

PROMPTS = {
    "en": {
        "init": "Use meos in init mode. Build the first sanitized operating-layer assets from the available local source material. Do not promote one-off behavior into stable assets.",
        "refresh": "Use meos in refresh mode. Refresh the existing MeOS assets from new local material. Prefer merge over duplication, preserve corrections as highest priority, and keep weak or conflicting facts in evidence only.",
        "apply": "Use meos in apply mode for this task. Read only the minimum relevant live assets and let them shape reasoning, workflow, output, and correction handling.",
    },
    "zh": {
        "init": "使用 meos 的 init 模式。请从当前可用的本地材料中建立第一版去隐私、保守的资产集合，不要把一次性行为直接升级成长期规则。",
        "refresh": "使用 meos 的 refresh 模式。请根据新增材料刷新已有资产，优先 merge，不要重复建规则；corrections 优先级最高；弱证据或冲突证据只留在 evidence。",
        "apply": "使用 meos 的 apply 模式处理这个任务。只读取最相关的 live assets，用它们来影响 reasoning、workflow、输出风格和 correction handling。",
    },
}


@dataclass(frozen=True)
class InstallTarget:
    runtime: str
    scope: str
    path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MeOS installer and helper CLI")
    subparsers = parser.add_subparsers(dest="command", required=False)

    install = subparsers.add_parser("install", help="Install MeOS into one or more runtimes")
    install.add_argument("--runtime", choices=["codex", "claude", "openclaw", "opencode", "all"], default="all")
    install.add_argument("--scope", choices=["global", "project"], default="global")
    install.add_argument("--project-dir", default=None, help="Project directory when --scope project is used")
    install.add_argument(
        "--mode",
        choices=["auto", "symlink", "copy"],
        default="auto",
        help="Install mode. auto uses runtime-safe defaults (copy for OpenClaw, symlink elsewhere).",
    )
    install.add_argument("--force", action="store_true", help="Replace an existing target if it differs")
    install.add_argument("--dry-run", action="store_true", help="Print actions without modifying the filesystem")
    install.add_argument("--skip-private-layout", action="store_true", help="Do not create local private directories")
    install.add_argument("--codex-dir", default=None, help="Override the Codex skill root for testing or custom install")
    install.add_argument("--claude-dir", default=None, help="Override the Claude Code skill root for testing or custom install")
    install.add_argument("--openclaw-dir", default=None, help="Override the OpenClaw skill root for testing or custom install")
    install.add_argument("--opencode-dir", default=None, help="Override the OpenCode skill root for testing or custom install")

    doctor = subparsers.add_parser("doctor", help="Check MeOS install targets and repository layout")
    doctor.add_argument("--project-dir", default=None)
    doctor.add_argument("--codex-dir", default=None)
    doctor.add_argument("--claude-dir", default=None)
    doctor.add_argument("--openclaw-dir", default=None)
    doctor.add_argument("--opencode-dir", default=None)

    prompts = subparsers.add_parser("print-prompts", help="Print suggested init/refresh/apply prompts")
    prompts.add_argument("--lang", choices=["en", "zh"], default="en")

    parser.set_defaults(command="install")
    return parser.parse_args()


def ensure_repo_layout() -> list[str]:
    required = [
        SKILL_ROOT / "SKILL.md",
        REPO_ROOT / "README.md",
        SKILL_ROOT / "references",
        SKILL_ROOT / "schemas",
        SKILL_ROOT / "assets",
        REPO_ROOT / "docs",
    ]
    missing = [str(path) for path in required if not path.exists()]
    return missing


def ensure_private_layout(dry_run: bool = False) -> list[Path]:
    targets = [
        SKILL_ROOT / "assets" / "live",
        SKILL_ROOT / "private" / "imported",
        SKILL_ROOT / "private" / "raw",
        SKILL_ROOT / "private" / "snapshots",
        SKILL_ROOT / "evidence",
        SKILL_ROOT / "runtime",
    ]
    created: list[Path] = []
    for target in targets:
        if target.exists():
            continue
        created.append(target)
        if not dry_run:
            target.mkdir(parents=True, exist_ok=True)
    return created


def resolve_targets(args: argparse.Namespace) -> list[InstallTarget]:
    runtimes = ["codex", "claude", "openclaw", "opencode"] if args.runtime == "all" else [args.runtime]
    scope = args.scope
    project_dir = Path(args.project_dir).expanduser().resolve() if args.project_dir else None
    if scope == "project" and project_dir is None:
        raise SystemExit("--project-dir is required when --scope project is used")

    home = Path.home()
    custom_roots = {
        "codex": Path(args.codex_dir).expanduser() if args.codex_dir else None,
        "claude": Path(args.claude_dir).expanduser() if args.claude_dir else None,
        "openclaw": Path(args.openclaw_dir).expanduser() if args.openclaw_dir else None,
        "opencode": Path(args.opencode_dir).expanduser() if args.opencode_dir else None,
    }

    resolved: list[InstallTarget] = []
    for runtime in runtimes:
        root = custom_roots[runtime]
        if root is None:
            if scope == "global":
                if runtime == "codex":
                    root = home / ".agents" / "skills"
                elif runtime == "claude":
                    root = home / ".claude" / "skills"
                elif runtime == "openclaw":
                    root = home / ".openclaw" / "skills"
                elif runtime == "opencode":
                    root = home / ".config" / "opencode" / "skills"
            else:
                assert project_dir is not None
                if runtime == "codex":
                    root = project_dir / ".agents" / "skills"
                elif runtime == "claude":
                    root = project_dir / ".claude" / "skills"
                elif runtime == "openclaw":
                    root = project_dir / "skills"
                elif runtime == "opencode":
                    root = project_dir / ".opencode" / "skills"
        assert root is not None
        resolved.append(InstallTarget(runtime=runtime, scope=scope, path=root / SKILL_DIRNAME))
    return resolved


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def copy_repo(src: Path, dst: Path) -> None:
    def _ignore(directory: str, names: list[str]) -> set[str]:
        ignored = {name for name in names if name in SKIP_COPY_NAMES}
        if Path(directory).resolve() == src.resolve():
            ignored.update({".git"})
        return ignored

    shutil.copytree(src, dst, symlinks=True, ignore=_ignore)


def path_is_within_root(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def resolve_install_mode(target: InstallTarget, requested_mode: str) -> str:
    if requested_mode != "auto":
        return requested_mode
    if target.runtime == "openclaw":
        return "copy"
    return "symlink"


def openclaw_external_symlink(path: Path) -> bool:
    if not path.is_symlink():
        return False
    try:
        return not path_is_within_root(path.resolve(), path.parent.resolve())
    except FileNotFoundError:
        return False


def duplicate_warnings(home: Path) -> list[str]:
    warnings: list[str] = []
    visible = {
        "codex": home / ".agents" / "skills" / SKILL_DIRNAME,
        "claude": home / ".claude" / "skills" / SKILL_DIRNAME,
        "openclaw": home / ".openclaw" / "skills" / SKILL_DIRNAME,
        "opencode": home / ".config" / "opencode" / "skills" / SKILL_DIRNAME,
    }
    existing = {name: path for name, path in visible.items() if path.exists() or path.is_symlink()}

    if sum(name in existing for name in ("codex", "claude", "opencode")) > 1:
        warnings.append(
            "OpenCode searches ~/.config/opencode/skills, ~/.claude/skills, and ~/.agents/skills. "
            "Installing MeOS in more than one of those paths causes duplicate-skill warnings."
        )
    if sum(name in existing for name in ("codex", "openclaw")) > 1:
        warnings.append(
            "OpenClaw searches both ~/.openclaw/skills and ~/.agents/skills. "
            "Installing MeOS in both paths causes duplicate-skill warnings."
        )
    return warnings


def install_target(target: InstallTarget, *, mode: str, force: bool, dry_run: bool) -> str:
    actual_mode = resolve_install_mode(target, mode)
    target.path.parent.mkdir(parents=True, exist_ok=True) if not dry_run else None
    if target.path.exists() or target.path.is_symlink():
        if target.path.is_symlink() and target.path.resolve() == SKILL_ROOT.resolve():
            if actual_mode == "symlink":
                return f"[skip] {target.runtime}: already linked at {target.path}"
            if not force:
                return (
                    f"[skip] {target.runtime}: existing symlink at {target.path} is incompatible with "
                    f"requested {actual_mode} mode (use --force to replace)"
                )
        if not force:
            return f"[skip] {target.runtime}: target exists at {target.path} (use --force to replace)"
        if not dry_run:
            remove_path(target.path)
    if dry_run:
        return f"[dry-run] {target.runtime}: would {actual_mode} install to {target.path}"
    if actual_mode == "symlink":
        os.symlink(SKILL_ROOT, target.path, target_is_directory=True)
    else:
        copy_repo(SKILL_ROOT, target.path)
    return f"[ok] {target.runtime}: installed to {target.path} using {actual_mode}"


def command_install(args: argparse.Namespace) -> int:
    missing = ensure_repo_layout()
    if missing:
        print("Missing required repository files:")
        for item in missing:
            print(f"- {item}")
        return 1

    if not args.skip_private_layout:
        created = ensure_private_layout(dry_run=args.dry_run)
    else:
        created = []
    targets = resolve_targets(args)
    messages = [install_target(target, mode=args.mode, force=args.force, dry_run=args.dry_run) for target in targets]

    print("MeOS install summary")
    print(f"- repository: {REPO_ROOT}")
    print(f"- skill-source: {SKILL_ROOT}")
    print(f"- mode: {args.mode}")
    print(f"- scope: {args.scope}")
    for line in messages:
        print(line)
    for warning in duplicate_warnings(Path.home()):
        print(f"- warning: {warning}")
    if created:
        print("- local private layout:")
        for path in created:
            print(f"  - {path}")
    print("\nSuggested next prompts:\n")
    for key, value in PROMPTS["en"].items():
        print(f"{key}: {value}\n")
    return 0


def command_doctor(args: argparse.Namespace) -> int:
    missing = ensure_repo_layout()
    targets = resolve_targets(argparse.Namespace(
        runtime="all",
        scope="project" if args.project_dir else "global",
        project_dir=args.project_dir,
        codex_dir=args.codex_dir,
        claude_dir=args.claude_dir,
        openclaw_dir=args.openclaw_dir,
        opencode_dir=args.opencode_dir,
    ))
    print("MeOS doctor")
    print(f"- repository: {REPO_ROOT}")
    print(f"- skill-source: {SKILL_ROOT}")
    print(f"- repository_layout_ok: {not missing}")
    if missing:
        for item in missing:
            print(f"  missing: {item}")
    for target in targets:
        exists = target.path.exists() or target.path.is_symlink()
        print(f"- {target.runtime}: {'installed' if exists else 'missing'} -> {target.path}")
        if target.runtime == "openclaw" and openclaw_external_symlink(target.path):
            print("  warning: OpenClaw skips symlinked skill roots whose realpath escapes the configured root; use copy mode.")
    for warning in duplicate_warnings(Path.home()):
        print(f"- warning: {warning}")
    return 0 if not missing else 1


def command_print_prompts(args: argparse.Namespace) -> int:
    bundle = PROMPTS[args.lang]
    for key in ("init", "refresh", "apply"):
        print(f"{key}:")
        print(bundle[key])
        print()
    return 0


def main() -> int:
    args = parse_args()
    if args.command == "install":
        return command_install(args)
    if args.command == "doctor":
        return command_doctor(args)
    if args.command == "print-prompts":
        return command_print_prompts(args)
    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
