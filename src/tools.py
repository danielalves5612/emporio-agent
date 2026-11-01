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
