from ecomm.models import Review
from django import forms
from account.models import Profile

class CreateReviewForm(forms.ModelForm):
    # author = forms.ChoiceField()
    # product = forms.ChoiceField()
    # def __init__(self, *args, **kwargs):
    #     self.author = 

    class Meta:
        model = Review
        fields = ['title', 'content', 'rating']
        excludes = ['author', 'product']



