from commands.command import Command
from commands.purchases.select_purchase_command import SelectPurchaseCommand


class UpdatePurchaseStatusCommand(Command):
    def run(self):
        self.output.title("Atualizando o status da compra")
        purchases = self.purchases_repository.findAll()
        if not purchases:
            self.output.error("Nenhuma compra encontrada.")
            return

        command = SelectPurchaseCommand()
        purchase = command.run()

        status = self.input.select(
            "Selecione o novo status:",
            [
                ("pendente", "pending"),
                ("aprovada", "approved"),
                ("cancelada", "canceled"),
            ],
        )

        purchase.status = status
        self.purchases_repository.update(purchase)
        self.output.loading()
        self.output.clear()
        self.output.success("Status da compra atualizado com sucesso!")
