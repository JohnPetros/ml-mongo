from commands.command import Command
from entities.purchase import Purchase
from commands.purchases.list_purchases_command import ListPurchasesCommand


class SelectPurchaseCommand(Command):
    def run(self) -> Purchase:
        purchases = self.purchases_repository.findAll()
        if not (len(purchases)):
            self.output.error("Nenhuma compra encontrada. Cadastre uma primeiro")
            return

        sellers = self.sellers_repository.findAll()
        if not (len(sellers)):
            self.output.error("Nenhum vendedor encontrado. Cadastre um primeiro")
            return

        command = ListPurchasesCommand()
        command.run()

        while self.is_running:
            purchase_id = self.input.text("ID da compra:")

            purchase = list(
                filter(lambda purchase: purchase.get_id() == purchase_id, purchases)
            )

            if len(purchase):
                self.exit()
                return purchase[0]

            self.output.error("Compra não encontrado")
