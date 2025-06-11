from commands.command import Command
from repositories.users_repository import UsersRepository


class CacheUsersCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = UsersRepository()

    def run(self):
        users = self.repository.findAll(is_cache_enable=False)
        self.repository.addMany(users, is_cache_enable=True)
        self.output.loading()
        self.output.success("Usuários adicionados em cache com sucesso!")
