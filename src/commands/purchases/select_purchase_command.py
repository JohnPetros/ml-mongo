from commands.command import Command
from entities.purchase import Purchase
from repositories.purchases_repository import PurchasesRepository
from commands.purchases.list_purchases_command import ListPurchasesCommand


class SelectPurchaseCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = PurchasesRepository()

    def run(self) -> Purchase:
        purchases = self.repository.findAll()
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

            self.output.error("Compra não encontrada")
