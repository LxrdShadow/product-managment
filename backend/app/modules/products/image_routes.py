from fastapi import APIRouter, Depends, Response

from app.modules.products.dependencies import get_cloudinary_storage
from upload.storage import Storage

image_router = APIRouter(tags=["Images"], prefix="/uploads")


@image_router.get("/{public_id:path}")
def get_image(public_id: str, storage: Storage = Depends(get_cloudinary_storage)):
    data, mime = storage.fetch(public_id)

    return Response(content=data, media_type=mime)
