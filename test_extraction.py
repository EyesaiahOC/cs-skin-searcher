#!/usr/bin/env python3

try:
    from scripts.weapon_url_to_json import extract_skin_data_from_html
    import json
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install required packages: pip install beautifulsoup4")
    exit(1)

def test_extraction(test_page):
    try:
        with open(test_page, 'r', encoding='utf-8') as f:
            html = f.read()
        print("HTML loaded successfully.")
    except FileNotFoundError:
        print("Error: example_weapon_url file not found.")
        return
    except Exception as e:
        print(f"Error loading HTML: {e}")
        return

    try:
        skin_dict = extract_skin_data_from_html(html)
        print("Extracted skin dict:")
        for key, value in skin_dict.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Error during extraction: {e}")

if __name__ == "__main__":
    test_extraction("/home/eyes/workspace/eyes/skin-scraper/example_weapon_url_2.html")