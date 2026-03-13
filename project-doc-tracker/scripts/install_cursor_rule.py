from __future__ import annotations

from setup_tool_rules import run_installer


def main() -> int:
    return run_installer("cursor", "Install a .cursorrules file for project-doc-tracker.")


if __name__ == "__main__":
    raise SystemExit(main())
