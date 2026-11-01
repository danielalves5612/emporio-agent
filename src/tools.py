from src.order_lookup import find_order, verify_order_owner
from src.product_search import get_availability, search_products


def find_products(query: str) -> list:
    """Search the store's products by name.

    Use this tool whenever the customer asks about the price, stock or
    availability of a product, or wants to find products by name or brand.

    Returns a list of matching products. Each product has its price in reais
    (price_brl), its stock quantity, its status and an availability label:
    "available", "out_of_stock", "discontinued" or "coming_soon".
    The list is empty if no product matches.

    Args:
        query: part of the product name, such as a brand or a model
            (for example "Yamaha" or "C40").
    """
    products = search_products(query)
    products_list = products.to_dict(orient="records")
    for item in products_list:
        item["availability"] = get_availability(item["status"], item["stock_quantity"])
    return products_list


def get_order_status(order_id: int, email: str) -> dict:
    """Check the status of a customer's order.

    Before using this tool, ask the customer for the order number and the
    email used to place the order. Never call it without both.

    Returns the order_id, status, order_date and estimated_delivery. If the
    order does not exist or the email does not match, it returns an error and
    no order data. In that case, tell the customer politely that you could not
    find an order with that information, without saying which of the two is
    wrong.

    Args:
        order_id: the order number, for example 1.
        email: the email address registered by the customer.
    """
    if not verify_order_owner(order_id, email):
        return {"error": "Order not found or email does not match."}
    order = find_order(order_id)
    return {
        "order_id": order["order_id"],
        "status": order["status"],
        "order_date": order["order_date"],
        "estimated_delivery": order["estimated_delivery"],
    }
