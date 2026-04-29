import json
import pytest
from pathlib import Path

from application.skin_store import SkinStore


def _populate(tmp_path: Path, skins: list[dict]) -> SkinStore:
    for i, skin in enumerate(skins):
        (tmp_path / f"skin_{i:04d}.json").write_text(json.dumps(skin))
    store = SkinStore(tmp_path)
    store.load_all()
    return store


def test_load_all_returns_correct_count(tmp_path):
    store = _populate(tmp_path, [{"name": f"Skin {i}"} for i in range(5)])
    assert len(store.load_all()) == 5


def test_save_writes_updated_tags(tmp_path):
    (tmp_path / "skin.json").write_text(json.dumps({"name": "Test", "tags": []}))
    store = SkinStore(tmp_path)
    store.load_all()
    skin = store.get(0)
    skin["tags"] = ["red", "dark"]
    store.save(0, skin)
    data = json.loads((tmp_path / "skin.json").read_text())
    assert data["tags"] == ["red", "dark"]


def test_save_does_not_corrupt_other_fields(tmp_path):
    original = {"name": "AK-47 | Test", "weapon": "AK-47", "rarity": "Covert", "tags": []}
    (tmp_path / "skin.json").write_text(json.dumps(original))
    store = SkinStore(tmp_path)
    store.load_all()
    skin = store.get(0)
    skin["tags"] = ["red"]
    store.save(0, skin)
    data = json.loads((tmp_path / "skin.json").read_text())
    assert data["name"] == original["name"]
    assert data["weapon"] == original["weapon"]
    assert data["rarity"] == original["rarity"]


def test_search_empty_returns_all(tmp_path):
    store = _populate(tmp_path, [{"name": f"Skin {i}", "weapon": "AK-47", "tags": []} for i in range(3)])
    assert store.search("") == [0, 1, 2]


def test_search_weapon_match(tmp_path):
    store = _populate(tmp_path, [
        {"name": "Skin A", "weapon": "AK-47", "tags": []},
        {"name": "Skin B", "weapon": "M4A4", "tags": []},
    ])
    assert store.search("ak-47") == [0]


def test_search_name_match(tmp_path):
    store = _populate(tmp_path, [
        {"name": "AK-47 | Redline", "weapon": "AK-47", "tags": []},
        {"name": "M4A4 | Howl", "weapon": "M4A4", "tags": []},
    ])
    assert store.search("redline") == [0]


def test_search_tag_match(tmp_path):
    store = _populate(tmp_path, [
        {"name": "Skin A", "weapon": "AK-47", "tags": ["graffiti"]},
        {"name": "Skin B", "weapon": "M4A4", "tags": ["clean"]},
    ])
    assert store.search("graffiti") == [0]


def test_untagged_indices_returns_skins_without_tags(tmp_path):
    store = _populate(tmp_path, [
        {"name": "Skin A", "tags": ["red"]},
        {"name": "Skin B", "tags": []},
        {"name": "Skin C"},
    ])
    assert store.untagged_indices() == [1, 2]


def test_untagged_indices_excludes_all_tagged(tmp_path):
    store = _populate(tmp_path, [
        {"name": "Skin A", "tags": ["red"]},
        {"name": "Skin B", "tags": ["blue"]},
    ])
    assert store.untagged_indices() == []
