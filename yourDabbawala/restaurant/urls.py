from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [

    path('home/',add_item , name='add_item'),
    path('delete/<int:id>/',delete_item, name='delete_item'),
    path('edit/<int:id>/',edit_item, name='edit_item'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    
    path('orders/', Orders, name='orders'),
    path('orderDetail/<int:id>/', orderDetail, name='orderdetail'),

    path('deliveryHome/',deliveryHome, name='deliveryHome'),
    path('delivery_order_detail/<int:id>/',delivery_order_detail,name='delivery_order_detail'),

    path('add_delivery_boy/',add_delivery_boy , name='add_delivery_boy'),
    path('delete_delivery/<int:id>', delete_delivery, name='delete_delivery'),

    path('about/', aboutUs, name='about'),
    path('contactus/', contactUs, name='contactUs'),
]