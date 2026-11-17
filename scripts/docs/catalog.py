#!/usr/bin/env python3
"""Generate an AST-based symbol reference for the repository's Python source."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "src"
OUTPUT = ROOT / "docs" / "engineering" / "generated" / "SYMBOLS.md"


def escape(value: str) -> str:
    return " ".join(value.replace("|", r"\|").split())


def signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    lead = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    args = ast.unparse(node.args)
    annotation = f" -> {ast.unparse(node.returns)}" if node.returns else ""
    return f"{lead} {node.name}({args}){annotation}"


def symbols(body: list[ast.stmt]):
    for node in body:
        if isinstance(node, ast.ClassDef):
            yield node.name, "class", f"class {node.name}", node
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    yield f"{node.name}.{child.name}", "method", signature(child), child
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node.name, "function", signature(node), node


def build() -> str:
    files = sorted(SOURCE.rglob("*.py"))
    if not files:
        raise RuntimeError("No Python sources under src/")
    lines = [
        "# Source symbol catalog (generated)",
        "",
        "> GENERATED from Python AST. Do not edit manually. Source of truth: `src/`.",
        "> This is a *static* declaration/import index, not a verified call graph,",
        "> behavioral contract, runtime dependency graph or proof of correctness.",
        "",
        "Generate: `python scripts/docs/catalog.py --write`.",
        "Check: `python scripts/docs/catalog.py --check`.",
        "",
    ]
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        module = ".".join(path.relative_to(SOURCE).with_suffix("").parts)
        source = path.read_text(encoding="utf-8")
        parsed = ast.parse(source, filename=relative)
        lines += [f"## `{escape(module)}`", "", f"Source: [`{relative}`](../../../{relative})", ""]
        imports = set()
        for node in ast.walk(parsed):
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add("." * node.level + (node.module or ""))
        if imports:
            joined = ", ".join(f"`{escape(i)}`" for i in sorted(imports))
            lines += [f"Static imports (including inside functions): {joined}", ""]
        entries = list(symbols(parsed.body))
        if entries:
            lines += ["| Symbol | Kind | Signature | Docstring first line | Source |",
                      "| --- | --- | --- | --- | --- |"]
            for label, kind, sig, node in entries:
                first = (ast.get_docstring(node) or "").strip().splitlines()
                summary = escape(first[0])[:180] if first else "—"
                lines.append(
                    f"| `{escape(label)}` | {kind} | `{escape(sig)}` | "
                    f"{summary} | [L{node.lineno}](../../../{relative}#L{node.lineno}) |"
                )
            lines.append("")
        else:
            lines += ["No top-level classes or functions.", ""]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true", help="Write the current catalog")
    group.add_argument("--check", action="store_true", help="Fail when committed catalog differs")
    args = parser.parse_args()
    generated = build()
    if args.check:
        if not OUTPUT.exists():
            print(f"Missing {OUTPUT.relative_to(ROOT)}; run --write", file=sys.stderr)
            return 1
        if OUTPUT.read_text(encoding="utf-8") != generated:
            print("Catalog is stale; run --write and commit the result.", file=sys.stderr)
            return 1
        print("Symbol catalog is current.")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(generated, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
