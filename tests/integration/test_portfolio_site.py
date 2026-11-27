"""Contract tests for the public-only static portal builder."""

import json
import re

import pytest

from examples.build_portfolio_site import OUTPUT_FILES, build_site


def test_public_site_has_only_explicit_synthetic_files(tmp_path):
    output = tmp_path / "site"
    sha = "a" * 40
    build_site(output, sha)
    assert {p.name for p in output.iterdir()} == OUTPUT_FILES
    assert all(p.is_file() and not p.is_symlink() for p in output.iterdir())
    manifest = json.loads((output / "build.json").read_text(encoding="utf-8"))
    assert manifest["source_sha"] == sha
    assert manifest["synthetic_only"] is True
    home = (output / "index.html").read_text(encoding="utf-8")
    assert "__SHA__" not in home
    assert sha in home
    assert 'href="demo.html"' in home
    assert "README.pt-BR.md" in home
    report = (output / "demo.html").read_text(encoding="utf-8")
    payload = re.search(
        r'<script id="workflow-result" type="application/json">(.*?)</script>',
        report, re.DOTALL,
    )
    assert payload is not None
    result = json.loads(payload.group(1))
    assert manifest["trace_sha256"] == result["trace_sha256"]
    assert result["action_authorized"] is False
    assert result["ingestion_authorized"] is False
    assert result["worldkernel_execution"] == "worldkernel_not_invoked"


def test_site_refuses_existing_directory_and_invalid_sha(tmp_path):
    existing = tmp_path / "site"
    existing.mkdir()
    sentinel = existing / "keep.txt"
    sentinel.write_text("keep", encoding="utf-8")
    with pytest.raises(ValueError):
        build_site(existing, "a" * 40)
    assert sentinel.read_text(encoding="utf-8") == "keep"
    with pytest.raises(ValueError):
        build_site(tmp_path / "new", "<invalid>")
    assert not (tmp_path / "new").exists()
