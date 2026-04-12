#!/usr/bin/env python3
import traceback

from scripts.weapon_url_to_json import extract_skin_data_from_html, weapon_url_to_json
import json

test_urls = [
    "https://csgoskins.gg/items/ak-47-nightwish",
    "https://csgoskins.gg/items/ak-47-crane-flight",
    "https://csgoskins.gg/items/ak-47-inheritance",
]


def test_extraction(test_urls: list[str]):

    for url in test_urls:
    
        try:
            weapon_json = weapon_url_to_json(url)
    
            
        except Exception as e:
            print(f"Error during extraction: {e}")

if __name__ == "__main__":
    test_extraction(test_urls)