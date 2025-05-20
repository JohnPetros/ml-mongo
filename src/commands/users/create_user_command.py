from commands.command import Command
from entities.user import User, Address
from validators.email_validator import EmailValidator
from validators.cpf_validator import CpfValidator
from validators.phone_validator import PhoneValidator
from validators.int_validator import IntValidator
from validators.zipcode_validator import ZipcodeValidator


class CreateUserCommand(Command):
    def run(self):
        self.output.title("Cadastrando usuário")

        name = self.input.text("Nome:")
        email = self.input.text("Email:", validator=EmailValidator())
        user = self.users_repository.findByEmail(email)
        if user:
            self.output.error("Email já cadastrado")
            return
        cpf = self.input.text("CPF:", validator=CpfValidator())
        user = self.users_repository.findByCpf(cpf)
        if user:
            self.output.error("CPF já cadastrado")
            return
        phone = self.input.text("Telefone:", validator=PhoneValidator())
        street = self.input.text("Rua:")
        neighbourhood = self.input.text("Bairro:")
        number = self.input.text("Número:", validator=IntValidator())
        city = self.input.text("Cidade:")
        state = self.input.text("Estado:")
        zipcode = self.input.text("CEP:", validator=ZipcodeValidator())
        complement = self.input.text("Complemento (opcional):", is_required=False)

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

        self.users_repository.add(user)
        self.output.loading()
        self.output.clear()
        self.output.success("Usuário cadastrado com sucesso!")
