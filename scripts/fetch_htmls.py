from pathlib import Path
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from scripts.constants import DEBUG, WeaponType


BASE_WEAPON_URL = "https://csgoskins.gg/weapons"
REPO_ROOT = Path(__file__).resolve().parent.parent
WEBPAGES_DIR = REPO_ROOT / "webpages"
REQUEST_TIMEOUT_SECONDS = 15
REQUEST_PAUSE_SECONDS = 3


def weapon_type_to_slug(weapon_type):
    return weapon_type.value.lower().replace(" ", "-")


def weapon_type_to_page_url(weapon_type):
    slug = weapon_type_to_slug(weapon_type)
    return f"{BASE_WEAPON_URL}/{slug}"


def weapon_type_to_file_path(weapon_type):
    slug = weapon_type_to_slug(weapon_type)
    return WEBPAGES_DIR / f"csgoskins.gg_weapons_{slug}.html"


def fetch_html_from_url(url):
    if DEBUG:
        print(f"Fetching URL: {url}")
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        },
    )
    with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        return response.read().decode("utf-8")


def save_html_to_file(html, file_path):
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(html, encoding="utf-8")
    return file_path


def fetch_and_save_weapon_html(weapon_type):
    url = weapon_type_to_page_url(weapon_type)
    file_path = weapon_type_to_file_path(weapon_type)
    if DEBUG:
        print(f"Fetching HTML for weapon: {weapon_type.name} ({weapon_type.value})")

    try:
        html = fetch_html_from_url(url)
    except HTTPError as error:
        print(f"HTTP error for {weapon_type.name}: {error.code} {error.reason}")
        print(f"Failed URL: {url}")
        raise

    save_html_to_file(html, file_path)
    if DEBUG:
        print(f"Saved HTML to: {file_path}")
    return file_path


def fetch_all_weapon_htmls():
    failed_weapons = []

    for weapon in WeaponType:
        try:
            fetch_and_save_weapon_html(weapon)
        except HTTPError:
            failed_weapons.append(weapon)

        if DEBUG:
            print(f"Pausing {REQUEST_PAUSE_SECONDS} seconds before next request...")
        time.sleep(REQUEST_PAUSE_SECONDS)

    if failed_weapons:
        failed_names = ", ".join(weapon.name for weapon in failed_weapons)
        print(f"Finished with fetch failures for: {failed_names}")
    else:
        if DEBUG:
            print("Finished fetching all weapon HTML files successfully.")
