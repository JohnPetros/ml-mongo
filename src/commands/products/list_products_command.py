from commands.command import Command
from repositories.products_repository import ProductsRepository


class ListProductsCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = ProductsRepository()

    def run(self):
        products = self.repository.findAll()

        if not products:
            self.output.error("Nenhum produto encontrado.")
            return

        self.output.table(
            columns=["ID", "Nome", "Preço", "Descrição", "Vendedor"],
            rows=[
                [
                    product.get_id(),
                    product.name,
                    f"R${product.price:.2f}",
                    product.description,
                    product.seller_name,
                ]
                for product in products
            ],
        )
