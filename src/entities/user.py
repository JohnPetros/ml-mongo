from dataclasses import dataclass

from entities.entity import Entity
from entities.product import Product


@dataclass
class Address:
    zipcode: str = None
    street: str = None
    neighbourhood: str = None
    number: int = None
    city: str = None
    state: str = None
    complement: str = None


@dataclass
class Favorite(Entity):
    id: str = None
    name: str = None
    price: float = None


@dataclass
class User(Entity):
    name: str = None
    cpf: str = None
    email: str = None
    phone: str = None
    address: Address = None
    favorites: list[Favorite] = None

    def add_favorite(self, product: Product):
        if self.favorites is None:
            self.favorites = []

        favorire = Favorite(id=product.id, name=product.name, price=product.price)
        self.favorites.append(favorire)

    def remove_favorite(self, favorite: Favorite):
        self.favorites.remove(favorite)
