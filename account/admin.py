from django.contrib import admin
from .models import Address, Profile
# Register your models here.

admin.site.register(Profile)
admin.site.register(Address)