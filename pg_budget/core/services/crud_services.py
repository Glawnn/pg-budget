"""Basic crud services for an model"""

from pg_budget.core import logger
from pg_budget.core.db import db


class CRUDService:
    """Basic crud services for an model"""

    def __init__(self, model_class, model_key: str = None):
        self.model_class = model_class
        self.model_key = model_class.__name__.lower() + "s" if model_key is None else model_key
        self.model_key_id = f"{self.model_key[:-1]}_id"
        logger.debug("Initialized CRUDService for model '%s'", self.model_class.__name__)

    def create(self, **kwargs):
        """create an object"""
        obj = self.model_class(**kwargs)
        data = db.load_data()
        data[self.model_key].append(obj.to_dict())
        db.write_data(data)
        logger.info("Created new %s: %s", self.model_class.__name__, obj.to_dict())
        return obj

    def get_all(self) -> list[dict]:
        """get all objects"""
        data = db.load_data()
        items = data.get(self.model_key, [])
        logger.debug("Retrieved all %d %s", len(items), self.model_class.__name__)
        return items

    def get_by_id(self, obj_id):
        """get object by an id"""
        data = db.load_data()
        for item in data.get(self.model_key, []):
            if item[self.model_key_id] == obj_id:
                logger.debug("Found %s by id %s", self.model_class.__name__, obj_id)
                return self.model_class(**item)
        logger.warning("%s with id %s not found", self.model_class.__name__, obj_id)
        return None

    def delete(self, obj_id):
        """delete an object by id"""
        data = db.load_data()
        items = data.get(self.model_key, [])
        items = [item for item in items if item[f"{self.model_key[:-1]}_id"] != obj_id]
        data[self.model_key] = items
        db.write_data(data)
        logger.info("Deleted %s with id %s", self.model_class.__name__, obj_id)

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
                logger.info(
                    "Updated %s id %s with %s",
                    self.model_class.__name__,
                    obj_id,
                    kwargs,
                )
                return self.model_class(**item)

        logger.warning("Update failed: %s with id %s not found", self.model_class.__name__, obj_id)
        return None
