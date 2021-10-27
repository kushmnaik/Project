from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
# Create your views here.
from .forms import *

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from restaurant.models import *
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/authentication/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html",
                  context={"password_reset_form": password_reset_form})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("restaurantInfo")
        return render(request=request, template_name="register.html", context={"register_form": form})
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('add_item')
            else:
                return render(request=request, template_name="login.html", context={"login_form": form})
        else:
            return render(request=request, template_name="login.html", context={"login_form": form})
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    return redirect("login")


# @login_required(login_url='/authentication/login/')
def get_info(request):
    # customer_info = CustomerInfo()
    if request.method == 'POST':
        customer_info = CustomerInfo(request.POST)
        if customer_info.is_valid():
            cust_info = Customer()
            cust_info.user = request.user
            cust_info.name = customer_info.cleaned_data['name']
            cust_info.address = customer_info.cleaned_data['address']
            cust_info.phone_no = customer_info.cleaned_data['phone_no']
            cust_info.save()
            return redirect('add_item')
    else:
        customer_info = CustomerInfo()

    return render(request, 'customerInfo.html', context={"customer_info": customer_info})


def restaurant_info(request):
    # customer_info = CustomerInfo()
    if request.method == 'POST':
        res_info = RestaurantInfo(request.POST, request.FILES)
        print(2)
        if res_info.is_valid():
            print(1)
            restaurant_info = Restaurant()
            restaurant_info.user = request.user
            restaurant_info.name = res_info.cleaned_data['name']
            restaurant_info.address = res_info.cleaned_data['address']
            restaurant_info.phone_no = res_info.cleaned_data['phone_no']
            restaurant_info.bio = res_info.cleaned_data['bio']
            restaurant_info.city = res_info.cleaned_data['city']
            restaurant_info.open_time = res_info.cleaned_data['open_time']
            restaurant_info.close_time = res_info.cleaned_data['close_time']
            restaurant_info.active = True
            restaurant_info.meal_price = 100
            restaurant_info.image = res_info.cleaned_data['image']
            restaurant_info.save()
            return redirect('add_item')
    else:
        print(3)
        res_info = RestaurantInfo()

    return render(request, 'restaurant_info.html', context={"form": res_info})



    #  user = models.OneToOneField(User,to_field="username",db_column="user", on_delete=models.CASCADE, primary_key=True)
    # name = models.CharField(max_length=200, null=True)
    # address = models.CharField(max_length=500, null=True)
    # phone_no = models.CharField(max_length=10, null=True)
    # bio = models.TextField(blank=True, null=True)
    # city = models.CharField(max_length=200, default="")
    # image = models.ImageField(upload_to='images', null=True)
    # open_time = models.TimeField(null=True)
    # close_time = models.TimeField(null=True)
    # active = models.BooleanField(null=True)
    # meal_price = models.IntegerField()