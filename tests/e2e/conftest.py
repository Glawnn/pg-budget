import json
import pytest
from pg_budget.core.db import db


pytestmark = pytest.mark.e2e


@pytest.fixture
def make_db(tmp_path):
    def _make_db(data=None, activate=False):
        db_file = tmp_path / "test_budget_load.json"
        db_file.write_text(json.dumps(data or {"expensesplans": [], "categories": [], "incomes": [], "expenses": []}))
        if activate:
            db.set_path(db_file)
        return db_file

    return _make_db
