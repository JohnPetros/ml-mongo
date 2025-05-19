from commands.command import Command
from commands.users.select_user_command import SelectUserCommand
from validators.email_validator import EmailValidator
from validators.cpf_validator import CpfValidator
from validators.phone_validator import PhoneValidator
from validators.int_validator import IntValidator
from validators.zipcode_validator import ZipcodeValidator


class UpdateUserCommand(Command):
    def __init__(self, is_cache_enable: bool = False):
        super().__init__()
        self.is_cache_enable = is_cache_enable

    def run(self):
        command = SelectUserCommand(is_cache_enable=self.is_cache_enable)
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

        while True:
            match value:
                case "name":
                    name = self.input.text("Novo nome:")
                    user.name = name
                case "email":
                    email = self.input.text("Novo email:", validator=EmailValidator())
                    existing_user = self.users_repository.findByEmail(
                        email, self.is_cache_enable
                    )
                    if existing_user:
                        self.output.error("Email já cadastrado")
                        continue
                    user.email = email
                case "cpf":
                    cpf = self.input.text("Novo CPF:", validator=CpfValidator())
                    existing_user = self.users_repository.findByCpf(
                        cpf, self.is_cache_enable
                    )
                    if existing_user:
                        self.output.error("CPF já cadastrado")
                        continue
                    user.cpf = cpf
                case "phone":
                    phone = self.input.text(
                        "Novo telefone:", validator=PhoneValidator()
                    )
                    user.phone = phone
                case "zipcode":
                    zipcode = self.input.text("Novo CEP:", validator=ZipcodeValidator())
                    user.address.zipcode = zipcode
                case "neighbourhood":
                    neighbourhood = self.input.text("Novo bairro:")
                    user.address.neighbourhood = neighbourhood
                case "number":
                    number = self.input.text("Novo número:", validator=IntValidator())
                    user.address.number = number
                case "city":
                    city = self.input.text("Nova cidade:")
                    user.address.city = city
                case "street":
                    street = self.input.text("Nova rua:")
                    user.address.street = street
                case "state":
                    state = self.input.text("Novo estado:")
                    user.address.state = state
                case "complement":
                    complement = self.input.text("Novo complemento:", is_required=False)
                    user.address.complement = complement
                case "exit":
                    self.exit()
                    self.output.clear()
                    return
            break

        self.users_repository.update(user, is_cache_enable=self.is_cache_enable)
        self.output.loading()
        self.output.success("Vendedor atualizado com sucesso!")
