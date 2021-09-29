from ecomm.models import Order
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
# Create your views here.

class Dashboard(ListView):
    model = Order
    template_name = 'sellercentral/dashboard.html'
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_order'] = self.object_list.count()
        context['total_order_amount'] = sum([order.order_amount for order in self.object_list])
        context['completed_orders'] = self.object_list.filter(status='Completed').count()
        context['canceled_orders'] = self.object_list.filter(status='Canceled').count()
        return context

class OrderDetails(DetailView):
    model = Order
    template_name = 'sellercentral/order-details.html'

    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self.object.get_order_items
        context['items'] = items
        return context
