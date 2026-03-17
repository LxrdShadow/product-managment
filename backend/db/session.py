from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.settings import get_settings

settings = get_settings()

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,  # ensures dead connections are revived
    pool_size=10,  # keep 10 connections in the connection pool
    max_overflow=20,  # maximum number of connections that can be opened beyond pool_size
)


AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_async_session_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async database session context
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async session dependency for FastAPI
    """
    async with get_async_session_context() as session:
        yield session
