#!/usr/bin/env python3
"""Validate the minimal Hermes Atlas documentation contract (stdlib only).

The optional-doc registry supports only comments, `version: 1`, `documents:`,
and exactly indented `  NAME.md: STATE` entries. No YAML features (quotes,
flow collections, aliases, or multiline values) are supported; unknown syntax
fails closed.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from core_docs import REQUIRED, core_docs_directory

SKILL_NAMES = ("project-navigator", "project-docs-maintainer")
OPTIONAL_DOCS = ("DESIGN.md", "DEVELOPMENT.md", "OPERATIONS.md")
REGISTRY_STATES = {"optional", "required", "present"}


def heading_slugs(text: str) -> set[str]:
    slugs: set[str] = set()
    counts: dict[str, int] = {}
    for line in text.splitlines():
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        title = re.sub(r"<[^>]*>", "", match.group(1))
        title = re.sub(r"[`*_~]", "", title).lower()
        base = re.sub(r"[^\w\- ]", "", title, flags=re.UNICODE)
        base = re.sub(r"\s+", "-", base.strip())
        count = counts.get(base, 0)
        counts[base] = count + 1
        slugs.add(base if count == 0 else f"{base}-{count}")
    return slugs


def parse_optional_registry(text: str) -> tuple[dict[str, str], list[str]]:
    entries: dict[str, str] = {}
    errors: list[str] = []
    seen_version = seen_documents = False
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line == "version: 1" and not seen_version and not seen_documents:
            seen_version = True
        elif line == "documents:" and seen_version and not seen_documents:
            seen_documents = True
        else:
            match = re.fullmatch(r"  ([A-Z][A-Z_]*\.md): (optional|required|present)", line)
            if not match or not seen_documents:
                errors.append(f"invalid optional-doc registry syntax on line {number}: {stripped}")
                continue
            name, state = match.groups()
            if name not in OPTIONAL_DOCS:
                errors.append(f"unknown optional-doc registry document: {name}")
            if name in entries:
                errors.append(f"duplicate optional-doc registry key: {name}")
            else:
                entries[name] = state
    if not seen_version:
        errors.append("optional-doc registry requires version: 1")
    if not seen_documents:
        errors.append("optional-doc registry requires documents:")
    for name in OPTIONAL_DOCS:
        if name not in entries:
            errors.append(f"optional-doc registry missing required entry: {name}")
    return entries, errors


def errors_for(root: Path) -> list[str]:
    errors: list[str] = []
    root = root.resolve()
    docs_dir = core_docs_directory(root)
    for name in REQUIRED:
        if not (docs_dir / name).is_file():
            path = (docs_dir.relative_to(root) / name).as_posix() if docs_dir != root else name
            errors.append(f"missing required document: {path}")
    for name in REQUIRED:
        doc = docs_dir / name
        if doc.is_file():
            text = doc.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^]]*\]\(([^)]+)\)", text):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                path, sep, anchor = target.partition("#")
                target_doc = (doc.parent / path).resolve() if path else doc
                if path and not target_doc.is_file():
                    label = (docs_dir.relative_to(root) / name).as_posix() if docs_dir != root else name
                    errors.append(f"broken internal link in {label}: {target}")
                elif sep and target_doc.is_file() and anchor not in heading_slugs(target_doc.read_text(encoding="utf-8")):
                    label = (docs_dir.relative_to(root) / name).as_posix() if docs_dir != root else name
                    errors.append(f"broken internal link anchor in {label}: {target}")
    registry = root / "docs/optional-docs.yaml"
    if not registry.is_file():
        errors.append("missing optional-doc registry: docs/optional-docs.yaml")
    else:
        optional, registry_errors = parse_optional_registry(registry.read_text(encoding="utf-8"))
        errors.extend(registry_errors)
        for name, state in optional.items():
            exists = (root / name).is_file()
            if state in {"required", "present"} and not exists:
                errors.append(f"registry marks missing document {name} as {state}")

    for schema in sorted((root / "docs").glob("*.schema.json")):
        try:
            parsed = json.loads(schema.read_text(encoding="utf-8"))
            if not isinstance(parsed, dict):
                raise ValueError("schema root must be an object")
        except (json.JSONDecodeError, ValueError) as exc:
            errors.append(f"invalid JSON schema {schema.relative_to(root)}: {exc}")

    for name in SKILL_NAMES:
        skill = root / "skills" / name / "SKILL.md"
        if not skill.is_file():
            errors.append(f"missing skill file: skills/{name}/SKILL.md")
            continue
        text = skill.read_text(encoding="utf-8")
        rel = skill.relative_to(root)
        if not text.startswith("---\n"):
            errors.append(f"invalid skill frontmatter start: {rel}")
            continue
        end = text.find("\n---\n", 4)
        if end < 0:
            errors.append(f"unterminated skill frontmatter: {rel}")
            continue
        fields: dict[str, str] = {}
        malformed = False
        for line in text[4:end].splitlines():
            if not line or line.lstrip().startswith("#"):
                continue
            match = re.fullmatch(r"(name|description):[ \t]*(.+?)[ \t]*", line)
            if not match:
                malformed = True
                break
            key, value = match.groups()
            if key in fields or not value.strip("\"'"):
                malformed = True
                break
            fields[key] = value.strip()
        if malformed or set(fields) != {"name", "description"} or fields.get("name", "").strip("\"'") != name or not fields.get("description", "").strip("\"'"):
            errors.append(f"invalid skill frontmatter: requires unique name and nonempty description in {rel}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = errors_for(args.root)
    if errors:
        print("Documentation validation FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Documentation validation passed: {args.root.resolve()}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
