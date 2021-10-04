from django.urls import path
from . import views

urlpatterns = [
    path('getcartquantity', views.get_total_cart_quantity, name='cart-quantity'),
    path('review/helpful', views.helpful_review, name='helpful-review')
]