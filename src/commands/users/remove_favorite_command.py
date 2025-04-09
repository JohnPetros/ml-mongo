from commands.command import Command
from repositories.users_repository import UsersRepository
from commands.users.list_favorites_command import ListFavoritesCommand


class RemoveFavoriteCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = UsersRepository()

    def run(self):
        command = ListFavoritesCommand()
        user = command.run()

        if user.favorites is None:
            return

        while self.is_running:
            favorite_id = self.input.text("ID do favorito:")
            favorite = list(
                filter(lambda user: user.get_id() == favorite_id, user.favorites)
            )

            if len(favorite):
                self.exit()
                return favorite[0]

            self.output.error("Favorito não encontrado")

        user.remove_favorite(favorite)

        self.repository.update(user)
        self.output.loading()
        self.output.clear()
        self.output.success("Produto removido dos favoritos com sucesso!")
