from commands.command import Command
from entities.seller import Seller
from repositories.sellers_repository import SellersRepository
from commands.sellers.list_sellers_command import ListSellersCommand


class SelectSellerCommand(Command):

    def __init__(self):
        super().__init__()
        self.repository = SellersRepository()

    def run(self) -> Seller:
        sellers = self.repository.findAll()
        command = ListSellersCommand()
        command.run()

        while self.is_running:
            seller_id = self.input.text("ID do vendedor:")

            seller = list(filter(lambda seller: seller.get_id() == seller_id, sellers))

            if len(seller):
                self.exit()
                return seller[0]

            self.output.error("Vendedor não encontrado")
