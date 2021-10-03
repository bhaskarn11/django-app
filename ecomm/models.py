from django.db import models
from django.contrib.auth.models import User
from ecomm.utils import order_id_generator, sku_generator, sku_barcode_gen
from django.core.files import File
from django.db.models import Avg
# Create your models here.
PRODUCT_CATEGORY = [
    ('Books', 'Books'),
    ('electronics', 'Electronics'),
    ('Other', 'Other'),
    ("men's clothing", "men's clothing"),
    ("women's clothing", "women's clothing"),
    ("jewelery", "jewelery")
]

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    category = models.CharField(max_length=30, choices=PRODUCT_CATEGORY,default=None, null=True)
    unitprice = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    discount_unitprice = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
    image = models.ImageField(
        default='products/default.jpg', upload_to='products')
    stock = models.PositiveIntegerField()
    sku = models.CharField(max_length=20, blank=True, default=sku_generator())
    dimensions = models.CharField(max_length=15, help_text="e.g - LxBxH", blank=True)
    weight = models.FloatField(help_text="in Kg.", blank=True, null=True)
    sku_barcode = models.ImageField(upload_to='products/barcodes', blank = True)

    def save(self, *args, **kwargs):
        
        buffer = sku_barcode_gen(self.sku)
        self.sku_barcode.save(f"{self.sku}.png", File(buffer), save=False)
        return super().save(*args, **kwargs)
    
    def __repr__(self):
        return f"Product: {self.id}, {self.title}"

    @property
    def get_all_reviews(self):
        return Review.objects.filter(product=self).all()

    @property
    def get_average_rating(self):
        reviews = self.get_all_reviews.order_by('-review_date')
        avg_rating = reviews.aggregate(Avg('rating')).get('rating__avg') # calculates avarage rating
        return round(avg_rating,1) if avg_rating else None

    @property
    def total_review_count(self):
        return self.get_all_reviews.count()

    @property
    def get_review_stats(self):
        stats = []
        for i in range(1,6):
            stats.append(int(self.get_all_reviews.filter(rating=i).count()/self.total_review_count * 100))
        
        return stats


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
    @property
    def get_cartitems(self):
        cartitems = self.cartitem_set.all()
        return cartitems
    

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
        ('Canceled', 'Canceled'),
        ('Pending', 'Pending')
    ]

    PAYMENT_OPTION = [
        ('Credit Card/Debit Card', 'Credit Card/Debit Card'),
        ('COD', 'COD'),
        ('Wallet', 'Wallet'),
        ('UPI', 'UPI'),
        ('Net Banking','Net Banking')
    ]

    order_id = models.CharField(unique=True, primary_key=True, max_length=25, default=order_id_generator())
    order_amount = models.DecimalField(default=None, null=True, decimal_places=2, max_digits=50)
    order_date = models.DateTimeField(auto_now_add=True) # adds datetime automaticaly wen object is created
    shipping_address = models.TextField(max_length=150)
    billing_address = models.TextField(max_length=150)
    status = models.CharField(choices=ORDER_STATUS, default='Pending', max_length=12)
    transaction_id = models.CharField(max_length=50, null=True)
    payment_id = models.CharField(max_length=50, null=True)
    payment_method = models.CharField(choices=PAYMENT_OPTION, max_length=30, null= True)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    
    @property
    def get_order_amount(self):
        items = self.get_order_items
        order_amount = sum([item.get_total for item in items])
        return order_amount
    @property
    def get_order_items(self):
        items = self.orderitem_set.all()
        return items

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __repr__(self):
        return f"OrdeID: {self.order_id} - {self.order_date}"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=30)
    
    @property
    def get_total(self):
        total = self.price * self.quantity
        return total
    
