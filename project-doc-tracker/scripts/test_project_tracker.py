from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import importlib.util


SCRIPT_PATH = Path(__file__).with_name("project_tracker.py")
SPEC = importlib.util.spec_from_file_location("project_tracker", SCRIPT_PATH)
assert SPEC and SPEC.loader
project_tracker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(project_tracker)

STEERING_SCRIPT_PATH = Path(__file__).with_name("setup_kiro_steering.py")
STEERING_SPEC = importlib.util.spec_from_file_location("setup_kiro_steering", STEERING_SCRIPT_PATH)
assert STEERING_SPEC and STEERING_SPEC.loader
setup_kiro_steering = importlib.util.module_from_spec(STEERING_SPEC)
STEERING_SPEC.loader.exec_module(setup_kiro_steering)

TOOL_RULES_SCRIPT_PATH = Path(__file__).with_name("setup_tool_rules.py")
TOOL_RULES_SPEC = importlib.util.spec_from_file_location("setup_tool_rules", TOOL_RULES_SCRIPT_PATH)
assert TOOL_RULES_SPEC and TOOL_RULES_SPEC.loader
setup_tool_rules = importlib.util.module_from_spec(TOOL_RULES_SPEC)
TOOL_RULES_SPEC.loader.exec_module(setup_tool_rules)


class ProjectTrackerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        project_tracker.ensure_initialized(self.root)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_sync_item_preserves_existing_formal_doc_when_not_provided(self) -> None:
        project_tracker.sync_item(
            root=self.root,
            feature_id="alpha",
            title="Alpha",
            status="done",
            summary="first pass",
            next_step="keep doc",
            files=["src/alpha.py"],
            blockers=None,
            formal_doc="docs/modules/alpha.md",
        )

        project_tracker.sync_item(
            root=self.root,
            feature_id="alpha",
            title="Alpha",
            status="done",
            summary="second pass",
            next_step="still keep doc",
            files=["src/alpha.py"],
            blockers=None,
            formal_doc=None,
        )

        overview = project_tracker.overview_path(self.root).read_text(encoding="utf-8")
        self.assertIn("docs/modules/alpha.md", overview)
        self.assertEqual(overview.count("docs/modules/alpha.md"), 1)
        self.assertIn("still keep doc", overview)

    def test_feature_note_rejects_path_traversal_feature_id(self) -> None:
        with self.assertRaises(SystemExit):
            parser = project_tracker.build_parser()
            parser.parse_args(
                [
                    "feature-note",
                    "--feature-id",
                    "..\\..\\outside-test",
                    "--title",
                    "Escape",
                    "--status",
                    "done",
                    "--background",
                    "b",
                    "--implementation",
                    "i",
                    "--next-step",
                    "n",
                ]
            )

    def test_feature_note_stays_inside_features_directory(self) -> None:
        target = project_tracker.write_feature_note(
            root=self.root,
            feature_id="alpha_note",
            title="Alpha",
            status="done",
            background="background",
            implementation="implementation",
            next_step="next",
            files=[],
            risks=None,
            formal_doc=None,
        )

        self.assertEqual(target.parent, project_tracker.tracker_root(self.root) / "features")
        self.assertTrue(target.exists())

    def test_feature_note_preserves_formal_doc_and_supports_richer_sections(self) -> None:
        project_tracker.write_feature_note(
            root=self.root,
            feature_id="alpha-note",
            title="Alpha",
            status="in_progress",
            background="background",
            implementation="implementation",
            next_step="next",
            files=["src/alpha.py"],
            risks="risk",
            evidence=["修改了 src/alpha.py", "补了 tracker 记录"],
            related_docs=["docs/specs/alpha.md"],
            formal_doc="docs/modules/alpha.md",
        )

        project_tracker.write_feature_note(
            root=self.root,
            feature_id="alpha-note",
            title="Alpha",
            status="done",
            background="updated background",
            implementation="updated implementation",
            next_step="publish",
            files=["src/alpha.py"],
            risks="low risk",
            evidence=None,
            related_docs=None,
            formal_doc=None,
        )

        note = project_tracker.feature_note_path(self.root, "alpha-note").read_text(encoding="utf-8")
        self.assertIn("## 状态判断依据", note)
        self.assertIn("- 修改了 src/alpha.py", note)
        self.assertIn("## 相关文档", note)
        self.assertIn("- docs/specs/alpha.md", note)
        self.assertIn("docs/modules/alpha.md", note)

    def test_setup_kiro_steering_installs_only_the_copy_block(self) -> None:
        target = setup_kiro_steering.install_steering(self.root, force=False)
        content = target.read_text(encoding="utf-8")

        self.assertTrue(target.exists())
        self.assertIn("## Project Progress Tracking Rules", content)
        self.assertNotIn("# Steering Template: project-doc-tracker", content)

    def test_setup_tool_rules_installs_cursor_and_codex_targets(self) -> None:
        cursor_target = setup_tool_rules.install_rule(self.root, "cursor", force=False)
        codex_target = setup_tool_rules.install_rule(self.root, "codex", force=False)

        self.assertEqual(cursor_target, self.root / ".cursorrules")
        self.assertEqual(codex_target, self.root / "AGENTS.md")
        self.assertIn("## Project Progress Tracking Rules", cursor_target.read_text(encoding="utf-8"))
        self.assertIn("## Project Progress Tracking Rules", codex_target.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
