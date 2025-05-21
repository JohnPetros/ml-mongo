from abc import ABC, abstractmethod

from utils.input import Input
from utils.output import Output
from repositories.mongodb import (
    MongoDbUsersRepository,
    MongoDbProductsRepository,
    MongoDbPurchasesRepository,
    MongoDbSellersRepository,
)
from repositories.cassandra import (
    CassandraUsersRepository,
    CassandraProductsRepository,
    CassandraPurchasesRepository,
    CassandraSellersRepository,
)
from repositories.redis import (
    RedisUsersRepository,
    RedisProductsRepository,
    RedisSessionRepository,
)
from repositories.neo4j import (
    Neo4jUsersRepository,
    Neo4jProductsRepository,
    Neo4jPurchasesRepository,
    Neo4jSellersRepository,
)


class Command(ABC):
    def __init__(self, subcommand=None):
        self.SESSION_CREDENTIALS = {"email": "admin@gmail.com", "password": "admin123"}
        self.is_running = True
        self.subcommand = subcommand
        self.session_repository = RedisSessionRepository()
        selected_database = self.session_repository.get_selected_database()
        if not selected_database:
            self.session_repository.set_selected_database("cassandra")
            selected_database = "cassandra"
        self.selected_database = selected_database
        self.input = Input()
        self.output = Output(selected_database)
        self.__set_repositories()
        self.__set_cache_repositories()

        if not self.session_repository.has_session():
            self.__require_session()

    @abstractmethod
    def run(self): ...

    def exit(self):
        self.is_running = False

    def run_subcommand(self):
        if self.subcommand:
            self.subcommand.run()

    def select_database(self, database: str):
        self.selected_database = database
        self.session_repository.set_selected_database(database)
        self.output = Output(database)

    def __require_session(self):
        self.output.title("Login do usuário admnistrador")

        while True:
            email = self.input.text("Email:")
            password = self.input.password()

            if (
                self.SESSION_CREDENTIALS["email"] == email
                and self.SESSION_CREDENTIALS["password"] == password
            ):
                self.session_repository.add_session()
                self.output.success("Login realizado com sucesso!")
                break
            else:
                self.output.error("Email ou senha inválidos!")

    def __set_repositories(self):
        match self.selected_database:
            case "mongodb":
                self.users_repository = MongoDbUsersRepository()
                self.products_repository = MongoDbProductsRepository()
                self.purchases_repository = MongoDbPurchasesRepository()
                self.sellers_repository = MongoDbSellersRepository()
            case "cassandra":
                self.users_repository = CassandraUsersRepository()
                self.products_repository = CassandraProductsRepository()
                self.purchases_repository = CassandraPurchasesRepository()
                self.sellers_repository = CassandraSellersRepository()
            case "neo4j":
                self.users_repository = Neo4jUsersRepository()
                self.products_repository = Neo4jProductsRepository()
                self.purchases_repository = Neo4jPurchasesRepository()
                self.sellers_repository = Neo4jSellersRepository()

    def __set_cache_repositories(self):
        self.users_cache_repository = RedisUsersRepository()
        self.products_cache_repository = RedisProductsRepository()
