from bson import ObjectId

from entities.seller import Seller
from repositories.mongodb.mongodb import mongodb


class MongoDbSellersRepository:
    def __init__(self):
        self.collection = mongodb["vendedor"]

    def add(self, seller: Seller):
        self.collection.insert_one(
            {
                "name": seller.name,
                "email": seller.email,
                "cpf": seller.cpf,
                "phone": seller.phone,
            }
        )

    def findAll(self):
        documents = self.collection.find()
        if not documents:
            return []

        sellers = []
        for seller in documents:
            sellers.append(self.__map_seller(seller))
        return sellers

    def findByEmail(self, email: str):
        document = self.collection.find_one({"email": email})
        return self.__map_seller(document[0]) if document else None

    def findByCpf(self, cpf: str):
        document = self.collection.find_one({"cpf": cpf})
        return self.__map_seller(document[0]) if document else None

    def update(self, seller: Seller):
        self.collection.update_one(
            {"_id": ObjectId(seller.id)},
            {
                "$set": {
                    "name": seller.name,
                    "email": seller.email,
                    "cpf": seller.cpf,
                    "phone": seller.phone,
                }
            },
        )

    def remove(self, seller: Seller):
        self.collection.delete_one({"_id": ObjectId(seller.id)})

    def __map_seller(self, document):
        return Seller(
            id=str(document["_id"]),
            name=document["name"],
            email=document["email"],
            cpf=document["cpf"],
            phone=document["phone"],
        )
