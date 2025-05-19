from bson import ObjectId

from entities.user import User, Address, Favorite
from repositories.cassandra.cassandra import cassandra


class CassandraUsersRepository:
    def add(self, user: User):
        cassandra.execute(
            "INSERT INTO users (id, name, email, cpf, phone, address, favorites) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                user.id,
                user.name,
                user.email,
                user.cpf,
                user.phone,
                user.address.street,
                user.address.neighbourhood,
                user.address.number,
                user.address.city,
                user.address.state,
                user.address.zipcode,
                user.address.complement,
                [
                    {
                        "_id": ObjectId(favorite.id),
                        "name": favorite.name,
                        "price": favorite.price,
                    }
                    for favorite in user.favorites
                ]
                if user.favorites
                else [],
            ),
        )

    def addMany(self, users: list[User]):
        for user in users:
            self.add(user)

    def findAll(self) -> list[User]:
        documents = cassandra.execute("SELECT * FROM users")
        if not documents:
            return []

        users = []
        for user in documents:
            users.append(self.__map_cassandra_user(user))
        return users

    def findByEmail(self, email: str):
        document = cassandra.execute("SELECT * FROM users WHERE email = %s", (email,))
        return self.__map_cassandra_user(document) if document else None

    def findByCpf(self, cpf: str):
        document = cassandra.execute("SELECT * FROM users WHERE cpf = %s", (cpf,))
        return self.__map_cassandra_user(document) if document else None

    def update(self, user: User):
        cassandra.execute(
            "UPDATE users SET name = %s, email = %s, cpf = %s, phone = %s, address = %s, favorites = %s WHERE id = %s",
            (
                user.name,
                user.email,
                user.cpf,
                user.phone,
                user.address.street,
                user.address.neighbourhood,
                user.address.number,
                user.address.city,
                user.address.state,
                user.address.zipcode,
                user.address.complement,
                [
                    {
                        "_id": ObjectId(favorite.id),
                        "name": favorite.name,
                        "price": favorite.price,
                    }
                    for favorite in user.favorites
                ]
                if user.favorites
                else [],
            ),
        )

    def remove(self, user: User):
        cassandra.execute("DELETE FROM users WHERE id = %s", (user.id,))

    def removeAll(self):
        cassandra.execute("DELETE FROM users")

    def __map_cassandra_user(self, document):
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
