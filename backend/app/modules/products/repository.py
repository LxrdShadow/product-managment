from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.products.models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def insert(self, product: Product) -> Product:
        """Insert a product in the database."""
        stmt = insert(Product).values(product).returning(Product)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
