import json
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from ecomm.models import Cart, CartItem, Product, Order, Review
from django.db.models import Q
from django.contrib import messages
from ecomm.forms import ReviewForm
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    messages.info(request,'This site is currently in development')
    return redirect('search-result')


class SearchView(ListView):
    model = Product
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page')
        query = self.request.GET.get('query') if not (self.request.GET.get('query') == '') else None
        category = self.request.GET.get('category')
        context['query'] = query if query else ""
        # if page_number:
        #     context['current_query'] = self.request.GET.dict().pop('page')
        
        if category and query:
            products = Product.objects.filter(
                Q(description__icontains=query) |
                Q(title__icontains=query) & 
                Q(category__icontains=category)
            )
            paginator = Paginator(products, 8)
            context['products'] = paginator.get_page(page_number)
        elif (query):
            paginator = Paginator(Product.objects.filter(
                Q(description__icontains=query) |
                Q(title__icontains=query)
            ), 8)
            context['products'] = paginator.get_page(page_number)
        else:
            paginator = Paginator(Product.objects.all(), 8)
            context['products'] = paginator.get_page(page_number)
        
        return context


def productDetailView(request, sku):
    model = Product.objects.get(sku=sku)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                data = form.cleaned_data
                review = Review(title= data['title'], content=data['content'], author=request.user.profile, product = model, rating=data['rating'])
                review.save()
                messages.success(request,'Review posted!')
                return redirect('product-details', sku)
            else:
                pass 
        else:
            messages.warning(request, 'You have to login to post a review!')
            return redirect('product-details', sku)  

    form = ReviewForm()
    reviews = Review.objects.filter(product=model.id).all().order_by('-review_date')

    return render(request, 'ecomm/product-details.html', {'form': form, 'reviews': reviews, 'object': model })


class OrderListView(ListView):
    model = Order
    paginate_by = 15
    # ordering = ['-order_date']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        query = Order.objects.filter(customer=self.request.user).order_by('-order_date')
        return query


class OrderDetailView(DetailView):
    model = Order

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.pk
        items = self.object.get_order_items
        context['items'] = items
        return context

    

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
    cartitem, created = CartItem.objects.get_or_create(cart = cart, product=product, price=product.unitprice)
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
