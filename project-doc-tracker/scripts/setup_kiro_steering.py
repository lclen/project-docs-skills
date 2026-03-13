from __future__ import annotations

import argparse
from pathlib import Path

from setup_tool_rules import install_rule


def project_root(value: str | None) -> Path:
    return Path(value).resolve() if value else Path.cwd()


def install_steering(root: Path, *, force: bool) -> Path:
    return install_rule(root, "kiro", force=force)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install the project-doc-tracker steering file into a target Kiro project."
    )
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--force", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    target = install_steering(project_root(args.project_root), force=args.force)
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
