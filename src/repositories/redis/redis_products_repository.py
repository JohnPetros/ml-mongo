from json import dumps, loads

from entities.product import Product

from repositories.redis.redis import redis


class RedisProductsRepository:
    def __init__(self):
        self.redis = redis

    def add(self, product: Product):
        self.redis.set(product.id, product.to_json())

    def addMany(self, products: list[Product]):
        redis.set(self.__CACHE_KEY, dumps([product.__dict__ for product in products]))

        for product in products:
            self.add(product)

    def findAll(self) -> list[Product]:
        products = redis.get(self.__CACHE_KEY)
        if not products:
            return []
        return [self.__map_redis_product(product) for product in loads(products)]

    def update(self, product: Product):
        products_cache = redis.get(self.__CACHE_KEY)
        if products_cache:
            products_cache = loads(products_cache)
            products_cache = [
                (
                    product.__dict__
                    if product_cache["id"] == product.id
                    else product_cache
                )
                for product_cache in products_cache
            ]
            redis.set(self.__CACHE_KEY, dumps(products_cache))

    def removeAll(self):
        redis.delete(self.__CACHE_KEY)

    def __map_redis_product(self, cache):
        return Product(
            name=cache["name"],
            price=cache["price"],
            description=cache["description"],
            seller_id=cache["seller_id"],
            seller_name=cache["seller_name"],
            id=cache["id"],
        )
