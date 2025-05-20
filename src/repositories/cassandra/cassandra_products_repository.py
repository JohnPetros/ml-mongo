from entities.product import Product
from entities.seller import Seller
from uuid import UUID
from repositories.cassandra.cassandra import cassandra


class CassandraProductsRepository:
    def add(self, product: Product):
        cassandra.execute(
            "INSERT INTO products (id, name, price, description, seller_id, seller_name) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                UUID(product.id),
                product.name,
                product.price,
                product.description,
                UUID(product.seller_id),
                product.seller_name,
            ),
        )

    def addMany(self, products: list[Product]):
        for product in products:
            self.add(product)

    def findAll(self) -> list[Product]:
        rows = cassandra.execute("SELECT * FROM products")

        products = []
        for row in rows:
            products.append(self.__map_cassandra_product(row))
        return products

    def update(self, product: Product):
        cassandra.execute(
            "UPDATE products SET name = %s, price = %s, description = %s WHERE id = %s",
            (product.name, product.price, product.description, UUID(product.id)),
        )

    def remove(self, product: Product):
        cassandra.execute(
            "DELETE FROM products WHERE id = %s",
            (UUID(product.id),),
        )

    def removeAll(self):
        cassandra.execute("DELETE FROM products")

    def removeAllBySeller(self, seller: Seller):
        cassandra.execute(
            "DELETE FROM products WHERE seller_id = %s",
            (UUID(seller.id),),
        )

    def __map_cassandra_product(self, row):
        return Product(
            id=str(row.id),
            name=row.name,
            price=float(row.price),
            description=row.description,
            seller_id=str(row.seller_id),
            seller_name=row.seller_name,
        )
