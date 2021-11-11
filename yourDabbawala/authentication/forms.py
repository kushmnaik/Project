from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import re
from django.core.exceptions import ValidationError

from restaurant.models import *
# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomerInfo(forms.Form):
    name = forms.CharField(max_length=200)
    address = forms.CharField(max_length=500)
    phone = forms.CharField(max_length=10)

    def clean_phone_no(self):
        number = self.cleaned_data['phone']
        if len(number) != 10:
            raise ValidationError("Not a valid Number")
        for i in number:
            if i not in ['1','2','3','4','5','6','7','8','9','0']:
                raise ValidationError("Not a valid Number")
        return number


class RestaurantInfo(forms.ModelForm):
    class Meta :
        model = Restaurant
        exclude = ['user','active','meal_price']
    def clean_phone_no(self):
        number = self.cleaned_data['phone']
        if len(number) != 10:
            raise ValidationError("Not a valid Number")
        for i in number:
            if i not in ['1','2','3','4','5','6','7','8','9','0']:
                raise ValidationError("Not a valid Number")
        return number