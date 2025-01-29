# models.py
# pylint: disable=R0903
"""
This module contains the SQLAlchemy models for the application. 
It defines the 'Order' model with basic attributes like 'id', 'user_id', 'product_id', 'product_num'.
"""
from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Order(Base):
    """
    order model representing a order in the system.
    Attributes:
        id (int): Primary key for the order.
        name (str): Name of the order.
        orders (list): A list of integer values representing the order's orders.
    """

    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    order_total = Column(Float, nullable=False)


    def __repr__(self):
        # A string representation of the order object
        return f"<order(user_id={self.user_id}, order_toal={self.order_total})>"
    
class OrderItem(Base):

    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    product_num = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    item_total = Column(Float, nullable=False)


    def __repr__(self):
        # A string representation of the order object
        return f"<order(order_id={self.order_id}, product_id={self.product_id}), product_num={self.product_num}), item_total={self.item_total})>"
