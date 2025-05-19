from commands.command import Command
from commands.products.select_product_command import SelectProductCommand
from validators.float_validator import FloatValidator


class UpdateProductCommand(Command):
    def __init__(self, is_cache_enable: bool = False):
        super().__init__()
        self.is_cache_enable = is_cache_enable

    def run(self):
        command = SelectProductCommand(self.is_cache_enable)
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

        self.products_repository.update(product, self.is_cache_enable)
        self.output.loading()
        self.output.success("Vendedor atualizado com sucesso!")
