from abc import ABC, abstractmethod

from utils.input import Input
from utils.output import Output
from repositories.session_repository import SessionRepository


class Command(ABC):
    def __init__(self, subcommand=None):
        self.SESSION_CREDENTIALS = {"email": "admin@gmail.com", "password": "admin123"}
        session_repository = SessionRepository()

        if not session_repository.has_session():
            self.__require_session()

        self.is_running = True
        self.subcommand = subcommand
        self.input = Input()
        self.output = Output()

    @abstractmethod
    def run(self): ...

    def exit(self):
        self.is_running = False

    def run_subcommand(self):
        if self.subcommand:
            self.subcommand.run()

    def __require_session(self):
        self.output.title("Login do usuário admnistrador")
        self.repository.add_session()

        while True:
            email = self.input.text("Email:")
            password = self.input.password()

            if (
                self.SESSION_CREDENTIALS["email"] == email
                and self.SESSION_CREDENTIALS["password"] == password
            ):
                self.repository.add_session()
                self.output.success("Login realizado com sucesso!")
                break
            else:
                self.output.error("Email ou senha inválidos!")
