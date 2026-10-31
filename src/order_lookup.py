from src.data_loader import load_orders

def find_order(order_id):
    orders = load_orders()
    match = orders[orders["order_id"] == order_id]
    if match.empty:
        return None
    return match.iloc[0].to_dict()