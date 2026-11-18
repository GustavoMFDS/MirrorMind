"""Fail closed if claims drift from the reviewed capability ledger."""
import json
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = spec_from_file_location("mm_capabilities", ROOT / "scripts/docs/capabilities.py")
assert SPEC is not None and SPEC.loader is not None
guard = module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


def _fixture(tmp_path):
    source = tmp_path / "src/mirrormind/feature.py"
    test = tmp_path / "tests/unit/test_feature.py"
    source.parent.mkdir(parents=True)
    test.parent.mkdir(parents=True)
    source.write_text("def execute():\n    return 1\n", encoding="utf-8")
    test.write_text("def test_execute():\n    assert True\n", encoding="utf-8")
    row = {
        "id": "demonstration",
        "status": "implemented",
        "source": "src/mirrormind/feature.py",
        "test": "tests/unit/test_feature.py::test_execute",
        "notes": "Only the synthetic test is verified, not a production capability.",
    }
    manifest = tmp_path / "capabilities.json"
    manifest.write_text(
        json.dumps({"schema_version": "1", "capabilities": [row]}), encoding="utf-8"
    )
    return row, manifest, test


def test_repository_ledger_has_valid_source_and_test_references():
    assert guard.audit(ROOT, ROOT / "docs/engineering/CAPABILITY_LEDGER.json") == []


def test_valid_ledger_and_renamed_test_fail_closed(tmp_path):
    _row, manifest, test = _fixture(tmp_path)
    assert guard.audit(tmp_path, manifest) == []
    test.write_text("def test_other():\n    pass\n", encoding="utf-8")
    assert "missing top-level pytest function test_execute" in "\n".join(
        guard.audit(tmp_path, manifest)
    )


def test_implemented_status_requires_source_and_test(tmp_path):
    row, manifest, _test = _fixture(tmp_path)
    row["test"] = None
    manifest.write_text(
        json.dumps({"schema_version": "1", "capabilities": [row]}), encoding="utf-8"
    )
    assert "needs source and test" in "\n".join(guard.audit(tmp_path, manifest))


def test_duplicate_name_and_unknown_status_are_rejected(tmp_path):
    row, manifest, _test = _fixture(tmp_path)
    manifest.write_text(
        json.dumps({"schema_version": "1", "capabilities": [row, row]}),
        encoding="utf-8",
    )
    assert "duplicate id" in "\n".join(guard.audit(tmp_path, manifest))
    row["status"] = "magically_complete"
    manifest.write_text(
        json.dumps({"schema_version": "1", "capabilities": [row]}), encoding="utf-8"
    )
    assert "invalid status" in "\n".join(guard.audit(tmp_path, manifest))


def test_planned_capability_can_exist_without_code_but_needs_caveat(tmp_path):
    row, manifest, _test = _fixture(tmp_path)
    row.update({"status": "planned", "source": None, "test": None})
    manifest.write_text(
        json.dumps({"schema_version": "1", "capabilities": [row]}), encoding="utf-8"
    )
    assert guard.audit(tmp_path, manifest) == []
    row["notes"] = "pending"
    manifest.write_text(
        json.dumps({"schema_version": "1", "capabilities": [row]}), encoding="utf-8"
    )
    assert "meaningful caveat" in "\n".join(guard.audit(tmp_path, manifest))
