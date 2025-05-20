from commands.command import Command
from commands.products.cache_products_command import CacheProductsCommand


class SynchronizeProductsDatabaseWithCache(Command):
    def __init__(self):
        super().__init__()
        self.command = CacheProductsCommand()

    def run(self):
        products_cache = self.products_cache_repository.findAll()
        self.products_repository.removeAll()
        self.products_repository.addMany(products_cache)
        self.output.loading()
        self.output.success("Produtos sincronizados com banco de dados!")
