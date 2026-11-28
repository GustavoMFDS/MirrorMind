#!/usr/bin/env python3
"""Check that the public lock input reflects the current project metadata."""
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def expected_requirements(root: Path) -> str:
    """Resolve direct public requirements only; never query the private engine."""
    meta = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    project = meta["project"]
    requirements = list(project["dependencies"])
    for name in ("dev", "quality", "uci", "review"):
        requirements.extend(project["optional-dependencies"][name])
    requirements.extend(meta["build-system"]["requires"])
    if any("@" in item or "worldkernel" in item.lower() for item in requirements):
        raise ValueError("direct references are outside the public lock scope")
    return "\n".join(dict.fromkeys(requirements)) + "\n"


def main() -> None:
    input_path = ROOT / "requirements/public-dev.in"
    if input_path.read_text(encoding="utf-8") != expected_requirements(ROOT):
        raise SystemExit("Public lock input is stale; regenerate and review the lock.")
    print("Public lock input matches project metadata.")


if __name__ == "__main__":
    main()
