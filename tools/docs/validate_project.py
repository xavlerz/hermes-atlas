from pathlib import Path
import re
import subprocess
from core_docs import REQUIRED, core_docs_directory

def git_root(root: Path) -> Path:
    result = subprocess.run(["git", "-C", str(root.resolve()), "rev-parse", "--show-toplevel"], check=True, text=True, capture_output=True)
    actual = Path(result.stdout.strip()).resolve()
    if actual != root.resolve():
        raise ValueError(f"target must be Git root: {actual}")
    return actual

def errors_for(root: Path) -> list[str]:
    root = git_root(root)
    errors = []
    docs_dir = core_docs_directory(root)
    for name in REQUIRED:
        doc = docs_dir / name
        if not doc.is_file():
            errors.append(f"missing core document: {docs_dir.relative_to(root) / name if docs_dir != root else name}")
            continue
        for target in re.findall(r"\[[^]]*\]\(([^)]+)\)", doc.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            path, _, anchor = target.partition("#")
            linked = (doc.parent / path).resolve() if path else doc
            if path and not linked.is_file():
                errors.append(f"broken link in {docs_dir.relative_to(root) / name if docs_dir != root else name}: {target}")
            elif anchor and linked.is_file():
                headings = {re.sub(r"[^\w -]", "", h.group(1).lower()).strip().replace(" ", "-") for h in re.finditer(r"^#+\s+(.+)$", linked.read_text(encoding="utf-8"), re.M)}
                if anchor not in headings:
                    errors.append(f"broken anchor in {docs_dir.relative_to(root) / name if docs_dir != root else name}: {target}")
    return errors

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generic third-party project docs/link checker")
    parser.add_argument("project_root", type=Path)
    args = parser.parse_args()
    try:
        errors = errors_for(args.project_root)
    except (ValueError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}"); return 2
    for error in errors: print(error)
    print("Project documentation check " + ("FAILED" if errors else "passed"))
    return bool(errors)
if __name__ == "__main__":
    raise SystemExit(main())
