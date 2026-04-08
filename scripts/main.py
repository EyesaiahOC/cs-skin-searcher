from html_to_weapon_urls import html_to_weapon_urls, file_to_weapon_urls
from constants import WeaponType

def main():
    ak_urls = file_to_weapon_urls("/home/eyes/workspace/eyes/skin-scraper/webpages/csgoskins.gg_weapons_ak-47.html")
    for name, url in ak_urls.items():
        print(f"{name}: {url}")






if __name__ == "__main__":
    main()