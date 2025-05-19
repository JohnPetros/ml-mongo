from commands.command import Command
from formatters.cpf_formatter import CpfFormatter
from formatters.phone_formatter import PhoneFormatter


class ListUsersCommand(Command):
    def __init__(self, subcommand: Command = None, is_cache_enable: bool = False):
        super().__init__(subcommand)
        self.is_cache_enable = is_cache_enable

    def run(self):
        if self.is_cache_enable:
            users = self.users_cache_repository.findAll()
        else:
            users = self.users_repository.findAll()

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

        self.run_subcommand()
        return users
