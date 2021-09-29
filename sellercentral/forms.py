from sellercentral.models import Seller
from django import forms

class SellerSignupForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['diplay_name', 'email']
