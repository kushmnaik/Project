from django.contrib import admin

# Register your models here.
from .models import MenuItem
# from .models import MealItem
from .models import Customer
from .models import Restaurant
from .models import OrderItem
from .models import Order


admin.site.register(MenuItem)
# admin.site.register(MealItem)
admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(OrderItem)
admin.site.register(Order)