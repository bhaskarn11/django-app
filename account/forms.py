from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Address, Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length= 40)
    last_name = forms.CharField(max_length = 40)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'mobileNumber',  'image',]


class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'pincode', 'city', 'state', 'country']
