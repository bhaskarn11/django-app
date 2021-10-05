from django.urls import path
from sellercentral import views
from .views import Dashboard, OrderDetails, InventoryView

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('order/<order_id>', OrderDetails.as_view(), name='order-details-seller'),
    path('inventory', InventoryView.as_view(), name='inventory')
]