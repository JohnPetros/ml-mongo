from bson import ObjectId
from json import dumps, loads

from entities.user import User, Address, Favorite
from repositories.mongodb import mongodb
from repositories.redis import redis


class UsersRepository:
    def __init__(self):
        self.collection = mongodb["usuario"]
        self.__CACHE_KEY = "users"

    def add(self, user: User):
        self.collection.insert_one(
            {
                "_id": user.id if user.id else ObjectId(),
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

    def addMany(self, users: list[User], is_cache_enable: bool = False):
        if is_cache_enable:
            redis.set(
                self.__CACHE_KEY,
                dumps([self.__map_redis_user_reverse(user) for user in users]),
            )
            return

        for user in users:
            self.add(user)

    def findAll(self, is_cache_enable: bool = False) -> list[User]:
        if is_cache_enable:
            users = redis.get(self.__CACHE_KEY)
            if not users:
                return []
            return [self.__map_redis_user(user) for user in loads(users)]

        documents = self.collection.find()
        if not documents:
            return []

        users = []
        for user in documents:
            users.append(self.__map_user(user))
        return users

    def findByEmail(self, email: str, is_cache_enable: bool = False):
        if is_cache_enable:
            users_cache = redis.get(self.__CACHE_KEY)
            if not users_cache:
                return
            users_cache = loads(users_cache)
            for user in users_cache:
                if user["email"] == email:
                    return self.__map_redis_user(user)

        document = self.collection.find_one({"email": email})
        return self.__map_user(document) if document else None

    def findByCpf(self, cpf: str, is_cache_enable: bool = False):
        if is_cache_enable:
            users_cache = redis.get(self.__CACHE_KEY)
            if not users_cache:
                return
            users_cache = loads(users_cache)
            for user in users_cache:
                if user["cpf"] == cpf:
                    return self.__map_redis_user(user)

        document = self.collection.find_one({"cpf": cpf})
        return self.__map_user(document) if document else None

    def update(self, user: User, is_cache_enable: bool = False):
        if is_cache_enable:
            users_cache = redis.get(self.__CACHE_KEY)
            if users_cache:
                users_cache = loads(users_cache)
                users_cache = [
                    (
                        self.__map_redis_user_reverse(user)
                        if user_cache["id"] == user.id
                        else user_cache
                    )
                    for user_cache in users_cache
                ]
                redis.set(self.__CACHE_KEY, dumps(users_cache))
                return

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

    def removeAll(self, is_cache_enable: bool = False):
        if is_cache_enable:
            redis.delete(self.__CACHE_KEY)
            return

        self.collection.delete_many({})

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

    def __map_redis_user(self, cache: dict):
        return User(
            name=cache["name"],
            email=cache["email"],
            cpf=cache["cpf"],
            phone=cache["phone"],
            address=Address(
                street=cache["address"]["street"],
                neighbourhood=cache["address"]["neighbourhood"],
                number=cache["address"]["number"],
                city=cache["address"]["city"],
                state=cache["address"]["state"],
                zipcode=cache["address"]["zipcode"],
                complement=cache["address"]["complement"],
            ),
            favorites=[
                Favorite(
                    id=favorite["id"],
                    name=favorite["name"],
                    price=favorite["price"],
                )
                for favorite in cache.get("favorites", [])
            ],
            id=cache["id"],
        )

    def __map_redis_user_reverse(self, user: User):
        return {
            "id": user.id,
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
            "favorites": [
                {
                    "id": favorite.id,
                    "name": favorite.name,
                    "price": favorite.price,
                }
                for favorite in user.favorites
            ],
        }
