from commands.command import Command
from commands.users.select_user_command import SelectUserCommand


class DeleteUserCommand(Command):
    def run(self):
        command = SelectUserCommand()
        user = command.run()
        if user is None:
            return

        self.users_repository.remove(user)
        self.output.loading()
        self.output.clear()
        self.output.success("Usuário removido com sucesso!")
