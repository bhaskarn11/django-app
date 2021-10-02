from django.core.mail import send_mail
from django.template.loader import render_to_string
import nanoid
import barcode
from barcode.writer import ImageWriter
from io import BytesIO

def order_confirmation_mail(order, user, **kwarg):
    send_mail(
        subject=f'Your Order #{order.order_id} placed successfully!',
        message='Order placed successfully!',
        from_email='Order Confirmation <develeper.bhaskarn@gmail.com>',
        recipient_list = [user.email],
        html_message = render_to_string("ecomm/order_conf_email.html", { 'order': order.order_id, 'user': user, 'items': order.get_order_items })
    )

def sku_generator():
    nano = nanoid.generate('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', 10)
    return f"SKU{nano}"
    
def order_id_generator():
    return f"ODR-{nanoid.generate('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', 20)}"

def sku_barcode_gen(code):
    code128 = barcode.get('code128', code, writer=ImageWriter())
    buffer = BytesIO()
    code128.write(buffer)
    return buffer

# def search_filter(prod,**kwargs):
#     query = kwargs.get('query')
#     category = kwargs.get('category')
#     if category:
#         product = prod.objects.filter(
#             Q(description__icontains=query) |
#             Q(title__icontains=query) & 
#             Q(category__icontains=category)
#         )
#         return product
#     else:
#         product = prod.objects.filter(
#             Q(description__icontains=query) |
#             Q(title__icontains=query)
#         )
#         return product
