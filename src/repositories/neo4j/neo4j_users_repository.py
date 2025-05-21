from entities.user import User, Address, Favorite
from repositories.neo4j.neo4j import neo4j


class Neo4jUsersRepository:
    def add(self, user: User):
        with neo4j.session() as session:
            session.execute_write(self._create_user, user)

    def addMany(self, users):
        for user in users:
            self.add(user)

    def findAll(self):
        with neo4j.session() as session:
            result = session.execute_read(self._find_all_users)
            return [self.__map_neo4j_user(record) for record in result]

    def findByEmail(self, email: str):
        with neo4j.session() as session:
            result = session.run(
                """
                MATCH (u:User {email: $email})-[:LIVES_AT]->(a:Address)
                OPTIONAL MATCH (u)-[:FAVORITES]->(p:Product)
                RETURN u, a, collect(p) as favorites
                """,
                email=email,
            )
            record = result.single()
            return self.__map_neo4j_user_with_details(record) if record else None

    def findByCpf(self, cpf: str):
        with neo4j.session() as session:
            result = session.run(
                """
                MATCH (u:User {cpf: $cpf})-[:LIVES_AT]->(a:Address)
                OPTIONAL MATCH (u)-[:FAVORITES]->(p:Product)
                RETURN u, a, collect(p) as favorites
                """,
                cpf=cpf,
            )
            record = result.single()
            return self.__map_neo4j_user_with_details(record) if record else None

    def update(self, user: User):
        with neo4j.session() as session:
            session.execute_write(self._update_user, user)

    def remove(self, user: User):
        with neo4j.session() as session:
            session.run("MATCH (u:User {id: $id}) DETACH DELETE u", id=user.id)
            session.run(
                "MATCH (a:Address {zipcode: $zipcode}) DETACH DELETE a",
                zipcode=user.address.zipcode,
            )

    def removeAll(self):
        with neo4j.session() as session:
            session.execute_write("MATCH (u:User) DETACH DELETE u")

    @staticmethod
    def _create_user(tx, user: User):
        tx.run(
            """
            MERGE (u:User {id: $id})
            SET u.name = $name, u.email = $email, u.cpf = $cpf, u.phone = $phone

            MERGE (a:Address {
                zipcode: $zipcode,
                street: $street,
                neighbourhood: $neighbourhood,
                number: $number,
                city: $city,
                state: $state,
                complement: $complement
            })

            MERGE (u)-[:LIVES_AT]->(a)
            """,
            id=user.id,
            name=user.name,
            email=user.email,
            cpf=user.cpf,
            phone=user.phone,
            zipcode=user.address.zipcode if user.address else None,
            street=user.address.street if user.address else None,
            neighbourhood=user.address.neighbourhood if user.address else None,
            number=user.address.number if user.address else None,
            city=user.address.city if user.address else None,
            state=user.address.state if user.address else None,
            complement=user.address.complement if user.address else None,
        )

        if user.favorites:
            for fav in user.favorites:
                tx.run(
                    """
                    MERGE (p:Product {id: $pid})
                    SET p.name = $pname, p.price = $pprice
                    WITH p
                    MATCH (u:User {id: $uid})
                    MERGE (u)-[:FAVORITES]->(p)
                    """,
                    pid=fav.id,
                    pname=fav.name,
                    pprice=fav.price,
                    uid=user.id,
                )

    @staticmethod
    def _find_all_users(tx):
        result = tx.run(
            """
            MATCH (u:User)-[:LIVES_AT]->(a:Address)
            OPTIONAL MATCH (u)-[:FAVORITES]->(p:Product)
            RETURN u, a, collect(p) AS favorites
            """
        )
        return result.data()

    @staticmethod
    def _find_user_by_property(tx, prop_name, prop_value):
        result = tx.run(
            f"""
            MATCH (u:User)-[:LIVES_AT]->(a:Address)
            OPTIONAL MATCH (u)-[:FAVORITES]->(p:Product)
            WHERE u.{prop_name} = $prop_value
            RETURN u, a, collect(p) AS favorites
            LIMIT 1
            """,
            prop_value=prop_value,
        )
        return result.single()

    @staticmethod
    def _update_user(tx, user: User):
        tx.run(
            """
            MATCH (u:User {id: $id})-[:LIVES_AT]->(a:Address)
            SET u.name = $name,
                u.email = $email,
                u.cpf = $cpf,
                u.phone = $phone
            SET a.street = $street,
                a.zipcode = $zipcode,
                a.neighbourhood = $neighbourhood,
                a.number = $number,
                a.city = $city,
                a.state = $state,
                a.complement = $complement
            """,
            id=user.id,
            name=user.name,
            email=user.email,
            cpf=user.cpf,
            phone=user.phone,
            zipcode=user.address.zipcode if user.address else None,
            street=user.address.street if user.address else None,
            neighbourhood=user.address.neighbourhood if user.address else None,
            number=user.address.number if user.address else None,
            city=user.address.city if user.address else None,
            state=user.address.state if user.address else None,
            complement=user.address.complement if user.address else None,
        )

        # Remove relações antigas
        tx.run(
            """
            MATCH (u:User {id: $id})-[r:FAVORITES]->(:Product)
            DELETE r
            """,
            id=user.id,
        )

        # Cria novas relações de favoritos
        if user.favorites:
            for fav in user.favorites:
                tx.run(
                    """
                    MERGE (p:Product {id: $pid})
                    SET p.name = $pname, p.price = $pprice
                    WITH p
                    MATCH (u:User {id: $uid})
                    MERGE (u)-[:FAVORITES]->(p)
                    """,
                    pid=fav.id,
                    pname=fav.name,
                    pprice=fav.price,
                    uid=user.id,
                )

    def __map_neo4j_user(self, record) -> User:
        return self.__map_neo4j_user_with_details(record)

    def __map_neo4j_user_with_details(self, record) -> User:
        u = record["u"]
        a = record["a"]
        favorites = record["favorites"]

        return User(
            id=u["id"],
            name=u.get("name"),
            email=u.get("email"),
            cpf=u.get("cpf"),
            phone=u.get("phone"),
            address=Address(
                street=a.get("street"),
                neighbourhood=a.get("neighbourhood"),
                number=a.get("number"),
                city=a.get("city"),
                state=a.get("state"),
                zipcode=a.get("zipcode"),
                complement=a.get("complement"),
            ),
            favorites=[
                Favorite(
                    id=favorite["id"],
                    name=favorite["name"],
                    price=float(favorite["price"]),
                )
                for favorite in favorites
                if favorite is not None
            ],
        )
