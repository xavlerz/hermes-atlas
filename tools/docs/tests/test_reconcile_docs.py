import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
SCRIPT = TOOLS / "reconcile_docs.py"


class ReconcileDocsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.email", "test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.name", "Test"], check=True)
        (self.root / "src").mkdir()
        (self.root / "src/a file.py").write_text("baseline\n")
        (self.root / "docs").mkdir()
        (self.root / "docs/ARCHITECTURE.md").write_text("KEEP UNTOUCHED\n")
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "base"], check=True)

    def tearDown(self):
        self.tmp.cleanup()

    def run_tool(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), *args], text=True, capture_output=True)

    def test_empty_diff_and_docs_untouched(self):
        result = self.run_tool()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("No changed paths", result.stdout)
        self.assertEqual("KEEP UNTOUCHED\n", (self.root / "docs/ARCHITECTURE.md").read_text())

    def test_staged_unstaged_rename_delete_and_space_paths(self):
        (self.root / "src/deleted.py").write_text("baseline deletion target\n")
        subprocess.run(["git", "-C", str(self.root), "add", "src/deleted.py"], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "add deletion target"], check=True)
        subprocess.run(["git", "-C", str(self.root), "mv", "src/a file.py", "src/renamed file.py"], check=True)
        (self.root / "src/renamed file.py").write_text("unstaged edit\n")
        subprocess.run(["git", "-C", str(self.root), "add", "-A"], check=True)
        (self.root / "src/renamed file.py").write_text("worktree edit\n")
        (self.root / "src/deleted.py").unlink()
        (self.root / "src/untracked.py").write_text("untracked\n")
        result = self.run_tool()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("src/renamed file.py", result.stdout)
        self.assertIn("src/a file.py", result.stdout)
        self.assertIn("src/deleted.py", result.stdout)
        self.assertNotIn("src/untracked.py", result.stdout)
        self.assertIn("proposed", result.stdout)
        self.assertIn("Observed", result.stdout)
        self.assertEqual("KEEP UNTOUCHED\n", (self.root / "docs/ARCHITECTURE.md").read_text())

    def test_base_compares_committed_range_only_and_preserves_worktree(self):
        base = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "HEAD"],
            check=True, text=True, capture_output=True,
        ).stdout.strip()
        (self.root / "src/committed.py").write_text("committed\n")
        subprocess.run(["git", "-C", str(self.root), "add", "src/committed.py"], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "committed change"], check=True)
        (self.root / "src/staged.py").write_text("staged\n")
        subprocess.run(["git", "-C", str(self.root), "add", "src/staged.py"], check=True)
        (self.root / "src/unstaged.py").write_text("unstaged\n")
        (self.root / "src/untracked.py").write_text("untracked\n")
        before = subprocess.run(
            ["git", "-C", str(self.root), "status", "--porcelain"],
            check=True, text=True, capture_output=True,
        ).stdout

        result = self.run_tool("--base", base)

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("src/committed.py", result.stdout)
        self.assertNotIn("src/staged.py", result.stdout)
        self.assertNotIn("src/unstaged.py", result.stdout)
        self.assertNotIn("src/untracked.py", result.stdout)
        after = subprocess.run(
            ["git", "-C", str(self.root), "status", "--porcelain"],
            check=True, text=True, capture_output=True,
        ).stdout
        self.assertEqual(before, after)

    def test_recommendations_follow_docs_first_and_legacy_layouts(self):
        (self.root / "docs/INDEX.md").write_text("# index\n")
        (self.root / "src/a file.py").write_text("changed\n")
        out = self.run_tool().stdout
        self.assertIn("- docs/INDEX.md", out)
        self.assertIn("## Atlas tooling checks", out)
        self.assertIn(str(TOOLS / "tests"), out)
        self.assertNotIn("- python3 -m unittest discover -s tools/docs/tests", out)
        (self.root / "docs/INDEX.md").unlink()
        (self.root / "INDEX.md").write_text("# legacy\n")
        out = self.run_tool().stdout
        self.assertIn("- INDEX.md", out)
        self.assertNotIn("- docs/INDEX.md", out)

    def test_verification_does_not_assume_atlas_tools_in_target(self):
        out = self.run_tool().stdout
        self.assertIn("## Atlas tooling checks", out)
        self.assertIn("## Target project checks", out)
        self.assertIn(f"{TOOLS / 'validate_atlas.py'}", out)
        self.assertIn(f"{TOOLS / 'validate_project.py'} {self.root}", out)
        self.assertNotIn("python3 tools/docs/", out)
        self.assertFalse((self.root / "tools/docs").exists())

    def test_target_git_recommendations_are_anchored_and_shell_quoted(self):
        root_with_spaces = self.root / "target project with spaces"
        root_with_spaces.mkdir()
        subprocess.run(["git", "init", "-q", str(root_with_spaces)], check=True)
        subprocess.run(["git", "-C", str(root_with_spaces), "config", "user.email", "test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(root_with_spaces), "config", "user.name", "Test"], check=True)
        (root_with_spaces / "src").mkdir()
        (root_with_spaces / "src/file.py").write_text("baseline\\n")
        subprocess.run(["git", "-C", str(root_with_spaces), "add", "."], check=True)
        subprocess.run(["git", "-C", str(root_with_spaces), "commit", "-qm", "base"], check=True)
        self.root = root_with_spaces
        out = self.run_tool().stdout
        quoted_root = shlex.quote(str(self.root))
        self.assertIn(f"- git -C {quoted_root} diff --check", out)
        self.assertIn(f"- git -C {quoted_root} status --short; git -C {quoted_root} diff --; git -C {quoted_root} diff --cached --", out)

    def test_not_git_root_fails(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root / "missing")], text=True, capture_output=True)
        self.assertNotEqual(0, result.returncode)


if __name__ == "__main__":
    unittest.main()
