from commands.command import Command
from commands.sellers.create_seller_command import CreateSellerCommand
from commands.sellers.list_sellers_command import ListSellersCommand
from commands.sellers.update_seller_command import UpdateSellerCommand
from commands.sellers.delete_seller_command import DeleteSellerCommand


class ShowSellersMenuCommand(Command):
    def run(self):
        self.output.title("Menu do Vendedor")

        while self.is_running:
            choice = self.input.select(
                "Opções",
                [
                    ("Listar vendedores", "list-sellers"),
                    ("Cadastrar vendedor", "create-seller"),
                    ("Atualizar vendedor", "update-seller"),
                    ("Deletar vendedor", "delete-seller"),
                    ("Voltar", "exit"),
                ],
            )
            command = None

            match choice:
                case "list-sellers":
                    command = ListSellersCommand()
                case "create-seller":
                    command = CreateSellerCommand()
                case "update-seller":
                    command = UpdateSellerCommand()
                case "delete-seller":
                    command = DeleteSellerCommand()
                case "exit":
                    self.exit()
                case _:
                    self.output.error("Opção inválida")

            if command:
                self.output.clear()
                command.run()
