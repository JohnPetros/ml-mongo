from dataclasses import dataclass

from entities.entity import Entity


@dataclass
class Seller(Entity):
    name: str = None
    email: str = None
    cpf: str = None
    phone: str = None
