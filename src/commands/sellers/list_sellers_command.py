from commands.command import Command
from formatters.cpf_formatter import CpfFormatter
from formatters.phone_formatter import PhoneFormatter


class ListSellersCommand(Command):
    def run(self):
        sellers = self.sellers_repository.findAll()

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
                    CpfFormatter.format(seller.cpf),
                    PhoneFormatter.format(seller.phone),
                ]
                for seller in sellers
            ],
        )
