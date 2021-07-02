from django.urls import path
from . import views
from .views import OrderCreateView, SearchView, productDetailView, OrderListView, cart

urlpatterns = [
    path('', views.index, name='index'),
    path('search', SearchView.as_view(template_name = 'ecomm/search-result.html'), name='search-result'),
    path('product/<pk>', views.productDetailView, name='product-details'),
    path('checkout', OrderCreateView.as_view(template_name='ecomm/order-checkout.html'), name='order-checkout'),
    path('orders', OrderListView.as_view(template_name='ecomm/myorders.html'), name='myorder'),
    path('cart', cart, name='cart'),
    path('orders/<pk>', views.OrderDetailView.as_view(template_name='ecomm/order-details.html'), name='order-details')
]