from repositories.neo4j.neo4j import neo4j
from entities.seller import Seller
from typing import Optional, List


class Neo4jSellersRepository:
    def add(self, seller: Seller):
        with neo4j.session() as session:
            session.run(
                """
                CREATE (s:Seller {
                    id: $id,
                    name: $name,
                    email: $email,
                    cpf: $cpf,
                    phone: $phone
                })
            """,
                id=seller.id,
                name=seller.name,
                email=seller.email,
                cpf=seller.cpf,
                phone=seller.phone,
            )

    def findAll(self) -> List[Seller]:
        with neo4j.session() as session:
            result = session.run("MATCH (s:Seller) RETURN s")
            return [self.__map_neo4j_seller(record["s"]) for record in result]

    def findByEmail(self, email: str) -> Optional[Seller]:
        with neo4j.session() as session:
            result = session.run(
                "MATCH (s:Seller {email: $email}) RETURN s", email=email
            )
            record = result.single()
            return self.__map_neo4j_seller(record["s"]) if record else None

    def findByCpf(self, cpf: str) -> Optional[Seller]:
        with neo4j.session() as session:
            result = session.run("MATCH (s:Seller {cpf: $cpf}) RETURN s", cpf=cpf)
            record = result.single()
            return self.__map_neo4j_seller(record["s"]) if record else None

    def update(self, seller: Seller):
        with neo4j.session() as session:
            session.run(
                """
                MATCH (s:Seller {id: $id})
                SET s.name = $name,
                    s.email = $email,
                    s.cpf = $cpf,
                    s.phone = $phone
            """,
                id=seller.id,
                name=seller.name,
                email=seller.email,
                cpf=seller.cpf,
                phone=seller.phone,
            )

    def remove(self, seller: Seller):
        with neo4j.session() as session:
            session.run("MATCH (s:Seller {id: $id}) DETACH DELETE s", id=seller.id)

    def __map_neo4j_seller(self, node) -> Seller:
        return Seller(
            id=node["id"],
            name=node["name"],
            email=node["email"],
            cpf=node["cpf"],
            phone=node["phone"],
        )
