#!/usr/bin/env python3
"""Safe additive documentation bootstrap and managed source-map refresh."""
from pathlib import Path
import subprocess
import argparse
import os
import tempfile
import difflib

FILES = {
    "AGENTS.md": "# Repository guidance\n\nKeep project documentation evidence-based. See docs/INDEX.md for navigation and docs/ARCHITECTURE.md for verified contracts.\n",
    "INDEX.md": "# Documentation index\n\nSee [codebase map](docs/INDEX.md), [architecture](docs/ARCHITECTURE.md), [roadmap](docs/ROADMAP.md), and [project state](docs/PROJECT_STATE.md).\n",
    "ARCHITECTURE.md": "# Architecture\n\nDocument only verified contracts; mark unknowns.\n",
    "ROADMAP.md": "# Roadmap\n\nNo commitments recorded.\n",
    "PROJECT_STATE.md": "# Project state\n\nRecord verified state and evidence here.\n",
    "docs/INDEX.md": "# Codebase map\n\nUpdate this map from repository evidence.\n\n<!-- hermes-atlas:code-map:start -->\n<!-- hermes-atlas:code-map:end -->\n",
    "docs/ARCHITECTURE.md": "# Architecture\n\nRecord verified contracts; mark unknowns explicitly.\n",
    "docs/ROADMAP.md": "# Roadmap\n\nRecord proposals, not assumptions.\n",
    "docs/PROJECT_STATE.md": "# Project state\n\nRecord verified state and checks.\n",
}
START = "<!-- hermes-atlas:code-map:start -->"
END = "<!-- hermes-atlas:code-map:end -->"
IGNORED = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".tox", ".venv", "venv", "node_modules", "build", "dist", "target"}

def root_for(path):
    path = path.resolve()
    result = subprocess.run(["git", "-C", str(path), "rev-parse", "--show-toplevel"], text=True, capture_output=True, check=True)
    root = Path(result.stdout.strip()).resolve()
    if root != path: raise ValueError(f"explicit target must be Git root ({root})")
    return root

def plan(root):
    return [(name, root / name) for name in FILES if not (root / name).exists()]

def map_block(root):
    paths = []
    for directory, dirs, files in os.walk(root, followlinks=False):
        here = Path(directory)
        dirs[:] = sorted(d for d in dirs if d not in IGNORED and not (here / d).is_symlink())
        for name in sorted(files):
            p = here / name
            if p.is_symlink(): continue
            rel = p.relative_to(root).as_posix()
            if rel == "docs/INDEX.md": continue
            paths.append(rel)
    paths.sort()
    lines = [START, "## Managed source map", "", *[f"- `{p}`" for p in paths[:250]]]
    if len(paths) > 250: lines.append(f"- … ({len(paths) - 250} additional paths omitted)")
    lines.append(END)
    return "\n".join(lines)

def update_map(root, dry_run=False):
    path = root / "docs/INDEX.md"
    if not path.is_file() or path.is_symlink(): raise ValueError("docs/INDEX.md must be a regular file inside project root")
    old_bytes = path.read_bytes()
    try: old = old_bytes.decode("utf-8")
    except UnicodeDecodeError as exc: raise ValueError("docs/INDEX.md is not UTF-8") from exc
    starts, ends = old.count(START), old.count(END)
    if starts != ends or starts > 1: raise ValueError("malformed or duplicate managed map markers")
    block = map_block(root)
    if starts:
        begin, finish = old.index(START), old.index(END) + len(END)
        new = old[:begin] + block + old[finish:]
    else:
        new = old + ("" if not old or old.endswith("\n") else "\n") + "\n" + block + "\n"
    if new.encode() == old_bytes:
        print("No map changes needed."); return 0
    print("--- docs/INDEX.md (before)\n+++ docs/INDEX.md (after)")
    print("".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile="before", tofile="after")), end="")
    if not dry_run:
        fd, name = tempfile.mkstemp(prefix=".INDEX.md.", dir=path.parent)
        try:
            with os.fdopen(fd, "wb") as f: f.write(new.encode("utf-8"))
            os.replace(name, path)
        finally:
            if os.path.exists(name): os.unlink(name)
    return 0

def apply(root, dry_run=False, update=False):
    root = root_for(root)
    status = subprocess.run(["git", "-C", str(root), "status", "--short"], text=True, capture_output=True, check=True).stdout
    if status: print("Preserving existing Git changes:\n" + status, end="")
    if update: return update_map(root, dry_run)
    changes = plan(root)
    if not changes:
        print("No changes needed."); return 0
    for name, path in changes:
        print(("Would create " if dry_run else "Create ") + name)
        if not dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("x", encoding="utf-8") as handle: handle.write(FILES[name])
    return 0

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--update", action="store_true", help="refresh only the managed map in docs/INDEX.md")
    args = parser.parse_args()
    try: return apply(args.project_root, args.dry_run, args.update)
    except (ValueError, subprocess.CalledProcessError, FileExistsError) as exc:
        print(f"ERROR: {exc}"); return 2
if __name__ == "__main__": raise SystemExit(main())