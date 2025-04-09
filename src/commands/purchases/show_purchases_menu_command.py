from commands.command import Command
from commands.purchases.create_purchase_command import CreatePurchaseCommand
from commands.purchases.list_purchases_command import ListPurchasesCommand


class ShowPurchasesMenuCommand(Command):

    def run(self):
        self.output.title("Menu de compras")

        while self.is_running:
            choice = self.input.select(
                "Opções",
                [
                    ("Listar compras", "list-purchases"),
                    ("Fazer compra", "create-purchase"),
                    ("Atualizar status de compra", "update-purchase-status"),
                    ("Voltar", "exit"),
                ],
            )
            command = None

            match choice:
                case "list-purchases":
                    command = ListPurchasesCommand()
                case "create-purchase":
                    command = CreatePurchaseCommand()
                case "exit":
                    self.exit()
                case _:
                    self.output.error("Opção inválida")

            if command:
                self.output.clear()
                command.run()
