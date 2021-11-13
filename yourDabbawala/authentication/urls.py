from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('login/',login ),
    path("register/", register_request, name="register"),
    path("login/", login_request, name="login"),
    path("logout/", logout_request, name= "logout"),
    path("customerInfo/",get_info, name='customerInfo'),
    path("restaurantInfo/",restaurant_info, name='restaurantInfo'),
    path("deliveryInfo/",get_info_delivery_boy, name='deliveryInfo'),
    path("email_sent/",email_sent, name='email_sent'),


    path('password_reset/done/',
    auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
         name='password_reset_complete'),
    path("password_reset/", password_reset_request, name="password_reset")
]