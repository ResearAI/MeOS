#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import sys
import webbrowser
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent
SKILL_ROOT = REPO_ROOT / "SKILL"
GRAPH_TEMPLATE_PATH = SKILL_ROOT / "references" / "owner-graph-view.template.html"
SOURCE_IS_PACKAGED_INSTALL = "node_modules" in REPO_ROOT.parts or not (REPO_ROOT / ".git").exists()
SKILL_DIRNAME = "meos"
DEFAULT_GRAPH_HOST = "127.0.0.1"
DEFAULT_GRAPH_PORT = 20998
GRAPH_OUTPUT_DIRNAME = "graph"
GRAPH_JSON_FILENAME = "owner-graph.json"
GRAPH_HTML_FILENAME = "owner-graph.html"
GRAPH_INDEX_FILENAME = "index.html"
ALIGNMENT_PACKET_FILENAME = "alignment-packet.json"
STABILITY_ORDER = {
    "stable": 0,
    "candidate": 1,
    "weak": 2,
}
DIMENSION_ORDER = {
    "role": 0,
    "interest": 1,
    "preference": 2,
    "behavior": 3,
    "workflow": 4,
    "principle": 5,
    "constraint": 6,
    "knowledge": 7,
    "taste": 8,
}
DIMENSION_COLORS = {
    "role": "#e57a44",
    "interest": "#c95b73",
    "preference": "#1c8c72",
    "behavior": "#2c6ed5",
    "workflow": "#7b5ad9",
    "principle": "#d19b2f",
    "constraint": "#b24343",
    "knowledge": "#177e89",
    "taste": "#8a4fff",
    "subject": "#4f5f73",
    "owner": "#111111",
    "unknown": "#7f8b99",
}
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

    graph = subparsers.add_parser("graph", help="Build and preview local MeOS person-graph outputs")
    graph_subparsers = graph.add_subparsers(dest="graph_command", required=True)

    graph_build = graph_subparsers.add_parser("build", help="Build graph JSON, alignment packet, and HTML preview")
    graph_build.add_argument("--skill-root", default=None, help="Path to a MeOS skill root or repository root")
    graph_build.add_argument("--owner-id", default="owner", help="Fallback owner id when claims do not use `owner`")
    graph_build.add_argument("--host", default=DEFAULT_GRAPH_HOST, help="Preview host to print in next-step instructions")
    graph_build.add_argument("--port", type=int, default=DEFAULT_GRAPH_PORT, help="Preview port to print in next-step instructions")

    graph_serve = graph_subparsers.add_parser("serve", help="Build the graph outputs and serve them locally")
    graph_serve.add_argument("--skill-root", default=None, help="Path to a MeOS skill root or repository root")
    graph_serve.add_argument("--owner-id", default="owner", help="Fallback owner id when claims do not use `owner`")
    graph_serve.add_argument("--host", default=DEFAULT_GRAPH_HOST, help="Local bind host")
    graph_serve.add_argument("--port", type=int, default=DEFAULT_GRAPH_PORT, help="Local bind port")
    graph_serve.add_argument("--open-browser", action="store_true", help="Open the preview URL in the default browser")

    parser.set_defaults(command="install")
    return parser.parse_args()


def ensure_repo_layout() -> list[str]:
    required = [
        SKILL_ROOT / "SKILL.md",
        REPO_ROOT / "README.md",
        SKILL_ROOT / "references",
        SKILL_ROOT / "schemas",
        SKILL_ROOT / "assets",
    ]
    missing = [str(path) for path in required if not path.exists()]
    return missing


