from commands.command import Command
from entities.seller import Seller
from repositories.sellers_repository import SellersRepository


class CreateSellerCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = SellersRepository()

    def run(self):
        self.output.title("Cadastrando vendedor")

        name = self.input.text("Nome:")
        email = self.input.text("Email:")
        cpf = self.input.text("CPF:")
        phone = self.input.text("Telefone:")

        seller = Seller(name=name, email=email, cpf=cpf, phone=phone)

        self.repository.add(seller)
        self.output.loading()
        self.output.clear()
        self.output.success("Vendedor cadastrado com sucesso!")
