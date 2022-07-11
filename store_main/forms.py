from email.policy import default
from .globals import CATEGORIES
from django import forms


class SearchItemForm(forms.Form):
    item_name = forms.CharField(max_length=255)
    category = forms.MultipleChoiceField(choices=CATEGORIES, widget=forms.CheckboxSelectMultiple, required=False)
    price_min = forms.IntegerField(label='Min price', max_value=1000, required=False)
    price_max = forms.IntegerField(label='Max price', max_value=10000, required=False)

