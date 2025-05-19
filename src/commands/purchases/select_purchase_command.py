from commands.command import Command
from entities.product import Product
from commands.purchases.list_purchases_command import ListPurchasesCommand


class SelectPurchaseCommand(Command):
    def run(self) -> Product:
        products = self.products_repository.findAll()
        if not (len(products)):
            self.output.error("Nenhum produto encontrado. Cadastre um primeiro")
            return

        sellers = self.sellers_repository.findAll()
        if not (len(sellers)):
            self.output.error("Nenhum vendedor encontrado. Cadastre um primeiro")
            return

        command = ListPurchasesCommand()
        command.run()

        while self.is_running:
            product_id = self.input.text("ID do compra:")

            product = list(
                filter(lambda product: product.get_id() == product_id, products)
            )

            if len(product):
                self.exit()
                return product[0]

            self.output.error("Compra não encontrado")
