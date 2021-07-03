from ecomm.models import CartItem, Order
from django.shortcuts import render
from django.views.generic import ListView, DetailView
# Create your views here.

class Dashboard(ListView):
    model = Order
    template_name = 'sellercentral/dashboard.html'

class OrderDetails(DetailView):
    model = Order
    template_name = 'sellercentral/order-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = CartItem.objects.filter(cart=self.object.items)
        context['items'] = items
        return context
