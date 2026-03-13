from __future__ import annotations

import argparse
import re
from pathlib import Path


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def project_root(value: str | None) -> Path:
    return Path(value).resolve() if value else Path.cwd()


def steering_template_path() -> Path:
    return skill_root() / "references" / "steering-template.md"


def target_steering_path(root: Path) -> Path:
    return root / ".kiro" / "steering" / "project-doc-tracker.md"


def extract_copy_block(content: str) -> str:
    match = re.search(r"```markdown\n(.*?)\n```", content, re.DOTALL)
    if not match:
        raise ValueError("Could not find the markdown copy block in steering-template.md")
    return match.group(1).strip() + "\n"


def install_steering(root: Path, *, force: bool) -> Path:
    template = steering_template_path().read_text(encoding="utf-8")
    steering_text = extract_copy_block(template)
    target = target_steering_path(root)

    if target.exists() and not force:
        raise FileExistsError(f"Steering file already exists: {target}")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(steering_text, encoding="utf-8")
    return target


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
