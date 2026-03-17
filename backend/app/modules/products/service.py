from app.modules.products.repository import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    @property
    def repository(self) -> ProductRepository:
        """The repository property."""
        if not self._repository:
            raise ValueError("Repository not set")
        return self._repository
