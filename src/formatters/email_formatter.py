class EmailFormatter:
    @staticmethod
    def format(email: str) -> str:
        email = email.strip().lower()
        
        if len(email) < 6:
            raise ValueError("Email deve conter pelo menos 6 caracteres")
            
        if '@' not in email:
            raise ValueError("Email deve conter o caractere '@'")
            
        local_part, domain = email.split('@')
        
        if not local_part or not domain:
            raise ValueError("Email deve ter uma parte local e um domínio válidos")
            
        return email