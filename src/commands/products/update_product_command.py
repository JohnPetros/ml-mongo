from commands.command import Command
from repositories.products_repository import ProductsRepository
from commands.products.select_product_command import SelectProductCommand


class UpdateProductCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = ProductsRepository()

    def run(self):
        command = SelectProductCommand()
        seller = command.run()

        value = self.input.select(
            "Qual valor deseja atualizar?",
            [
                (f"Nome ({seller.name})", "name"),
                (f"Preço ({seller.price})", "price"),
                (f"Descrição ({seller.description})", "description"),
                ("Voltar", "exit"),
            ],
        )

        match value:
            case "name":
                name = self.input.text("Novo nome:")
                seller.name = name
            case "price":
                price = self.input.text("Novo preço:")
                seller.price = price
            case "description":
                description = self.input.text("Nova descrição:")
                seller.description = description
            case "exit":
                self.exit()
                self.output.clear()
                return

        self.repository.update(seller)
        self.output.loading()
        self.output.clear()
        self.output.success("Vendedor atualizado com sucesso!")
        print(seller)
