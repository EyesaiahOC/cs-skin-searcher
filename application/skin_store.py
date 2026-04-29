import json
import re
from pathlib import Path


class SkinStore:
    def __init__(self, json_dir: Path):
        self._json_dir = Path(json_dir)
        self._files: list[Path] = []
        self._skins: list[dict] = []

    def load_all(self) -> list[dict]:
        self._files = sorted(self._json_dir.glob("*.json"))
        self._skins = [json.loads(p.read_text()) for p in self._files]
        return self._skins

    def get(self, index: int) -> dict:
        return self._skins[index]

    def save(self, index: int, skin: dict) -> None:
        self._skins[index] = skin
        with open(self._files[index], "w") as f:
            json.dump(skin, f, indent=4)

    @staticmethod
    def _normalize(s: str) -> str:
        return re.sub(r'[^a-z0-9]', '', s.lower())

    def search(self, query: str) -> list[int]:
        if not query:
            return list(range(len(self._skins)))
        query_norm = self._normalize(query)
        results = []
        for i, skin in enumerate(self._skins):
            weapon_norm = self._normalize(skin.get("weapon", ""))
            weapon_match = bool(query_norm) and query_norm in weapon_norm
            haystack = " ".join([skin.get("name", ""), *skin.get("tags", [])]).lower()
            if weapon_match or query.lower() in haystack:
                results.append(i)
        return results

    def untagged_indices(self) -> list[int]:
        return [i for i, s in enumerate(self._skins) if not s.get("tags")]
