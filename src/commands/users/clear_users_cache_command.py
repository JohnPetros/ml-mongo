from commands.command import Command
from repositories.users_repository import UsersRepository


class ClearUsersCacheCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = UsersRepository()

    def run(self):
        self.repository.removeAll(is_cache_enable=True)
        self.output.loading()
        self.output.success("Cache limpado com sucesso!")
