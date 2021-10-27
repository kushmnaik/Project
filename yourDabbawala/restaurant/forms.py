from django import forms
from .models import *


class AddItem(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['itemName','itemPrice','discription','category','restaurant']
        label = {'itemName':'Item Name','itemPrice' : 'Price' }
