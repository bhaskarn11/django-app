from django.contrib import admin
from .models import OrderItem , Product, Review, Order, CartItem, Cart
# Register your models here.

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(OrderItem)
