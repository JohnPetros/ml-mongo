from commands.command import Command
from commands.sellers.select_seller_command import SelectSellerCommand


class DeleteSellerCommand(Command):
    def run(self):
        sellers = self.sellers_repository.findAll()
        if not sellers:
            self.output.error("Nenhum vendedor encontrado. Cadastre um primeiro")
            return

        command = SelectSellerCommand()
        seller = command.run()

        self.sellers_repository.remove(seller)
        self.products_repository.removeAllBySeller(seller)
        self.output.loading()
        self.output.clear()
        self.output.success("Vendedor removido com sucesso!")
