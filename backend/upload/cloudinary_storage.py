import cloudinary
import cloudinary.uploader

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
    def save(self, path: str, content: bytes) -> str:
        result = cloudinary.uploader.upload(content, public_id=path, folder="product-management")
        return result.get("public_id")
