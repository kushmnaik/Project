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
    phone_no = forms.CharField(max_length=10)

    # def clean(self):
    #     number = self.cleaned_data['phone_no']
    #     if re.match('^[\d]{10}$', number):
    #         raise ValidationError("Passwords did not match")


class RestaurantInfo(forms.ModelForm):
    class Meta :
        model = Restaurant
        exclude = ['user','active','meal_price']



    # name = forms.CharField(max_length=50)
    # address = forms.CharField(max_length=200, widget=forms.Textarea)
    # phone_no = forms.CharField(max_length=10)
    # bio = forms.CharField(max_length = 200, widget=forms.Textarea)
    # city = forms.CharField(max_length=50)
    # open_time = forms.TimeField()
    # close_time = forms.TimeField()
    # image = forms.ImageField()

    # def clean(self):
    #     number = self.cleaned_data['phone_no']
    #     if re.match('^[\d]{10}$', number):
    #         raise ValidationError("Passwords did not match")