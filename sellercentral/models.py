from django.contrib.auth.models import User
from django.db import models
from ecomm.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=40, blank=True ,null=True, help_text='It will be fetch automatically from user profile')
    avatar = models.ImageField(upload_to='profile_pics', default='profile_pics/default.jpg')
    email = models.EmailField(null=True, max_length=100)

    class Meta:
        permissions = [('is_seller', 'Seller')]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def save(self, *args, **kwargs):
        self.display_name = self.user.get_full_name()
        return super().save(*args, **kwargs)

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True)
    stock = models.PositiveIntegerField(null=True)
    sku = models.CharField(null=True, max_length=30)
    offering_price = models.DecimalField(decimal_places=2,null=True, max_digits=20,help_text='put what price you wanna offer for this product')

# class SKU(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)

