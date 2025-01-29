# models.py
# pylint: disable=R0903
"""
This module contains the SQLAlchemy models for the application. 
It defines the 'Product' model with basic attributes like 'id', 'name', 'price' and 'stock_left'.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    """
    product model representing a product in the system.
    Attributes:
        id (int): Primary key for the product.
        name (str): Name of the product.
        price: The price of the product.
        stock_left: The quality of the item left in the stock.
    """

    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    stock_left = Column(Integer, nullable=False)

    def __repr__(self):
        # A string representation of the Product object
        return f"<Product(name={self.name}, price={self.price}, stock_left={self.stock_left})>"
