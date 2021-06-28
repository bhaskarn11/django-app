from django.db import models
from account.models import Profile
from django.http import request
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Product, Order

# Create your views here.

def index(request):
    return render(request, 'ecomm/index.html')


class SearchView(ListView):
    model = Product
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET
        context['query'] = query.get('query')
        context['products'] = Product.objects.filter(description__contains=query.get('query'))
        return context


class ProductDetailView(DetailView):
    model = Product
 

class OrderCreateView(CreateView):
    model = Order
    fields = ['shipping_address', 'billing_address']
