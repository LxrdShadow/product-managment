from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.products.repository import ProductRepository
from app.modules.products.service import ProductService
from core.settings import get_settings
from db.session import get_async_session
from upload.cloudinary_storage import CloudinaryStorage
from upload.local_storage import LocalStorage
from upload.storage import Storage

settings = get_settings()


async def get_product_repository(
    session: AsyncSession = Depends(get_async_session),
) -> ProductRepository:
    return ProductRepository(session)


async def get_local_storage() -> Storage:
    return LocalStorage()


async def get_cloudinary_storage() -> Storage:
    return CloudinaryStorage(settings.CLOUDINARY_CLOUD_NAME)


async def get_product_service(
    repo: ProductRepository = Depends(get_product_repository),
    storage: Storage = Depends(get_cloudinary_storage),
) -> ProductService:
    return ProductService(repo, storage)
