import pytest

from pg_budget.core.services.crud_services import CRUDService


class FakeModel:
    def __init__(self, fake_id=None, name=None):
        self.fake_id = fake_id
        self.name = name

    def to_dict(self):
        return {"fake_id": self.fake_id, "name": self.name}


class TestCRUDService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.service = CRUDService(FakeModel)
        self.service.model_key = "fakes"
        self.service.model_key_id = "fake_id"

    def test_create(self, mocker):
        mocker.patch("pg_budget.core.db.db.load_data", return_value={"fakes": []})
        mock_write = mocker.patch("pg_budget.core.db.db.write_data")

        obj = self.service.create(fake_id=1, name="Test")
        assert obj.fake_id == 1
        assert obj.name == "Test"
        mock_write.assert_called_once()

    def test_get_all(self, mocker):
        mocker.patch(
            "pg_budget.core.db.db.load_data",
            return_value={"fakes": [{"fake_id": 1, "name": "Alpha"}]},
        )
        items = self.service.get_all()
        assert len(items) == 1
        assert items[0]["name"] == "Alpha"

    def test_get_by_id_found(self, mocker):
        mocker.patch(
            "pg_budget.core.db.db.load_data",
            return_value={"fakes": [{"fake_id": 1, "name": "Alpha"}]},
        )
        obj = self.service.get_by_id(1)
        assert isinstance(obj, FakeModel)
        assert obj.name == "Alpha"

    def test_get_by_id_not_found(self, mocker):
        mocker.patch("pg_budget.core.db.db.load_data", return_value={"fakes": []})
        obj = self.service.get_by_id(99)
        assert obj is None

    def test_delete(self, mocker):
        mocker.patch(
            "pg_budget.core.db.db.load_data",
            return_value={"fakes": [{"fake_id": 1, "name": "Alpha"}]},
        )
        mock_write = mocker.patch("pg_budget.core.db.db.write_data")

        self.service.delete(1)
        mock_write.assert_called_once()

    def test_update_success(self, mocker):
        mocker.patch(
            "pg_budget.core.db.db.load_data",
            return_value={"fakes": [{"fake_id": 1, "name": "Alpha"}]},
        )
        mock_write = mocker.patch("pg_budget.core.db.db.write_data")

        obj = self.service.update(1, name="Beta")
        assert obj.name == "Beta"
        mock_write.assert_called_once()

    def test_update_not_found(self, mocker):
        mocker.patch("pg_budget.core.db.db.load_data", return_value={"fakes": []})
        obj = self.service.update(42, name="Beta")
        assert obj is None
