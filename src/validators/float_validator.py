from validators.validator import Validator


class FloatValidator(Validator):
    def validate(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            self.output.error("Valor deve ser um número decimal válido")
            return False
