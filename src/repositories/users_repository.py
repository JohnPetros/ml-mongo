from bson import ObjectId

from entities.user import User, Address, Favorite
from repositories.mongodb import mongodb


class UsersRepository:
    def __init__(self):
        self.collection = mongodb["usuario"]

    def add(self, user: User):
        self.collection.insert_one(
            {
                "name": user.name,
                "email": user.email,
                "cpf": user.cpf,
                "phone": user.phone,
                "address": {
                    "street": user.address.street,
                    "neighbourhood": user.address.neighbourhood,
                    "number": user.address.number,
                    "city": user.address.city,
                    "state": user.address.state,
                    "zipcode": user.address.zipcode,
                    "complement": user.address.complement,
                },
                "favorites": (
                    [
                        {
                            "_id": ObjectId(favorite.id),
                            "name": favorite.name,
                            "price": favorite.price,
                        }
                        for favorite in user.favorites
                    ]
                    if user.favorites
                    else []
                ),
            }
        )

    def findAll(self):
        documents = self.collection.find()
        if not documents:
            return []

        users = []
        for user in documents:
            users.append(self.__map_user(user))
        return users

    def findByEmail(self, email: str):
        document = self.collection.find_one({"email": email})
        return self.__map_seller(document[0]) if document else None

    def findByCpf(self, cpf: str):
        document = self.collection.find_one({"cpf": cpf})
        return self.__map_seller(document[0]) if document else None

    def update(self, user: User):
        self.collection.update_one(
            {"_id": ObjectId(user.id)},
            {
                "$set": {
                    "name": user.name,
                    "email": user.email,
                    "cpf": user.cpf,
                    "phone": user.phone,
                    "address": {
                        "street": user.address.street,
                        "neighbourhood": user.address.neighbourhood,
                        "number": user.address.number,
                        "city": user.address.city,
                        "state": user.address.state,
                        "zipcode": user.address.zipcode,
                        "complement": user.address.complement,
                    },
                    "favorites": (
                        [
                            {
                                "_id": ObjectId(favorite.id),
                                "name": favorite.name,
                                "price": favorite.price,
                            }
                            for favorite in user.favorites
                        ]
                        if user.favorites
                        else []
                    ),
                }
            },
        )

    def remove(self, user: User):
        self.collection.delete_one({"_id": ObjectId(user.id)})

    def __map_user(self, document):
        return User(
            name=document["name"],
            email=document["email"],
            cpf=document["cpf"],
            phone=document["phone"],
            address=Address(
                street=document["address"]["street"],
                neighbourhood=document["address"]["neighbourhood"],
                number=document["address"]["number"],
                city=document["address"]["city"],
                state=document["address"]["state"],
                zipcode=document["address"]["zipcode"],
                complement=document["address"]["complement"],
            ),
            favorites=[
                Favorite(
                    id=str(favorite["_id"]),
                    name=favorite["name"],
                    price=favorite["price"],
                )
                for favorite in document.get("favorites", [])
            ],
            id=str(document["_id"]),
        )
