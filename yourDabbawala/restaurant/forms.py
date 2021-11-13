from django import forms
from .models import *

status_choices = (('2','ready'),('3','delivered'))

class AddItem(forms.ModelForm):
    
    class Meta:
        model = MenuItem
        exclude = ['restaurant']
        labels = {'name':'Item Name','price' : 'price' , 'image':'Image'}

# class RegisterRestaurent(forms. ModelForm):

class OrderDetail(forms.ModelForm):
    status = forms.ChoiceField(
        choices=status_choices,)

    class Meta:
        model = Order
        fields = ['status']
        
       