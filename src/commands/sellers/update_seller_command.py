from commands.command import Command
from repositories.sellers_repository import SellersRepository
from commands.sellers.select_seller_command import SelectSellerCommand
from validators.phone_validator import PhoneValidator
from validators.cpf_validator import CpfValidator
from validators.email_validator import EmailValidator


class UpdateSellerCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = SellersRepository()

    def run(self):
        command = SelectSellerCommand()
        seller = command.run()
        if seller is None:
            return

        value = self.input.select(
            "Qual valor deseja atualizar?",
            [
                (f"Nome ({seller.name})", "name"),
                (f"Email ({seller.email})", "email"),
                (f"CPF ({seller.cpf})", "cpf"),
                (f"Telefone ({seller.phone})", "phone"),
                ("Voltar", "exit"),
            ],
        )

        match value:
            case "name":
                name = self.input.text("Novo nome:")
                seller.name = name
            case "email":
                email = self.input.text("Novo email:", validator=EmailValidator())
                seller.email = email
            case "cpf":
                cpf = self.input.text("Novo CPF:", validator=CpfValidator())
                seller.cpf = cpf
            case "phone":
                phone = self.input.text("Novo telefone:", validator=PhoneValidator())
                seller.phone = phone
            case "exit":
                self.exit()
                self.output.clear()
                return

        self.repository.update(seller)
        self.output.loading()
        self.output.clear()
        self.output.success("Vendedor atualizado com sucesso!")
        print(seller)
