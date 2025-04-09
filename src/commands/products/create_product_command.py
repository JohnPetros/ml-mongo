from commands.command import Command
from commands.sellers.select_seller_command import SelectSellerCommand
from entities.product import Product
from repositories.products_repository import ProductsRepository


class CreateProductCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = ProductsRepository()

    def run(self):
        self.output.title("Cadastrando produto")

        name = self.input.text("Nome:")
        price = self.input.text("Preco: R$")
        description = self.input.text("Descrição:")

        command = SelectSellerCommand()
        seller = command.run()

        product = Product(
            name=name, price=price, description=description, seller_name=seller.name
        )

        self.repository.add(product)
        self.output.loading()
        self.output.clear()
        self.output.success("Produto cadastrado com sucesso!")
