from entities.purchase import Purchase, Customer, PurchaseProduct
from repositories.cassandra.cassandra import cassandra
from uuid import UUID


class CassandraPurchasesRepository:
    def add(self, purchase: Purchase):
        cassandra.execute(
            "INSERT INTO purchases (id, status, total_price, products, customer) VALUES (%s, %s, %s, %s, %s)",
            (
                UUID(purchase.id),
                purchase.status,
                purchase.calculate_total_price(),
                purchase.products,
                purchase.customer,
            ),
        )

    def findAll(self) -> list[Purchase]:
        rows = cassandra.execute("SELECT * FROM purchases")
        if not rows:
            return []

        purchases = []
        for row in rows:
            purchases.append(self.__map_cassandra_purchase(row))
        return purchases

    def update(self, purchase: Purchase):
        cassandra.execute(
            "UPDATE purchases SET status = %s WHERE id = %s",
            (purchase.status, UUID(purchase.id)),
        )

    def remove(self, purchase: Purchase):
        cassandra.execute("DELETE FROM purchases WHERE id = %s", (UUID(purchase.id),))

    def __map_cassandra_purchase(self, row):
        return Purchase(
            id=str(row.id),
            status=row.status,
            totalPrice=row.customer["totalPrice"],
            products=[
                PurchaseProduct(
                    id=str(product["id"]),
                    name=product["name"],
                    price=product["price"],
                    quantity=product["quantity"],
                )
                for product in row["products"]
            ],
            customer=Customer(
                id=str(row["customer"]["id"]),
                name=row["customer"]["name"],
                cpf=row["customer"]["cpf"],
            ),
        )