def ensure_private_layout(skill_root: Path, dry_run: bool = False) -> list[Path]:
    targets = [
        skill_root / "assets" / "live",
        skill_root / "private" / "imported",
        skill_root / "private" / "raw",
        skill_root / "private" / "snapshots",
        skill_root / "evidence",
        skill_root / "runtime",
        skill_root / "runtime" / GRAPH_OUTPUT_DIRNAME,
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
    if SOURCE_IS_PACKAGED_INSTALL:
        return "copy"
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

    created: list[Path] = []
    target_created: list[Path] = []
    if not args.skip_private_layout and not SOURCE_IS_PACKAGED_INSTALL:
        created = ensure_private_layout(SKILL_ROOT, dry_run=args.dry_run)
    targets = resolve_targets(args)
    messages = [install_target(target, mode=args.mode, force=args.force, dry_run=args.dry_run) for target in targets]
    if not args.skip_private_layout and not args.dry_run:
        for target in targets:
            if target.path.exists() and not target.path.is_symlink():
                target_created.extend(ensure_private_layout(target.path, dry_run=False))

    print("MeOS install summary")
    print(f"- repository: {REPO_ROOT}")
    print(f"- skill-source: {SKILL_ROOT}")
    print(f"- source_kind: {'packaged' if SOURCE_IS_PACKAGED_INSTALL else 'repository'}")
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
    if target_created:
        print("- installed private layout:")
        for path in target_created:
            print(f"  - {path}")
    if SOURCE_IS_PACKAGED_INSTALL and not args.skip_private_layout:
        print("- note: packaged installs use copied runtime skill directories so mutable local assets do not live inside node_modules.")
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


def normalize_skill_root(path: Path) -> Path:
    candidate = path.expanduser().resolve()
    if (candidate / "SKILL.md").exists():
        return candidate
    if (candidate / "SKILL" / "SKILL.md").exists():
        return candidate / "SKILL"
    raise SystemExit(f"Could not find a MeOS skill root from {candidate}")


def detect_skill_root(start: Path) -> Path | None:
    current = start.expanduser().resolve()
    for candidate in (current, *current.parents):
        if (candidate / "SKILL.md").exists():
            return candidate
        if (candidate / "SKILL" / "SKILL.md").exists():
            return candidate / "SKILL"
    return None


def resolve_skill_root(path_value: str | None) -> Path:
    if path_value:
        return normalize_skill_root(Path(path_value))
    detected = detect_skill_root(Path.cwd())
    if detected is not None:
        return detected
    return SKILL_ROOT


def ensure_graph_runtime_layout(skill_root: Path) -> Path:
    graph_root = skill_root / "runtime" / GRAPH_OUTPUT_DIRNAME
    graph_root.mkdir(parents=True, exist_ok=True)
    (skill_root / "evidence").mkdir(parents=True, exist_ok=True)
    return graph_root


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "item"


def humanize(value: str) -> str:
    text = value.replace("_", " ").replace("-", " ")
    text = text.replace("::", ": ").replace(":", ": ")
    text = re.sub(r"\s+", " ", text).strip()
    return text or value


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def claim_sort_key(claim: dict[str, Any]) -> tuple[Any, ...]:
    return (
        STABILITY_ORDER.get(str(claim.get("stability", "candidate")), 99),
        DIMENSION_ORDER.get(str(claim.get("dimension", "")), 99),
        -float(claim.get("confidence", 0.0)),
        str(claim.get("scope", "")),
        str(claim.get("object", "")),
        str(claim.get("id", "")),
    )


def sanitize_claim(raw: dict[str, Any], *, line_number: int) -> dict[str, Any]:
    evidence_ids = raw.get("evidence_ids", [])
    if not isinstance(evidence_ids, list):
        evidence_ids = [evidence_ids]
    conflicts_with = raw.get("conflicts_with", [])
    if not isinstance(conflicts_with, list):
        conflicts_with = [conflicts_with]

    confidence_raw = raw.get("confidence", 0.5)
    try:
        confidence = clamp(float(confidence_raw), 0.0, 1.0)
    except (TypeError, ValueError):
        confidence = 0.5

    dimension = str(raw.get("dimension", "preference"))
    stability = str(raw.get("stability", "candidate"))
    explicitness = str(raw.get("explicitness", "inferred"))

    return {
        "id": str(raw.get("id") or f"claim_{line_number:04d}"),
        "subject": str(raw.get("subject") or "owner"),
        "dimension": dimension,
        "predicate": str(raw.get("predicate") or "relates_to"),
        "object": str(raw.get("object") or "unspecified"),
        "scope": str(raw.get("scope") or "global"),
        "explicitness": explicitness,
        "stability": stability,
        "confidence": round(confidence, 4),
        "evidence_ids": [str(item) for item in evidence_ids if str(item)],
        "first_seen": str(raw.get("first_seen") or ""),
        "last_seen": str(raw.get("last_seen") or ""),
        "conflicts_with": [str(item) for item in conflicts_with if str(item)],
    }


def load_claims(claims_path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    if not claims_path.exists():
        return [], [f"claims ledger not found at {claims_path}; generated an empty preview shell"]

    claims: list[dict[str, Any]] = []
    warnings: list[str] = []
    for line_number, line in enumerate(claims_path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON in {claims_path}:{line_number}: {exc.msg}") from exc
        if not isinstance(payload, dict):
            raise SystemExit(f"Invalid claim entry in {claims_path}:{line_number}: expected a JSON object")
        claims.append(sanitize_claim(payload, line_number=line_number))

    if not claims:
        warnings.append(f"claims ledger at {claims_path} is empty; generated an empty preview shell")

    claims.sort(key=claim_sort_key)
    return claims, warnings


def infer_owner_id(claims: list[dict[str, Any]], fallback: str) -> str:
    if not claims:
        return fallback
    subjects = Counter(str(claim.get("subject") or fallback) for claim in claims)
    if fallback != "owner":
        return fallback
    if "owner" in subjects:
        return "owner"
    return subjects.most_common(1)[0][0]


def summarize_claim(claim: dict[str, Any], *, include_scope: bool = True) -> str:
    body = f"{humanize(str(claim['predicate']))} {humanize(str(claim['object']))}".strip()
    if include_scope and claim.get("scope") and claim["scope"] != "global":
        return f"{body} [{claim['scope']}]"
    return body


def unique_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def take_claim_summaries(
    claims: list[dict[str, Any]],
    *,
    dimensions: set[str] | None = None,
    predicate_names: set[str] | None = None,
    scoped_only: bool = False,
    limit: int = 8,
) -> list[str]:
    selected: list[str] = []
    for claim in claims:
        dimension = str(claim.get("dimension", ""))
        predicate = str(claim.get("predicate", ""))
        if dimensions is not None and dimension not in dimensions:
            continue
        if predicate_names is not None and predicate not in predicate_names:
            continue
        if scoped_only and claim.get("scope") == "global":
            continue
        selected.append(summarize_claim(claim))
    return unique_preserve_order(selected)[:limit]


def compile_alignment_packet(claims: list[dict[str, Any]]) -> dict[str, Any]:
    stable_claims = [claim for claim in claims if claim.get("stability") == "stable"]
    output_preferences = take_claim_summaries(stable_claims, dimensions={"preference", "taste"}, limit=10)
    constraints = take_claim_summaries(
        stable_claims,
        dimensions={"constraint"},
        limit=10,
    )
    avoided = take_claim_summaries(
        stable_claims,
        predicate_names={"avoids", "overrides"},
        limit=10,
    )
    return {
        "tone": take_claim_summaries(stable_claims, dimensions={"taste", "preference"}, limit=6),
        "reasoning_style": take_claim_summaries(stable_claims, dimensions={"principle", "behavior", "knowledge"}, limit=8),
        "workflow_style": take_claim_summaries(stable_claims, dimensions={"workflow"}, limit=8),
        "output_preferences": unique_preserve_order(output_preferences + avoided)[:10],
        "constraints": unique_preserve_order(constraints + avoided)[:10],
        "task_scoped_traits": take_claim_summaries(stable_claims, scoped_only=True, limit=10),
        "active_scope": unique_preserve_order([str(claim.get("scope", "global")) for claim in stable_claims])[:10],
        "source_claim_ids": [str(claim["id"]) for claim in stable_claims],
    }


def build_graph_projection(claims: list[dict[str, Any]], owner_id: str, claims_path: Path) -> dict[str, Any]:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    nodes_by_id: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []

    def ensure_node(node_id: str, *, label: str, node_type: str, dimension: str | None = None) -> dict[str, Any]:
        node = nodes_by_id.get(node_id)
        if node is None:
            color_key = dimension or node_type
            node = {
                "id": node_id,
                "label": label,
                "type": node_type,
                "dimension": dimension,
                "color": DIMENSION_COLORS.get(color_key, DIMENSION_COLORS["unknown"]),
                "claim_ids": [],
                "scopes": [],
                "stability_levels": [],
            }
            nodes_by_id[node_id] = node
        return node

    ensure_node(owner_id, label=humanize(owner_id), node_type="owner", dimension="owner")

    for claim in claims:
        source_subject = str(claim.get("subject") or owner_id)
        source_id = source_subject
        source_type = "owner" if source_subject == owner_id else "subject"
        ensure_node(source_id, label=humanize(source_subject), node_type=source_type, dimension=source_type)

        object_value = str(claim.get("object") or "unspecified")
        dimension = str(claim.get("dimension") or "preference")
        target_id = f"{dimension}:{slugify(object_value)}"
        target_node = ensure_node(
            target_id,
            label=humanize(object_value),
            node_type=dimension,
            dimension=dimension,
        )
        target_node["claim_ids"].append(claim["id"])
        target_node["scopes"].append(str(claim.get("scope") or "global"))
        target_node["stability_levels"].append(str(claim.get("stability") or "candidate"))

        edges.append(
            {
                "id": str(claim["id"]),
                "source": source_id,
                "target": target_id,
                "predicate": str(claim.get("predicate") or "relates_to"),
                "label": humanize(str(claim.get("predicate") or "relates_to")),
                "dimension": dimension,
                "scope": str(claim.get("scope") or "global"),
                "stability": str(claim.get("stability") or "candidate"),
                "confidence": float(claim.get("confidence", 0.5)),
                "explicitness": str(claim.get("explicitness") or "inferred"),
                "evidence_ids": claim.get("evidence_ids", []),
                "first_seen": str(claim.get("first_seen") or ""),
                "last_seen": str(claim.get("last_seen") or ""),
            }
        )

    nodes: list[dict[str, Any]] = []
    for node in nodes_by_id.values():
        node["claim_ids"] = unique_preserve_order([str(item) for item in node["claim_ids"]])
        node["scopes"] = unique_preserve_order([str(item) for item in node["scopes"]])
        node["stability_levels"] = unique_preserve_order([str(item) for item in node["stability_levels"]])
        nodes.append(node)

    nodes.sort(
        key=lambda node: (
            0 if node["id"] == owner_id else 1,
            0 if node["type"] == "owner" else 1,
            DIMENSION_ORDER.get(str(node.get("dimension") or node["type"]), 99),
            str(node["label"]).lower(),
        )
    )
    edges.sort(key=lambda edge: claim_sort_key(edge))

    stability_counts = Counter(str(claim.get("stability") or "candidate") for claim in claims)
    dimension_counts = Counter(str(claim.get("dimension") or "unknown") for claim in claims)
    scope_counts = Counter(str(claim.get("scope") or "global") for claim in claims)
    average_confidence = round(
        sum(float(claim.get("confidence", 0.0)) for claim in claims) / len(claims),
        4,
    ) if claims else 0.0

    return {
        "owner_id": owner_id,
        "generated_at": timestamp,
        "metadata": {
            "claim_count": len(claims),
            "node_count": len(nodes),
            "edge_count": len(edges),
            "stable_claim_count": stability_counts.get("stable", 0),
            "candidate_claim_count": stability_counts.get("candidate", 0),
            "weak_claim_count": stability_counts.get("weak", 0),
            "average_confidence": average_confidence,
            "dimension_counts": dict(sorted(dimension_counts.items(), key=lambda item: DIMENSION_ORDER.get(item[0], 99))),
            "scope_counts": dict(sorted(scope_counts.items())),
            "claims_source": str(claims_path),
        },
        "claims": claims,
        "nodes": nodes,
        "edges": edges,
    }


def json_for_html(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2).replace("</", "<\\/")


def load_graph_template() -> str:
    if not GRAPH_TEMPLATE_PATH.exists():
        raise SystemExit(f"Missing graph viewer template: {GRAPH_TEMPLATE_PATH}")
    return GRAPH_TEMPLATE_PATH.read_text(encoding="utf-8")


def render_graph_html(
    *,
    graph_data: dict[str, Any],
    alignment_packet: dict[str, Any],
    preview_url: str,
    serve_command: str,
) -> str:
    template = load_graph_template()
    replacements = {
        "__GRAPH_TITLE__": f"MeOS Graph Preview: {humanize(str(graph_data['owner_id']))}",
        "__GRAPH_DATA__": json_for_html(graph_data),
        "__ALIGNMENT_DATA__": json_for_html(alignment_packet),
        "__GRAPH_JSON_FILENAME__": GRAPH_JSON_FILENAME,
        "__ALIGNMENT_JSON_FILENAME__": ALIGNMENT_PACKET_FILENAME,
        "__PREVIEW_URL__": preview_url,
        "__SERVE_COMMAND__": serve_command,
    }
    rendered = template
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    return rendered


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_graph_outputs(skill_root: Path, *, owner_id: str, host: str, port: int) -> dict[str, Any]:
    graph_root = ensure_graph_runtime_layout(skill_root)
    claims_path = skill_root / "evidence" / "claims.jsonl"
    claims, warnings = load_claims(claims_path)
    resolved_owner_id = infer_owner_id(claims, owner_id)
    graph_data = build_graph_projection(claims, resolved_owner_id, claims_path)
    alignment_packet = compile_alignment_packet(claims)

    graph_json_path = graph_root / GRAPH_JSON_FILENAME
    alignment_path = graph_root / ALIGNMENT_PACKET_FILENAME
    html_path = graph_root / GRAPH_HTML_FILENAME
    index_path = graph_root / GRAPH_INDEX_FILENAME
    preview_url = f"http://{host}:{port}/"
    serve_command = (
        f"meos graph serve --skill-root {shlex.quote(str(skill_root))} "
        f"--host {host} --port {port}"
    )
    html = render_graph_html(
        graph_data=graph_data,
        alignment_packet=alignment_packet,
        preview_url=preview_url,
        serve_command=serve_command,
    )

    write_json(graph_json_path, graph_data)
    write_json(alignment_path, alignment_packet)
    html_path.write_text(html, encoding="utf-8")
    index_path.write_text(html, encoding="utf-8")

    return {
        "skill_root": skill_root,
        "graph_root": graph_root,
        "claims_path": claims_path,
        "graph_json_path": graph_json_path,
        "alignment_path": alignment_path,
        "html_path": html_path,
        "index_path": index_path,
        "preview_url": preview_url,
        "preview_html_url": f"http://{host}:{port}/{GRAPH_HTML_FILENAME}",
        "serve_command": serve_command,
        "warnings": warnings,
        "claim_count": len(claims),
        "stable_claim_count": graph_data["metadata"]["stable_claim_count"],
        "owner_id": resolved_owner_id,
    }


def print_graph_build_summary(summary: dict[str, Any]) -> None:
    print("MeOS graph build summary")
    print(f"- skill-root: {summary['skill_root']}")
    print(f"- claims-source: {summary['claims_path']}")
    print(f"- owner-id: {summary['owner_id']}")
    print(f"- claims-loaded: {summary['claim_count']}")
    print(f"- stable-claims: {summary['stable_claim_count']}")
    print(f"- graph-json: {summary['graph_json_path']}")
    print(f"- alignment-packet: {summary['alignment_path']}")
    print(f"- html-preview: {summary['html_path']}")
    print(f"- index-preview: {summary['index_path']}")
    print(f"- local-preview-url: {summary['preview_url']}")
    print(f"- local-preview-file: {summary['html_path']}")
    print(f"- next-step: {summary['serve_command']}")
    for warning in summary["warnings"]:
        print(f"- note: {warning}")


class QuietSimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        return


class ReusableThreadingHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True


def command_graph_build(args: argparse.Namespace) -> int:
    skill_root = resolve_skill_root(args.skill_root)
    summary = build_graph_outputs(skill_root, owner_id=args.owner_id, host=args.host, port=args.port)
    print_graph_build_summary(summary)
    return 0


def command_graph_serve(args: argparse.Namespace) -> int:
    skill_root = resolve_skill_root(args.skill_root)
    summary = build_graph_outputs(skill_root, owner_id=args.owner_id, host=args.host, port=args.port)
    print_graph_build_summary(summary)
    handler = partial(QuietSimpleHTTPRequestHandler, directory=str(summary["graph_root"]))
    try:
        server = ReusableThreadingHTTPServer((args.host, args.port), handler)
    except OSError as exc:
        print(f"Failed to bind {args.host}:{args.port}: {exc}", file=sys.stderr)
        return 1

    print(f"- serving: {summary['graph_root']}")
    print(f"- open: {summary['preview_url']}")
    print("- stop: Ctrl+C")
    if args.open_browser:
        webbrowser.open(summary["preview_url"])
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nMeOS graph preview stopped")
    finally:
        server.server_close()
    return 0


def main() -> int:
    args = parse_args()
    if args.command == "install":
        return command_install(args)
    if args.command == "doctor":
        return command_doctor(args)
    if args.command == "print-prompts":
        return command_print_prompts(args)
    if args.command == "graph" and args.graph_command == "build":
        return command_graph_build(args)
    if args.command == "graph" and args.graph_command == "serve":
        return command_graph_serve(args)
    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
