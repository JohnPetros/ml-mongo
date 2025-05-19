from commands.command import Command
from commands.users.list_favorites_command import ListFavoritesCommand


class RemoveFavoriteCommand(Command):
    def run(self):
        command = ListFavoritesCommand()
        user = command.run()

        if not user:
            return

        if not len(user.favorites):
            self.output.error("Favoritos não encontrado")
            return

        favorite_id = self.input.text("ID do favorito:")
        favorite = None
        while not favorite:
            favorite = list(
                filter(lambda favorite: favorite.id[-4:] == favorite_id, user.favorites)
            )[0]

        user.remove_favorite(favorite)
        self.users_repository.update(user)
        self.output.loading()
        self.output.clear()
        self.output.success("Usuário removido dos favoritos com sucesso!")
