# Project Docs Skills Package

This package bundles two related skills:

- `project-doc-tracker`
- `professional-markdown`

Together they provide a lightweight tracker workflow plus high-quality long-form Markdown generation.

## Package Contents

- `project-doc-tracker`
  - maintains `docs/project-tracker/`
  - records progress logs and lightweight feature notes
  - identifies mature modules that should be promoted into formal documentation

- `professional-markdown`
  - writes polished, publication-quality Markdown
  - is intended for formal docs such as `docs/modules/*.md`, architecture writeups, and high-quality READMEs

## Recommended Flow

1. Use `project-doc-tracker` to initialize or update project memory.
2. Keep `OVERVIEW.md`, `PROGRESS.md`, and lightweight feature notes current.
3. When a module becomes mature, use `professional-markdown` to create the formal long-form document.

## Build the Package

From the repo root:

```bash
python scripts/build_skill_package.py
```

This creates:

```text
publish/project-docs-skills/
├─ README.md
├─ project-doc-tracker/
└─ professional-markdown/
```

## Publishing Notes

The generated `publish/project-docs-skills/` directory is the intended package payload for release or for moving into a dedicated public repository.

If you want to publish these skills through a public package repo later, use the generated folder as the source of truth for the release artifact.
