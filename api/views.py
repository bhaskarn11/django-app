from django.shortcuts import render
from django.http import JsonResponse
from ecomm.models import Review, Cart
# Create your views here.

def post_review(request):
    if request.method == 'POST':
        data = request.POST
        try:
            review = Review(data, author=request.user)
            review.save()
        except Exception as e:
            return JsonResponse({'error': e}, safe=False)
    return JsonResponse({"posted": True}, safe=False)
        
def get_total_cart_quantity(request):
    if request.method == 'GET':
        try:
            cart = Cart.objects.get(user = request.user)
            return JsonResponse({"data": cart.get_cart_quantity}, safe=False)
        except Exception as e:
            return JsonResponse({'error': e}, safe=False)
