from commands.command import Command
from repositories.sellers_repository import SellersRepository
from repositories.products_repository import ProductsRepository
from commands.sellers.select_seller_command import SelectSellerCommand


class DeleteSellerCommand(Command):
    def __init__(self):
        super().__init__()
        self.selleers_repository = SellersRepository()
        self.products_repository = ProductsRepository()

    def run(self):
        sellers = self.selleers_repository.findAll()
        if not sellers:
            self.output.error("Nenhum vendedor encontrado. Cadastre um primeiro")
            return

        command = SelectSellerCommand()
        seller = command.run()

        self.selleers_repository.remove(seller)
        self.products_repository.removeAllBySeller(seller)
        self.output.loading()
        self.output.clear()
        self.output.success("Vendedor removido com sucesso!")
