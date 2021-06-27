from account.models import Profile
from django.http import request
from django.shortcuts import render
from django.views.generic import ListView
from .models import Product

# Create your views here.

def index(request):
    return render(request, 'ecomm/index.html')


class SearchView(ListView):
    model = Product
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(title__contains = self.request.GET.get('query'))
        return context

