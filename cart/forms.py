from django import forms


class card_form(forms.Form):
    pro_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'product id'}))
    pro_seller = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'pro_seller'}))

