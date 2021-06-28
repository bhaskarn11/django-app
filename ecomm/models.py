from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from django.utils import timezone
# Create your models here.


class Review(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=120)
    author = models.ForeignKey(
        'account.Profile', on_delete=models.CASCADE, default=None)

    def __repr__(self):
        return f"Review: {self.id}, {self.title}"


class Product(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=500)
    price = models.FloatField(null=True)
    image = models.ImageField(
        default='products/default.jpg', upload_to='products')
    stock = models.PositiveIntegerField()
    is_in_stock = models.BooleanField(default=True)

    def __repr__(self):
        return f"Product: {self.id}, {self.title}"


class Order(models.Model):
    oid = models.UUIDField(default=uuid4().hex, unique=True)
    order_amount = models.FloatField()
    order_date = models.DateTimeField(default=timezone.now)
    shipping_address = models.TextField(max_length=300)
    billing_address = models.TextField(max_length=300)
    shipped = models.BooleanField(default=False)
    placed_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __repr__(self):
        return f"OrdeID: {self.oid} - {self.order_date}"
