from entities.product import Product
from entities.seller import Seller
from repositories.neo4j.neo4j import neo4j


class Neo4jProductsRepository:
    def add(self, product: Product):
        with neo4j.session() as session:
            session.execute_write(self._create_product, product)

    def addMany(self, products):
        for product in products:
            self.add(product)

    def findAll(self):
        with neo4j.session() as session:
            result = session.run("MATCH (p:Product) RETURN p")
            return [self.__map_neo4j_product(record["p"]) for record in result]

    def update(self, product: Product):
        with neo4j.session() as session:
            session.run(
                """
                MATCH (p:Product {id: $id})
                SET p.name = $name,
                    p.price = $price,
                    p.description = $description
                """,
                id=product.id,
                name=product.name,
                price=product.price,
                description=product.description,
            )

    def remove(self, product: Product):
        with neo4j.session() as session:
            session.run("MATCH (p:Product {id: $id}) DETACH DELETE p", id=product.id)

    def removeAll(self):
        with neo4j.session() as session:
            session.run("MATCH (p:Product) DETACH DELETE p")

    def removeAllBySeller(self, seller: Seller):
        with neo4j.session() as session:
            session.run(
                """
                MATCH (p:Product)<-[:SELLS]-(s:Seller {id: $seller_id})
                DETACH DELETE p
                """,
                seller_id=seller.id,
            )

    @staticmethod
    def _create_product(tx, product: Product):
        tx.run(
            """
            MATCH (s:Seller {id: $seller_id})
            CREATE (p:Product {
                id: $id,
                name: $name,
                price: $price,
                description: $description,
                seller_name: $seller_name
            })
            CREATE (s)-[:SELLS]->(p)
            """,
            id=product.id,
            name=product.name,
            price=product.price,
            description=product.description,
            seller_id=product.seller_id,
            seller_name=product.seller_name,
        )

    def __map_neo4j_product(self, node) -> Product:
        return Product(
            id=node["id"],
            name=node["name"],
            price=float(node["price"]),
            description=node["description"],
            seller_name=node.get("seller_name"),
        )
