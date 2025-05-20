from entities.seller import Seller
from repositories.cassandra.cassandra import cassandra
from uuid import UUID


class CassandraSellersRepository:
    def add(self, seller: Seller):
        cassandra.execute(
            "INSERT INTO sellers (id, name, email, cpf, phone) VALUES (%s, %s, %s, %s, %s)",
            (UUID(seller.id), seller.name, seller.email, seller.cpf, seller.phone),
        )

    def findAll(self):
        rows = cassandra.execute("SELECT * FROM sellers")
        return [self.__map_cassandra_seller(row) for row in rows]

    def findByEmail(self, email: str):
        row = cassandra.execute(
            "SELECT * FROM sellers WHERE email = %s ALLOW FILTERING", (email,)
        )
        return self.__map_cassandra_seller(row[0]) if row else None

    def findByCpf(self, cpf: str):
        row = cassandra.execute(
            "SELECT * FROM sellers WHERE cpf = %s ALLOW FILTERING", (cpf,)
        )
        return self.__map_cassandra_seller(row[0]) if row else None

    def update(self, seller: Seller):
        cassandra.execute(
            "UPDATE sellers SET name = %s, email = %s, cpf = %s, phone = %s WHERE id = %s",
            (seller.name, seller.email, seller.cpf, seller.phone, UUID(seller.id)),
        )

    def remove(self, seller: Seller):
        cassandra.execute("DELETE FROM sellers WHERE id = %s", (UUID(seller.id),))

    def __map_cassandra_seller(self, row):
        return Seller(
            id=str(row.id),
            name=row.name,
            email=row.email,
            cpf=row.cpf,
            phone=row.phone,
        )
