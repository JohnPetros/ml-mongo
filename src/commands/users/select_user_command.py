from commands.command import Command
from entities.user import User
from repositories.users_repository import UsersRepository
from commands.users.list_users_command import ListUsersCommand


class SelectUserCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = UsersRepository()

    def run(self) -> User:
        users = self.repository.findAll()
        command = ListUsersCommand()
        users = command.run()
        if not users:
            return

        while self.is_running:
            user_id = self.input.text("ID do usuário:")

            user = list(filter(lambda user: user.get_id() == user_id, users))

            if len(user):
                self.exit()
                return user[0]

            self.output.error("Usuário não encontrado")
