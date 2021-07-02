from django.urls import path
from . import views

urlpatterns = [
    path('getcartquantity', views.get_total_cart_quantity, name='cart-quantity')
]