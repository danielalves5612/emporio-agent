from src.data_loader import load_categories, load_products
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


def browse_products(category: str, max_price: float) -> list:
    """List the products that can be bought now in a category, up to a price.

    Use this tool when the customer wants options or recommendations, for
    example "acoustic guitars up to R$ 1000". Do not use it for a specific
    product name; use find_products for that.

    Returns at most 15 products, cheapest first, each with product_id, name,
    price_brl and stock_quantity. Only products that are active and in stock
    are returned. The list is empty if nothing matches.

    Args:
        category: the category name. One of: "Guitarras", "Baixos",
            "Baterias e Percussão", "Teclados e Pianos", "Violões",
            "Instrumentos de Sopro (Madeiras)", "Instrumentos de Sopro (Metais)",
            "Cordas Orquestrais", "Ukuleles".
        max_price: the maximum price in reais. If the customer gave no limit,
            use 1000000.
    """
    categories = load_categories()
    products = load_products()
    matching = categories[categories["name"].str.contains(category, case=False)]
    in_category = products["category_id"].isin(matching["category_id"])
    can_buy = (products["status"] == "active") & (products["stock_quantity"] > 0)
    affordable = products["price_brl"] <= max_price
    results = products[in_category & can_buy & affordable]
    results = results.sort_values("price_brl").head(15)
    columns = ["product_id", "name", "price_brl", "stock_quantity"]
    return results[columns].to_dict(orient="records")
