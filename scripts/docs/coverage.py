#!/usr/bin/env python3
"""Verify a linked repository atlas and local Markdown targets.

Structural inventory only: this cannot prove documentation semantics,
test sufficiency, data provenance, or product security.
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
ATLAS = ROOT / "docs" / "engineering" / "REPOSITORY_ATLAS.md"
CATALOG = ROOT / "docs" / "engineering" / "generated" / "SYMBOLS.md"
ROOT_FILES = {
    ".env.example", ".gitignore", "AGENTS.md", "README.md",
    "Dockerfile", "compose.yml", "pyproject.toml",
}
TRACKED_DIRS = ("src/", "tests/", "scripts/", "examples/", "docs/", ".github/")


def tracked_paths(root: Path) -> set[str]:
    """Git-tracked plus untracked, nonignored paths during a PR."""
    proc = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "--others",
         "--exclude-standard", "-z"],
        check=True, capture_output=True,
    )
    return {
        raw.decode("utf-8").replace("\\", "/")
        for raw in proc.stdout.split(b"\0")
        if raw and (
            raw.decode("utf-8").replace("\\", "/").startswith(TRACKED_DIRS)
            or raw.decode("utf-8").replace("\\", "/") in ROOT_FILES
        )
    }


def markdown_links(text: str) -> list[str]:
    """Find Markdown links even with code-formatted labels.

    A link displayed *inside* inline code is not a navigable link.
    A code-formatted label, e.g. [`module.py`](module.py), is valid.
    """
    no_blocks = re.sub(r"(?ms)^\x60\x60\x60.*?^\x60\x60\x60[ \t]*$", "", text)
    code_spans = [
        match.span() for match in re.finditer(r"\x60[^\x60\n]*\x60", no_blocks)
    ]
    found: list[str] = []
    for match in re.finditer(r"(?<!!)\[[^\]\n]+\]\(([^)\s]+)\)", no_blocks):
        if not any(start <= match.start() < end for start, end in code_spans):
            found.append(match.group(1))
    return found

def local_target(root: Path, document: Path, href: str) -> Path | None:
    url = unquote(href.split("#", 1)[0])
    if not url or url.startswith(("https://", "http://", "mailto:")):
        return None
    return (document.parent / url).resolve()


def missing_atlas_entries(
    root: Path, atlas_text: str, required: set[str],
) -> list[str]:
    """Only an actual resolving Markdown link counts as an atlas entry."""
    atlas = root / "docs/engineering/REPOSITORY_ATLAS.md"
    mentioned = {
        p.relative_to(root.resolve()).as_posix()
        for href in markdown_links(atlas_text)
        if (p := local_target(root, atlas, href)) is not None
        and p.is_relative_to(root.resolve())
    }
    return sorted(required - mentioned)


def broken_links(root: Path) -> list[str]:
    docs = sorted((root / "docs").rglob("*.md"))
    docs += [root / "README.md", root / "AGENTS.md"]
    errors: list[str] = []
    for document in docs:
        if not document.is_file():
            continue
        for href in markdown_links(document.read_text(encoding="utf-8")):
            target = local_target(root, document, href)
            if target is not None and (
                not target.is_relative_to(root.resolve()) or not target.exists()
            ):
                errors.append(f"{document.relative_to(root)} -> {href}")
    return errors


def audit(root: Path) -> list[str]:
    atlas, catalog = (
        root / "docs/engineering/REPOSITORY_ATLAS.md",
        root / "docs/engineering/generated/SYMBOLS.md",
    )
    if not atlas.is_file():
        return ["Missing docs/engineering/REPOSITORY_ATLAS.md"]
    errors: list[str] = []
    required = tracked_paths(root)
    errors += [
        f"Atlas has no resolving link to: {path}"
        for path in missing_atlas_entries(root, atlas.read_text(encoding="utf-8"), required)
    ]
    if not catalog.is_file():
        errors.append("Missing generated symbol catalog")
    else:
        text = catalog.read_text(encoding="utf-8")
        for path in sorted((root / "src").rglob("*.py")):
            module = ".".join(path.relative_to(root / "src").with_suffix("").parts)
            if f"## `{module}`" not in text:
                errors.append(f"Catalog omits source module: {path.relative_to(root)}")
    errors += [f"Broken local Markdown link: {item}" for item in broken_links(root)]
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    try:
        problems = audit(ROOT)
    except (OSError, subprocess.CalledProcessError, UnicodeError) as exc:
        problems = [f"Cannot check repository inventory: {exc}"]
    for problem in problems:
        print(problem)
    if problems:
        return 1
    print("Every tracked project surface has a resolving atlas link; local links resolve.")
    print("This does not prove semantic correctness, tests, or production readiness.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
