from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from scripts.constants import WeaponType
from scripts.fetch_htmls import (
    fetch_and_save_weapon_html,
    fetch_html_from_url,
    save_html_to_file,
    weapon_type_to_file_path,
    weapon_type_to_page_url,
    weapon_type_to_slug,
)


class TestFetchHtmls(unittest.TestCase):
    def test_weapon_type_to_slug(self):
        self.assertEqual(weapon_type_to_slug(WeaponType.AK_47), "ak-47")
        self.assertEqual(weapon_type_to_slug(WeaponType.SG_553), "sg-553")
        self.assertEqual(weapon_type_to_slug(WeaponType.GALIL_AR), "galil-ar")

    def test_weapon_type_to_page_url(self):
        self.assertEqual(
            weapon_type_to_page_url(WeaponType.AK_47),
            "https://csgoskins.gg/weapons/ak-47",
        )

    def test_weapon_type_to_file_path(self):
        self.assertEqual(
            weapon_type_to_file_path(WeaponType.AK_47),
            Path("/home/eyes/workspace/eyes/skin-scraper/webpages/csgoskins.gg_weapons_ak-47.html"),
        )

    def test_save_html_to_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.html"
            saved_path = save_html_to_file("<html>test</html>", file_path)

            self.assertEqual(saved_path, file_path)
            self.assertTrue(file_path.exists())
            self.assertEqual(file_path.read_text(encoding="utf-8"), "<html>test</html>")

    @patch("scripts.fetch_htmls.urlopen")
    def test_fetch_html_from_url(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b"<html>test</html>"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        html = fetch_html_from_url("https://example.com")

        self.assertEqual(html, "<html>test</html>")
        request_arg = mock_urlopen.call_args[0][0]
        self.assertEqual(request_arg.full_url, "https://example.com")
        self.assertIn("Mozilla/5.0", request_arg.headers["User-agent"])

    @patch("scripts.fetch_htmls.save_html_to_file")
    @patch("scripts.fetch_htmls.fetch_html_from_url")
    def test_fetch_and_save_weapon_html(self, mock_fetch_html, mock_save_html):
        mock_fetch_html.return_value = "<html>weapon page</html>"
        mock_save_html.return_value = weapon_type_to_file_path(WeaponType.AK_47)

        file_path = fetch_and_save_weapon_html(WeaponType.AK_47)

        self.assertEqual(file_path, weapon_type_to_file_path(WeaponType.AK_47))
        mock_fetch_html.assert_called_once_with("https://csgoskins.gg/weapons/ak-47")
        mock_save_html.assert_called_once_with(
            "<html>weapon page</html>",
            weapon_type_to_file_path(WeaponType.AK_47),
        )


if __name__ == "__main__":
    unittest.main()
