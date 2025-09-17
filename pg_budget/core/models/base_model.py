
from dataclasses import dataclass


@dataclass
class BaseModel:
    def to_dict(self):
        return self.__dict__