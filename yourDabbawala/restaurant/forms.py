from django import forms
from .models import *


class AddItem(forms.ModelForm):
    
    class Meta:
        model = MenuItem
        exclude = ['restaurant']
        labels = {'name':'Item Name','price' : 'price' , 'image':'Image'}

# class RegisterRestaurent(forms. ModelForm):