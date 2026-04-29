import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "application"))

from utils import resolve_asset_path


def test_resolves_relative_path(tmp_path):
    (tmp_path / "webm").mkdir()
    f = tmp_path / "webm" / "test.webm"
    f.write_bytes(b"")
    result = resolve_asset_path("webm/test.webm", repo_root=tmp_path)
    assert result == f


def test_resolves_valid_absolute_path(tmp_path):
    f = tmp_path / "test.webm"
    f.write_bytes(b"")
    result = resolve_asset_path(str(f), repo_root=tmp_path)
    assert result == f


def test_returns_none_for_missing_file(tmp_path):
    result = resolve_asset_path("webm/nonexistent.webm", repo_root=tmp_path)
    assert result is None


def test_returns_none_for_empty_string(tmp_path):
    result = resolve_asset_path("", repo_root=tmp_path)
    assert result is None


def test_returns_none_for_broken_absolute(tmp_path):
    result = resolve_asset_path("/home/wrong/path/file.webm", repo_root=tmp_path)
    assert result is None
