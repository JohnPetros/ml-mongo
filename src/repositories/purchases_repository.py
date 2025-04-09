from bson import ObjectId

from entities.purchase import Purchase, Customer, PurchaseProduct
from repositories.mongodb import db


class PurchasesRepository:
    def __init__(self):
        self.collection = db["compra"]

    def add(self, purchase: Purchase):
        self.collection.insert_one(
            {
                "name": purchase.name,
                "totalPrice": purchase.calculate_total_price(),
                "products": [
                    {
                        "_id": ObjectId(product.id),
                        "name": product.name,
                        "price": product.price,
                        "quantity": product.quantity,
                    }
                    for product in purchase.products
                ],
                "customer": {
                    "_id": ObjectId(purchase.customer.id),
                    "name": purchase.customer.name,
                    "cpf": purchase.customer.name,
                },
            }
        )

    def findAll(self) -> list[Purchase]:
        documents = self.collection.find()
        if not documents:
            return []

        purchases = []
        for purchase in documents:
            purchases.append(self.__map_purchase(purchase))
        return purchases

    def update(self, purchase: Purchase):
        self.collection.update_one(
            {"_id": ObjectId(purchase.id)},
            {
                "$set": {
                    "status": purchase.status,
                }
            },
        )

    def remove(self, purchase: Purchase):
        self.collection.delete_one({"_id": ObjectId(purchase.id)})

    def __map_purchase(self, document):
        return Purchase(
            id=str(document["_id"]),
            status=document["status"],
            totalPrice=document["customer"]["totalPrice"],
            products=[
                PurchaseProduct(
                    id=str(product["_id"]),
                    name=product["name"],
                    price=product["price"],
                    quantity=product["quantity"],
                )
                for product in document["products"]
            ],
            customer=Customer(
            id=str(document["_id"]),
            name=document["customer"]["name"],
            cpf=document["customer"]["cpf"],
        ),
        )
