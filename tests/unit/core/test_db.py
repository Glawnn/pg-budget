import json

from pg_budget.core.db import Database


class TestDatabase:
    def test_ensure_file_creates_file(self, tmp_path):
        db_path = tmp_path / "db.json"
        Database(str(db_path))

        assert db_path.exists()
        data = json.loads(db_path.read_text(encoding="utf-8"))
        assert "expensesplans" in data
        assert "categories" in data
        assert "expenses" in data
        assert len(data["categories"]) > 0  # Ensure categories are initialized

    def test_set_path_creates_new_file(self, tmp_path):
        db_path1 = tmp_path / "db1.json"
        db_path2 = tmp_path / "sub/db2.json"
        db = Database(str(db_path1))

        db.set_path(str(db_path2))
        assert db_path2.exists()
        data = json.loads(db_path2.read_text(encoding="utf-8"))
        assert "expensesplans" in data

    def test_write_and_load_data(self, tmp_path):
        db_path = tmp_path / "db.json"
        db = Database(str(db_path))

        sample_data = {
            "expensesplans": [{"name": "Plan1"}],
            "categories": [{"name": "Cat1"}],
            "expenses": [{"name": "Expense1"}],
        }
        db.write_data(sample_data)
        loaded = db.load_data()
        assert loaded == sample_data
