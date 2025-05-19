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


class Command(ABC):
    def __init__(self, subcommand=None):
        self.SESSION_CREDENTIALS = {"email": "admin@gmail.com", "password": "admin123"}
        self.is_running = True
        self.subcommand = subcommand
        self.input = Input()
        self.output = Output()
        self.selected_database = "mongodb"
        self.session_repository = RedisSessionRepository()
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

    def __set_cache_repositories(self):
        self.users_cache_repository = RedisUsersRepository()
        self.products_cache_repository = RedisProductsRepository()
