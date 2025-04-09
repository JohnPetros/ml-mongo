from commands.command import Command
from entities.product import Product
from repositories.products_repository import ProductsRepository
from commands.products.list_products_command import ListProductsCommand


class SelectProductCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = ProductsRepository()

    def run(self) -> Product:
        products = self.repository.findAll()
        command = ListProductsCommand()
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
