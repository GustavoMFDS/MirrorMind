#!/usr/bin/env python3
"""Verify curated claim/guide/test links, not the truth of documented claims.

Pure structural checks: inspect source, assertions, data and runtime
conditions independently. Passing here never means tests were executed.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/engineering/EVIDENCE_MAP.json"
FIELDS = {"id", "guide", "test", "function", "limitation"}


def safe_path(root: Path, name: str, prefix: str, suffix: str) -> Path:
    if not isinstance(name, str) or not name.startswith(prefix) or "\\" in name:
        raise ValueError(f"invalid location: {name!r}")
    candidate = Path(name)
    if candidate.is_absolute() or ".." in candidate.parts or candidate.suffix != suffix:
        raise ValueError(f"unsafe location: {name!r}")
    target = (root / candidate).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f"outside repository: {name!r}")
    return target


def audit(root: Path, manifest: Path) -> list[str]:
    try:
        rows = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"Cannot read evidence map: {exc}"]
    if not isinstance(rows, list) or not rows:
        return ["Evidence map must contain at least one record"]
    errors: list[str] = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != FIELDS:
            errors.append(f"Row {index}: expected exactly {sorted(FIELDS)}")
            continue
        claim_id, guide, test, function, limitation = (
            row[k] for k in ("id", "guide", "test", "function", "limitation")
        )
        if not isinstance(claim_id, str) or re.fullmatch(r"MM-[A-Z]{1,8}-[0-9]{3}", claim_id) is None:
            errors.append(f"Row {index}: invalid claim identifier")
            continue
        if claim_id in seen:
            errors.append(f"Row {index}: duplicate claim identifier {claim_id}")
            continue
        seen.add(claim_id)
        if not isinstance(function, str) or re.fullmatch(r"test_[a-zA-Z0-9_]+", function) is None:
            errors.append(f"Row {index}: invalid test function")
            continue
        if not isinstance(limitation, str) or len(limitation.strip()) < 20:
            errors.append(f"Row {index}: missing meaningful evidence limitation")
            continue
        try:
            guide_path = safe_path(root, guide, "docs/engineering/", ".md")
            test_path = safe_path(root, test, "tests/", ".py")
        except ValueError as exc:
            errors.append(f"Row {index}: {exc}")
            continue
        if not guide_path.is_file() or not test_path.is_file():
            errors.append(f"Row {index}: missing guide/test file ({guide}, {test})")
            continue
        guide_text = guide_path.read_text(encoding="utf-8")
        for item in (claim_id, test, function):
            if item not in guide_text:
                errors.append(f"Row {index}: {guide} does not cite {item}")
        try:
            tree = ast.parse(test_path.read_text(encoding="utf-8"), filename=test)
        except (SyntaxError, UnicodeError, OSError) as exc:
            errors.append(f"Row {index}: cannot parse {test}: {exc}")
            continue
        top_level = {
            node.name for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        if function not in top_level:
            errors.append(f"Row {index}: {test} does not declare top-level {function}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    errors = audit(ROOT, MANIFEST)
    for error in errors:
        print(error)
    if errors:
        return 1
    print("Curated claims cite existing guide paths and top-level pytest functions.")
    print("Evidence limitations remain explicit; test execution and claim truth are NOT checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
