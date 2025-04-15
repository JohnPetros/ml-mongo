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

    def remove_favorite(self, _favorite: Favorite):
        favorites = []
        for favorite in self.favorites:
            if favorite.id != _favorite.id:
                favorites.append(favorite)
                break
        self.favorites = favorites
        
    def has_favorite(self, product: Product):
        if not len(self.favorites) or self.favorites is None:
            return False
        
        ids = [favorite.id for favorite in self.favorites]

        return product.id in ids
