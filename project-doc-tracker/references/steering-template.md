# Steering Template: project-doc-tracker

Copy the content below into the rule file used by your AI tool so it remembers to record meaningful project progress automatically.

For Kiro users, you can install this block automatically with:

```bash
python .agents/skills/project-doc-tracker/scripts/setup_kiro_steering.py --project-root .
```

## Tool Mapping

| Tool | Rule File Location |
| --- | --- |
| Kiro | `.kiro/steering/project-doc-tracker.md` (install with `scripts/setup_kiro_steering.py`, or copy manually if needed) |
| Claude Code | `CLAUDE.md` or `.claude/CLAUDE.md` |
| Cursor | `.cursorrules` or `.cursor/rules/*.mdc` |
| Windsurf | `.windsurfrules` |
| Codex | `AGENTS.md` |
| Other | `AGENTS.md` at the repo root or the tool-specific rules file |

---

## Copy Block

```markdown
## Project Progress Tracking Rules

This project uses the `project-doc-tracker` skill to preserve development progress over time.

### When to Record Progress

Update the tracker proactively after any meaningful change, without waiting for the user to remind you:
- finishing a feature or sub-feature
- fixing a bug
- completing a refactor or architecture change
- making several meaningful code changes in one conversation

### How to Record Progress

Append a progress log entry:

  python .agents/skills/project-doc-tracker/scripts/project_tracker.py \
    --project-root . log \
    --change-type <feature|bugfix|refactor|docs|research|decision> \
    --feature-id <feature-id> \
    --summary "What changed in this session" \
    --file "path/to/changed/file.py" \
    --next-step "What should happen next" \
    --confidence <high|medium|low>

Sync the overview:

  python .agents/skills/project-doc-tracker/scripts/project_tracker.py \
    --project-root . sync-item \
    --feature-id <feature-id> \
    --title "Feature title" \
    --status <in_progress|done|blocked|stable> \
    --summary "One-sentence current status" \
    --next-step "Recommended next step" \
    --file "key/file.py"

### Confidence Rules

- high: directly supported by code changes or explicit user statements
- medium: inferred from multiple strong signals
- low: plausible but still uncertain, so mark it clearly

### What Not To Do

- Do not write high-confidence progress from memory alone; check `git status`, changed files, or specs first.
- Do not delete or overwrite the history in `PROGRESS.md`.
- Do not auto-edit `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, or similar rule files.

### Tracker Paths

docs/project-tracker/OVERVIEW.md   - project overview and active-item table
docs/project-tracker/PROGRESS.md   - append-only session log
docs/project-tracker/features/     - lightweight feature notes

If `docs/project-tracker/` does not exist yet, run:

  python .agents/skills/project-doc-tracker/scripts/project_tracker.py --project-root . init
```
