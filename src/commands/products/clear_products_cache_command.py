from commands.command import Command


class ClearProductsCacheCommand(Command):
    def run(self):
        self.products_repository.removeAll(is_cache_enable=True)
        self.output.loading()
        self.output.success("Cache limpado com sucesso!")
