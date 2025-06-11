from commands.command import Command
from commands.users.cache_users_command import CacheUsersCommand
from repositories.users_repository import UsersRepository


class SynchronizeUsersDatabaseWithCacheCommand(Command):
    def __init__(self):
        super().__init__()
        self.command = CacheUsersCommand()
        self.repository = UsersRepository()

    def run(self):
        users_cache = self.repository.findAll(is_cache_enable=True)
        self.repository.removeAll(is_cache_enable=False)
        self.repository.addMany(users_cache, is_cache_enable=False)
        self.output.loading()
        self.output.success("Usuários sincronizados com banco de dados!")
