from questionary import Choice, Style, select, text


class Input:
    def select(self, message: str, choices: list[tuple[str]]):
        return select(
            message,
            choices=[Choice(title=choice[0], value=choice[1]) for choice in choices],
            qmark="?",
            pointer=">",
            style=Style(
                [
                    ("qmark", "fg:#FFEA00 bold"),
                    ("pointer", "fg:#FFEA00 bold"),
                    ("selected", "fg:#FFEA00 bold"),
                    ("question", "bold"),
                ]
            ),
        ).ask()

    def text(self, messege: str):
        return text(messege).ask()
