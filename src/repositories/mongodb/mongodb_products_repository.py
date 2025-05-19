from bson import ObjectId
from json import dumps, loads

from entities.product import Product
from entities.seller import Seller
from repositories.mongodb import mongodb
from repositories.redis.redis import redis


class MongoDbProductsRepository:
    def __init__(self):
        self.collection = mongodb["produto"]
        self.__CACHE_KEY = "products"

    def add(self, product: Product):
        self.collection.insert_one(
            {
                "_id": product.id if product.id else ObjectId(),
                "name": product.name,
                "price": product.price,
                "description": product.description,
                "seller": {
                    "_id": ObjectId(product.seller_id),
                    "name": product.seller_name,
                },
            }
        )

    def addMany(self, products: list[Product], is_cache_enable: bool = False):
        if is_cache_enable:
            redis.set(
                self.__CACHE_KEY, dumps([product.__dict__ for product in products])
            )
            return

        for product in products:
            self.add(product)

    def findAll(self, is_cache_enable: bool = False) -> list[Product]:
        if is_cache_enable:
            products = redis.get(self.__CACHE_KEY)
            if not products:
                return []
            return [self.__map_redis_product(product) for product in loads(products)]

        documents = self.collection.find()
        if not documents:
            return []

        products = []
        for product in documents:
            products.append(self.__map_mongo_product(product))
        return products

    def update(self, product: Product, is_cache_enable: bool = False):
        if is_cache_enable:
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
                return

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

    def removeAll(self, is_cache_enable: bool = False):
        if is_cache_enable:
            redis.delete(self.__CACHE_KEY)
            return

        self.collection.delete_many({})

    def removeAllBySeller(self, seller: Seller):
        self.collection.delete_many({"seller._id": ObjectId(seller.id)})

    def __map_mongo_product(self, document):
        return Product(
            name=document["name"],
            price=float(document["price"]),
            description=document["description"],
            seller_id=str(document["seller"]["_id"]),
            seller_name=document["seller"]["name"],
            id=str(document["_id"]),
        )

    def __map_redis_product(self, cache):
        return Product(
            name=cache["name"],
            price=cache["price"],
            description=cache["description"],
            seller_id=cache["seller_id"],
            seller_name=cache["seller_name"],
            id=cache["id"],
        )
