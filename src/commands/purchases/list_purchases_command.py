from commands.command import Command
from repositories.purchases_repository import PurchasesRepository


class ListPurchasesCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = PurchasesRepository()

    def run(self):
        purchases = self.repository.findAll()

        if not purchases:
            self.output.error("Nenhuma compra encontrada.")
            return

        self.output.title("Compras")

        for purchase in purchases:
            self.output.table(
                columns=["ID", "Cliente", "Preço total", "Status"],
                rows=[
                    [
                        purchase.get_id(),
                        f"{purchase.customer.name} | {purchase.customer.cpf}",
                        f"R${purchase.calculate_total_price():.2f}",
                        purchase.status.upper(),
                    ]
                    for purchase in purchases
                ],
            )

            self.output.table(
                columns=["Produto", "Preço unit.", "Qtd."],
                rows=[
                    [
                        product.name,
                        f"R${product.price:.2f}",
                        str(product.quantity),
                    ]
                    for product in purchase.products
                ],
            )
