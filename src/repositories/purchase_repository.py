from bson import ObjectId

from entities.product import Product
from repositories.mongodb import db


class PurchasesRepository:
    def __init__(self):
        self.collection = db["compra"]

    def add(self, product: Product):
        self.collection.insert_one(
            {
                "name": product.name,
                "totalPrice": product.price,
                "customer": {
                    "id": ObjectId(product.seller_id),
                    "name": product.seller_name,
                },
            }
        )

    def findAll(self):
        documents = self.collection.find()
        if not documents:
            return []

        products = []
        for product in documents:
            products.append(self.__map_product(product))
        return products

    def update(self, product: Product):
        self.collection.update_one(
            {"_id": ObjectId(product.id)},
            {
                "$set": {
                    "name": product.name,
                    "price": product.price,
                    "description": product.description,
                }
            },
        )

    def remove(self, product: Product):
        self.collection.delete_one({"_id": ObjectId(product.id)})

    def __map_product(self, document):
        return Product(
            name=document["name"],
            price=float(document["price"]),
            description=document["description"],
            seller_name=document["seller"]["name"],
            id=str(document["_id"]),
        )
