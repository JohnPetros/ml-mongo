from commands.command import Command
from commands.users.show_users_menu_command import ShowUsersMenuCommand
from commands.sellers.show_sellers_menu_command import ShowSellersMenuCommand
from commands.products.show_product_menu_command import ShowProductsMenuCommand
from commands.purchases.show_purchases_menu_command import ShowPurchasesMenuCommand


class StartAppCommand(Command):
    def run(self):
        self.output.title("Bem-vindo ao Mercado Livre")

        while self.is_running:
            choice = self.input.select(
                "Home",
                [
                    ("1 - Área de clientes", "customers-menu"),
                    ("2 - Área de produtos", "products-menu"),
                    ("3 - Área de vendedores", "sellers-menu"),
                    ("4 - Área de compras", "purchases-menu"),
                    ("5 - Sair", "exit"),
                ],
            )
            command = None

            match choice:
                case "customers-menu":
                    command = ShowUsersMenuCommand()
                case "products-menu":
                    command = ShowProductsMenuCommand()
                case "sellers-menu":
                    command = ShowSellersMenuCommand()
                case "purchases-menu":
                    command = ShowPurchasesMenuCommand()
                case "exit":
                    self.exit()
                    self.output.clear()
                    self.output.success("Até mais!")
                case _:
                    self.output.error("Opção inválida")

            if command:
                command.run()
