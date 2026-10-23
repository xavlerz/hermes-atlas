import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_docs import REQUIRED, errors_for


class ValidatorScenarios(unittest.TestCase):
    def fixture(self, root: Path) -> None:
        for name in REQUIRED:
            (root / name).write_text("# Doc\n\n[Go](ARCHITECTURE.md#hello-world)\n", encoding="utf-8")
        (root / "ARCHITECTURE.md").write_text("# Hello, World!\n", encoding="utf-8")
        docs = root / "docs"
        docs.mkdir()
        (docs / "optional-docs.yaml").write_text(
            "version: 1\ndocuments:\n  DESIGN.md: optional\n  DEVELOPMENT.md: optional\n  OPERATIONS.md: optional\n", encoding="utf-8")
        (docs / "optional-docs.schema.json").write_text('{"type": "object"}', encoding="utf-8")
        for name in ("project-navigator", "project-docs-maintainer"):
            folder = root / "skills" / name
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(f"---\nname: {name}\ndescription: Test skill\n---\n# Skill\n", encoding="utf-8")

    def test_valid_fixture_and_optional_absence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            self.assertEqual([], errors_for(root))
            self.assertFalse((root / "DESIGN.md").exists())

    def test_docs_core_is_authoritative_over_root_legacy_copies(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            docs = root / "docs"
            for name in REQUIRED:
                (docs / name).write_text("# Canonical\n", encoding="utf-8")
            (docs / "INDEX.md").write_text("[valid](ARCHITECTURE.md)\n", encoding="utf-8")
            (root / "INDEX.md").write_text("[broken](missing.md)\n", encoding="utf-8")
            errors = errors_for(root)
            self.assertFalse(any("missing required document" in e for e in errors))
            self.assertFalse(any("broken internal link" in e for e in errors))

    def test_docs_index_makes_partial_docs_layout_authoritative(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            docs = root / "docs"
            for name in REQUIRED:
                (docs / name).write_text("# Canonical\n", encoding="utf-8")
            (docs / "ROADMAP.md").unlink()
            errors = errors_for(root)
            self.assertIn("missing required document: docs/ROADMAP.md", errors)

    def test_missing_required_document(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            (root / "ROADMAP.md").unlink()
            self.assertTrue(any("missing required document: ROADMAP.md" in e for e in errors_for(root)))

    def test_broken_internal_link(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            (root / "INDEX.md").write_text("[Missing](not-here.md)\n", encoding="utf-8")
            self.assertTrue(any("broken internal link" in e for e in errors_for(root)))

    def test_missing_heading_anchor(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            (root / "INDEX.md").write_text("[Missing](ARCHITECTURE.md#not-there)\n", encoding="utf-8")
            self.assertTrue(any("broken internal link anchor" in e for e in errors_for(root)))

    def test_heading_slug_normalization(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            (root / "ARCHITECTURE.md").write_text("# Hello, World!\n", encoding="utf-8")
            (root / "INDEX.md").write_text("[Go](ARCHITECTURE.md#hello-world)\n", encoding="utf-8")
            self.assertEqual([], errors_for(root))

    def test_registry_rejects_incomplete_and_duplicate_keys(self):
        for body in (
            "version: 1\ndocuments:\n  DESIGN.md: optional\n",
            "version: 1\ndocuments:\n  DESIGN.md: optional\n  DESIGN.md: present\n  DEVELOPMENT.md: optional\n  OPERATIONS.md: optional\n",
            "version: 1\ndocuments:\n  DESIGN.md optional\n  DEVELOPMENT.md: optional\n  OPERATIONS.md: optional\n",
        ):
            with self.subTest(body=body), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                self.fixture(root)
                (root / "docs/optional-docs.yaml").write_text(body, encoding="utf-8")
                self.assertTrue(errors_for(root))

    def test_registry_requires_allowed_optional_documents(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            (root / "docs/optional-docs.yaml").write_text(
                "version: 1\ndocuments:\n  DESIGN.md: optional\n  EXTRA.md: optional\n  DEVELOPMENT.md: optional\n", encoding="utf-8")
            self.assertTrue(errors_for(root))

    def test_malformed_skill_frontmatter_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            skill = root / "skills/project-navigator/SKILL.md"
            skill.write_text("---\nname: project-navigator\nname: shadow\ndescription: Test\n---\n", encoding="utf-8")
            self.assertTrue(any("frontmatter" in e for e in errors_for(root)))

    def test_malformed_json_schema_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            (root / "docs/optional-docs.schema.json").write_text("{broken", encoding="utf-8")
            self.assertTrue(any("invalid JSON schema" in e for e in errors_for(root)))

    def test_schema_constraints_validate_registry(self):
        for body in (
            "version: 2\ndocuments:\n  DESIGN.md: optional\n  DEVELOPMENT.md: optional\n  OPERATIONS.md: optional\n",
            "version: 1\nextra: true\ndocuments:\n  DESIGN.md: optional\n  DEVELOPMENT.md: optional\n  OPERATIONS.md: optional\n",
            "version: 1\ndocuments:\n  DESIGN.md: optional\n  DEVELOPMENT.md: invalid\n  OPERATIONS.md: optional\n",
        ):
            with self.subTest(body=body), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                self.fixture(root)
                (root / "docs/optional-docs.yaml").write_text(body, encoding="utf-8")
                self.assertTrue(errors_for(root))

    def test_markdown_destinations_support_spaces_parentheses_and_angle_brackets(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            (root / "file (one).md").write_text("# A heading\n", encoding="utf-8")
            (root / "INDEX.md").write_text(
                "[Space](<file (one).md#a-heading>)\n[Plain](file\\ (one\\).md#a-heading)\n", encoding="utf-8")
            self.assertEqual([], errors_for(root))


if __name__ == "__main__":
    unittest.main()
