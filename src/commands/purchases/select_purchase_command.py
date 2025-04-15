from repositories.purchase_repository import PurchasesRepository
from entities.purchase import Purchase
from commands.command import Command
from commands.purchases.list_purchases_command import ListPurchasesCommand


class SelectPurchaseCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = PurchasesRepository()

    def run(self) -> Purchase:
        products = self.repository.findAll()
        command = ListPurchasesCommand()
        command.run()

        while self.is_running:
            product_id = self.input.text("ID da compra:")

            product = list(
                filter(lambda product: product.get_id() == product_id, products)
            )

            if len(product):
                self.exit()
                return product[0]

            self.output.error("Compra não encontrada")
