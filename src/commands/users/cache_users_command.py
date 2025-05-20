from commands.command import Command


class CacheUsersCommand(Command):
    def run(self):
        users = self.users_repository.findAll()
        self.users_cache_repository.addMany(users)
        # self.repository.removeAll(is_cache_enable=False)
        self.output.loading()
        self.output.clear()
        self.output.success("Usuários adicionados em cache com sucesso!")
