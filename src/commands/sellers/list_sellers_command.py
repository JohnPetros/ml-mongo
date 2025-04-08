from commands.command import Command
from repositories.sellers_repository import SellersRepository


class ListSellersCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = SellersRepository()

    def run(self):
        sellers = self.repository.findAll()

        if not sellers:
            self.output.error("Nenhum vendedor encontrado.")
            return

        self.output.table(
            columns=["ID", "Nome", "Email", "CPF", "Telefone"],
            rows=[
                [
                    seller.get_id(),
                    seller.name,
                    seller.email,
                    seller.cpf,
                    seller.phone,
                ]
                for seller in sellers
            ],
        )
