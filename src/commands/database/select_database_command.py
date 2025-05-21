from commands.command import Command


class SelectDatabaseCommand(Command):
    def run(self):
        self.output.title("Selecionar banco de dados")

        while self.is_running:
            choice = self.input.select(
                "Opções",
                [
                    (
                        f"MongoDB {'(Selecionado)' if self.selected_database == 'mongodb' else ''}",
                        "mongodb",
                    ),
                    (
                        f"Cassandra {'(Selecionado)' if self.selected_database == 'cassandra' else ''}",
                        "cassandra",
                    ),
                    (
                        f"Neo4j {'(Selecionado)' if self.selected_database == 'neo4j' else ''}",
                        "neo4j",
                    ),
                    ("Voltar", "exit"),
                ],
            )
            match choice:
                case "mongodb":
                    self.select_database("mongodb")
                    self.exit()
                case "cassandra":
                    self.select_database("cassandra")
                    self.exit()
                case "neo4j":
                    self.select_database("neo4j")
                    self.exit()
                case "exit":
                    self.exit()
                case _:
                    self.output.error("Opção inválida")
