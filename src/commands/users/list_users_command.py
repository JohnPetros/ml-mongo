from commands.command import Command
from repositories.users_repository import UsersRepository
from formatters.cpf_formatter import CpfFormatter
from formatters.phone_formatter import PhoneFormatter


class ListUsersCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = UsersRepository()

    def run(self):
        users = self.repository.findAll()

        if not users:
            self.output.error("Nenhum usuário encontrado.")
            return

        self.output.table(
            columns=[
                "ID",
                "Nome",
                "Email",
                "CPF",
                "Telefone",
                "Rua",
                "Nº",
                "Bairro",
                "Cidade",
                "Estado",
                "CEP",
                "Complemento",
            ],
            rows=[
                [
                    user.get_id(),
                    user.name,
                    user.email,
                    CpfFormatter.format(user.cpf),
                    PhoneFormatter.format(user.phone),
                    user.address.street,
                    user.address.number,
                    user.address.neighbourhood,
                    user.address.city,
                    user.address.state,
                    user.address.zipcode,
                    user.address.complement if user.address.complement else "N/A",
                ]
                for user in users
            ],
        )
        return users
