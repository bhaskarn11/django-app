import json
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView
from .models import Cart, CartItem, Product, Order, Review
from django.db.models import Avg
from django.contrib import messages
from ecomm.forms import CreateReviewForm
# Create your views here.

def index(request):
    messages.info(request,'This site is currently in development')
    return render(request, 'ecomm/index.html')


class SearchView(ListView):
    model = Product
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET
        context['query'] = query.get('query')
        context['products'] = Product.objects.filter(description__contains=query.get('query'))
        return context


def productDetailView(request, pk):
    model = Product.objects.get(id=pk)
    if request.method == 'GET':
        form = CreateReviewForm()
        context = {'object': model}
        context['reviews'] = Review.objects.filter(product=pk).all().order_by('-review_date')
        avg_rating = context['reviews'].aggregate(Avg('rating')).get('rating__avg') # calculates avarage rating
        context['rating'] = int(avg_rating) if avg_rating else None 
        context['form'] = form
        return render(request, 'ecomm/product-details.html', context)
    elif request.method == 'POST':
        review = Review(title = request.POST['title'], content=request.POST['content'], rating=request.POST['rating'], author=request.user.profile, product = model)
        review.save()
        messages.success(request,'Review posted!')
        return redirect('product-details', pk)
 

class OrderCreateView(CreateView):
    model = Order

    @method_decorator(login_required) # to check whether user is logged in
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    fields = ['shipping_address', 'billing_address']


class OrderListView(ListView):
    model = Order
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = Order.objects.filter(customer=self.request.user)
        return query


class OrderDetailView(DetailView):
    model = Order
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        shop_cart, created = Cart.objects.get_or_create(user=customer)
        items = shop_cart.cartitem_set.all()
    else:
        items = []
        shop_cart = {'get_cart_total': 0, 'get_cart_quantity':0, 'total_cart_item': 0}

    context = { 'items': items, 'cart': shop_cart}
    return render(request, 'ecomm/cart.html', context)


# shopping cart API endpoint
def updateCart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=productId)
    cart = Cart.objects.get(user=customer)
    cartitem, created = CartItem.objects.get_or_create(cart = cart, product=product, price=product.price)
    if action == 'add':
        cartitem.quantity = cartitem.quantity + 1
        cartitem.save()
    elif action == 'remove':
        if cartitem.quantity == 1:
            cartitem.delete()
        else:
            cartitem.quantity = cartitem.quantity - 1
            cartitem.save()

    return JsonResponse({"added": True}, safe=False)
