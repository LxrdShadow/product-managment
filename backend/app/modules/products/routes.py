from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.modules.products.dependencies import get_product_service
from app.modules.products.exceptions import ProductNotFound
from app.modules.products.schema import ProductCreate, ProductOut
from app.modules.products.service import ProductService

router = APIRouter(tags=["Products"], prefix="/products")


@router.post("/", response_model=ProductOut)
async def create_product(
    product: ProductCreate, service: ProductService = Depends(get_product_service)
):
    try:
        return await service.create_product(product)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, {"error": str(e)})


@router.get("/", response_model=list[ProductOut])
async def get_all_products(service: ProductService = Depends(get_product_service)):
    try:
        return await service.get_all()
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, {"error": str(e)})


@router.get("/:number", response_model=ProductOut)
async def get_one_product(
    number: str = Query(...), service: ProductService = Depends(get_product_service)
):
    try:
        return await service.get_one(number)
    except ProductNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, {"error": e.message})
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, {"error": str(e)})


@router.delete("/:number", response_model=ProductOut)
async def delete_product(
    number: str = Query(...), service: ProductService = Depends(get_product_service)
):
    try:
        return await service.delete_product(number)
    except ProductNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, {"error": e.message})
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, {"error": str(e)})
