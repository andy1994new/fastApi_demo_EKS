# schemas.py
# pylint: disable=R0903
"""
This module contains the Pydantic schemas for validating and --
serializing the request and response data.
It defines two schemas: orderCreateSchema for creating orders and --
orderSchema for representing order data.
"""
from typing import List
from pydantic import BaseModel


class OrderItemRequestSchema(BaseModel):
    """
    Schema for the items contains in the order request body.

    Attributes:
        name (str): The name of the order.
        orders (List[int]): A list of orders associated with the order.
    """
    product_id: int
    number: int


class OrderRequestSchema(BaseModel):
    """
    Schema for creating a new order.

    Attributes:
        name (str): The name of the order.
        orders (List[int]): A list of orders associated with the order.
    """

    user_id: int
    items: list[OrderItemRequestSchema]


class OrderSchema(BaseModel):
    """
    Schema for representing a order.

    Attributes:
        id (int): The unique identifier for the order.
        name (str): The name of the order.
        orders (List[int]): A list of orders associated with the order.
    """

    id: int
    user_id: int
    order_total: float

    class Config:

        orm_mode = True


class OrderItemSchema(BaseModel):
    """
    Schema for representing a order.

    Attributes:
        id (int): The unique identifier for the order.
        name (str): The name of the order.
        orders (List[int]): A list of orders associated with the order.
    """

    id: int
    order_id: int
    product_id: int
    product_num: int
    price: float
    item_total: float

    class Config:

        orm_mode = True
