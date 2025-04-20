from questionary import Choice, Style, select, text, password
from utils.output import Output
from validators.validator import Validator


class Input:
    def select(self, message: str, choices: list[tuple[str]]):
        return select(
            message,
            choices=[Choice(title=choice[0], value=choice[1]) for choice in choices],
            qmark="?",
            pointer=">",
            style=Style(
                [
                    ("qmark", "fg:#FFEA00 bold"),
                    ("pointer", "fg:#FFEA00 bold"),
                    ("selected", "fg:#FFEA00 bold"),
                    ("question", "bold"),
                ]
            ),
        ).ask()

    def text(self, messege: str, is_required: bool = True, validator: Validator = None):
        while True:
            value = text(messege).ask()
            if is_required and not value:
                Output().error("Campo obrigatório")
                continue
            if validator and not validator.validate(value):
                continue
            return value

    def password(self):
        while True:
            value = password("Senha").ask()
            if not value:
                Output().error("Campo obrigatório")
                continue
            return value
