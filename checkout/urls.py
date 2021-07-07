from django.urls import path
from . import views
from checkout.views import CheckoutView


urlpatterns = [
    path('', CheckoutView.as_view(), name='order-checkout'),
    path('payment/<order_id>', views.payment, name='payment'),
    path('payment/success/<order_id>', views.payment_success, name='payment-success')
]