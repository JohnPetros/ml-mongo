from commands.command import Command
from commands.products.select_product_command import SelectProductCommand


class DeleteProductCommand(Command):
    def run(self):
        command = SelectProductCommand()
        product = command.run()
        if product is None:
            return

        self.products_repository.remove(product)
        self.output.loading()
        self.output.clear()
        self.output.success("Produto removido com sucesso!")
