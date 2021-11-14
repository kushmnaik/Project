from django import forms
from .models import *
from django.core.exceptions import ValidationError



class AddItem(forms.ModelForm):
    
    class Meta:
        model = MenuItem
        exclude = ['restaurant']
        labels = {'name':'Item Name','price' : 'price' , 'image':'Image'}

# class RegisterRestaurent(forms. ModelForm):

class OrderDetail(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    status_choices = (('2','ready'),('3','delivered'))
    status = forms.ChoiceField(
        choices=status_choices,)

    class Meta:
        model = Order
        fields = ('status', 'delivery')
        required = ('status', 'delivery')

    def clean_delivery(self):
        delivery = self.cleaned_data.get('delivery')

        if delivery.user not in User.objects.all():
            raise ValidationError("not such delivery boy with given user name")
        else :
            user = delivery.user
            group=None
            if user.groups.exists():
                group = user.groups.all()[0].name
            if group != "delivery":
                raise ValidationError("not such delivery boy with given user name")
            
        return delivery



class AddDelivery(forms.Form):
    username = forms.CharField(max_length=200)
       
    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except:
            user=None
        
        if not user:
            raise ValidationError("not such delivery boy with given user name")
        else :
            user = User.objects.get(username=username)
            group=None
            if user.groups.exists():
                group = user.groups.all()[0].name
            if group != "delivery":
                raise ValidationError("not such delivery boy with given user name")
        return username


class deliveryOrderDetail(forms.ModelForm):

    status_choices = (('3','delivered'),)
    status = forms.ChoiceField(
        choices=status_choices)

    class Meta:
        model = Order
        fields = ['status']
        