"""One-time migration: rewrite absolute webm_filepath and thumbnail_path values
in all JSON skin records to paths relative to the repo root.

Safe to run multiple times — already-relative paths are left unchanged.
"""

import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent
_JSON_DIR = _REPO_ROOT / "raw_json"
_MARKER = "skin-scraper/"


def to_relative(path: str) -> str:
    """Strip everything up to and including the repo directory name."""
    idx = path.find(_MARKER)
    if idx != -1:
        return path[idx + len(_MARKER):]
    return path


def migrate_file(json_path: Path) -> bool:
    """Migrate one JSON file. Returns True if the file was modified."""
    data = json.loads(json_path.read_text(encoding="utf-8"))
    changed = False

    for field in ("webm_filepath", "thumbnail_path"):
        original = data.get(field, "")
        if not original:
            continue
        migrated = to_relative(original)
        if migrated != original:
            data[field] = migrated
            changed = True

    if changed:
        json_path.write_text(json.dumps(data, indent=4), encoding="utf-8")

    return changed


def migrate_all(json_dir: Path = _JSON_DIR) -> tuple[int, int]:
    """Migrate all JSON files in json_dir. Returns (total, modified) counts."""
    files = sorted(json_dir.glob("*.json"))
    modified = sum(migrate_file(p) for p in files)
    return len(files), modified


if __name__ == "__main__":
    total, modified = migrate_all()
    print(f"Migrated {modified} / {total} files")
    sys.exit(0)
