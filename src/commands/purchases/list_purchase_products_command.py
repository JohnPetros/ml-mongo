from commands.command import Command
from repositories.purchases_repository import PurchasesRepository


class ListPurchaseProductsCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = PurchasesRepository()

    def run(self):
        purchases = self.repository.findAll()

        if not purchases:
            self.output.error("Nenhuma compra encontrado.")
            return

        self.output.table(
            columns=["ID", "Status", "Preço total", "Cliente"],
            rows=[
                [
                    purchase.get_id(),
                    purchase.status,
                    f"{purchase.customer.name} - {purchase.customer.cpf}",
                    f"R${purchase.totalPrice:.2f}",
                ]
                for purchase in purchases
            ],
        )
