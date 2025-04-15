from bson import ObjectId

from entities.purchase import Purchase, PurchaseProduct, Customer
from repositories.mongodb import db


class PurchasesRepository:
    def __init__(self):
        self.collection = db["compra"]

    def add(self, purchase: Purchase):
        print(purchase)
        self.collection.insert_one(
            {
                "totalPrice": purchase.total_price,
                "status": purchase.status,
                "customer": {
                    "_id": ObjectId(purchase.customer.id),
                    "name": purchase.customer.name,
                    "cpf": purchase.customer.cpf,
                },
                "products": [
                    {
                        "_id": ObjectId(product.id),
                        "name": product.name,
                        "price": product.price,
                        "quantity": product.quantity,
                    }
                    for product in purchase.products
                ],
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
        print(purchase.status)
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
            products=[
                PurchaseProduct(
                    id=str(product["_id"]),
                    name=product["name"],
                    price=float(product["price"]),
                    quantity=product["quantity"],
                )
                for product in document["products"]
            ],
            customer=Customer(
                id=str(document["customer"]["_id"]),
                name=document["customer"]["name"],
                cpf=document["customer"]["cpf"],
            ),
        )
