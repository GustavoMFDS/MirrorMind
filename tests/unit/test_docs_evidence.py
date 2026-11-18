"""Curated claim evidence is traceable, not a semantics/proof certificate."""
import json
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = spec_from_file_location("mm_docs_evidence", ROOT / "scripts/docs/evidence.py")
assert SPEC is not None and SPEC.loader is not None
guard = module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


def _fixture(tmp_path):
    guide = tmp_path / "docs/engineering/LESSON.md"
    test = tmp_path / "tests/unit/test_example.py"
    guide.parent.mkdir(parents=True)
    test.parent.mkdir(parents=True)
    guide.write_text(
        "MM-CON-001: tests/unit/test_example.py::test_behavior\n", encoding="utf-8"
    )
    test.write_text("def test_behavior():\n    assert True\n", encoding="utf-8")
    record = {
        "id": "MM-CON-001",
        "guide": "docs/engineering/LESSON.md",
        "test": "tests/unit/test_example.py",
        "function": "test_behavior",
        "limitation": "This demonstrates one synthetic branch, not general correctness.",
    }
    manifest = tmp_path / "map.json"
    manifest.write_text(json.dumps([record]), encoding="utf-8")
    return guide, test, record, manifest


def test_live_claim_map_references_existing_functions():
    assert guard.audit(ROOT, ROOT / "docs/engineering/EVIDENCE_MAP.json") == []


def test_valid_map_and_renamed_function_rejected(tmp_path):
    _guide, test, _record, manifest = _fixture(tmp_path)
    assert guard.audit(tmp_path, manifest) == []
    test.write_text("def test_other():\n    assert True\n", encoding="utf-8")
    assert "does not declare top-level test_behavior" in "\n".join(
        guard.audit(tmp_path, manifest)
    )


def test_guide_must_cite_claim_id_and_exact_test_path(tmp_path):
    guide, _test, _record, manifest = _fixture(tmp_path)
    guide.write_text("test_behavior only\n", encoding="utf-8")
    errors = "\n".join(guard.audit(tmp_path, manifest))
    assert "MM-CON-001" in errors
    assert "tests/unit/test_example.py" in errors


def test_duplicate_claim_id_is_rejected(tmp_path):
    _guide, _test, record, manifest = _fixture(tmp_path)
    manifest.write_text(json.dumps([record, record]), encoding="utf-8")
    assert "duplicate claim identifier" in "\n".join(guard.audit(tmp_path, manifest))


def test_invalid_path_and_missing_limitation_rejected(tmp_path):
    _guide, _test, record, manifest = _fixture(tmp_path)
    manifest.write_text(
        json.dumps([{**record, "test": "tests/../../outside.py"}]), encoding="utf-8"
    )
    assert "unsafe location" in "\n".join(guard.audit(tmp_path, manifest))
    manifest.write_text(
        json.dumps([{**record, "limitation": "unclear"}]), encoding="utf-8"
    )
    assert "meaningful evidence limitation" in "\n".join(guard.audit(tmp_path, manifest))


def test_empty_manifest_and_wrong_shape_rejected(tmp_path):
    _guide, _test, record, manifest = _fixture(tmp_path)
    manifest.write_text("[]", encoding="utf-8")
    assert "at least one record" in "\n".join(guard.audit(tmp_path, manifest))
    record.pop("function")
    manifest.write_text(json.dumps([record]), encoding="utf-8")
    assert "expected exactly" in "\n".join(guard.audit(tmp_path, manifest))
