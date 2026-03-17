from fastapi import APIRouter, Depends, HTTPException, status

from app.modules.products.dependencies import get_product_service
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
        raise HTTPException(status.HTTP_500_BAD_REQUEST, {"error": str(e)})


@router.get("/", response_model=list[ProductOut])
async def get_all_products(service: ProductService = Depends(get_product_service)):
    try:
        return await service.get_all()
    except Exception as e:
        raise HTTPException(status.HTTP_500_BAD_REQUEST, {"error": str(e)})
