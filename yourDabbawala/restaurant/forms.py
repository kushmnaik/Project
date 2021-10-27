from django import forms
from .models import *


class AddItem(forms.ModelForm):
    
    class Meta:
        model = MenuItem
        exclude = ['restaurant']
        labels = {'itemName':'Item Name','itemPrice' : 'Price' , 'img':'Image'}

# class RegisterRestaurent(forms. ModelForm):