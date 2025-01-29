# main.py
"""This module provides order-related APIs for order creation and retrieval."""

import logging
import os
from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, get_db
from schemas import OrderRequestSchema, OrderItemSchema, OrderSchema
import httpx
from utils import validate_product_stock, generate_order, generate_order_items, product_update, user_update

ENV = os.getenv("ENV", "eks")

if ENV == "docker":
    user_service_url = "http://user-service:8000/user"
    product_service_url = "http://product-service:8000/product"

if ENV == "eks":
    user_service_url = "http://user-service/user"
    product_service_url = "http://product-service/product"

if ENV == "local":
    user_service_url = "http://localhost:8000/user"
    product_service_url = "http://localhost:8001/product"

if ENV == "k8s":
    user_service_url = "http://user-service/user"
    product_service_url = "http://product-service/product"

models.Base.metadata.create_all(engine)

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.get("/")
def get_index():
    """Handle GET request for the root endpoint."""
    return {"msg": "Order service"}

@app.post("/order")
async def post_order(request: OrderRequestSchema, db: Session = Depends(get_db)):
    try:
        products = await validate_product_stock(request, f"{product_service_url}/getlist", client=httpx.AsyncClient())
        order = generate_order(products, request)
        db.add(order)
        db.commit()
        db.refresh(order)

        items = generate_order_items(products, order)
        for item in items:
            db.add(item)
            db.commit()
            db.refresh(item)
        
        await product_update(products,  product_service_url, client=httpx.AsyncClient())

        await user_update(order, user_service_url, client=httpx.AsyncClient())
        
        return order

    except HTTPException as e:
        # Handle the exception if any product is missing
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
@app.get("/order/{order_id}", response_model=OrderSchema)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="User not found")
    return order

@app.get("/order/items/{order_id}", response_model=list[OrderItemSchema])
def get_items_by_id(order_id: int, db: Session = Depends(get_db)):
    items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()
    if not items:
        raise HTTPException(status_code=404, detail="User not found")
    return items