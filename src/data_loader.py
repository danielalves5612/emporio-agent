import pandas as pd

def load_products():
    products = pd.read_csv('data/desafio_tecnico_ai_eng - products.csv')
    return products

def load_customers():
    customers = pd.read_csv('data/desafio_tecnico_ai_eng - customers.csv')
    return customers