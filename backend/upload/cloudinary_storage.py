from typing import Tuple

import cloudinary
import cloudinary.uploader
import requests

from core.settings import get_settings
from upload.storage import Storage

settings = get_settings()
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


class CloudinaryStorage(Storage):
    def __init__(self, cloud_name: str) -> None:
        self.base_url = (
            f"https://res.cloudinary.com/{cloudinary.cloud_name}/image/upload"
        )

    def save(self, path: str, content: bytes) -> str:
        result = cloudinary.uploader.upload(
            content, public_id=path, folder="product-management"
        )
        return result.get("public_id")

    def fetch(self, id: str) -> Tuple[bytes, str]:
        url = f"{self.base_url}/{id}"
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception("Image not found")

        return r.content, r.headers["Content-Type"]
