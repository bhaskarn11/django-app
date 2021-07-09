from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.views.generic import View
from ecomm.models import Cart, OrderItem, Product, Order
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from checkout.forms import CheckoutForm
import os
# razorpay API
import razorpay
client = razorpay.Client(auth=(os.getenv('RAZORPAY_API_KEY'), os.getenv('RAZORPAY_API_KEY_SECRET')))
# Create your views here.

class CheckoutView(View):

    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        profile = self.request.user.profile
        form = CheckoutForm(initial= profile.address.get_address)
        if self.request.GET.get('productId') and self.request.GET.get('action') == 'buynow':
            product = Product.objects.get(pk=self.request.GET.get('productId'))
            context = {
                'product': product,
                'form': form
            }
        elif self.request.GET.get('action') == 'cart' and self.request.GET.get('cartId'):
            data = self.request.POST
            cartitems = Cart.objects.get(user=self.request.user.id).get_cartitems
            context = {
                'cartitems': cartitems,
                'form' : form,
                'cartId': data.get('cartId')
            }

        return render(self.request, 'checkout/order-checkout.html', context)


    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST)
        if form.is_valid():
            data = form.cleaned_data
            address = f"{data['address']},\n{data['city']} ,{data['state']}-{data['pincode']},\n{data['country']}"
            if self.request.POST.get('productId'):
                product = Product.objects.get(id=self.request.POST.get('productId'))
                order = Order(customer = self.request.user, order_amount = product.unitprice,
                                payment_method=data['payment_method'], shipping_address = address, billing_address=address)
            else:
                cart = Cart.objects.get(user=self.request.user.id)
                order = Order(customer = self.request.user, order_amount = cart.get_cart_total,
                                payment_method=data['payment_method'], shipping_address = address, billing_address=address)
                order.save()
                for item in cart.get_cartitems:
                    orderitem = OrderItem(product=item.product, quantity=item.quantity, price=item.price, order=order)
                    orderitem.save()
            
            order_amount = int(order.order_amount * 100)
            order_receipt = order.order_id
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

@login_required
def payment(request, order_id):
    if request.method == 'GET':
        order = Order.objects.get(pk=order_id)
        context = {
            'amount': int(order.order_amount * 100),
            'order_id': order.transaction_id,
            'order': order
        }
        return render(request, 'checkout/checkout-payment.html', context)
    else:
        return HttpResponseNotAllowed

@csrf_exempt
def payment_success(request, order_id):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        cart.delete()
        order = Order.objects.get(pk=order_id)
        params_dict = {
            'razorpay_order_id': order.transaction_id ,
            'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
            'razorpay_signature': request.POST.get('razorpay_signature')
        }
        err = client.utility.verify_payment_signature(params_dict)
        if not err:
            Order.objects.filter(pk=order_id).update(payment_id=request.POST.get('razorpay_payment_id'), status='Ordered')
            return render(request, 'checkout/order-success.html')
        else:
            return render(request, 'checkout/payment-error.html', {"error": True}, status=500)

    else:
        return HttpResponseNotAllowed

