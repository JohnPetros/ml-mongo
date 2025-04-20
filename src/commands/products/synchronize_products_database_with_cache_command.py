from commands.command import Command
from commands.products.cache_products_command import CacheProductsCommand
from repositories.products_repository import ProductsRepository


class SynchronizeProductsDatabaseWithCache(Command):
    def __init__(self):
        super().__init__()
        self.command = CacheProductsCommand()
        self.repository = ProductsRepository()

    def run(self):
        products_cache = self.repository.findAll(is_cache_enable=True)
        self.repository.removeAll(is_cache_enable=False)
        self.repository.addMany(products_cache, is_cache_enable=False)
        self.output.loading()
        self.output.success("Produtos sincronizados com banco de dados!")
