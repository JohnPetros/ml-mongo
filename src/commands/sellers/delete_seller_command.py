from commands.command import Command
from repositories.sellers_repository import SellersRepository
from commands.sellers.select_seller_command import SelectSellerCommand


class DeleteSellerCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = SellersRepository()

    def run(self):
        sellers = self.repository.findAll()
        if not sellers:
            self.output.error("Nenhum vendedor encontrado. Cadastre um primeiro")
            return

        command = SelectSellerCommand()
        seller = command.run()

        self.repository.remove(seller)
        self.output.loading()
        self.output.clear()
        self.output.success("Vendedor removido com sucesso!")
