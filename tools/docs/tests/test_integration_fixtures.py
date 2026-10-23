import subprocess
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from manage_project_docs import FILES, apply, map_block
from validate_project import REQUIRED, errors_for
REPO = Path(__file__).resolve().parents[3]

class IntegrationFixtures(unittest.TestCase):
    def test_skills_share_docs_first_legacy_fallback_contract(self):
        navigator = (REPO / "skills/project-navigator/SKILL.md").read_text()
        maintainer = (REPO / "skills/project-docs-maintainer/SKILL.md").read_text()
        for text in (navigator, maintainer):
            self.assertIn("docs/INDEX.md", text)
            self.assertIn("root-level legacy", text)
            self.assertTrue("Only when `docs/INDEX.md` is absent" in text or "Only when that entry point is absent" in text)
            self.assertIn("partial or mixed", text)
            self.assertIn("authoritative", text)
            self.assertIn("silently merging", text)
            self.assertRegex(text, r"Prefer `docs/` when `docs/INDEX\.md` exists")
            self.assertRegex(text, r"Only when (?:`docs/INDEX\.md`|that entry point) is absent,? (?:fall back|fall back to)")

    def test_docs_first_and_root_only_legacy_layouts(self):
        temp, root = self.repo()
        with temp:
            (root / "docs").mkdir()
            (root / "docs/INDEX.md").write_text("# map\n")
            (root / "docs/ARCHITECTURE.md").write_text("# code map\n")
            (root / "INDEX.md").write_text("# compatibility\n")
            docs_index = root / "docs/INDEX.md"
            root_index = root / "INDEX.md"
            self.assertTrue(docs_index.is_file())
            self.assertTrue(root_index.is_file())
            # Contract fixture: docs/INDEX.md is authoritative when both copies exist.
            authoritative_index = docs_index if docs_index.is_file() else root_index
            self.assertEqual(docs_index, authoritative_index)
        temp, root = self.repo()
        with temp:
            for name in ("INDEX.md", "ARCHITECTURE.md", "ROADMAP.md", "PROJECT_STATE.md"):
                (root / name).write_text("# legacy\n")
            self.assertFalse((root / "docs/INDEX.md").exists())
            root_index = root / "INDEX.md"
            self.assertTrue(root_index.is_file())
            # Contract fixture: without docs/INDEX.md, legacy root INDEX.md is the fallback.
            authoritative_index = (root / "docs/INDEX.md" if (root / "docs/INDEX.md").is_file()
                                  else root_index)
            self.assertEqual(root_index, authoritative_index)
    def repo(self):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        return temp, root

    def write_core(self, root, directory=""):
        target = root / directory
        target.mkdir(parents=True, exist_ok=True)
        for name in REQUIRED:
            (target / name).write_text("# Core\n", encoding="utf-8")

    def test_docs_only_and_root_legacy_layouts_validate(self):
        temp, root = self.repo()
        with temp:
            self.write_core(root, "docs")
            self.assertEqual([], errors_for(root))
        temp, root = self.repo()
        with temp:
            self.write_core(root)
            self.assertEqual([], errors_for(root))

    def test_mixed_layout_uses_docs_and_resolves_links_there(self):
        temp, root = self.repo()
        with temp:
            self.write_core(root, "docs")
            self.write_core(root)
            (root / "docs/INDEX.md").write_text("[local](ARCHITECTURE.md)\n", encoding="utf-8")
            (root / "INDEX.md").write_text("[broken](missing-root-target.md)\n", encoding="utf-8")
            (root / "docs/ARCHITECTURE.md").unlink()
            errors = errors_for(root)
            self.assertIn("missing core document: docs/ARCHITECTURE.md", errors)
            self.assertNotIn("broken link in INDEX.md: missing-root-target.md", errors)

    def test_missing_layout_reports_every_core_document(self):
        temp, root = self.repo()
        with temp:
            errors = errors_for(root)
            self.assertEqual({f"missing core document: {name}" for name in REQUIRED}, set(errors))

    def test_empty_project_bootstrap_and_rerun(self):
        temp, root = self.repo()
        with temp:
            apply(root)
            self.assertEqual([], errors_for(root))
            before = {p: (root/p).read_bytes() for p in FILES}
            apply(root)
            self.assertEqual(before, {p: (root/p).read_bytes() for p in FILES})

    def test_bootstrap_docs_first_does_not_duplicate_core_docs(self):
        temp, root = self.repo()
        with temp:
            (root / "docs").mkdir()
            for name in REQUIRED:
                (root / "docs" / name).write_text("# Canonical\n", encoding="utf-8")
            apply(root)
            self.assertFalse(any((root / name).exists() for name in REQUIRED))
            self.assertTrue(all((root / "docs" / name).is_file() for name in REQUIRED))
    def test_existing_content_preserved_and_only_absent_added(self):
        temp, root = self.repo()
        with temp:
            root.joinpath("INDEX.md").write_text("# My index\nprivate text\n")
            apply(root)
            self.assertEqual("# My index\nprivate text\n", (root/"INDEX.md").read_text())
            self.assertTrue((root/"ARCHITECTURE.md").exists())
    def test_source_change_and_stale_map_non_destructive(self):
        temp, root = self.repo()
        with temp:
            apply(root)
            (root/"src").mkdir(); (root/"src/new.py").write_text("pass\n")
            subprocess.run(["git", "-C", str(root), "add", "--", "src/new.py"], check=True)
            apply(root, update=True)
            updated = (root/"docs/INDEX.md").read_text()
            self.assertIn("src/new.py", updated)
            self.assertEqual([], errors_for(root))
            apply(root, update=True)
            self.assertEqual(updated, (root/"docs/INDEX.md").read_text())

    def test_update_preserves_unmanaged_bytes_and_appends_missing_block(self):
        temp, root = self.repo()
        with temp:
            apply(root)
            p = root / "docs/INDEX.md"
            p.write_text("# User index\n\nKeep this exactly.\n")
            original = p.read_bytes()
            apply(root, update=True)
            self.assertTrue(p.read_bytes().startswith(original))

    def test_malformed_markers_fail_without_write(self):
        temp, root = self.repo()
        with temp:
            apply(root)
            p = root / "docs/INDEX.md"
            p.write_text("prefix\n<!-- hermes-atlas:code-map:start -->\n")
            old = p.read_bytes()
            with self.assertRaises(ValueError): apply(root, update=True)
            self.assertEqual(old, p.read_bytes())

    def test_reversed_markers_fail_without_write(self):
        temp, root = self.repo()
        with temp:
            apply(root)
            p = root / "docs/INDEX.md"
            original = b"Before\r\n<!-- hermes-atlas:code-map:end -->\r\nuser text\r\n<!-- hermes-atlas:code-map:start -->\r\nAfter\r\n"
            p.write_bytes(original)
            with self.assertRaises(ValueError):
                apply(root, update=True)
            self.assertEqual(original, p.read_bytes())

    def test_map_uses_tracked_files_only_and_excludes_sensitive_paths(self):
        temp, root = self.repo()
        with temp:
            tracked = ["tracked file.py", "ordinary.txt", ".env", "secrets/token.txt", "credentials.json", "private/key.pem"]
            for name in tracked:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("tracked\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "--"] + tracked, check=True)
            subprocess.run(["git", "-C", str(root), "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "fixtures"], check=True)
            (root / "untracked.txt").write_text("untracked\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "rm", "--cached", "-q", "credentials.json", "secrets/token.txt"], check=True)
            (root / "credentials.json").unlink()
            (root / "secrets/token.txt").unlink()
            (root / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
            (root / "ignored.txt").write_text("ignored\n", encoding="utf-8")
            block = map_block(root)
            self.assertIn("`tracked file.py`", block)
            self.assertIn("`ordinary.txt`", block)
            for name in ("ignored.txt", ".env", "secrets/token.txt", "credentials.json", "private/key.pem"):
                self.assertNotIn(name, block)
            self.assertNotIn("relation", block.lower())

    def test_deleted_tracked_path_is_not_indexed(self):
        temp, root = self.repo()
        with temp:
            p = root / "deleted.txt"
            p.write_text("content\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "--", "deleted.txt"], check=True)
            subprocess.run(["git", "-C", str(root), "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "fixture"], check=True)
            p.unlink()
            self.assertNotIn("deleted.txt", map_block(root))
if __name__ == "__main__": unittest.main()
