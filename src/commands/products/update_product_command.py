from commands.command import Command
from repositories.products_repository import ProductsRepository
from commands.products.select_product_command import SelectProductCommand
from validators.float_validator import FloatValidator


class UpdateProductCommand(Command):
    def __init__(self):
        super().__init__()
        self.repository = ProductsRepository()

    def run(self):
        command = SelectProductCommand()
        product = command.run()

        if product is None:
            return

        value = self.input.select(
            "Qual valor deseja atualizar?",
            [
                (f"Nome ({product.name})", "name"),
                (f"Preço ({product.price})", "price"),
                (f"Descrição ({product.description})", "description"),
                ("Voltar", "exit"),
            ],
        )

        match value:
            case "name":
                name = self.input.text("Novo nome:")
                product.name = name
            case "price":
                price = self.input.text("Novo preço R$:", validator=FloatValidator())
                product.price = price
            case "description":
                description = self.input.text("Nova descrição:")
                product.description = description
            case "exit":
                self.exit()
                self.output.clear()
                return

        self.repository.update(product)
        self.output.loading()
        self.output.clear()
        self.output.success("Vendedor atualizado com sucesso!")
        print(product)
