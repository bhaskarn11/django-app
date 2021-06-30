from django.urls import path
from . import views
from .views import OrderCreateView, SearchView, ProductDetailView, OrderListView

urlpatterns = [
    path('', views.index, name='index'),
    path('search', SearchView.as_view(template_name = 'ecomm/search-result.html'), name='search-result'),
    path('product/<pk>', ProductDetailView.as_view(template_name='ecomm/product-details.html'), name='product-details'),
    path('checkout', OrderCreateView.as_view(template_name='ecomm/order-checkout.html'), name='order-checkout'),
    path('orders', OrderListView.as_view(template_name='ecomm/myorders.html'), name='myorder')
]