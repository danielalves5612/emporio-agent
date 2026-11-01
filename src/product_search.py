from src.data_loader import load_products


def search_products(query):
    products = load_products()
    filter_name_products = products["name"].str.contains(query, case=False)
    name_after_filters = products[filter_name_products]
    return name_after_filters[
        ["product_id", "name", "price_brl", "stock_quantity", "status"]
    ]


def get_availability(status, stock_quantity):
    if status == "active" and stock_quantity > 0:
        return "available"
    elif status == "active" and stock_quantity == 0:
        return "out_of_stock"
    elif status == "discontinued":
        return "discontinued"
    elif status == "coming_soon":
        return "coming_soon"
    else:
        return "unknown"
