from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    picture: Optional[str] = None


class ProductCreate(ProductBase):
    number: str
    design: str
    price: int
    quantity: int


class ProductOut(ProductBase):
    number: str
    design: str
    price: int
    quantity: int


class ProductUpdate(ProductBase):
    design: Optional[str] = None
    price: Optional[int] = None
