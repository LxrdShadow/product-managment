from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Response,
    UploadFile,
    status,
)

from app.modules.products.dependencies import (
    get_cloudinary_storage,
    get_product_service,
)
from app.modules.products.exceptions import ProductNotFound
from app.modules.products.schema import ProductCreate, ProductOut, ProductUpdate
from app.modules.products.service import ProductService
from upload.storage import Storage

router = APIRouter(tags=["Products"], prefix="/products")
image_router = APIRouter(tags=["Images"], prefix="/uploads")


@router.post("/", response_model=ProductOut)
async def create_product(
    number: str = Form(...),
    design: str = Form(...),
    price: int = Form(...),
    quantity: int = Form(...),
    picture: Optional[UploadFile] = File(None),
    service: ProductService = Depends(get_product_service),
):
    try:
        product = ProductCreate(
            number=number, design=design, price=price, quantity=quantity
        )
        return await service.create_product(product, picture)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, {"error": str(e)})


@router.get("/stats")
async def get_stat_metrics(service: ProductService = Depends(get_product_service)):
    try:
        return await service.get_stat_metrics()
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, {"error": str(e)})


@router.get("/", response_model=list[ProductOut])
async def get_all_products(service: ProductService = Depends(get_product_service)):
    try:
        return await service.get_all()
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, {"error": str(e)})


@router.get("/{number}", response_model=ProductOut)
async def get_one_product(
    number: str, service: ProductService = Depends(get_product_service)
):
    try:
        return await service.get_one(number)
    except ProductNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, {"error": e.message})
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, {"error": str(e)})


@router.delete("/{number}", response_model=ProductOut)
async def delete_product(
    number: str, service: ProductService = Depends(get_product_service)
):
    try:
        return await service.delete_product(number)
    except ProductNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, {"error": e.message})
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, {"error": str(e)})


@router.patch("/{number}", response_model=ProductOut)
async def update_product(
    number: str,
    design: Optional[str] = Form(None),
    price: Optional[int] = Form(None),
    quantity: Optional[int] = Form(None),
    picture: Optional[UploadFile] = File(None),
    service: ProductService = Depends(get_product_service),
):
    try:
        product = ProductUpdate(design=design, price=price, quantity=quantity)
        return await service.update_product(number, product, picture)
    except ProductNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, {"error": e.message})
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, {"error": str(e)})


@image_router.get("/{public_id:path}")
def get_image(public_id: str, storage: Storage = Depends(get_cloudinary_storage)):
    data, mime = storage.fetch(public_id)

    return Response(content=data, media_type=mime)
