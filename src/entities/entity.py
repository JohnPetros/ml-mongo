from dataclasses import dataclass


@dataclass
class Entity:
    id: str = None

    def get_id(self):
        return self.id[-4:]
