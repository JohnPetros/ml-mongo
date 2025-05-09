from commands.command import Command
from entities.seller import Seller
from repositories.sellers_repository import SellersRepository
from validators.phone_validator import PhoneValidator
from validators.cpf_validator import CpfValidator
from validators.email_validator import EmailValidator


class CreateSellerCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = SellersRepository()

    def run(self):
        self.output.title("Cadastrando vendedor")
        name = self.input.text("Nome:")
        email = self.input.text("Email:", validator=EmailValidator())
        seller = self.repository.findByEmail(email)
        if seller:
            self.output.error("Email já cadastrado")
            return
        cpf = self.input.text("CPF:", validator=CpfValidator())
        seller = self.repository.findByCpf(cpf)
        if seller:
            self.output.error("CPF já cadastrado")
            return
        phone = self.input.text("Telefone:", validator=PhoneValidator())

        seller = Seller(name=name, email=email, cpf=cpf, phone=phone)

        self.repository.add(seller)
        self.output.loading()
        self.output.clear()
        self.output.success("Vendedor cadastrado com sucesso!")
