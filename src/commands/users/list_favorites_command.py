from commands.command import Command
from repositories.users_repository import UsersRepository
from commands.users.select_user_command import SelectUserCommand


class ListFavoritesCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = UsersRepository()

    def run(self):
        command = SelectUserCommand()
        user = command.run()

        if not user:
            return

        if not user.favorites:
            self.output.error("Esse usuário não possui nenhum favorito.")
            return user

        self.output.table(
            columns=[
                "ID",
                "Nome",
                "Preço",
            ],
            rows=[
                [
                    favorite.get_id(),
                    favorite.name,
                    f"R${favorite.price:.2f}",
                ]
                for favorite in user.favorites
            ],
        )

        return user
