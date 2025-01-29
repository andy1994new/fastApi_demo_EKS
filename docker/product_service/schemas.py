# schemas.py
# pylint: disable=R0903
"""
This module contains the Pydantic schemas for validating and --
serializing the request and response data.
It defines two schemas: productCreateSchema for creating products and --
productSchema for representing product data.
"""
from pydantic import BaseModel


class ProductCreateSchema(BaseModel):
    """
    Schema for creating a new product.

    Attributes:
        name (str): The name of the product.
        price: The price of the product.
        stock_left: The quality of the item left in the stock.
    """

    name: str
    price: int
    stock_left: int


class ProductSchema(BaseModel):
    """
    Schema for representing a product.

    Attributes:
        id (int): The unique identifier for the product.
        name (str): The name of the product.
        price: The price of the product.
        stock_left: The quality of the item left in the stock.
    """

    id: int
    name: str
    price: int
    stock_left: int

    class Config:
        """
        Configuration for the ProductSchema.

        orm_mode = True tells Pydantic to treat the data as ORM models, --
        allowing automatic conversion
        from SQLAlchemy model instances to Pydantic models.
        """

        orm_mode = True


class ProductStockUpdateSchema(BaseModel):
    """
    Schema for update the stock of a product.

    Attributes:
        add_amount (str): The number of the product to add into stock.
    """

    add_amount: int


class ProductRequireSchema(BaseModel):
    """
    Schema for update the stock of a product.

    Attributes:
        add_amount (str): The number of the product to add into stock.
    """

    ids: list[int]
