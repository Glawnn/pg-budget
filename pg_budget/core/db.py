


import json
import os


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_file()

        

    def _ensure_file(self):
        folder = os.path.dirname(self.db_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w'):
                json.dump({"expensesplans": [], "categories": [], "expenses": []}, open(self.db_path, 'w'))
    
    def set_path(self, db_path: str):
        self.db_path = db_path
        self._ensure_file()

    def load_data(self):
        with open(self.db_path, 'r') as f:
            return json.load(f)

    def write_data(self, data):
        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=4)


db = Database('budget_db.json')