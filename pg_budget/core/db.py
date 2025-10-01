"""Manage json database file"""

import json
import os
from pathlib import Path
from platformdirs import user_documents_dir

DATABASE_FOLDER = os.path.join(user_documents_dir(), "pg_budget")


class Database:
    """class for manage database"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_file()

    def _ensure_file(self):
        folder = os.path.dirname(self.db_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w", encoding="utf-8") as file:
                json.dump(
                    {"expensesplans": [], "categories": [], "expenses": []},
                    file,
                    indent=4,
                )

    def set_path(self, db_path: str):
        """set new db file path

        Args:
            db_path (str): new file path
        """
        self.db_path = db_path
        self._ensure_file()

    def load_data(self):
        """Load data from db

        Returns:
            dict: all datas from db
        """
        with open(self.db_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def write_data(self, data):
        """Write all data in db

        Args:
            data (dict): all data to save
        """
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def get_username(self):
        """Return current username

        Returns:
            str: username
        """
        return Path(self.db_path).stem


db = Database(os.path.join(DATABASE_FOLDER, "default.json"))
