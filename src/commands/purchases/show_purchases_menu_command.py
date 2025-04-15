from commands.command import Command
from commands.purchases.create_purchase_command import CreatePurchaseCommand
from commands.purchases.list_purchases_command import ListPurchasesCommand
from commands.purchases.update_purchase_status_command import (
    UpdatePurchaseStatusCommand,
)


class ShowPurchasesMenuCommand(Command):

    def run(self):
        self.output.title("Menu de compras")

        while self.is_running:
            choice = self.input.select(
                "Opções",
                [
                    ("Listar compras", "list-purchases"),
                    ("Fazer uma compra", "create-purchase"),
                    ("Atualizar o status de uma compra", "update-purchase-status"),
                    ("Voltar", "exit"),
                ],
            )
            command = None

            match choice:
                case "list-purchases":
                    command = ListPurchasesCommand()
                case "create-purchase":
                    command = CreatePurchaseCommand()
                case "update-purchase-status":
                    command = UpdatePurchaseStatusCommand()
                case "exit":
                    self.exit()
                case _:
                    self.output.error("Opção inválida")

            if command:
                self.output.clear()
                command.run()
