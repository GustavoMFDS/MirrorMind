"""Public lock input drift and private-source exclusion tests."""
from pathlib import Path

import pytest

from scripts.check_public_lock import ROOT, expected_requirements


def test_public_lock_input_matches_project_metadata():
    assert (ROOT / "requirements/public-dev.in").read_text(
        encoding="utf-8"
    ) == expected_requirements(ROOT)


def test_public_lock_rejects_direct_reference(tmp_path: Path):
    project = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    project = project.replace(
        '"fastapi>=0.115,<1"', '"fictional @ https://example.invalid/archive.whl"', 1
    )
    (tmp_path / "pyproject.toml").write_text(project, encoding="utf-8")
    with pytest.raises(ValueError, match="direct references"):
        expected_requirements(tmp_path)


def test_public_lock_contains_no_private_engine_reference():
    lock = (ROOT / "requirements/public-dev.txt").read_text(encoding="utf-8")
    assert "worldkernel" not in lock.lower()
    assert "git+" not in lock
