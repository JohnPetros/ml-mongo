import re

from validators.validator import Validator


class EmailValidator(Validator):
    def validate(self, email: str) -> bool:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, email):
            self.output.error("E-mail inválido")
            return False
        return True
