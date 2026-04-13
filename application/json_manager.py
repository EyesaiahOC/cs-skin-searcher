import json
from pathlib import Path

class JsonManager:
    def __init__ (self, file_path):
        self.file_path = Path(file_path)


    def load_json(self):
        if self.file_path.exists():
            with open(self.file_path, 'r') as file:
                return json.load(file)
        else:
            return None