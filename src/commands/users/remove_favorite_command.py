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
        self.repository.update(user)
        self.output.loading()
        self.output.clear()
        self.output.success("Usuário removido dos favoritos com sucesso!")
