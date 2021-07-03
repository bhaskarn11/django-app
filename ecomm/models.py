from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
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
        'account.Profile', on_delete=models.CASCADE, default=None, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.IntegerField(choices=RATING_CHOICE, default=None, blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return f"Review: {self.id}, {self.title}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    ordered = models.BooleanField(default=False)

    @property
    def get_cart_total(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.get_total for item in cartitems ])
        return total

    @property
    def get_cart_quantity(self):
        cartitems = self.cartitem_set.all()
        return sum(item.quantity for item in cartitems)
    

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=30)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    @property
    def get_total(self):
        total = self.price * self.quantity
        return total
    

class Order(models.Model):

    ORDER_STATUS = [
        ('Ordered', 'Ordered'),
        ('Shipped', 'Shipped'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled')
    ]

    PAYMENT_OPTION = [
        ('Credit Card/Debit Card', 'Credit Card/Debit Card'),
        ('COD', 'COD'),
        ('Wallet', 'Wallet'),
        ('UPI', 'UPI'),
        ('Net Banking','Net Banking')
    ]

    order_id = models.UUIDField(default=uuid4().hex, unique=True, primary_key=True)
    order_amount = models.FloatField(default=None, null=True)
    order_date = models.DateTimeField(auto_now_add=True) # adds datetime automaticaly wen object is created
    shipping_address = models.TextField(max_length=150)
    billing_address = models.TextField(max_length=150)
    status = models.CharField(choices=ORDER_STATUS, default='Ordered', max_length=12)
    transaction_id = models.CharField(max_length=50, null=True)
    payment_method = models.CharField(choices=PAYMENT_OPTION, max_length=30, null= True)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    items = models.ForeignKey(Cart, on_delete=models.DO_NOTHING, null=True)

    def __repr__(self):
        return f"OrdeID: {self.order_id} - {self.order_date}"
