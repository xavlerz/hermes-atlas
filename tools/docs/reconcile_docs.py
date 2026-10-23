#!/usr/bin/env python3
"""Print a deterministic, opt-in human review packet for changed source paths."""
import argparse
import subprocess
import sys
from pathlib import Path


# Deliberately broad, transparent routing suggestions; no dependency graph implied.
DOCS = ("docs/ARCHITECTURE.md", "docs/PROJECT_STATE.md", "docs/ROADMAP.md", "docs/INDEX.md")
SOURCE_PREFIXES = ("src/", "tools/", "tests/", "skills/")


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def changed_paths(root, base=None):
    if not git(root, "rev-parse", "--show-toplevel").returncode:
        top = Path(git(root, "rev-parse", "--show-toplevel").stdout.decode().strip()).resolve()
        if top != root.resolve():
            raise ValueError(f"root must be Git top-level: {top}")
    else:
        raise ValueError(f"not a Git repository: {root}")
    args = ["diff", "--name-status", "-z", "--find-renames"]
    if base:
        args.extend((base, "HEAD", "--"))
    else:
        args.extend(("HEAD", "--"))
    result = git(root, *args)
    if result.returncode:
        raise ValueError(result.stderr.decode(errors="replace").strip())
    tokens = result.stdout.split(b"\0")
    output = []
    i = 0
    while i < len(tokens) and tokens[i]:
        status = tokens[i].decode(errors="replace")
        i += 1
        if status.startswith(("R", "C")):
            old, new = tokens[i].decode(errors="surrogateescape"), tokens[i + 1].decode(errors="surrogateescape")
            output.append((status, old, new)); i += 2
        else:
            path = tokens[i].decode(errors="surrogateescape")
            output.append((status, path, path)); i += 1
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="explicit Git repository root")
    parser.add_argument("--base", help="optional base ref; compare base..HEAD plus worktree changes")
    args = parser.parse_args()
    try:
        root = Path(args.root).resolve()
        changes = changed_paths(root, args.base)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr); return 2
    print("# Documentation reconciliation review packet")
    print("Mode: advisory only; no documents are edited and no LLM is invoked.")
    print("Claim labels: Observed = Git path/status only; inferred = routing suggestion; proposed = human follow-up.")
    if not changes:
        print("\nNo changed paths (untracked files are intentionally excluded).")
    else:
        print("\n## Observed changed paths")
        for status, old, new in changes:
            print(f"- {status}: {old}" + (f" -> {new}" if old != new else ""))
        source = any(any(path.startswith(prefix) for prefix in SOURCE_PREFIXES) for _, old, new in changes for path in (old, new))
        candidates = DOCS if source else ("docs/INDEX.md", "docs/PROJECT_STATE.md")
        print("\n## Inferred documents to inspect (routing only; verify relevance)")
        for doc in candidates:
            print(f"- {doc}")
        print("\n## Proposed human checklist")
        print("- Compare each candidate document with source and tests; update only evidenced claims.")
        print("- Mark claims observed, inferred, or proposed; do not infer dependencies from path matching.")
    print("\n## Proposed verification commands")
    print("- python3 -m unittest discover -s tools/docs/tests -v")
    print("- PYTHONDONTWRITEBYTECODE=1 python3 tools/docs/validate_atlas.py")
    print("- git diff --check")
    print("\n## Proposed Git review commands")
    print("- git status --short; git diff --; git diff --cached --")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
