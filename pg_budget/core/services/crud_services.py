"""Basic crud services for an model"""

from pg_budget.core.db import db


class CRUDService:
    """Basic crud services for an model"""

    def __init__(self, model_class):
        self.model_class = model_class
        self.model_key = model_class.__name__.lower() + "s"
        self.model_key_id = f"{self.model_key[:-1]}_id"

    def create(self, **kwargs):
        """create an object"""
        obj = self.model_class(**kwargs)
        data = db.load_data()
        data[self.model_key].append(obj.to_dict())
        db.write_data(data)
        return obj

    def get_all(self):
        """get all objects"""
        data = db.load_data()
        return data.get(self.model_key, [])

    def get_by_id(self, obj_id):
        """get object by an id"""
        data = db.load_data()
        for item in data.get(self.model_key, []):
            if item[self.model_key_id] == obj_id:
                return self.model_class(**item)
        return None

    def delete(self, obj_id):
        """delete an object by id"""
        data = db.load_data()
        items = data.get(self.model_key, [])
        items = [item for item in items if item[f"{self.model_key[:-1]}_id"] != obj_id]
        data[self.model_key] = items
        db.write_data(data)

    def update(self, obj_id: str, **kwargs):
        """update object with an id and args to update"""
        if f"{self.model_key[:-1]}_id" in kwargs:
            del kwargs[f"{self.model_key[:-1]}_id"]

        data = db.load_data()
        items = data.get(self.model_key, [])
        for index, item in enumerate(items):
            if item[f"{self.model_key[:-1]}_id"] == obj_id:
                for key, value in kwargs.items():
                    if key in item:
                        item[key] = value
                items[index] = item
                data[self.model_key] = items
                db.write_data(data)
                return self.model_class(**item)
        return None
