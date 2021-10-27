from django import forms
from .models import *


class AddItem(forms.ModelForm):
    
    class Meta:
        model = MenuItem
        fields = ['itemName','itemPrice','discription','category']
        labels = {'itemName':'Item Name','itemPrice' : 'Price' }
       
# class RegisterRestaurent(forms. ModelForm):