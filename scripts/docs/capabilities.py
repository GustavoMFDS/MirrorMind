#!/usr/bin/env python3
"""Validate the reviewed MirrorMind capability ledger structurally.

This verifies source/test references and honest status vocabulary, not
runtime behavior, permissions, statistical quality or actual test results.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/engineering/CAPABILITY_LEDGER.json"
FIELDS = {"id", "status", "source", "test", "notes"}
STATUSES = {"implemented", "experimental", "interface_only", "planned", "deferred"}


def _local(root: Path, value: str, prefix: str, suffix: str) -> Path:
    if not isinstance(value, str) or not value.startswith(prefix) or "\\" in value:
        raise ValueError(f"invalid location: {value!r}")
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts or candidate.suffix != suffix:
        raise ValueError(f"unsafe location: {value!r}")
    path = (root / candidate).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"outside root: {value!r}")
    return path


def audit(root: Path, manifest: Path) -> list[str]:
    try:
        document = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"Cannot read ledger: {exc}"]
    if not isinstance(document, dict) or set(document) != {"schema_version", "capabilities"}:
        return ["Ledger requires schema_version and capabilities"]
    rows = document["capabilities"]
    if document["schema_version"] != "1" or not isinstance(rows, list) or not rows:
        return ["Unsupported ledger version or empty capabilities"]
    errors: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(rows):
        if not isinstance(item, dict) or set(item) != FIELDS:
            errors.append(f"Row {index}: invalid ledger field set")
            continue
        name, status, source, test, notes = (
            item[k] for k in ("id", "status", "source", "test", "notes")
        )
        if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9_]{1,79}", name):
            errors.append(f"Row {index}: invalid id")
            continue
        if name in seen:
            errors.append(f"Row {index}: duplicate id {name}")
            continue
        seen.add(name)
        if status not in STATUSES:
            errors.append(f"Row {index}: invalid status for {name}")
            continue
        if not isinstance(notes, str) or len(notes.strip()) < 30:
            errors.append(f"Row {index}: {name} missing a meaningful caveat")
        active = status in {"implemented", "experimental"}
        if active and (source is None or test is None):
            errors.append(f"Row {index}: active capability {name} needs source and test")
        if status == "interface_only" and source is None:
            errors.append(f"Row {index}: interface {name} needs source")
        if source is not None:
            try:
                path = _local(root, source, "src/", ".py")
                if not path.is_file():
                    errors.append(f"Row {index}: missing source {source}")
            except ValueError as exc:
                errors.append(f"Row {index}: {exc}")
        if test is not None:
            if not isinstance(test, str) or test.count("::") != 1:
                errors.append(f"Row {index}: invalid test selector")
                continue
            testfile, fn = test.split("::")
            if not re.fullmatch(r"test_[A-Za-z0-9_]+", fn):
                errors.append(f"Row {index}: invalid pytest function")
                continue
            try:
                path = _local(root, testfile, "tests/", ".py")
            except ValueError as exc:
                errors.append(f"Row {index}: {exc}")
                continue
            if not path.is_file():
                errors.append(f"Row {index}: missing test file {testfile}")
                continue
            try:
                parsed = ast.parse(path.read_text(encoding="utf-8"), filename=testfile)
            except (SyntaxError, OSError, UnicodeError) as exc:
                errors.append(f"Row {index}: cannot parse test file: {exc}")
                continue
            declared = {
                node.name for node in parsed.body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
            if fn not in declared:
                errors.append(f"Row {index}: missing top-level pytest function {fn}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    failures = audit(ROOT, MANIFEST)
    for failure in failures:
        print(failure)
    if failures:
        return 1
    print("Capability ledger paths and top-level pytest selectors are structurally valid.")
    print("Verify live API claims separately; this does not certify execution or safety.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
