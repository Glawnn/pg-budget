"""Base model for models"""

from dataclasses import dataclass


@dataclass
class BaseModel:
    """Base class model for models"""

    def to_dict(self):
        """return model as dict

        Returns:
            dict: dict of model
        """
        return self.__dict__
