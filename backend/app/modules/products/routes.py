from fastapi import APIRouter, HTTPException, status

from app.modules.products.dependencies import get_product_service
from app.modules.products.schema import ProductCreate, ProductOut

router = APIRouter(tags=["Products"], prefix="/products")


@router.post("/", response_model=ProductOut)
async def create_product(product: ProductCreate, service: get_product_service):
    try:
        return service.create_product(product)
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": str(e)})
