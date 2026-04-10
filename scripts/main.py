from scripts.fetch_htmls import fetch_all_weapon_htmls
from scripts.html_to_weapon_urls import weapon_type_to_weapon_urls
from scripts.constants import WeaponType


def main():

    weapon_urls = weapon_type_to_weapon_urls(WeaponType.AK_47)

    for name, url in weapon_urls.items():
        print(f"{name}: {url}")

if __name__ == "__main__":
    main()
