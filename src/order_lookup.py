from src.data_loader import load_orders, load_customers

def find_order(order_id):
    orders = load_orders()
    match = orders[orders["order_id"] == order_id]
    if match.empty:
        return None
    return match.iloc[0].to_dict()

def verify_order_owner(order_id, email):
    order = find_order(order_id)
    if order is None:
        return False
    customer_number = order["customer_id"]
    customers = load_customers()
    match = customers[customers["customer_id"] == customer_number]
    if match.empty:
        return False
    customer = match.iloc[0].to_dict()
    store_email = customer["email"].strip().lower()
    provide_email = email.strip().lower()
    return store_email == provide_email