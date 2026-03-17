from app.modules.products.repository import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    @property
    def repository(self):
        """The repository property."""
        return self._repository
