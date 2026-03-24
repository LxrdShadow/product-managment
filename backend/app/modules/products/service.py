import os
from typing import Optional
from uuid import uuid4

from fastapi import UploadFile

from app.modules.products.exceptions import ProductAlreadyExists, ProductNotFound
from app.modules.products.models import Product
from app.modules.products.repository import ProductRepository
from app.modules.products.schema import ProductCreate, ProductUpdate
from core.settings import get_settings
from upload.storage import Storage

settings = get_settings()


class ProductService:
    def __init__(
        self, repository: ProductRepository, storage: Optional[Storage] = None
    ) -> None:
        self._repository = repository
        self._storage = storage

    @property
    def repository(self) -> ProductRepository:
        """The repository property."""
        if not self._repository:
            raise ValueError("Repository not set")
        return self._repository

    @property
    def storage(self) -> Storage:
        """The storage property."""
        if not self._storage:
            raise ValueError("Storage not set")
        return self._storage

    async def create_product(
        self, product: ProductCreate, picture: Optional[UploadFile]
    ) -> Product:
        existing = await self.repository.get_one(product.number)
        if existing:
            raise ProductAlreadyExists(product.number)

        data = {
            "number": product.number,
            "design": product.design,
            "price": product.price,
            "quantity": product.quantity,
        }

        if picture:
            filename = f"{uuid4()}_{picture.filename}"
            save_path = os.path.join(settings.UPLOAD_PATH, filename)

            id = self.storage.save(save_path, await picture.read())

            picture_path = f"/uploads/{id}"
            data["picture"] = picture_path

        return await self.repository.insert(data)

    async def get_all(self) -> list[Product]:
        return await self.repository.get_all()

    async def get_one(self, number: str) -> Product:
        product = await self.repository.get_one(number)
        if not product:
            raise ProductNotFound(number)
        return product

    async def delete_product(self, number: str) -> Product:
        product = await self.repository.get_one(number)
        if not product:
            raise ProductNotFound(number)

        return await self.repository.delete(number)

    async def update_product(
        self, number: str, product: ProductUpdate, picture: Optional[UploadFile]
    ) -> Product:
        existing = await self.repository.get_one(number)
        if not existing:
            raise ProductNotFound(number)

        updates = product.dict(exclude_unset=True, exclude_none=True)
        if picture:
            filename = f"{uuid4()}_{picture.filename}"
            save_path = os.path.join(settings.UPLOAD_PATH, filename)

            id = self.storage.save(save_path, await picture.read())

            picture_path = f"/uploads/{id}"
            updates["picture"] = picture_path

        return await self.repository.update(number, **updates)

    async def get_stat_metrics(self):
        return await self.repository.get_stats()
