from commands.command import Command
from repositories.products_repository import ProductsRepository
from commands.products.select_product_command import SelectProductCommand


class DeleteProductCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = ProductsRepository()

    def run(self):
        command = SelectProductCommand()
        product = command.run()

        self.repository.remove(product)
        self.output.loading()
        self.output.clear()
        self.output.success("Produto removido com sucesso!")
