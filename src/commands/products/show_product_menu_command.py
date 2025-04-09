from commands.command import Command
from commands.products.create_product_command import CreateProductCommand
from commands.products.list_products_command import ListProductsCommand
from commands.products.update_product_command import UpdateProductCommand
from commands.products.delete_product_command import DeleteProductCommand


class ShowProductsMenuCommand(Command):

    def run(self):
        self.output.title("Menu de produtos")

        while self.is_running:
            choice = self.input.select(
                "Opções",
                [
                    ("Listar produtos", "list-products"),
                    ("Cadastrar produto", "create-product"),
                    ("Atualizar produto", "update-product"),
                    ("Deletar produto", "delete-product"),
                    ("Voltar", "exit"),
                ],
            )
            command = None

            match choice:
                case "list-products":
                    command = ListProductsCommand()
                case "create-product":
                    command = CreateProductCommand()
                case "update-product":
                    command = UpdateProductCommand()
                case "delete-product":
                    command = DeleteProductCommand()
                case "exit":
                    self.exit()
                case _:
                    self.output.error("Opção inválida")

            if command:
                self.output.clear()
                command.run()
