import json
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from ecomm.models import Cart, CartItem, Product, Order, Review, PRODUCT_CATEGORY
from django.db.models import Q
from django.contrib import messages
from ecomm.forms import ReviewForm
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def index(request):
    messages.info(request,'This site is currently in development')
    return redirect('search-result')


class SearchView(ListView):
    model = Product
    # def paginate_query(self, paginator, page_number):
    #     try:
    #         return paginator.get_page(page_number)
    #     except PageNotAnInteger:
    #         return paginator.get_page(1)
    #     except EmptyPage:
    #         return paginator.get_page(page_number)

    paginate_by = 8
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query') if not (self.request.GET.get('query') == '') else None
        category = self.request.GET.get('category')
        sort_by = self.request.GET.get('sort_by')
        context['query'] = query if query else ""
        context['category'] = category if category else ""
        context['product_category'] = [i[0] for i in PRODUCT_CATEGORY]
        if category and query and sort_by:
            products = Product.objects.filter(
                Q(description__icontains=query) |
                Q(title__icontains=query) | 
                Q(category__icontains=category)
            ).filter(stock__gt = 0).order_by(sort_by)
            # paginator = Paginator(products, 8)
            context['products'] = self.paginate_queryset(products,self.paginate_by)[1]
        elif query and sort_by:
            products = Product.objects.filter(
                Q(description__icontains=query) |
                Q(title__icontains=query)
            ).filter(stock__gt = 0).order_by(sort_by)
            context['products'] =  self.paginate_queryset(products,self.paginate_by)[1]
        elif category:
            products = Product.objects.filter(
                Q(description__icontains=category) |
                Q(category__icontains=category)
            ).filter(stock__gt = 0).order_by('title')
            context['products'] =  self.paginate_queryset(products,self.paginate_by)[1]
        else:
            # paginator = Paginator(Product.objects.all(), 8)
            products = Product.objects.filter(stock__gt = 0).order_by('title')
            context['products'] = self.paginate_queryset(products,self.paginate_by)[1]
        
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
    reviews = Review.objects.filter(product=model.id).all().order_by('-review_date')[:3]
    cart = Cart.objects.get(user=request.user) if not request.user.is_anonymous else None
    return render(request, 'ecomm/product-details.html', {'form': form, 'reviews': reviews, 'object': model, 'cart': cart })



class ReviewListView(ListView):
    model = Review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(sku=self.kwargs['sku'])
        context['product'] = product
        context['reviews'] = Review.objects.filter(product=product).all().order_by('-review_date')
        return context



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
    slug_field = 'order_id'
    slug_url_kwarg = 'order_id'
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # order = self.model.get(order_id=kwargs.get('order_id'))
        return super().dispatch(request, *args, **kwargs)

    # def get

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
    cartitem, created = CartItem.objects.get_or_create(cart = cart, product=product, price=product.get_unitprice)
    if action == 'add':
        if cartitem.product.stock > cartitem.quantity:
            cartitem.quantity = cartitem.quantity + 1
            cartitem.save()
        else:
            return JsonResponse({"added": False}, safe=False)
    elif action == 'remove':
        if cartitem.quantity == 1:
            cartitem.delete()
        else:
            cartitem.quantity = cartitem.quantity - 1
            cartitem.save()

    return JsonResponse({"added": True}, safe=False)
