from django.urls import path
from . import views
from .views import CheckoutView, SearchView, productDetailView, OrderListView, cart

urlpatterns = [
    path('', views.index, name='index'),
    path('search', SearchView.as_view(template_name = 'ecomm/search-result.html'), name='search-result'),
    path('product/<pk>', views.productDetailView, name='product-details'),
    path('checkout/', CheckoutView.as_view(), name='order-checkout'),
    path('checkout/payment/<order_id>', views.payment, name='payment'),
    path('payment/success/<order_id>', views.payment_success, name='payment-success'),
    path('orders', OrderListView.as_view(template_name='ecomm/myorders.html'), name='myorder'),
    path('cart', cart, name='cart'),
    path('orders/<pk>', views.OrderDetailView.as_view(template_name='ecomm/order-details.html'), name='order-details')
]