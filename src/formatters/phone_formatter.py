class PhoneFormatter:
    @staticmethod
    def format(phone: str) -> str:
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"