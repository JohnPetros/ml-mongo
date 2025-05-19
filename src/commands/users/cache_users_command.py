from commands.command import Command


class SynchronizeUsersDatabaseWithCache(Command):
    def run(self):
        users = self.users_repository.findAll()
        self.users_cache_repository.addMany(users)
        self.output.loading()
        self.output.success("Usuários adicionados em cache com sucesso!")
