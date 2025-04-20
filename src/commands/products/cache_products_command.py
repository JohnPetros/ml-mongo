from commands.command import Command
from repositories.products_repository import ProductsRepository


class CacheProductsCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = ProductsRepository()

    def run(self):
        products = self.repository.findAll(is_cache_enable=False)
        self.repository.addMany(products, is_cache_enable=True)
        # self.repository.removeAll(is_cache_enable=False)
        self.output.loading()
        self.output.clear()
        self.output.success("Produtos adicionados em cache com sucesso!")
