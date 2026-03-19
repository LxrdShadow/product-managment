from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Product(Base):

    __tablename__ = "products"

    number: Mapped[str] = mapped_column(String(20), primary_key=True)
    design: Mapped[str] = mapped_column(String(30), index=True)
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)
    picture: Mapped[str] = mapped_column(String, nullable=False)
