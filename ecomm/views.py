import os
from django.http.response import HttpResponseNotAllowed
from account.models import Address
import json
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView, View
from ecomm.models import Cart, CartItem, OrderItem, Product, Order, Review
from django.db.models import Avg
from django.contrib import messages
from ecomm.forms import CheckoutForm, ReviewForm
# razorpay api
import razorpay
import hmac
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


class CheckoutView(View):
    def get(self, *args, **kwargs):
        profile = self.request.user.profile
        form = CheckoutForm(initial= profile.address.get_address)
        if self.request.GET.get('productId') and self.request.GET.get('action') == 'buynow':
            product = Product.objects.get(pk=self.request.GET.get('productId'))
            context = {
                'product': product,
                'form': form
            }
            
        else:
            context = {
            'form': form
            }

        return render(self.request, 'ecomm/order-checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST)
        client = razorpay.Client(auth=(os.getenv('RAZORPAY_API_KEY'), os.getenv('RAZORPAY_API_KEY_SECRET')))
        if form.is_valid():
            data = form.cleaned_data
            address = f"{data['address']},\n{data['city']} ,{data['state']}-{data['pincode']},\n {data['country']}"
            product = Product.objects.get(id=self.request.POST.get('productId'))
            order = Order(
                        customer = self.request.user, order_amount = product.unitprice,
                        payment_method=data['payment_method'], shipping_address = address, billing_address=address)
            order.save()
            order_amount = int(order.order_amount * 100)
            order_receipt = order.order_id
            # print(order_amount)
            DATA = {
                'amount': order_amount,
                'currency': 'INR',
                'receipt': order_receipt,
                'payment_capture': 1
            }
            res = client.order.create(data=DATA)
            Order.objects.filter(pk=order.order_id).update(transaction_id=res.get('id'))
            return redirect('payment', order_id=order.order_id, permanent=True)
        messages.warning('Plese enter')
        return redirect('order-checkout')

def payment(request, order_id):
    if request.method == 'GET':
        order = Order.objects.get(pk=order_id)
        context = {
            'amount': int(order.order_amount * 100),
            'order_id': order.transaction_id,
        }
        return render(request, 'ecomm/checkout-payment.html', context)
    else:
        return HttpResponseNotAllowed

def payment_success(request):
    response = request.POST
    # hmac.digest(bytearray(os.getenv('RAZORPAY_API_KEY_SECRET')))
    return render(request, 'ecomm/order-success.html')

