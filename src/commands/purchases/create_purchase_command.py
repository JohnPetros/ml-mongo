from commands.command import Command
from entities.purchase import Purchase, PurchaseProduct
from repositories.purchase_repository import PurchasesRepository
from commands.users.select_user_command import SelectUserCommand
from commands.products.select_product_command import SelectProductCommand


class CreatePurchaseCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = PurchasesRepository()

    def run(self):
        self.output.title("Fazendo compra")
        user = self.__select_user()
        products = list()

        if not user:
            return

        while True:
            product = self.__select_product()

            if not product:
                self.output.error("Nenhum produto encontrado")
                return

            is_product_already_included = any(product.id == p.id for p in products)
            if is_product_already_included:
                self.output.error("Produto já adicionado")
                continue

            product_quantity = int(self.input.text("Quantidade do produto:"))
            products.append(
                PurchaseProduct(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    quantity=product_quantity,
                )
            )
            choice = self.input.select(
                "Deseja adicionar mais produtos?",
                [("Sim", "yes"), ("Não", "no")],
            )
            if choice == "no":
                break

        purchase = Purchase(customer=user, products=products, status="Pendente")
        purchase.calculate_total_price()
        self.repository.add(purchase)
        self.output.loading()
        self.output.clear()
        self.output.success("Vendedor cadastrado com sucesso!")

    def __select_user(self):
        command = SelectUserCommand()
        user = command.run()
        if user is None:
            return

        return user

    def __select_product(self):
        command = SelectProductCommand()
        product = command.run()
        return product
