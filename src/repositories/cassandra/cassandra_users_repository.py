from bson import ObjectId

from entities.user import User, Address, Favorite
from repositories.cassandra.cassandra import cassandra
from uuid import UUID


class CassandraUsersRepository:
    def add(self, user: User):
        address_map = {
            "street": user.address.street,
            "neighbourhood": user.address.neighbourhood,
            "number": user.address.number,
            "city": user.address.city,
            "state": user.address.state,
            "zipcode": user.address.zipcode,
            "complement": user.address.complement,
        }

        favorites_list = [
            {
                "id": str(favorite.id),
                "name": favorite.name,
                "price": str(favorite.price),
            }
            for favorite in (user.favorites or [])
        ]

        cassandra.execute(
            "INSERT INTO users (id, name, email, cpf, phone, address, favorites) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                UUID(user.id),
                user.name,
                user.email,
                user.cpf,
                user.phone,
                address_map,
                favorites_list,
            ),
        )

    def addMany(self, users: list[User]):
        for user in users:
            self.add(user)

    def findAll(self) -> list[User]:
        rows = cassandra.execute("SELECT * FROM users")
        if not rows:
            return []

        users = []
        for user in rows:
            users.append(self.__map_cassandra_user(user))
        return users

    def findByEmail(self, email: str):
        row = cassandra.execute(
            "SELECT * FROM users WHERE email = %s ALLOW FILTERING", (email,)
        )
        return self.__map_cassandra_user(row[0]) if row else None

    def findByCpf(self, cpf: str):
        row = cassandra.execute(
            "SELECT * FROM users WHERE cpf = %s ALLOW FILTERING", (cpf,)
        )
        return self.__map_cassandra_user(row[0]) if row else None

    def update(self, user: User):
        address_map = {
            "street": user.address.street,
            "neighbourhood": user.address.neighbourhood,
            "number": user.address.number,
            "city": user.address.city,
            "state": user.address.state,
            "zipcode": user.address.zipcode,
            "complement": user.address.complement,
        }

        favorites_list = [
            {
                "id": str(favorite.id),
                "name": favorite.name,
                "price": str(favorite.price),
            }
            for favorite in (user.favorites or [])
        ]

        cassandra.execute(
            "UPDATE users SET name = %s, email = %s, cpf = %s, phone = %s, address = %s, favorites = %s WHERE id = %s",
            (
                user.name,
                user.email,
                user.cpf,
                user.phone,
                address_map,
                favorites_list,
                UUID(user.id),
            ),
        )

    def remove(self, user: User):
        cassandra.execute("DELETE FROM users WHERE id = %s", (UUID(user.id),))

    def removeAll(self):
        cassandra.execute("DELETE FROM users")

    def __map_cassandra_user(self, row):
        return User(
            name=row.name,
            email=row.email,
            cpf=row.cpf,
            phone=row.phone,
            address=Address(
                street=row.address["street"],
                neighbourhood=row.address["neighbourhood"],
                number=row.address["number"],
                city=row.address["city"],
                state=row.address["state"],
                zipcode=row.address["zipcode"],
                complement=row.address["complement"],
            ),
            favorites=[
                Favorite(
                    id=favorite["id"],
                    name=favorite["name"],
                    price=float(favorite["price"]),
                )
                for favorite in (row.favorites or [])
            ],
            id=str(row.id),
        )
