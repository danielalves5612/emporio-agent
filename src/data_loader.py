import pandas as pd

def load_products():
    products = pd.read_csv('data/desafio_tecnico_ai_eng - products.csv')
    return products

def load_customers():
    customers = pd.read_csv('data/desafio_tecnico_ai_eng - customers.csv')
    return customers

def load_order_items():
    items = pd.read_csv('data/desafio_tecnico_ai_eng - order_items.csv')
    return items

def load_orders():
    orders = pd.read_csv('data/desafio_tecnico_ai_eng - orders.csv')
    return orders

def load_promotions():
    promotions = pd.read_csv('data/desafio_tecnico_ai_eng - promotions.csv')
    return promotions