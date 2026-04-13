from fileinput import filename
import json
import pprint
import time
from pathlib import Path
from scripts.fetch_htmls import fetch_all_weapon_htmls
from scripts.html_to_weapon_urls import weapon_type_to_weapon_urls
from scripts.constants import WeaponType
from scripts.weapon_url_to_json import weapon_url_to_json, skin_dict_to_json


def main():

    output_dir = Path("/home/eyes/workspace/eyes/skin-scraper/raw_json")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    weapon_url = weapon_type_to_weapon_urls(WeaponType.AK_47)
    
    for name, url in weapon_url.items():
        try:
            skin_dict = weapon_url_to_json(url)

            safe_name = name.replace(" | ", "-").replace("/", "-")
            output_path = output_dir / f"{safe_name}.json"

            with open(output_path, "w") as f:
                json.dump(skin_dict, f, indent=4)

            print(f"Saved JSON for {name} → {output_path}")
            time.sleep(1)  # Be polite and avoid hammering the server

        except Exception as e:
            print(f"Error processing {name}: {e}")
    
    print("All done!")
    
    

    

   

if __name__ == "__main__":
    main()
