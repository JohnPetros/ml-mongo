from commands.command import Command
from repositories.products_repository import ProductsRepository


class ClearProductsCacheCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = ProductsRepository()

    def run(self):
        self.repository.removeAll(is_cache_enable=True)
        self.output.loading()
        self.output.success("Cache limpado com sucesso!")
