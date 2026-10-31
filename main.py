from src.data_loader import load_products
from src.data_loader import load_customers

print()
print('====== Lista de Produtos ======')
print()
products = load_products()
print(products.shape)
print()
print('====== Lista de Clientes ======')
print()
customers = load_customers()
print(customers.shape)