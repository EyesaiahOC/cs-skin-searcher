import json
from scripts.constants import WeaponType
from scripts.fetch_htmls import weapon_type_to_file_path


def load_html_from_file(file_path):
    with open(file_path, "r") as f:
        return f.read()


def html_to_json_ld_blocks(html):
    print(f"HTML length: {len(html)} characters")

    script_marker = 'type="application/ld+json">'
    blocks = html.split(script_marker)

    print(f"Split produced {len(blocks)} parts")

    json_ld_blocks = []

    for index, block in enumerate(blocks[1:], start=1):
        json_ld = block.split("</script>")[0].strip()
        print(f"Candidate block {index} length: {len(json_ld)}")

        if json_ld:
            json_ld_blocks.append(json_ld)

    print(f"Extracted {len(json_ld_blocks)} JSON-LD blocks")

    if not json_ld_blocks:
        raise ValueError("No JSON-LD blocks were extracted from the HTML.")

    return json_ld_blocks

def json_ld_blocks_to_item_list_block(json_ld_blocks):
    if not json_ld_blocks:
        raise ValueError("No JSON-LD blocks were found in the HTML.")

    for index, block in enumerate(json_ld_blocks, start=1):
        try:
            block_dict = json.loads(block)
        except json.JSONDecodeError:
            print(f"Block {index} is not valid JSON, skipping it.")
            continue

        block_type = block_dict.get("@type")
        print(f"Block {index} has @type = {block_type}")

        if block_type == "ItemList":
            print(f"ItemList block found at block {index}")
            return block

    raise ValueError("No ItemList JSON-LD block was found.")



def json_ld_to_dict(json_ld):
    items_dict = json.loads(json_ld)
    return items_dict


def weapon_count_check(weapon_count, true_weapon_count):
    if weapon_count != true_weapon_count:
        raise ValueError(f"Warning: Weapon count mismatch. Found {weapon_count} weapons, but expected {true_weapon_count}.")
    else:
        print(f"Weapon count check passed. Found {weapon_count} weapons as expected.")
        return


def html_to_weapon_urls(html):
    if html is None:
        raise ValueError("HTML file must be provided for processing.")

    json_ld_blocks = html_to_json_ld_blocks(html)
    item_list_block = json_ld_blocks_to_item_list_block(json_ld_blocks)
    items_dict = json_ld_to_dict(item_list_block)
    item_list_elements = items_dict.get("itemListElement", [])
    urls = {}
    weapon_count = 0
    true_weapon_count = int(items_dict["numberOfItems"])

    for element in item_list_elements:
        item = element.get("item", {})
        url = item.get("url", "")
        name = item.get("name", "")
        urls[name] = url
        weapon_count += 1

    weapon_count_check(weapon_count, true_weapon_count)
    return urls


def file_to_weapon_urls(file_path: str):
    html = load_html_from_file(file_path)
    return html_to_weapon_urls(html)

def weapon_type_to_weapon_urls(weapon_type: WeaponType):
    file_path = weapon_type_to_file_path(weapon_type)
    return file_to_weapon_urls(file_path)
