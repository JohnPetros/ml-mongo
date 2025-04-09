from commands.command import Command
from repositories.users_repository import UsersRepository
from commands.users.select_user_command import SelectUserCommand


class UpdateUserCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = UsersRepository()

    def run(self):
        command = SelectUserCommand()
        user = command.run()
        if user is None:
            return

        value = self.input.select(
            "Qual valor deseja atualizar?",
            [
                (f"Nome ({user.name})", "name"),
                (f"Email ({user.email})", "email"),
                (f"CPF ({user.cpf})", "cpf"),
                (f"Telefone ({user.phone})", "phone"),
                (f"Rua ({user.address.street})", "street"),
                (f"Bairro ({user.address.neighbourhood})", "neighbourhood"),
                (f"Número ({user.address.number})", "number"),
                (f"Cidade ({user.address.city})", "city"),
                (f"Estado ({user.address.state})", "state"),
                (f"CEP ({user.address.zipcode})", "zipcode"),
                (
                    f"Complemento {'(' + user.address.complement + ')' if user.address.complement else ''}",
                    "complement",
                ),
                ("Voltar", "exit"),
            ],
        )

        match value:
            case "name":
                name = self.input.text("Novo nome:")
                user.name = name
            case "email":
                email = self.input.text("Novo email:")
                user.email = email
            case "cpf":
                cpf = self.input.text("Novo CPF:")
                user.cpf = cpf
            case "phone":
                phone = self.input.text("Novo telefone:")
                user.phone = phone
            case "zipcode":
                zipcode = self.input.text("Novo CEP:")
                user.address.zipcode = zipcode
            case "neighbourhood":
                neighbourhood = self.input.text("Novo bairro:")
                user.address.neighbourhood = neighbourhood
            case "number":
                number = self.input.text("Novo número:")
                user.address.number = number
            case "city":
                city = self.input.text("Novo número:")
                user.address.city = city
            case "street":
                street = self.input.text("Nova rua:")
                user.address.street = street
            case "state":
                state = self.input.text("Novo estado:")
                user.address.state = state
            case "complement":
                complement = self.input.text("Novo complemento:")
                user.address.complement = complement
            case "exit":
                self.exit()
                self.output.clear()
                return

        self.repository.update(user)
        self.output.loading()
        self.output.clear()
        self.output.success("Vendedor atualizado com sucesso!")
