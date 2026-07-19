#!/usr/bin/env python3
"""Apply carinyaparc instance deployments to cloud platforms.

Usage:
  python3 scripts/deploy-squad-agents.py --dry-run --instance ../carinyaparc
  python3 scripts/deploy-squad-agents.py apply --instance ../carinyaparc
  python3 scripts/deploy-squad-agents.py apply --ritual weekly-planning --dry-run-first --instance ../carinyaparc
  python3 scripts/deploy-squad-agents.py pause|resume --id weekly-planning-product-manager --instance ../carinyaparc
  python3 scripts/deploy-squad-agents.py apply --run-now --ritual weekly-planning --instance ../carinyaparc

Reads:  {instance}/config/deployments/*.json
        {instance}/config/cadence/{ritual}.md
        managed-agents/{agent}/agent.yaml

Secrets (env): CURSOR_API_TOKEN, ANTHROPIC_ADMIN_KEY — never stored in repo.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CATALOGUE_ROOT = Path(__file__).resolve().parents[1]
PLATFORM_RE = re.compile(r"^platform:\s*(\S+)", re.MULTILINE)


def resolve_instance(raw: str) -> Path:
    path = Path(raw).expanduser().resolve()
    if not path.is_dir():
        print(f"error: instance path not found: {raw}", file=sys.stderr)
        sys.exit(1)
    return path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_platform(cookbook_platform: str, deployment_platform: str | None) -> str:
    if deployment_platform:
        return deployment_platform
    if cookbook_platform == "either":
        if os.environ.get("CURSOR_API_TOKEN"):
            return "cursor"
        if os.environ.get("ANTHROPIC_ADMIN_KEY"):
            return "claude-cma"
        return "either"
    return cookbook_platform


def validate_instance(instance: Path) -> None:
    if not (instance / "config" / "instance.json").is_file():
        print(f"error: missing {instance}/config/instance.json", file=sys.stderr)
        sys.exit(1)
    deployments_dir = instance / "config" / "deployments"
    if not deployments_dir.is_dir():
        print(f"error: missing {instance}/config/deployments/", file=sys.stderr)
        sys.exit(1)
    validator = instance / "scripts" / "validate-deployments.py"
    if validator.is_file():
        result = subprocess.run(
            [sys.executable, str(validator), str(instance)],
            check=False,
        )
        if result.returncode != 0:
            sys.exit(result.returncode)


def list_deployments(instance: Path) -> list[Path]:
    deployments_dir = instance / "config" / "deployments"
    return sorted(deployments_dir.glob("*.json"))


def load_deployment(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def cookbook_platform(cookbook: Path) -> str:
    text = cookbook.read_text()
    match = PLATFORM_RE.search(text)
    return match.group(1) if match else ""


def plan_deployment(instance: Path, deploy_file: Path) -> dict[str, Any]:
    data = load_deployment(deploy_file)
    agent = data.get("agent") or ""
    ritual = data.get("ritual")
    squad = data.get("squad") or ""
    platform = data.get("platform")
    enabled = data.get("enabled", True)
    deploy_id = data.get("id") or ""

    cookbook = CATALOGUE_ROOT / "managed-agents" / agent / "agent.yaml"
    if not cookbook.is_file():
        print(f"error: missing cookbook for agent '{agent}': {cookbook}", file=sys.stderr)
        sys.exit(1)

    resolved = resolve_platform(cookbook_platform(cookbook), platform)

    ritual_path: Path | None = None
    ritual_hash: str | None = None
    if ritual:
        ritual_path = instance / "config" / "cadence" / f"{ritual}.md"
        if not ritual_path.is_file():
            print(f"error: missing ritual {ritual_path}", file=sys.stderr)
            sys.exit(1)
        ritual_hash = sha256_file(ritual_path)

    return {
        "id": deploy_id,
        "agent": agent,
        "platform": resolved,
        "squad": squad,
        "repos": data.get("repos", []),
        "ritual": ritual,
        "ritual_hash": ritual_hash,
        "schedule": data.get("schedule", {}),
        "enabled": bool(enabled),
        "cookbook": str(cookbook),
        "ritual_path": str(ritual_path) if ritual_path else None,
    }


def emit_dashboard_import(instance: Path, plan: dict[str, Any]) -> None:
    out_dir = instance / ".deploy-artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{plan['id']}.json"
    artifact = dict(plan)
    artifact["generated_at"] = (
        datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    )
    artifact["import_note"] = (
        "Manual dashboard import until platform schedule API is wired"
    )
    with out_file.open("w") as handle:
        json.dump(artifact, handle, indent=2)
        handle.write("\n")
    print(f"wrote {out_file}")


def apply_via_api(plan: dict[str, Any]) -> bool:
    platform = plan["platform"]
    if platform == "cursor":
        if not os.environ.get("CURSOR_API_TOKEN"):
            return False
        # Placeholder: Cursor Automations API not yet wired in this repo.
        return False
    if platform == "claude-cma":
        if not os.environ.get("ANTHROPIC_ADMIN_KEY"):
            return False
        # Placeholder: Claude CMA schedule API not yet wired in this repo.
        return False
    return False


def toggle_enabled(instance: Path, deploy_id: str, action: str) -> None:
    for path in list_deployments(instance):
        data = load_deployment(path)
        if data.get("id") != deploy_id:
            continue
        data["enabled"] = action == "resume"
        with path.open("w") as handle:
            json.dump(data, handle, indent=2)
            handle.write("\n")
        state = "enabled" if data["enabled"] else "disabled"
        print(f"{state}: {data['id']}")
        return
    print(f"error: deployment id not found: {deploy_id}", file=sys.stderr)
    sys.exit(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Apply carinyaparc instance deployments to cloud platforms.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "mode",
        nargs="?",
        default="dry-run",
        choices=("dry-run", "apply", "pause", "resume"),
        help="Operation mode (default: dry-run)",
    )
    parser.add_argument(
        "--instance",
        help="Path to carinyaparc instance repo root",
    )
    parser.add_argument(
        "--ritual",
        dest="ritual_filter",
        help="Only process deployments for this ritual",
    )
    parser.add_argument(
        "--id",
        dest="deployment_id",
        help="Deployment id (required for pause/resume; optional filter otherwise)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Plan only; do not apply (same as mode dry-run)",
    )
    parser.add_argument(
        "--dry-run-first",
        action="store_true",
        help="Print plans before applying",
    )
    parser.add_argument(
        "--run-now",
        action="store_true",
        help="Remind to trigger manual execution after apply",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    mode = "dry-run" if args.dry_run else args.mode

    instance_path = args.instance
    if not instance_path:
        sibling = CATALOGUE_ROOT.parent / "carinyaparc"
        if sibling.is_dir():
            instance_path = str(sibling)
        else:
            print("error: --instance <path> is required", file=sys.stderr)
            return 1

    instance_root = resolve_instance(instance_path)
    validate_instance(instance_root)

    if mode in ("pause", "resume"):
        if not args.deployment_id:
            print("error: --id <deployment-id> required for pause/resume", file=sys.stderr)
            return 1
        toggle_enabled(instance_root, args.deployment_id, mode)
        return 0

    print("Digital Agency — deploy squad agents")
    print(f"  instance:  {instance_root}")
    print(f"  catalogue: {CATALOGUE_ROOT}")
    print(f"  mode:      {mode}")
    if args.ritual_filter:
        print(f"  ritual:    {args.ritual_filter}")
    print()

    plans: list[dict[str, Any]] = []
    for deploy_file in list_deployments(instance_root):
        data = load_deployment(deploy_file)
        if args.ritual_filter and data.get("ritual") != args.ritual_filter:
            continue
        if args.deployment_id and data.get("id") != args.deployment_id:
            continue
        plans.append(plan_deployment(instance_root, deploy_file))

    if not plans:
        print("No deployments matched filters.")
        return 0

    for plan in plans:
        print(json.dumps(plan, indent=2))
        print()

    if mode == "dry-run":
        print(
            f"dry-run complete — {len(plans)} deployment(s) planned, no changes applied."
        )
        return 0

    if args.dry_run_first:
        print("(dry-run-first) plans printed above; proceeding to apply...")

    for plan in plans:
        if not plan.get("enabled"):
            print(f"skip disabled: {plan['id']}")
            continue
        if apply_via_api(plan):
            print(f"applied via API: {plan['id']}")
        else:
            emit_dashboard_import(instance_root, plan)

    if args.run_now:
        print()
        print(
            "run-now: trigger manual execution in Cursor Cloud Agents or Claude CMA dashboard"
        )
        print(
            "  expected output: planning PR + labelled issues (never direct push to main)"
        )

    print("apply complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
