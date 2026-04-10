import json
from bs4 import BeautifulSoup

from scripts.skin_dict_template import skin_template
from scripts.fetch_htmls import fetch_html_from_url as fetch_html
from scripts.constants import Source, WeaponType, Rarity
from scripts.skin_dict_template import skin_template




# for weapon skin url in weapon skin urls:

# store weapon skin url html data in CACHE and store as a variable. 
# create a skin dict from the template
# assign extraction points to each bit of the weapon skin class
# once all points of data has been extracted, do checks to ensure we have everything 
# once checks have been completed, delete weapon skin url html data from cache and free the memory
# convert the weapon skin dict to a json file and store it in raw jsons

def store_html(weapon_skin_url):
    html = fetch_html(weapon_skin_url)
    if html == "":
        raise ValueError(f"Failed to fetch HTML for URL: {weapon_skin_url}")
    return html

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

def extract_weapon_webm_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    canvas = soup.find('canvas', attrs={'data-video-url': True})
    return canvas.get('data-video-url', '') if canvas else ''

def extract_weapon_source_type_and_name(html):
    soup = BeautifulSoup(html, 'html.parser')

    source_anchor = None
    for parent in soup.find_all('div', class_='flex'):
        label_div = parent.find('div', class_='flex-none')
        if label_div and label_div.get_text(strip=True) == 'Update':
            source_anchor = parent.find('a', class_='custom-underline')
            break

    if source_anchor is None:
        return None

    source_text = source_anchor.get_text().strip().strip('"')
    for source_member in Source:
        if source_member.value == source_text:
            return source_member

    raise ValueError(f'source does not exist in constants: "{source_text}"')


def extract_weapon_rarity(html):
    soup = BeautifulSoup(html, 'html.parser')
    rarity_elem = soup.find('div', string=lambda s: s and s.strip() == 'Rarity')
    if rarity_elem:
        next_div = rarity_elem.find_next_sibling('div')
        if next_div:
            rarity_str = next_div.get_text().strip()
            return getattr(Rarity, rarity_str.upper().replace(' ', '_'), None)
    return None

def extract_weapon_type(html):
    name = extract_skin_name(html)
    weapon_str = name.split(' | ')[0] if ' | ' in name else ''
    return getattr(WeaponType, weapon_str.upper().replace('-', '_').replace(' ', '_'), None)

def extract_skin_name(html):
    soup = BeautifulSoup(html, "html.parser")
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_ld_scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get('@type') == 'Product':
                return data.get('name', 'Unknown Skin Name')
        except json.JSONDecodeError:
            continue

def extract_skin_data_from_html(html):

    skin_dict = skin_template.copy()

    skin_dict["name"] = extract_skin_name(html)
    skin_dict["weapon"] = extract_weapon_type(html)
    skin_dict["rarity"] = extract_weapon_rarity(html)
    skin_dict["source"] = extract_weapon_source_type_and_name(html)
    skin_dict["webm_url"] = extract_weapon_webm_url(html)
    skin_dict["is_patterned_based"] = extract_is_pattern_based(html)
    skin_dict["workshop_url"] = extract_weapon_workshop_url(html)
    skin_dict["in_game_url"] = extract_weapon_in_game_url(html)

    # Do check before returning skin dict

    return skin_dict

def skin_dict_to_json(skin_dict):

    skin_json = json.dumps(skin_dict, indent=4)
    return skin_json
    

def weapon_url_to_json(weapon_skin_url):
    
    skin_html = store_html(weapon_skin_url)
    skin_dict = extract_skin_data_from_html(skin_html)
    skin_json = skin_dict_to_json(skin_dict)

    return skin_json


