from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=500, null=True)
    phone = models.CharField(max_length=10, null=True)
    # bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name +"("+str(self.user)+")"


class Restaurant(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=500, null=True)
    phone = models.CharField(max_length=10, null=True)
    bio = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=200, default="")
    image = models.ImageField(upload_to='images/')
    open_time = models.TimeField(null=True)
    close_time = models.TimeField(null=True)
    active = models.BooleanField(null=True)
    meal_price = models.IntegerField()

    def __str__(self):
        return self.name+"("+str(self.user)+")"


class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    desc = models.TextField(blank=True)
    image = models.ImageField(upload_to='images', blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + "-" + self.restaurant.name


class OrderItem(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.quantity) + self.menu_item.name

    @property
    def amount(self):
        total = self.menu_item.price * self.quantity
        return total

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.name + self.restaurant.name

    @property
    def total_cart_items(self):
        items = self.items.all()
        total = sum([item.quantity for item in items])
        return total

    @property
    def total_cart_amount(self):
        items = self.items.all()
        total = sum([item.amount for item in items])
        return total
