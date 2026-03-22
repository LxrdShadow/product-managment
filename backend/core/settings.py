from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TITLE: str = "Product management"
    DESCRIPTION: str = "School project for product management"
    VERSION: str = "1.0.0"

    DATABASE_URL: str

    UPLOAD_PATH: str = "data"

    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings(*args, **kwargs) -> Settings:
    return Settings(args, kwargs)
