# models.py
# pylint: disable=R0903
"""
This module contains the SQLAlchemy models for the application. 
It defines the 'User' model with basic attributes like 'id', 'name', and 'orders'.
"""
from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User model representing a user in the system.
    Attributes:
        id (int): Primary key for the user.
        name (str): Name of the user.
        orders (list): A list of integer values representing the user's orders.
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    orders = Column(ARRAY(Integer), nullable=False)

    def __repr__(self):
        # A string representation of the User object
        return f"<User(name={self.name}, orders={self.orders})>"
