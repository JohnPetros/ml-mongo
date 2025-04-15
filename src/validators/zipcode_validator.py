from validators.validator import Validator


class ZipcodeValidator(Validator):
    def validate(self, value: str) -> bool:
        if not value.isdigit() or len(value) != 8:
            self.output.error("CEP deve conter 8 dígitos numéricos")
            return False
        return True
