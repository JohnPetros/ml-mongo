from validators.validator import Validator


class IntValidator(Validator):
    def validate(self, value: str) -> bool:
        try:
            int(value)
            return True
        except ValueError:
            self.output.error("Valor deve ser um número inteiro válido")
            return False
