import httpx
import pytest

order_service_url = "http://localhost:8000"
user_service_url = "http://localhost:8001"
product_service_url = "http://localhost:8002"

# Helper function to create users
async def create_user(client, name: str):
    response = await client.post(
        f"{user_service_url}/user", json={"name": name}
    )
    assert response.status_code == 200
    return response.json()["id"]

# Helper function to create products
async def create_product(client, name: str, price: float, stock_left: int):
    response = await client.post(
        f"{product_service_url}/product",
        json={"name": name, "price": price, "stock_left": stock_left},
    )
    assert response.status_code == 200
    return response.json()["id"]

# user_service_tests
@pytest.mark.asyncio
async def test_user_service():
    async with httpx.AsyncClient() as client:
        # Test the root endpoint of the user service
        response = await client.get(f"{user_service_url}/")
        assert response.status_code == 200
        assert response.json() == {"msg": "User service"}

@pytest.mark.asyncio
async def test_create_user():
    async with httpx.AsyncClient() as client:
        # Create a user
        user_id = await create_user(client, "Test User")
        assert user_id is not None

# product_service_tests
@pytest.mark.asyncio
async def test_product_service():
    async with httpx.AsyncClient() as client:
        # Test the root endpoint of the product service
        response = await client.get(f"{product_service_url}/")
        assert response.status_code == 200
        assert response.json() == {"msg": "Product service"}

@pytest.mark.asyncio
async def test_post_product():
    async with httpx.AsyncClient() as client:
        # Create a product
        product_id = await create_product(client, "Test Product", 10.0, 100)
        assert product_id is not None

# order_service_tests
@pytest.mark.asyncio
async def test_post_order():
    async with httpx.AsyncClient() as client:
        # Create a user and product
        user_id = await create_user(client, "Test User")
        product_id = await create_product(client, "Test Product", 10.0, 100)

        # Create order request payload
        order_payload = {
            "user_id": user_id,
            "items": [
                {"product_id": product_id, "number": 1},
            ],
        }

        # Simulate creating an order
        response = await client.post(f"{order_service_url}/order", json=order_payload)
        assert response.status_code == 200
        order_id = response.json()["id"]
        assert order_id is not None

        # Verify user and product details have been updated
        # Check if the user has an order_id now
        response = await client.get(f"{user_service_url}/user/{user_id}")
        assert response.status_code == 200
        user_data = response.json()
        assert order_id in user_data["orders"]  # Verify the order was linked to the user

        # Check if the product stock has been reduced
        response = await client.get(f"{product_service_url}/product/{product_id}")
        assert response.status_code == 200
        product_data = response.json()
        assert product_data["stock_left"] == 99  # The stock should have been reduced by 1

@pytest.mark.asyncio
async def test_get_order_by_id():
    async with httpx.AsyncClient() as client:
        # Create a user and product
        user_id = await create_user(client, "Test User")
        product_id = await create_product(client, "Test Product", 10.0, 100)

        # Create order request payload
        order_payload = {
            "user_id": user_id,
            "items": [
                {"product_id": product_id, "number": 1},
            ],
        }

        # Simulate creating an order
        response = await client.post(f"{order_service_url}/order", json=order_payload)
        order_id = response.json()["id"]

        # Retrieve the created order
        response = await client.get(f"{order_service_url}/order/{order_id}")
        assert response.status_code == 200
        order_data = response.json()
        assert order_data["user_id"] == user_id
        assert order_data["order_total"] == 10.0  # Verify the total price of the order

@pytest.mark.asyncio
async def test_get_order_items():
    async with httpx.AsyncClient() as client:
        # Create a user and product
        user_id = await create_user(client, "Test User")
        product_id = await create_product(client, "Test Product", 10.0, 100)

        # Create order request payload
        order_payload = {
            "user_id": user_id,
            "items": [
                {"product_id": product_id, "number": 2},
            ],
        }

        # Simulate creating an order
        response = await client.post(f"{order_service_url}/order", json=order_payload)
        order_id = response.json()["id"]

        # Retrieve order items by order ID
        response = await client.get(f"{order_service_url}/order/items/{order_id}")
        assert response.status_code == 200
        items_data = response.json()
        assert len(items_data) == 1  # Verify there is 1 item in the order
        assert items_data[0]["product_id"] == product_id
        assert items_data[0]["product_num"] == 2  # Verify the correct quantity of the product

