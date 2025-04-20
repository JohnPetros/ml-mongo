from commands.command import Command
from commands.products.cache_products_command import CacheProductsCommand


class ShowProductsCacheMenuCommand(Command):
    def run(self):
        while self.is_running:
            choice = self.input.select(
                "Opções",
                [
                    ("Colocar produtos em cache", "cache-products"),
                    ("Voltar", "exit"),
                ],
            )
            command = None

            match choice:
                case "cache-products":
                    command = CacheProductsCommand()
                case "exit":
                    self.exit()
                    self.output.clear()
                case _:
                    self.output.error("Opção inválida")

            if command:
                command.run()
