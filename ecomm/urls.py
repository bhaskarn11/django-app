from django.urls import path
from . import views
from ecomm.views import SearchView, productDetailView, OrderListView, cart, ReviewListView

urlpatterns = [
    path('', views.index, name='index'),
    path('search', SearchView.as_view(template_name = 'ecomm/search-result.html'), name='search-result'),
    path('products/<sku>', productDetailView, name='product-details'),
    path('products/<sku>/reviews', ReviewListView.as_view(template_name='ecomm/reviews.html'), name='reviews'),
    path('orders', OrderListView.as_view(template_name='ecomm/myorders.html'), name='myorder'),
    path('cart', cart, name='cart'),
    path('orders/<order_id>', views.OrderDetailView.as_view(template_name='ecomm/order-details.html'), name='order-details')
]