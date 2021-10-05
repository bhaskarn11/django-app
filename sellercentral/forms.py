from sellercentral.models import Seller
from django import forms
from sellercentral.models import Inventory

# class SellerSignupForm(forms.ModelForm):
#     class Meta:
#         model = Seller
#         fields = ['diplay_name', 'email']

class InventoryForm(forms.ModelForm):

    class Meta:
        model = Inventory
        fields = ['product', 'stock', 'sku', 'offering_price']

    # product = forms.CharField(max)
    # seller = 
    # stock = 
    # sku 