from commands.command import Command


class ClearUsersCacheCommand(Command):
    def run(self):
        self.users_cache_repository.removeAll()
        self.output.loading()
        self.output.success("Cache limpado com sucesso!")
