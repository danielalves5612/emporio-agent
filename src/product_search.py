from src.data_loader import load_products

def search_products(query):
    products = load_products()
    filter_name_products = products["name"].str.contains(query, case=False)
    name_after_filters = products[filter_name_products]
    return name_after_filters[["product_id", "name", "price_brl", "stock_quantity", "status"]]