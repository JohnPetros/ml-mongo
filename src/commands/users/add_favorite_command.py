from commands.command import Command
from repositories.users_repository import UsersRepository
from commands.users.select_user_command import SelectUserCommand
from commands.products.select_product_command import SelectProductCommand


class AddFavoriteCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = UsersRepository()

    def run(self):
        user = self.__select_user()
        product = self.__select_product()
        user.add_favorite(product)

        self.repository.update(user)
        self.output.loading()
        self.output.clear()
        self.output.success("Produto adicionado aos favoritos com sucesso!")

    def __select_user(self):
        command = SelectUserCommand()
        user = command.run()
        return user

    def __select_product(self):
        command = SelectProductCommand()
        user = command.run()
        return user
