#!/usr/bin/env python3
"""Synchronize maintained files in the standalone skill package.

Use --check for a read-only check. Existing unrelated configuration is retained.
Historical UTF-8 BOM and trailing whitespace differences are ignored for text.
"""

import argparse
from pathlib import Path
import shutil
import sys


def maintained_paths(root):
    paths = [Path("SKILL.md"), Path("LICENSE"), Path("NOTICE.md"), Path("agents/openai.yaml")]
    for directory in ("skill", "examples"):
        paths.extend(path.relative_to(root) for path in sorted((root / directory).rglob("*.md")))
    paths.extend(Path("docs") / name for name in (
        "prompt_safety.md", "versioning.md", "reference-fidelity-validation.md",
    ))
    paths.extend(Path(path) for path in (
        "scripts/verify_protected_region.py", "tests/test_verify_protected_region.py",
    ))
    return paths


def normalized(data):
    return data.decode("utf-8-sig").rstrip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    package = root / "skills" / "female-portrait-director"
    changed = []
    paths = maintained_paths(root)
    for relative in paths:
        source = root / relative
        destination = package / relative
        if not source.is_file():
            print("Missing source: " + str(relative), file=sys.stderr)
            return 2
        if destination.is_file() and normalized(source.read_bytes()) == normalized(destination.read_bytes()):
            continue
        changed.append(str(relative))
        if not args.check:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
    if args.check and changed:
        print("Missing or stale package files:\n" + "\n".join(changed))
        return 1
    print(f"{'Checked' if args.check else 'Synchronized'} {len(paths)} maintained files; {len(changed)} updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
