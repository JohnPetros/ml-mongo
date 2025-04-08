from commands.command import Command
from commands.sellers.show_seller_menu_command import ShowSellersMenuCommand


class StartAppCommand(Command):
    def run(self):
        self.output.title("Bem-vindo ao Mercado Livre")

        while self.is_running:
            choice = self.input.select(
                "Home",
                [
                    ("1 - Área de clientes", "customers-menu"),
                    ("2 - Área de compras", "purchases-menu"),
                    ("3 - Área de vendedores", "sellers-menu"),
                    ("4 - Sair", "exit"),
                ],
            )
            command = None

            match choice:
                case "customers-menu":
                    self.output.title("Cliente")
                    self.output.success("Cliente")
                case "purchases-menu":
                    self.output.title("Compra")
                    self.output.success("Compra")
                case "sellers-menu":
                    command = ShowSellersMenuCommand()
                case "exit":
                    self.exit()
                    self.output.clear()
                    self.output.success("Até mais!")
                case _:
                    self.output.error("Opção inválida")

            if command:
                command.run()
