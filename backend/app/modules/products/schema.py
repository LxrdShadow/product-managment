from pydantic import BaseModel


class ProductBase(BaseModel):
    number: str
    design: str
    price: int
    quantity: int


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    pass
