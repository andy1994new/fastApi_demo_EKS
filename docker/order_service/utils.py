import httpx
from fastapi import HTTPException
from schemas import OrderRequestSchema, OrderSchema
from models import OrderItem, Order


async def validate_user(user_id: int, user_service_url: str, client: httpx.AsyncClient):
    try:
        response = await client.get(f"{user_service_url}/{user_id}")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="User not found")
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500, detail=f"User service communication error: {str(e)}"
        )


async def validate_product_stock(
    request: OrderRequestSchema, product_service_url: str, client: httpx.AsyncClient
):
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
                    f"Product {item['product_name']} - Ordered: {item['ordered_quantity']} Available: {item['stock_left']}"
                    for item in stock_less_than_order
                ]
            )
            raise HTTPException(
                status_code=400,
                detail=f"Some products have insufficient stock:\n{error_details}",
            )

        return products

    except httpx.HTTPStatusError as e:
        # Capture the exact error message from the product service
        error_message = await e.response.text()  # or e.response.json() if it's JSON
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Product service error: {error_message}",
        )

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500, detail=f"User service communication error: {str(e)}"
        )


def generate_order(products, request: OrderRequestSchema):
    total = 0
    for product in products:
        total += product["item_total"]
    return Order(user_id=request.user_id, order_total=total)


def generate_order_items(products, order: OrderSchema):
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
    for product in products:
        # params = {"add_amount": -product["order_number"]}
        try:
            response = await client.put(
                f"{product_service_url}/{product['id']}", json={"add_amount": -product["order_number"]}
            )
            response.raise_for_status()
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=404, detail="Product not found")
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f"Product service communication error: {str(e)}"
            )
        
async def user_update(order: Order, user_service_url: str, client: httpx.AsyncClient):
    try:
        await client.put(
            f"{user_service_url}/{order.user_id}", 
            json={"order_id": order.id}
        )
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="Product not found")
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500, detail=f"Product service communication error: {str(e)}"
        )