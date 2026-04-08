import unittest

from scripts.html_to_weapon_urls import (
    file_to_weapon_urls,
    html_to_json_ld_blocks,
    html_to_weapon_urls,
    json_ld_blocks_to_item_list_block,
    json_ld_to_dict,
    load_html_from_file,
    weapon_count_check,
)


AK47_HTML_PATH = "webpages/csgoskins.gg_weapons_ak-47.html"


class TestHtmlToWeaponUrls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ak47_html = load_html_from_file(AK47_HTML_PATH)

    def test_load_html_from_file_returns_html(self):
        self.assertIsInstance(self.ak47_html, str)
        self.assertGreater(len(self.ak47_html), 0)

    def test_html_to_json_ld_blocks_returns_blocks(self):
        blocks = html_to_json_ld_blocks(self.ak47_html)

        self.assertIsInstance(blocks, list)
        self.assertGreater(len(blocks), 0)

    def test_json_ld_blocks_to_item_list_block_finds_item_list(self):
        blocks = html_to_json_ld_blocks(self.ak47_html)
        item_list_block = json_ld_blocks_to_item_list_block(blocks)

        self.assertIsInstance(item_list_block, str)
        self.assertIn('"@type":"ItemList"', item_list_block.replace(" ", ""))

    def test_json_ld_to_dict_returns_item_list_dict(self):
        blocks = html_to_json_ld_blocks(self.ak47_html)
        item_list_block = json_ld_blocks_to_item_list_block(blocks)
        items_dict = json_ld_to_dict(item_list_block)

        self.assertIsInstance(items_dict, dict)
        self.assertEqual(items_dict["@type"], "ItemList")
        self.assertIn("itemListElement", items_dict)

    def test_weapon_count_check_passes_for_matching_counts(self):
        self.assertIsNone(weapon_count_check(48, 48))

    def test_weapon_count_check_raises_for_mismatch(self):
        with self.assertRaises(ValueError):
            weapon_count_check(47, 48)

    def test_html_to_weapon_urls_contains_nightwish(self):
        urls = html_to_weapon_urls(self.ak47_html)

        self.assertIn("AK-47 | Nightwish", urls)
        self.assertEqual(
            urls["AK-47 | Nightwish"],
            "https://csgoskins.gg/items/ak-47-nightwish",
        )

    def test_html_to_weapon_urls_returns_expected_count(self):
        urls = html_to_weapon_urls(self.ak47_html)

        self.assertEqual(len(urls), 48)

    def test_file_to_weapon_urls_returns_expected_count(self):
        urls = file_to_weapon_urls(AK47_HTML_PATH)

        self.assertEqual(len(urls), 48)


if __name__ == "__main__":
    unittest.main()
