"""Regression tests for the structural, link-based repository atlas."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = spec_from_file_location("mm_docs_coverage", ROOT / "scripts/docs/coverage.py")
assert SPEC is not None and SPEC.loader is not None
coverage = module_from_spec(SPEC)
SPEC.loader.exec_module(coverage)


def _fixture(tmp_path):
    src = tmp_path / "src" / "mirrormind" / "feature.py"
    src.parent.mkdir(parents=True)
    src.write_text("def work():\n    pass\n", encoding="utf-8")
    atlas = tmp_path / "docs" / "engineering" / "REPOSITORY_ATLAS.md"
    atlas.parent.mkdir(parents=True)
    return src, atlas


def test_atlas_requires_real_markdown_link_not_a_plain_mention(tmp_path):
    _src, atlas = _fixture(tmp_path)
    atlas.write_text("src/mirrormind/feature.py\n", encoding="utf-8")
    needed = {"src/mirrormind/feature.py"}
    assert coverage.missing_atlas_entries(tmp_path, atlas.read_text(), needed) == [
        "src/mirrormind/feature.py"
    ]


def test_atlas_accepts_resolving_link_to_source(tmp_path):
    _src, atlas = _fixture(tmp_path)
    atlas.write_text("[feature](../../src/mirrormind/feature.py)\n", encoding="utf-8")
    needed = {"src/mirrormind/feature.py"}
    assert coverage.missing_atlas_entries(tmp_path, atlas.read_text(), needed) == []


def test_atlas_does_not_count_fenced_code_as_link(tmp_path):
    _src, atlas = _fixture(tmp_path)
    atlas.write_text(
        "```md\n[feature](../../src/mirrormind/feature.py)\n```\n",
        encoding="utf-8",
    )
    missing = coverage.missing_atlas_entries(
        tmp_path, atlas.read_text(), {"src/mirrormind/feature.py"}
    )
    assert missing == ["src/mirrormind/feature.py"]


def test_detects_broken_local_markdown_links(tmp_path):
    _src, atlas = _fixture(tmp_path)
    atlas.write_text("[missing](../../src/mirrormind/missing.py)\n", encoding="utf-8")
    errors = coverage.broken_links(tmp_path)
    assert len(errors) == 1
    assert "missing.py" in errors[0]


def test_external_and_section_links_are_not_local_files(tmp_path):
    _src, atlas = _fixture(tmp_path)
    atlas.write_text(
        "[site](https://example.com) [section](#section)\n",
        encoding="utf-8",
    )
    assert coverage.broken_links(tmp_path) == []


def test_live_repository_passes_linked_inventory():
    assert coverage.audit(ROOT) == []
