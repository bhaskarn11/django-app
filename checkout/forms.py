from django import forms
from django.forms.widgets import RadioSelect
from account.state_list import STATES

class CheckoutForm(forms.Form):
    COUNTRIES = [
        ('IN', 'India')
    ]

    PAYMENT_OPTION = [
        ('Credit Card/Debit Card', 'Credit Card/Debit Card'),
        ('COD', 'COD (Cash on Delivery'),
        ('Wallet', 'Wallet'),
        ('UPI', 'UPI'),
        ('Net Banking','Net Banking')
    ]

    address = forms.CharField(max_length=100)
    pincode = forms.CharField(max_length=10)
    city = forms.CharField(max_length=20)
    state = forms.ChoiceField(choices=STATES)
    country = forms.ChoiceField(choices=COUNTRIES)
    payment_method = forms.ChoiceField(choices=PAYMENT_OPTION, widget=RadioSelect, initial='Credit Card/Debit Card')
    shipping_address_is_billing_address = forms.BooleanField(initial=True)

