from commands.command import Command
from commands.products.list_products_command import ListProductsCommand
from commands.products.update_product_cache_command import UpdateProductCacheCommand
from commands.products.clear_products_cache_command import ClearProductsCacheCommand
from commands.products.synchronize_products_database_with_cache_command import (
    SynchronizeProductsDatabaseWithCache,
)


class ShowProductsCacheManipulationMenuCommand(Command):
    def run(self):
        self.output.title("Menu de cache de produtos")

        while self.is_running:
            choice = self.input.select(
                "Opções",
                [
                    ("Mostrar cache", "show-cache"),
                    ("Atualizar cache", "update-cache"),
                    ("Sincronizar cache com banco de dados", "synchronize-cache"),
                    ("Limpar cache", "clear-cache"),
                    ("Voltar", "exit"),
                ],
            )
            command = None

            match choice:
                case "show-cache":
                    command = ListProductsCommand(is_cache_enable=True)
                case "update-cache":
                    command = UpdateProductCacheCommand(is_cache_enable=True)
                case "synchronize-cache":
                    command = SynchronizeProductsDatabaseWithCache()
                case "clear-cache":
                    command = ClearProductsCacheCommand()
                case "exit":
                    self.exit()
                case _:
                    self.output.error("Opção inválida")

            if command:
                self.output.clear()
                command.run()
