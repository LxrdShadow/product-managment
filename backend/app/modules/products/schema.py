from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    design: str
    price: int
    quantity: int
    picture: Optional[str] = None


class ProductCreate(ProductBase):
    number: str


class ProductOut(ProductBase):
    number: str


class ProductUpdate(ProductBase):
    pass
