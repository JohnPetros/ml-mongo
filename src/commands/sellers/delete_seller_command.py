from commands.command import Command
from repositories.sellers_repository import SellersRepository
from commands.sellers.select_seller_command import SelectSellerCommand


class DeleteSellerCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = SellersRepository()

    def run(self):
        command = SelectSellerCommand()
        seller = command.run()

        self.repository.remove(seller)
        self.output.loading()
        self.output.success("Vendedor removido com sucesso!")
