from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=40, null=True)
    avatar = models.ImageField(upload_to='profile_pics', default='profile_pics/default.jpg')
    email = models.EmailField(null=True, max_length=100)

    class Meta:
        permissions = [('is_seller', 'Seller')]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display_name = self.user.get_full_name()


