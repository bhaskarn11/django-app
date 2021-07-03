from django import forms

class ReviewForm(forms.Form):
    choice = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]
    title = forms.CharField(validators=[forms.ValidationError])
    content = forms.CharField(widget=forms.Textarea({'rows': 3}), label='Review')
    rating = forms.ChoiceField(choices=choice)


