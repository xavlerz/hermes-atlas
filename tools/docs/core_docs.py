"""Shared selection rule for required project documentation."""
from pathlib import Path

REQUIRED = ("INDEX.md", "ARCHITECTURE.md", "ROADMAP.md", "PROJECT_STATE.md")


def core_docs_directory(root: Path) -> Path:
    """Prefer canonical docs/ when its index exists; otherwise use root legacy docs."""
    docs = root / "docs"
    return docs if (docs / "INDEX.md").is_file() else root
