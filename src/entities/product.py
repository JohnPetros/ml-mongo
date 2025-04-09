from dataclasses import dataclass

from entities.entity import Entity


@dataclass
class Product(Entity):
    name: str = None
    description: str = None
    price: float = None
    seller_id: str = None
    seller_name: str = None
