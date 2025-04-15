from abc import ABC, abstractmethod

from utils.output import Output


class Validator(ABC):
    def __init__(self):
        self.output = Output()

    @abstractmethod
    def validate(self, value: str) -> bool: ...
