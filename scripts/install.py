#!/usr/bin/env python3
"""Link this collection into a personal skill directory without replacing content."""

import argparse
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    codex_home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=codex_home / "skills",
        help="Skill directory to link into (default: CODEX_HOME/skills or ~/.codex/skills)",
    )
    args = parser.parse_args()
    target_dir = args.target_dir.expanduser().absolute()
    source_dir = Path(__file__).resolve().parent.parent / "skills"
    sources = sorted(p for p in source_dir.iterdir() if (p / "SKILL.md").is_file())

    # Check every destination before adding links, so a conflict leaves the
    # existing installation intact rather than installing part of a collection.
    pending = []
    for source in sources:
        target = target_dir / source.name
        if target.is_symlink() and target.resolve() == source.resolve():
            print(f"Already linked: {target}")
        elif target.exists() or target.is_symlink():
            parser.exit(1, f"Refusing to replace existing path: {target}\n")
        else:
            pending.append((source, target))

    target_dir.mkdir(parents=True, exist_ok=True)
    for source, target in pending:
        target.symlink_to(source, target_is_directory=True)
        print(f"Linked: {target} -> {source}")


if __name__ == "__main__":
    main()
