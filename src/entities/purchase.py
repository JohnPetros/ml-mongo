from dataclasses import dataclass

from entities.entity import Entity


@dataclass
class PurchaseProduct(Entity):
    name: str = None
    cpf: str = None


@dataclass
class Customer(Entity):
    name: str = None
    price: float = None
    quantity: int = None


@dataclass
class Purchase(Entity):
    products: list[PurchaseProduct] = None
    customer: Customer = None
    status: str = "pendente"
    totalPrice: float = None

    def calculate_total_price(self):
        total = 0.0
        for product in self.products:
            total += product.price * product.quantity
        self.totalPrice = total
