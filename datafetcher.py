from ecomm.models import Product
import json

import itertools
products = Product.objects.all()
with open('products.json', 'r+') as f:
    data = json.load(f)
    for item, product in itertools.product(data, products[4:]):
        product.image.url = item['image']
