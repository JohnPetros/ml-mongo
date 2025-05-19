from bson import ObjectId
from json import dumps, loads

from entities.user import User, Address, Favorite
from repositories.redis.redis import redis


class RedisUsersRepository:
    def addMany(self, users: list[User]):
        redis.set(
            self.__CACHE_KEY,
            dumps([self.__map_redis_user_reverse(user) for user in users]),
        )

    def findAll(self, is_cache_enable: bool = False) -> list[User]:
        users = redis.get(self.__CACHE_KEY)
        if not users:
            return []
        return [self.__map_redis_user(user) for user in loads(users)]

    def findByEmail(self, email: str):
        users_cache = redis.get(self.__CACHE_KEY)
        if not users_cache:
            return
        users_cache = loads(users_cache)
        for user in users_cache:
            if user["email"] == email:
                return self.__map_redis_user(user)

    def findByCpf(self, cpf: str):
        users_cache = redis.get(self.__CACHE_KEY)
        if not users_cache:
            return
        users_cache = loads(users_cache)
        for user in users_cache:
            if user["cpf"] == cpf:
                return self.__map_redis_user(user)

    def update(self, user: User):
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

    def remove(self, user: User):
        self.collection.delete_one({"_id": ObjectId(user.id)})

    def removeAll(self):
        redis.delete(self.__CACHE_KEY)

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
