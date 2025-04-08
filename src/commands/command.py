from utils.input import Input
from utils.output import Output


class Command:
    def __init__(self):
        self.is_running = True
        self.input = Input()
        self.output = Output()

    def exit(self):
        self.is_running = False
