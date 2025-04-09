from commands.command import Command
from entities.purchase import Purchase, PurchaseProduct
from repositories.sellers_repository import SellersRepository
from commands.users.select_user_command import SelectUserCommand
from commands.products.select_product_command import SelectProductCommand


class CreatePurchaseCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = SellersRepository()

    def run(self):
        self.output.title("Fazendo compra")
        user = self.__select_user()
        products = list()

        while True:
            product = self.__select_product()
            product_quantity = int(self.input.text("Quantidade do produto:"))
            products.append(
                PurchaseProduct(
                    id=product.id, name=product.name, quantity=product_quantity
                )
            )
            choice = self.input.select(
                "Deseja adicionar mais produtos?", options=["Sim", "Não"]
            )
            if choice == "Não":
                break

        purchase = Purchase(user=user, products=products)
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
        user = command.run()
        if user is None:
            return

        return user
