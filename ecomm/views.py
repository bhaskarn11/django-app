import json
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView
from ecomm.models import Cart, CartItem, Product, Order, Review
from django.db.models import Avg
from django.contrib import messages
from ecomm.forms import ReviewForm
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
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                data = form.cleaned_data
                review = Review(title= data['title'], content=data['content'], author=request.user.profile, product = model)
                review.save()
                messages.success(request,'Review posted!')
                return redirect('product-details', pk)
            else:
                pass 
        else:
            messages.warning(request, 'You have to login to post a review!')
            return redirect('product-details', pk)  

    form = ReviewForm()
    reviews = Review.objects.filter(product=pk).all().order_by('-review_date')
    avg_rating = reviews.aggregate(Avg('rating')).get('rating__avg') # calculates avarage rating
    rating= int(avg_rating) if avg_rating else None 

    return render(request, 'ecomm/product-details.html', {'form': form, 'reviews': reviews, 'rating':rating, 'object': model })


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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     customer = self.request.user
    #     cart = self.object.get(customer = customer)
    #     items = cart.cartitem_set.all()
    #     context['items'] = items
    #     return context

    

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
