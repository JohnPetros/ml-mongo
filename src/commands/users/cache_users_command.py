from commands.command import Command


class CacheUsersCommand(Command):
    def run(self):
        users = self.repository.findAll(is_cache_enable=False)
        self.repository.addMany(users, is_cache_enable=True)
        self.output.loading()
        self.output.success("Usuários adicionados em cache com sucesso!")
