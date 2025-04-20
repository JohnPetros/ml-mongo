from commands.command import Command
from commands.users.cache_users_command import CacheUsersCommand


class ShowUsersCacheMenuCommand(Command):
    def run(self):
        while self.is_running:
            choice = self.input.select(
                "Opções",
                [
                    ("Colocar usuários em cache", "cache-users"),
                    ("Voltar", "exit"),
                ],
            )
            command = None

            match choice:
                case "cache-users":
                    command = CacheUsersCommand()
                case "exit":
                    self.exit()
                    self.output.clear()
                case _:
                    self.output.error("Opção inválida")

            if command:
                command.run()
