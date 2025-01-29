"""This module provides order-related APIs for order creation and retrieval."""

import logging
import os
import httpx
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, get_db
from schemas import OrderRequestSchema, OrderItemSchema, OrderSchema
from utils import (
    validate_product_stock,
    generate_order,
    generate_order_items,
    product_update,
    user_update,
)

# Environment-based configuration for service URLs
ENV = os.getenv("ENV", "eks")

DEFAULT_USER_SERVICE_URL = "http://localhost:8000/user"
DEFAULT_PRODUCT_SERVICE_URL = "http://localhost:8001/product"

if ENV == "docker":
    USER_SERVICE_URL = "http://user-service:8000/user"
    PRODUCT_SERVICE_URL = "http://product-service:8000/product"
elif ENV == "eks":
    USER_SERVICE_URL = "http://user-service/user"
    PRODUCT_SERVICE_URL = "http://product-service/product"
elif ENV == "local":
    USER_SERVICE_URL = "http://localhost:8000/user"
    PRODUCT_SERVICE_URL = "http://localhost:8001/product"
elif ENV == "k8s":
    USER_SERVICE_URL = "http://user-service/user"
    PRODUCT_SERVICE_URL = "http://product-service/product"
else:
    USER_SERVICE_URL = DEFAULT_USER_SERVICE_URL
    PRODUCT_SERVICE_URL = DEFAULT_PRODUCT_SERVICE_URL

models.Base.metadata.create_all(engine)

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.get("/")
def get_index():
    """Handle GET request for the root endpoint."""
    return {"msg": "Order service"}


@app.post("/order")
async def post_order(request: OrderRequestSchema, db: Session = Depends(get_db)):
    """Handles the creation of an order."""
    try:
        # Validate product stock
        products = await validate_product_stock(
            request, f"{PRODUCT_SERVICE_URL}/getlist", client=httpx.AsyncClient()
        )

        # Generate and save the order
        order = generate_order(products, request)
        db.add(order)
        db.commit()
        db.refresh(order)

        # Generate and save the order items
        items = generate_order_items(products, order)
        for item in items:
            db.add(item)
            db.commit()
            db.refresh(item)

        # Update the product stock and user information
        await product_update(products, PRODUCT_SERVICE_URL, client=httpx.AsyncClient())
        await user_update(order, USER_SERVICE_URL, client=httpx.AsyncClient())

        return order

    except HTTPException as e:
        # Re-raise the exception with context
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@app.get("/order/{order_id}", response_model=OrderSchema)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    """Retrieve an order by its ID."""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.get("/order/items/{order_id}", response_model=list[OrderItemSchema])
def get_items_by_id(order_id: int, db: Session = Depends(get_db)):
    """Retrieve order items by order ID."""
    items = (
        db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()
    )
    if not items:
        raise HTTPException(status_code=404, detail="Items not found")
    return items
