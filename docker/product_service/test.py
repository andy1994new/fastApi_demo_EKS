"""
Test module for the user service endpoints.
This module contains tests for the FastAPI user service, 
including testing the main endpoint, creating a user, and reading user details.
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_index():
    """
    Test the root endpoint ("/").
    Ensures the endpoint returns a 200 status code and the expected JSON response.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Product service"}


def test_post_product():
    """
    Test the product creation endpoint ("/product").
    Ensures a product can be created successfully.
    """
    response = client.post(
        "/product",
        json={
            "name": "Test Product",
            "price": 10.0,
            "stock_left": 100,
        },
    )
    assert response.status_code == 200


def test_get_product_by_id():
    """
    Test retrieving a product by its ID ("/product/{product_id}").
    Ensures a product is returned when using a valid ID.
    """
    # Create a product first
    response = client.post(
        "/product",
        json={
            "name": "Test Product 2",
            "price": 15.0,
            "stock_left": 50,
        },
    )
    assert response.status_code == 200

    # Get the product by ID
    response = client.get("/product/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"
    assert response.json()["price"] == 10.0
    assert response.json()["stock_left"] == 100


def test_get_product_by_ids():
    """
    Test retrieving multiple products by their IDs ("/product/getlist").
    Ensures the endpoint returns all requested products.
    """
    # Create multiple products
    client.post(
        "/product",
        json={
            "name": "Test Product 3",
            "price": 20.0,
            "stock_left": 30,
        },
    )
    client.post(
        "/product",
        json={
            "name": "Test Product 4",
            "price": 25.0,
            "stock_left": 40,
        },
    )

    # Retrieve products by their IDs
    response = client.post(
        "/product/getlist",
        json={"ids": [1, 2]},
    )
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Test Product"
    assert response.json()[1]["name"] == "Test Product 2"


def test_update_product_stock():
    """
    Test updating a product's stock ("/product/{product_id}").
    Ensures the stock is updated correctly.
    """
    # Create a product
    client.post(
        "/product",
        json={
            "name": "Test Product 5",
            "price": 30.0,
            "stock_left": 50,
        },
    )

    # Update the stock
    response = client.put(
        "/product/1",
        json={"add_amount": -10},
    )
    assert response.status_code == 200
    assert response.json()["stock_left"] == 90  # 100 - 10 = 90
