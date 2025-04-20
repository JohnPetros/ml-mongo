class PriceFormatter:
    @staticmethod
    def format(price: float) -> str:
        return f"R${price:.2f}"
