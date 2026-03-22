from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.modules.products.routes import router as product_router
from core.settings import get_settings
from db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    yield


settings = get_settings()
app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.include_router(product_router)
