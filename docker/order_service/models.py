# pylint: disable=R0903
"""
This module contains the SQLAlchemy models for the application. 
It defines the 'Order' model with basic attributes like:
 'id', 'user_id', 'product_id', 'product_num'.
"""
from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Order(Base):
    """
    Order model representing an order in the system.
    
    Attributes:
        id (int): Primary key for the order.
        user_id (int): ID of the user associated with the order.
        order_total (float): Total amount for the order.
    """

    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    order_total = Column(Float, nullable=False)

    def __repr__(self):
        # A string representation of the order object
        return f"<Order(user_id={self.user_id}, order_total={self.order_total})>"


class OrderItem(Base):
    """
    OrderItem model representing individual items in an order.
    
    Attributes:
        id (int): Primary key for the order item.
        order_id (int): ID of the associated order.
        product_id (int): ID of the product in the order.
        product_num (int): Quantity of the product in the order.
        price (float): Price of the product.
        item_total (float): Total cost for the order item.
    """

    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    product_num = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    item_total = Column(Float, nullable=False)

    def __repr__(self):
        # A string representation of the order item object
        return f"<OrderItem(order_id={self.order_id}, product_id={self.product_id}, " \
               f"product_num={self.product_num}, item_total={self.item_total})>"
