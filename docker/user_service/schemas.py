# schemas.py
# pylint: disable=R0903
"""
This module contains the Pydantic schemas for validating and --
serializing the request and response data.
It defines two schemas: UserCreateSchema for creating users and --
UserSchema for representing user data.
"""
from typing import List
from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        name (str): The name of the user.
        orders (List[int]): A list of orders associated with the user.
    """

    name: str
    orders: List[int] = []


class UserSchema(BaseModel):
    """
    Schema for representing a user.

    Attributes:
        id (int): The unique identifier for the user.
        name (str): The name of the user.
        orders (List[int]): A list of orders associated with the user.
    """

    id: int
    name: str
    orders: List[int]

    class Config:
        """
        Configuration for the UserSchema.

        orm_mode = True tells Pydantic to treat the data as ORM models, --
        allowing automatic conversion
        from SQLAlchemy model instances to Pydantic models.
        """

        orm_mode = True


class UserOrderUpdateSchema(BaseModel):
    """
    Schema for update the user's order list from the order service.

    Attributes:
        name (str): The name of the user.
        orders (List[int]): A list of orders associated with the user.
    """

    order_id: int