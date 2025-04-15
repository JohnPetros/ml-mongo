from commands.command import Command
from commands.sellers.select_seller_command import SelectSellerCommand
from entities.product import Product
from repositories.products_repository import ProductsRepository
from repositories.sellers_repository import SellersRepository
from validators.float_validator import FloatValidator


class CreateProductCommand(Command):
    def __init__(self):
        super().__init__()
        self.productsRepository = ProductsRepository()
        self.sellersRepository = SellersRepository()

    def run(self):
        sellers = self.sellersRepository.findAll()

        if not len(sellers):
            self.output.error("Nenhum vendedor encontrado. Cadastre um primeiro")
            return

        self.output.title("Cadastrando produto")

        name = self.input.text("Nome:")
        price = self.input.text("Preco: R$", validator=FloatValidator())
        description = self.input.text("Descrição:")

        command = SelectSellerCommand()
        seller = command.run()

        product = Product(
            name=name, price=price, description=description, seller_name=seller.name
        )

        self.productsRepository.add(product)
        self.output.loading()
        self.output.clear()
        self.output.success("Produto cadastrado com sucesso!")
