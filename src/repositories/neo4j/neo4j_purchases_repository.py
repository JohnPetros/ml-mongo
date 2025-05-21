from entities.purchase import Purchase, PurchaseProduct
from entities.user import User
from repositories.neo4j.neo4j import neo4j


class Neo4jPurchasesRepository:
    def add(self, purchase: Purchase):
        with neo4j.session() as session:
            session.execute_write(self._create_purchase, purchase)

    def findAll(self):
        with neo4j.session() as session:
            result = session.run("""
                MATCH (u:User)-[:PURCHASES]->(p:Purchase)
                OPTIONAL MATCH (p)-[r:CONTAINS]->(prod:Product)
                RETURN p, u, collect({product: prod, quantity: r.quantity}) AS products
            """)
            purchases = []
            for record in result:
                p_node = record["p"]
                u_node = record["u"]
                products_info = record["products"]
                purchases.append(
                    Purchase(
                        id=p_node["id"],
                        status=p_node["status"],
                        total_price=p_node["total_price"],
                        products=[
                            PurchaseProduct(
                                id=pi["product"]["id"],
                                name=pi["product"]["name"],
                                price=pi["product"]["price"],
                                quantity=pi["quantity"],
                            )
                            for pi in products_info
                        ],
                        customer=User(
                            id=u_node["id"],
                            name=u_node["name"],
                            cpf=u_node["cpf"],
                        ),
                    )
                )
            return purchases

    def update(self, purchase: Purchase):
        with neo4j.session() as session:
            session.run(
                """
                MATCH (p:Purchase {id: $id})
                SET p.status = $status
                """,
                id=purchase.id,
                status=purchase.status,
            )

    def remove(self, purchase: Purchase):
        with neo4j.session() as session:
            session.run("MATCH (p:Purchase {id: $id}) DETACH DELETE p", id=purchase.id)

    @staticmethod
    def _create_purchase(tx, purchase: Purchase):
        customer = purchase.customer

        # Garante que o usuário existe e atualiza seus dados
        tx.run(
            """
            MERGE (u:User {id: $uid})
            SET u.name = $uname, u.cpf = $ucpf
            """,
            uid=customer.id,
            uname=customer.name,
            ucpf=customer.cpf,
        )

        # Cria a Purchase e conecta com o User via PURCHASES
        tx.run(
            """
            CREATE (p:Purchase {
                id: $id,
                status: $status,
                total_price: $total
            })
            WITH p
            MATCH (u:User {id: $uid})
            MERGE (u)-[:PURCHASES]->(p)
            """,
            id=purchase.id,
            status=purchase.status,
            total=purchase.calculate_total_price(),
            uid=customer.id,
        )

        # Cria os produtos e conecta com CONTAINS
        for product in purchase.products:
            tx.run(
                """
                MERGE (prod:Product {id: $pid})
                SET prod.name = $pname, prod.price = $pprice

                WITH prod
                MATCH (p:Purchase {id: $purchase_id})
                MERGE (p)-[r:CONTAINS]->(prod)
                SET r.quantity = $quantity
                """,
                pid=product.id,
                pname=product.name,
                pprice=product.price,
                quantity=product.quantity,
                purchase_id=purchase.id,
            )
