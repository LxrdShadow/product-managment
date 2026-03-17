from app.modules.products.models import Product
from app.modules.products.repository import ProductRepository
from app.modules.products.schema import ProductCreate


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    @property
    def repository(self) -> ProductRepository:
        """The repository property."""
        if not self._repository:
            raise ValueError("Repository not set")
        return self._repository

    async def create_product(self, product: ProductCreate) -> Product:
        data = {
            "number": product.number,
            "design": product.design,
            "price": product.price,
            "quantity": product.quantity,
        }

        return await self.repository.insert(data)

    async def get_all(self) -> list[Product]:
        return await self.repository.get_all()

    async def get_one(self, number: str) -> Product:
        return await self.repository.get_one(number)

    async def delete_product(self, number: str) -> Product:
        product = await self.repository.get_one(number)
        if not product:
            raise ValueError("Produit introuvable")

        return await self.repository.delete(number)
