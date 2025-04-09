from commands.command import Command
from commands.users.create_user_command import CreateUserCommand
from commands.users.list_users_command import ListUsersCommand
from commands.users.update_user_command import UpdateUserCommand
from commands.users.delete_user_command import DeleteUserCommand
from commands.users.list_favorites_command import ListFavoritesCommand
from commands.users.add_favorite_command import AddFavoriteCommand
from commands.users.remove_favorite_command import RemoveFavoriteCommand


class ShowUsersMenuCommand(Command):
    def run(self):
        self.output.title("Menu do usuário")

        while self.is_running:
            choice = self.input.select(
                "Opções",
                [
                    ("Listar usuários", "list-users"),
                    ("Cadastrar usuário", "create-user"),
                    ("Atualizar usuário", "update-user"),
                    ("Deletar usuário", "delete-user"),
                    ("Listar favoritos", "list-favorites"),
                    ("Adicionar favorito", "add-favorite"),
                    ("Remover favorito", "remove-favorite"),
                    ("Voltar", "exit"),
                ],
            )
            command = None

            match choice:
                case "list-users":
                    command = ListUsersCommand()
                case "create-user":
                    command = CreateUserCommand()
                case "update-user":
                    command = UpdateUserCommand()
                case "delete-user":
                    command = DeleteUserCommand()
                case "list-favorites":
                    command = ListFavoritesCommand()
                case "remove-favorite":
                    command = RemoveFavoriteCommand()
                case "add-favorite":
                    command = AddFavoriteCommand()
                case "exit":
                    self.exit()
                case _:
                    self.output.error("Opção inválida")

            if command:
                self.output.clear()
                command.run()
