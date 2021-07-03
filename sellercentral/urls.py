from django.urls import path
from sellercentral import views
from .views import Dashboard, OrderDetails

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('order/<pk>', OrderDetails.as_view(), name='order-details-seller')
]