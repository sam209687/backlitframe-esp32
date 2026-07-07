from app.services.product_service import ProductService

product = ProductService.get_by_id(1)

print(product)

if product:
    print(product.product_name)