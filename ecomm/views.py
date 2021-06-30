from account.models import Profile
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from .models import Product, Order, Review
from django.db.models import Avg
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
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.object.id).all()
        avg_rating = context['reviews'].aggregate(Avg('rating')).get('rating__avg') # calculates avarage rating
        context['rating'] = int(avg_rating) if avg_rating else None 
        return context
 

class OrderCreateView(CreateView):
    model = Order

    @method_decorator(login_required) # to check whether user is logged in
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    fields = ['shipping_address', 'billing_address']


class OrderListView(ListView):
    model = Order
    def get_queryset(self):
        query = Order.objects.filter(customer=self.request.user)
        return query

# class CartListView(ListView):
#     model = 