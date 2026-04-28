import json
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from scripts.constants import Rarity, WeaponType
from scripts.fetch_htmls import fetch_html_from_url as fetch_html
from scripts.skin_dict_template import skin_template

_DEBUG_HTML_DIR = Path(__file__).resolve().parent.parent / "debug_html"




# for weapon skin url in weapon skin urls:

# store weapon skin url html data in CACHE and store as a variable. 
# create a skin dict from the template
# assign extraction points to each bit of the weapon skin class
# once all points of data has been extracted, do checks to ensure we have everything 
# once checks have been completed, delete weapon skin url html data from cache and free the memory
# convert the weapon skin dict to a json file and store it in raw jsons

def store_html(weapon_skin_url):
    referer = "https://csgoskins.gg/weapons"
    html = fetch_html(weapon_skin_url, referer=referer)
    if html == "":
        raise ValueError(f"Failed to fetch HTML for URL: {weapon_skin_url}")
    
    soup = BeautifulSoup(html, 'html.parser')
    toolbar = soup.find("nav", class_="bg-gray-800 shadow-md fixed custom-fixed-overlay w-full z-40")
    if toolbar:
        toolbar.decompose()
    else:
        print("Toolbar not found in HTML, skipping removal.")
    return str(soup)


def _safe_debug_name(value: str) -> str:
    return "".join(char if char.isalnum() or char in "-._" else "-" for char in value).strip("-") or "unknown"


def _save_debug_html(weapon_skin_url: str, html: str):
    _DEBUG_HTML_DIR.mkdir(parents=True, exist_ok=True)
    slug = _safe_debug_name(urlparse(weapon_skin_url).path.strip("/").replace("/", "_"))
    debug_path = _DEBUG_HTML_DIR / f"{slug}.html"
    debug_path.write_text(html, encoding="utf-8")
    print(f"Saved failing HTML to: {debug_path}")

def extract_weapon_in_game_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    steam_link = soup.find('a', href=lambda h: h and h.startswith('steam://'))
    return steam_link.get('href', '') if steam_link else ''

def extract_weapon_workshop_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    workshop_link = soup.find('a', string=lambda s: s and s.strip() == 'View Submission')
    return workshop_link.get('href', '') if workshop_link else ''

def extract_is_pattern_based(html):
    soup = BeautifulSoup(html, 'html.parser')
    patterned_elem = None
    for div in soup.find_all('div'):
        if div.get_text(strip=True) == 'Pattern Variants':
            patterned_elem = div
            break
    if patterned_elem:
        parent = patterned_elem.find_parent('div', class_='flex')
        if parent:
            value_div = parent.find('div', class_='grow')
            if value_div:
                patterned_text = value_div.get_text().strip().lower()
                return patterned_text == 'yes'
    return False

def extract_weapon_webm_and_download(
    html,
    save_dir: str = "/home/eyes/workspace/eyes/skin-scraper/webm"
) -> str:
    soup = BeautifulSoup(html, "html.parser")
    canvas = soup.find('canvas', attrs={'data-video-url': True})
    webm_url = canvas.get('data-video-url', '') if canvas else ''
    if not webm_url:
        raise ValueError("Missing data-video-url for skin preview.")

    # 3. filename from URL
    filename = str(urlparse(webm_url).path.split("/")[-1])
    if not filename:
        raise ValueError(f"Could not derive preview filename from URL: {webm_url}")

    # fallback safety
    if not filename.endswith(".webm"):
        raise ValueError(f"Preview URL does not point to a .webm file: {webm_url}")

    # 4. save path
    file_path = Path(save_dir) / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # 5. download binary (NOT via fetch_html_from_url)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    with requests.get(webm_url, stream=True, headers=headers, timeout=15) as r:
        r.raise_for_status()
        content_type = r.headers.get("Content-Type", "").lower()
        if "video" not in content_type and "webm" not in content_type:
            raise ValueError(
                f"Preview download returned unexpected content type: {content_type or 'unknown'}"
            )

        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    return str(file_path)

def extract_collection(html):
    soup = BeautifulSoup(html, "html.parser")

    results = ""

    for a in soup.select("a.group[href*='/collections/']"):
        name_tag = a.select_one("div.font-medium")

        if name_tag:
            results = name_tag.get_text(strip=True)
            break

    return results



def extract_weapon_rarity(html):
    soup = BeautifulSoup(html, 'html.parser')
    rarity_elem = soup.find('div', string=lambda s: s and s.strip() == 'Rarity')
    if rarity_elem:
        next_div = rarity_elem.find_next_sibling('div')
        if next_div:
            rarity_str = next_div.get_text().strip()
            rarity = getattr(Rarity, rarity_str.upper().replace(' ', '_'), None)
            return rarity.value if rarity else None
    return None

def extract_weapon_type(html):
    name = extract_skin_name(html)
    if not name:
        raise ValueError("Missing Product JSON-LD name for skin page.")

    weapon_str = name.split(' | ')[0] if ' | ' in name else ''
    weapon_type = getattr(WeaponType, weapon_str.upper().replace('-', '_').replace(' ', '_'), None)
    if weapon_type is None:
        raise ValueError(f"Unknown weapon type derived from skin name: {name}")
    return weapon_type.value

def extract_skin_name(html):
    soup = BeautifulSoup(html, "html.parser")
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_ld_scripts:
        try:
            if not script.string:
                continue
            data = json.loads(script.string)
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(data, dict) and data.get('@type') == 'Product':
            name = data.get('name')
            if isinstance(name, str) and name.strip():
                return name.strip()
    return None

def extract_skin_data_from_html(html):
    skin_dict = skin_template.copy()

    skin_name = extract_skin_name(html)
    if not skin_name:
        raise ValueError("Missing Product JSON-LD block or product name.")

    skin_dict["name"] = skin_name
    skin_dict["weapon"] = extract_weapon_type(html)
    skin_dict["rarity"] = extract_weapon_rarity(html)
    skin_dict["collection"] = extract_collection(html)
    skin_dict["webm_filepath"] = extract_weapon_webm_and_download(html)
    skin_dict["is_patterned_based"] = extract_is_pattern_based(html)
    skin_dict["workshop_url"] = extract_weapon_workshop_url(html)
    skin_dict["in_game_url"] = extract_weapon_in_game_url(html)
    skin_dict["colors"] = []
    skin_dict["tags"] = []

    # Do check before returning skin dict

    return skin_dict

def skin_dict_to_json(skin_dict):
    
    skin_json = json.dumps(skin_dict, indent=4)

    if skin_json == "":
        raise ValueError("Failed to convert skin dict to JSON.")
    
    print(skin_json)
    return skin_json
    

def weapon_url_to_json(weapon_skin_url):
    skin_html = store_html(weapon_skin_url)
    try:
        skin_dict = extract_skin_data_from_html(skin_html)
    except Exception:
        _save_debug_html(weapon_skin_url, skin_html)
        raise


    return skin_dict
