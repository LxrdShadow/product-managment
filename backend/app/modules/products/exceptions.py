class ProductNotFound(Exception):
    def __init__(self, number: str, message: str | None = None):
        self.message = message or f"Produit avec le numéro '{number}' est introuvable."
        super().__init__(self.message)


class ProductAlreadyExists(Exception):
    def __init__(self, number: str, message: str | None = None):
        self.message = message or f"Produit avec le numéro '{number}' existe déjà."
        super().__init__(self.message)
