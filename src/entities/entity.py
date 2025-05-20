from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Entity:
    id: str = None

    def get_id(self):
        return self.id[-4:]

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())
