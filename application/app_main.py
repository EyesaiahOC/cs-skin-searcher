from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import sys
from application.weapon_preview import WeaponPreview
from application.button_holder import ButtonHolder
from application.json_manager import JsonManager



app = QApplication(sys.argv)
json_manager = JsonManager("/home/eyes/workspace/eyes/skin-scraper/raw_json/AK-47-Crane Flight.json")
weapon_data = json_manager.load_json()
window = WeaponPreview(weapon_data)


window.show()
app.exec()