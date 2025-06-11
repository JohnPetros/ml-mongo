from commands.command import Command
from commands.users.list_users_command import ListUsersCommand
from commands.users.update_user_command import UpdateUserCommand
from commands.users.clear_users_cache_command import ClearUsersCacheCommand
from commands.users.synchronize_users_database_with_cache_command import (
    SynchronizeUsersDatabaseWithCacheCommand,
)


class ShowUsersCacheManipulationMenuCommand(Command):
    def run(self):
        self.output.title("Menu de cache de usuários")

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
                    command = ListUsersCommand(is_cache_enable=True)
                case "update-cache":
                    command = UpdateUserCommand(is_cache_enable=True)
                case "synchronize-cache":
                    command = SynchronizeUsersDatabaseWithCacheCommand()
                case "clear-cache":
                    command = ClearUsersCacheCommand()
                case "exit":
                    self.exit()
                case _:
                    self.output.error("Opção inválida")

            if command:
                self.output.clear()
                command.run()
