# pylint: disable=R0903
# pylint: disable=W0707
"""
This module contains utility functions to interact with external services such 
as validating users and product stock, creating orders, and updating users 
and products. Functions are asynchronous and use the HTTP client to communicate 
with external APIs.
"""
import httpx
from fastapi import HTTPException
from schemas import OrderRequestSchema, OrderSchema
from models import OrderItem, Order


async def validate_user(user_id: int, user_service_url: str, client: httpx.AsyncClient):
    """
    Validates whether a user exists by sending a GET request to the user service.

    Args:
        user_id (int): The ID of the user to be validated.
        user_service_url (str): The URL of the user service.
        client (httpx.AsyncClient): The HTTP client used to make the request.

    Returns:
        dict: The user data if found.

    Raises:
        HTTPException: If the user is not found or if there is a communication error.
    """
    try:
        response = await client.get(f"{user_service_url}/{user_id}")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="User not found")
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500, detail=f"User service communication error: {str(e)}"
        ) from e  # Re-raise with original exception


async def validate_product_stock(
    request: OrderRequestSchema, product_service_url: str, client: httpx.AsyncClient
):
    """
    Validates product stock based on the order request.

    Args:
        request (OrderRequestSchema): The order request data.
        product_service_url (str): The URL of the product service.
        client (httpx.AsyncClient): The HTTP client used to make the request.

    Returns:
        list: A list of products with updated stock information.

    Raises:
        HTTPException: If there are insufficient stock or communication errors.
    """
    ids = []
    id_num_map = {}
    for item in request.items:
        if item.product_id in id_num_map:
            id_num_map[item.product_id] += item.number
        else:
            id_num_map[item.product_id] = item.number
            ids.append(item.product_id)

    try:
        response = await client.post(product_service_url, json={"ids": ids})
        products = response.json()
        stock_less_than_order = []
        for product in products:
            if product["stock_left"] < id_num_map[product["id"]]:
                stock_less_than_order.append(
                    {
                        "product_name": product["name"],
                        "ordered_quantity": id_num_map[product["id"]],
                        "stock_left": product["stock_left"],
                    }
                )
            else:
                product["order_number"] = id_num_map[product["id"]]
                product["item_total"] = product["order_number"] * product["price"]

        if stock_less_than_order:
            error_details = "\n".join(
                [
                    f"Product {item['product_name']} - Ordered: {item['ordered_quantity']}"
                    for item in stock_less_than_order
                ]
            )
            raise HTTPException(
                status_code=400,
                detail=f"Some products have insufficient stock:\n{error_details}",
            )

        return products

    except httpx.HTTPStatusError as e:
        error_message = await e.response.text()
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Product service error: {error_message}",
        ) from e  # Re-raise with original exception

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500, detail=f"User service communication error: {str(e)}"
        ) from e  # Re-raise with original exception


def generate_order(products, request: OrderRequestSchema):
    """
    Generates an order object based on the product information and request.

    Args:
        products (list): A list of products with stock details.
        request (OrderRequestSchema): The order request data.

    Returns:
        Order: The generated order object.
    """
    total = 0
    for product in products:
        total += product["item_total"]
    return Order(user_id=request.user_id, order_total=total)


def generate_order_items(products, order: OrderSchema):
    """
    Generates order items based on the products and the associated order.

    Args:
        products (list): A list of products with stock details.
        order (OrderSchema): The order to which the items belong.

    Returns:
        list: A list of OrderItem objects.
    """
    items = []
    for product in products:
        item = OrderItem(
            order_id=order.id,
            product_id=product["id"],
            product_num=product["order_number"],
            price=product["price"],
            item_total=product["item_total"],
        )
        items.append(item)

    return items


async def product_update(products, product_service_url: str, client: httpx.AsyncClient):
    """
    Updates the product stock by reducing the stock based on the order quantity.

    Args:
        products (list): A list of products to update.
        product_service_url (str): The URL of the product service.
        client (httpx.AsyncClient): The HTTP client used to make the request.

    Raises:
        HTTPException: If there is a communication error.
    """
    for product in products:
        try:
            response = await client.put(
                f"{product_service_url}/{product['id']}",
                json={"add_amount": -product["order_number"]},
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=404, detail="Product not found") from exc
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f"Product service communication error: {str(e)}"
            ) from e  # Re-raise with original exception


async def user_update(order: Order, user_service_url: str, client: httpx.AsyncClient):
    """
    Updates the user with the new order ID.

    Args:
        order (Order): The order to update the user with.
        user_service_url (str): The URL of the user service.
        client (httpx.AsyncClient): The HTTP client used to make the request.

    Raises:
        HTTPException: If there is a communication error.
    """
    try:
        await client.put(
            f"{user_service_url}/{order.user_id}", json={"order_id": order.id}
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=404, detail="User not found") from exc
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500, detail=f"User service communication error: {str(e)}"
        ) from e  # Re-raise with original exception
