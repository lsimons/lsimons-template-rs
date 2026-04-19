#!/usr/bin/env python3
"""Rename this template to a new project.

Replaces the placeholder token `template` (and its compound forms:
`lsimons-template`, `lsimons_template`, `template-py`, `template-ts`,
`template-go`, `template-rs`) with your project name throughout source
files, manifests, and directory names.

Default name is auto-detected from the git remote basename (stripped of
a `lsimons-` prefix and of a language-suffix like `-mono/-py/-ts/-go/
-rs`), falling back to the current directory name. Pass `--name` to
override.

Idempotent: re-running after the rename is a no-op.

Usage:
    python3 scripts/init.py              # auto-detect + apply
    python3 scripts/init.py --name foo   # explicit name
    python3 scripts/init.py --dry-run    # show what would change
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

PLACEHOLDER = "template"

# Compound identifier patterns — replaced in any text file.
COMPOUND_PATTERNS = [
    "lsimons-{}",
    "lsimons_{}",
    "{}-py",
    "{}-ts",
    "{}-go",
    "{}-rs",
]

# File suffixes where we also replace bare `template` at word boundaries
# (it's unambiguously an identifier).
CODE_SUFFIXES = {
    ".toml",
    ".json",
    ".yaml",
    ".yml",
    ".py",
    ".ts",
    ".js",
    ".mjs",
    ".go",
    ".mod",
    ".rs",
    ".work",
    ".sh",
    ".lock",
}

# Prose files: only compound patterns are replaced; bare `template`
# kept as-is (likely descriptive English in a README).
PROSE_SUFFIXES = {".md"}

IGNORE_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "target",
    "dist",
    "build",
    "site-packages",
    "__pycache__",
    ".mise",
    ".pytest_cache",
    ".ruff_cache",
    ".next",
}

BARE_PATTERN = re.compile(r"\b" + re.escape(PLACEHOLDER) + r"\b")


def detect_name() -> str:
    """Derive a sensible project name from git remote or cwd."""
    name = ""
    try:
        url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        name = url.rstrip("/").rsplit("/", 1)[-1]
        if name.endswith(".git"):
            name = name[:-4]
    except Exception:
        pass
    if not name:
        name = Path.cwd().name
    if name.startswith("lsimons-"):
        name = name[len("lsimons-") :]
    for suffix in ("-mono", "-py", "-ts", "-go", "-rs"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    return name


def walk_files(root: Path):
    for path in root.rglob("*"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.suffix not in CODE_SUFFIXES and path.suffix not in PROSE_SUFFIXES:
            continue
        yield path


def walk_dirs(root: Path):
    matches = []
    for path in root.rglob("*"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if not path.is_dir():
            continue
        if PLACEHOLDER in path.name:
            matches.append(path)
    matches.sort(key=lambda p: len(p.parts), reverse=True)
    return matches


def substitute_text(text: str, suffix: str, new_name: str) -> str:
    for pattern in COMPOUND_PATTERNS:
        text = text.replace(
            pattern.format(PLACEHOLDER),
            pattern.format(new_name),
        )
    if suffix in CODE_SUFFIXES:
        text = BARE_PATTERN.sub(new_name, text)
    return text


def substitute_dirname(name: str, new_name: str) -> str:
    for pattern in COMPOUND_PATTERNS:
        name = name.replace(
            pattern.format(PLACEHOLDER),
            pattern.format(new_name),
        )
    if name == PLACEHOLDER:
        name = new_name
    return name


def file_has_placeholder(text: str, suffix: str) -> bool:
    if any(pattern.format(PLACEHOLDER) in text for pattern in COMPOUND_PATTERNS):
        return True
    return suffix in CODE_SUFFIXES and BARE_PATTERN.search(text) is not None


def already_initialized(root: Path) -> bool:
    for path in walk_files(root):
        if path.name == "init.py" and "scripts" in path.parts:
            continue
        if file_has_placeholder(path.read_text(errors="ignore"), path.suffix):
            return False
    for _ in walk_dirs(root):
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--name", help="Project name (default: auto-detected)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print changes without applying",
    )
    args = parser.parse_args()

    root = Path.cwd()
    new_name = args.name or detect_name()

    if not new_name or new_name == PLACEHOLDER:
        print(
            f"Auto-detected name is empty or equal to the placeholder "
            f"'{PLACEHOLDER}'. Pass --name explicitly.",
            file=sys.stderr,
        )
        return 1

    if already_initialized(root):
        print(f"Nothing to do: no '{PLACEHOLDER}' placeholders found — already initialized.")
        return 0

    print(f"Renaming '{PLACEHOLDER}' → '{new_name}'")
    if args.dry_run:
        print("(dry-run; no changes will be written)")

    for path in walk_files(root):
        if path.name == "init.py" and "scripts" in path.parts:
            continue
        original = path.read_text(errors="ignore")
        updated = substitute_text(original, path.suffix, new_name)
        if updated != original:
            print(f"  update: {path.relative_to(root)}")
            if not args.dry_run:
                path.write_text(updated)

    for path in walk_dirs(root):
        new_path = path.parent / substitute_dirname(path.name, new_name)
        if new_path == path:
            continue
        print(f"  rename: {path.relative_to(root)} -> {new_path.relative_to(root)}")
        if not args.dry_run:
            path.rename(new_path)

    if args.dry_run:
        print("\nDry-run complete. Re-run without --dry-run to apply.")
    else:
        print(
            f"\nDone. Review with `git diff` / `git status`, then commit:\n"
            f"  git add -A && git commit -m 'chore: init template as {new_name}'"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
