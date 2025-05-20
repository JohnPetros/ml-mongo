from commands.command import Command
from entities.user import User
from commands.users.list_users_command import ListUsersCommand


class SelectUserCommand(Command):
    def __init__(self, is_cache_enable: bool = False):
        super().__init__()
        self.is_cache_enable = is_cache_enable

    def run(self) -> User:
        if self.is_cache_enable:
            users = self.users_cache_repository.findAll()
        else:
            users = self.users_repository.findAll()

        if not (len(users)):
            self.output.error("Nenhum usuário encontrado. Cadastre um primeiro")
            return

        command = ListUsersCommand(is_cache_enable=self.is_cache_enable)
        command.run()

        while self.is_running:
            user_id = self.input.text("ID do usuário:")

            user = list(filter(lambda user: user.get_id() == user_id, users))

            if user:
                self.exit()
                return user[0]

            self.output.error("Usuário não encontrado")
