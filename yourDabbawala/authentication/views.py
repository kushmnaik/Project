from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
# Create your views here.
from .forms import *
from django.contrib.auth.models import Group
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
from restaurant.decorators import *
from django.conf import settings

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
                        send_mail(subject, email,settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
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
            subject = "Welcome to our family :)"
            email_template_name = "password/email_sent.txt"
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
                send_mail(subject, email,settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            # return redirect("/authentication/password_reset/done/")
            return redirect("email_sent")
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
                group = 'customer'
                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name
                if 'customer' ==  group :
                    return redirect('customer:home')
                elif 'restaurant' ==  group:
                    return redirect('add_item')
                elif 'delivery' == group:
                    return redirect('deliveryHome')
                    
            else:
                return render(request=request, template_name="login.html", context={"login_form": form})
        else:
            return render(request=request, template_name="login.html", context={"login_form": form})
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})

def email_sent(request):
    return render(request, 'email_sent.html')


def logout_request(request):
    logout(request)
    return redirect("login")


@is_authenticated
def get_info(request):
    # customer_info = CustomerInfo()
    if request.method == 'POST':
        customer_info = CustomerInfo(request.POST)
        if customer_info.is_valid():
            cust_info = Customer()
            cust_info.user = request.user
            cust_info.name = customer_info.cleaned_data['name']
            cust_info.address = customer_info.cleaned_data['address']
            cust_info.phone = customer_info.cleaned_data['phone']
            group = Group.objects.get(name='customer')
            request.user.groups.add(group)
            cust_info.save()
            return redirect('home')
    else:
        customer_info = CustomerInfo()

    return render(request, 'customerInfo.html', context={"customer_info": customer_info})


@is_authenticated
def get_info_delivery_boy(request):
   
    if request.method == 'POST':
        delivery_boy = DeliveryInfo(request.POST)
        if delivery_boy.is_valid():
            delivery_info = Delivery()
            delivery_info.user = request.user
            delivery_info.name = delivery_boy.cleaned_data['name']
            delivery_info.address = delivery_boy.cleaned_data['address']
            delivery_info.phone = delivery_boy.cleaned_data['phone']
            group = Group.objects.get(name='delivery')
            request.user.groups.add(group)
            delivery_info.save()
            return redirect('deliveryHome')
    else:
        delivery_boy = DeliveryInfo()

    return render(request, 'deliveryinfo.html', context={"form": delivery_boy})

@is_authenticated
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
            restaurant_info.phone = res_info.cleaned_data['phone']
            restaurant_info.bio = res_info.cleaned_data['bio']
            restaurant_info.city = res_info.cleaned_data['city']
            restaurant_info.open_time = res_info.cleaned_data['open_time']
            restaurant_info.close_time = res_info.cleaned_data['close_time']
            restaurant_info.active = True
            restaurant_info.meal_price = 100
            restaurant_info.image = res_info.cleaned_data['image']
            print(res_info.cleaned_data['image'])
            restaurant_info.save()
            group = Group.objects.get(name='restaurant')
            request.user.groups.add(group)
            return redirect('add_item')
    else:
        print(3)
        res_info = RestaurantInfo()

    return render(request, 'restaurant_info.html', context={"form": res_info})

