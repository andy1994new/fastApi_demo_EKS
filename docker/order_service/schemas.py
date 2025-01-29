# pylint: disable=R0903
"""
This module contains the Pydantic schemas for validating and --
serializing the request and response data.
It defines two schemas: orderCreateSchema for creating orders and --
orderSchema for representing order data.
"""
from pydantic import BaseModel


class OrderItemRequestSchema(BaseModel):
    """
    Schema for the items contained in the order request body.

    Attributes:
        product_id (int): The ID of the product being ordered.
        number (int): The quantity of the product ordered.
    """

    product_id: int
    number: int


class OrderRequestSchema(BaseModel):
    """
    Schema for creating a new order.

    Attributes:
        user_id (int): The ID of the user creating the order.
        items (List[OrderItemRequestSchema]): A list of items in the order,
        represented by OrderItemRequestSchema.
    """

    user_id: int
    items: list[OrderItemRequestSchema]


class OrderSchema(BaseModel):
    """
    Schema for representing an order.

    Attributes:
        id (int): The unique identifier for the order.
        user_id (int): The ID of the user who placed the order.
        order_total (float): The total amount for the order.
    """

    id: int
    user_id: int
    order_total: float

    class Config:
        """
        Configuration for the OrderSchema.

        orm_mode = True tells Pydantic to treat the data as ORM models,
        allowing automatic conversion from SQLAlchemy model instances to Pydantic models.
        """
        orm_mode = True


class OrderItemSchema(BaseModel):
    """
    Schema for representing an order item.

    Attributes:
        id (int): The unique identifier for the order item.
        order_id (int): The ID of the order to which the item belongs.
        product_id (int): The ID of the product in the item.
        product_num (int): The quantity of the product.
        price (float): The price of the product.
        item_total (float): The total price for the item (quantity * price).
    """

    id: int
    order_id: int
    product_id: int
    product_num: int
    price: float
    item_total: float

    class Config:
        """
        Configuration for the OrderItemSchema.

        orm_mode = True tells Pydantic to treat the data as ORM models,
        allowing automatic conversion from SQLAlchemy model instances to Pydantic models.
        """
        orm_mode = True
