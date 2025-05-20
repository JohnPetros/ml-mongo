from commands.command import Command
from entities.product import Product
from commands.products.list_products_command import ListProductsCommand


class SelectProductCommand(Command):
    def __init__(self, is_cache_enable: bool = False):
        super().__init__()
        self.is_cache_enable = is_cache_enable

    def run(self) -> Product:
        if self.is_cache_enable:
            products = self.products_cache_repository.findAll()
        else:
            products = self.products_repository.findAll()

        if not (len(products)):
            self.output.error("Nenhum produto encontrado. Cadastre um primeiro")
            return

        command = ListProductsCommand(is_cache_enable=self.is_cache_enable)
        command.run()

        while self.is_running:
            product_id = self.input.text("ID do produto:")

            product = list(
                filter(lambda product: product.get_id() == product_id, products)
            )

            if len(product):
                self.exit()
                return product[0]

            self.output.error("Produto não encontrado")
