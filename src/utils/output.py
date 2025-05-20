from time import sleep

from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.console import Console


class Output:
    def __init__(self, selected_database: str = None):
        self.console = Console(width=200)
        self.selected_database = selected_database

    def table(self, columns: list, rows: list[list]):
        table = Table(expand=False, leading=1)

        for column in columns:
            table.add_column(column, justify="center", style="cyan", no_wrap=True)

        for row in rows:
            table.add_row(*row)

        self.console.print(table)

    def loading(self):
        self.console.print("\n")
        with self.console.status("Carregando...", spinner="material"):
            sleep(2)
        self.console.print("\n")
        self.clear()

    def success(self, message: str):
        self.console.print("\n")
        text = Text(message, justify="center", style="green")
        self.console.print(text)
        self.console.print("\n")

    def error(self, message: str):
        self.console.print("\n")
        text = Text(message, justify="center", style="red")
        self.console.print(text)
        self.console.print("\n")

    def info(self, message: str):
        text = Text(message, justify="center", style="orange")
        self.console.print(text)

    def clear(self):
        self.console.clear()

    def title(self, title: str):
        self.clear()
        if self.selected_database:
            self.console.print(
                f"[bright_yellow] Banco de dados selecionado: {self.selected_database.upper()} [/bright_yellow]",
            )
        self.console.print(
            Panel.fit(
                f"[bright_yellow] {title} [/bright_yellow]",
                border_style="bright_blue",
                padding=(1, 1),
                title="[bold yellow]Mercado Livre 🤝 [/bold yellow]",
            )
        )
