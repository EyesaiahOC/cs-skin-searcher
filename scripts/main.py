import json
import random
import time
from pathlib import Path

from scripts.constants import WeaponType
from scripts.fetch_htmls import fetch_and_save_weapon_html, weapon_type_to_file_path
from scripts.html_to_weapon_urls import weapon_type_to_weapon_urls
from scripts.weapon_url_to_json import weapon_url_to_json

_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "raw_json"
_SKIN_PAUSE_MIN = 3.0
_SKIN_PAUSE_MAX = 7.0
_WEAPON_PAUSE_MIN = 8.0
_WEAPON_PAUSE_MAX = 15.0


def _jitter_sleep(min_s: float, max_s: float):
    time.sleep(random.uniform(min_s, max_s))


def _safe_name(name: str) -> str:
    return name.replace(" | ", "-").replace("/", "-")


def main():
    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for weapon_type in WeaponType:
        print(f"\n=== {weapon_type.value} ===")

        cache_path = weapon_type_to_file_path(weapon_type)
        if not cache_path.exists():
            print(f"  Fetching HTML for {weapon_type.value}…")
            try:
                fetch_and_save_weapon_html(weapon_type)
            except Exception as e:
                print(f"  Failed to fetch HTML: {e} — skipping weapon")
                _jitter_sleep(_WEAPON_PAUSE_MIN, _WEAPON_PAUSE_MAX)
                continue
            _jitter_sleep(_WEAPON_PAUSE_MIN, _WEAPON_PAUSE_MAX)

        try:
            skin_urls = weapon_type_to_weapon_urls(weapon_type)
        except Exception as e:
            print(f"  Failed to parse URLs: {e} — skipping weapon")
            continue

        made_requests = False
        for name, url in skin_urls.items():
            output_path = _OUTPUT_DIR / f"{_safe_name(name)}.json"
            if output_path.exists():
                print(f"  [skip] {name}")
                continue

            made_requests = True
            try:
                skin_dict = weapon_url_to_json(url)
                with open(output_path, "w") as f:
                    json.dump(skin_dict, f, indent=4)
                print(f"  [done] {name}")
            except Exception as e:
                print(f"  [fail] {name}: {e}")

            _jitter_sleep(_SKIN_PAUSE_MIN, _SKIN_PAUSE_MAX)

        if made_requests:
            _jitter_sleep(_WEAPON_PAUSE_MIN, _WEAPON_PAUSE_MAX)

    print("\nAll done!")


if __name__ == "__main__":
    main()
