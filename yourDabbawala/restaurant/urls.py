from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('home/',add_item , name='add_item'),
    path('delete/<int:id>/',delete_item, name='delete_item'),
    path('edit/<int:id>/',edit_item, name='edit_item'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('contactus/', contactUs, name='contactUs'),
     path('about/', aboutUs, name='about')
]