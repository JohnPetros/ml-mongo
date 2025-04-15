from validators.validator import Validator


class CpfValidator(Validator):
    def validate(self, value: str) -> bool:
        if not value.isdigit() or len(value) != 11:
            self.output.error("CPF deve conter 11 dígitos numéricos")
            return False
        return True
