from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from django.db.models.deletion import SET_NULL
from django.utils import timezone
# Create your models here.
PRODUCT_CATEGORY = [
    ('Books', 'Books'),
    ('Electronics', 'Electronics'),
    ('Clothing', 'Clothing'),
    ('Other', 'Other')
]

class Product(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=500)
    category = models.CharField(max_length=30, choices=PRODUCT_CATEGORY,default=None, null=True)
    price = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    discount_price = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
    image = models.ImageField(
        default='products/default.jpg', upload_to='products')
    stock = models.PositiveIntegerField()

    def __repr__(self):
        return f"Product: {self.id}, {self.title}"



class Review(models.Model):

    RATING_CHOICE = [
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5)
    ]

    title = models.CharField(max_length=50)
    content = models.CharField(max_length=120)
    author = models.ForeignKey(
        'account.Profile', on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.IntegerField(choices=RATING_CHOICE, default=None, blank=True, null=True)
    # review_date = models.DateTimeField(auto_now_add=True)
    def __repr__(self):
        return f"Review: {self.id}, {self.title}"


class Order(models.Model):
    ORDER_STATUS = [
        ('Ordered', 'Ordered'),
        ('Shipped', 'Shipped'),
        ('Completed', 'Completed')
    ]

    order_id = models.UUIDField(default=uuid4().hex, unique=True)
    order_amount = models.FloatField(default=None, null=True)
    order_date = models.DateTimeField(auto_now_add=True) # adds datetime automaticaly wen object is created
    shipping_address = models.TextField(max_length=200)
    billing_address = models.TextField(max_length=200)
    status = models.CharField(choices=ORDER_STATUS, default='Ordered', max_length=12)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    def __repr__(self):
        return f"OrdeID: {self.oid} - {self.order_date}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
