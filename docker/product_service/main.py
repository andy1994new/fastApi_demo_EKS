# main.py
"""This module provides product related APIs for product creation and retrieval."""


import logging
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, get_db
from schemas import (
    ProductCreateSchema,
    ProductSchema,
    ProductStockUpdateSchema,
    ProductRequireSchema,
)


models.Base.metadata.create_all(engine)

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.get("/")
def get_index():
    """Handle GET request for the root endpoint."""
    return {"msg": "Product service"}


@app.post("/product")
def post_product(request: ProductCreateSchema, db: Session = Depends(get_db)):
    """
    Handle POST request to create a new product.
    """
    product = models.Product(
        name=request.name, price=request.price, stock_left=request.stock_left
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return {"id": product.id}


@app.get("/product/{product_id}", response_model=ProductSchema)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """
    Handle GET request to retrieve a product by their ID.
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/product/getlist", response_model=list[ProductSchema])
def get_product_by_ids(request: ProductRequireSchema, db: Session = Depends(get_db)):
    """
    Handle POST request to retrieve a list of products by their IDs.
    """

    products = db.query(models.Product).filter(models.Product.id.in_(request.ids)).all()

    if not products:
        raise HTTPException(
            status_code=404, detail="No products found for the given IDs"
        )

    found_ids = {product.id for product in products}
    missing_ids = set(request.ids) - found_ids
    if missing_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Products not found for the following IDs: {missing_ids}",
        )
    return products


@app.put("/product/{product_id}", response_model=ProductSchema)
def update_product_stock(
    product_id: int, request: ProductStockUpdateSchema, db: Session = Depends(get_db)
):
    """
    Update the stock of a product by adding or subtracting from the existing stock.
    """

    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock_left + request.add_amount < 0:
        raise HTTPException(
            status_code=400, detail="stock is not enough for this order"
        )

    product.stock_left += request.add_amount
    db.commit()
    db.refresh(product)

    return product
