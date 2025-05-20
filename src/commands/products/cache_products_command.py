from commands.command import Command


class CacheProductsCommand(Command):
    def run(self):
        products = self.products_repository.findAll()
        self.products_cache_repository.addMany(products)
        # self.repository.removeAll(is_cache_enable=False)
        self.output.loading()
        self.output.clear()
        self.output.success("Produtos adicionados em cache com sucesso!")
