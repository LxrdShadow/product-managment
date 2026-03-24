from typing import Optional

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.products.models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def insert(self, product: dict[str, any]) -> Product:
        """Insert a product in the database."""
        stmt = insert(Product).values(product).returning(Product)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Product]:
        """Get all products in the database"""
        stmt = select(Product)
        result = await self.session.execute(stmt)
        return result.scalars()

    async def get_one(self, number: str) -> Product:
        """Get one products in the database"""
        stmt = select(Product).where(Product.number == number)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, number: str) -> Product:
        """Delete a product from the database"""
        stmt = delete(Product).where(Product.number == number).returning(Product)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, number: str, **data) -> Optional[Product]:
        """Update a product according to the data given"""
        stmt = (
            update(Product)
            .where(Product.number == number)
            .values(**data)
            .returning(Product)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_stats(self):
        """Get the stats (total, min, and max amount) in the database"""
        stmt = select(
            func.sum(Product.price * Product.quantity).label("total"),
            func.max(Product.price * Product.quantity).label("max"),
            func.min(Product.price * Product.quantity).label("min"),
        )
        result = (await self.session.execute(stmt)).one()
        return {"total": result.total, "max": result.max, "min": result.min}
