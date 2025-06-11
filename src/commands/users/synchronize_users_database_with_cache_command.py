from commands.command import Command
from commands.users.cache_users_command import CacheUsersCommand


class SynchronizeUsersDatabaseWithCacheCommand(Command):
    def __init__(self):
        super().__init__()
        self.command = CacheUsersCommand()

    def run(self):
        users_cache = self.users_cache_repository.findAll()
        self.users_repository.removeAll()
        self.users_repository.addMany(users_cache)
        self.output.loading()
        self.output.success("Usuários sincronizados com banco de dados!")
