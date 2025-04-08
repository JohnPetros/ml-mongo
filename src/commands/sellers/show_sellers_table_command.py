from commands.command import Command
from entities.seller import Seller


class ShowSellersTableCommand(Command):
    def __init__(self, sellers: list[Seller]):
        super().__init__()
        self.sellers = sellers

    def run(self):
        self.output.title("Tabela de Vendedores")
        self.output.table(
            headers=["ID", "Nome", "Email", "CPF", "Telefone"],
            rows=[
                [
                    seller.get_id(),
                    seller.name,
                    seller.email,
                    seller.cpf,
                    seller.telefone,
                ]
                for seller in self.sellers
            ],
        )
