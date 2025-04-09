from commands.command import Command
from repositories.users_repository import UsersRepository
from commands.users.select_user_command import SelectUserCommand


class DeleteUserCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = UsersRepository()

    def run(self):
        command = SelectUserCommand()
        user = command.run()
        if user is None:
            return

        self.repository.remove(user)
        self.output.loading()
        self.output.clear()
        self.output.success("Vendedor removido com sucesso!")
