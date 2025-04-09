from commands.command import Command
from entities.user import User, Address
from repositories.users_repository import UsersRepository


class CreateUserCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = UsersRepository()

    def run(self):
        self.output.title("Cadastrando usuário")

        name = self.input.text("Nome:")
        email = self.input.text("Email:")
        cpf = self.input.text("CPF:")
        phone = self.input.text("Telefone:")
        street = self.input.text("Rua:")
        neighbourhood = self.input.text("Bairro:")
        number = self.input.text("Número:")
        city = self.input.text("Cidade:")
        state = self.input.text("Estado:")
        zipcode = self.input.text("CEP:")
        complement = self.input.text("Complemento (opcional):")

        user = User(
            name=name,
            email=email,
            cpf=cpf,
            phone=phone,
            address=Address(
                street=street,
                neighbourhood=neighbourhood,
                city=city,
                number=number,
                state=state,
                zipcode=zipcode,
                complement=complement,
            ),
        )

        self.repository.add(user)
        self.output.loading()
        self.output.clear()
        self.output.success("Produto cadastrado com sucesso!")
