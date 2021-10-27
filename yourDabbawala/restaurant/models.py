from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=500, null=True)
    phone_no = models.CharField(max_length=10, null=True)
    # bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name +"("+str(self.user)+")"


class Restaurant(models.Model):
    user = models.OneToOneField(User,to_field="username",db_column="user", on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=500, null=True)
    phone_no = models.CharField(max_length=10, null=True)
    bio = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=200, default="")
    image = models.ImageField(upload_to='images', null=True)
    open_time = models.TimeField(null=True)
    close_time = models.TimeField(null=True)
    active = models.BooleanField(null=True)
    meal_price = models.IntegerField()

    def __str__(self):
        return self.name+"("+str(self.user)+")"


class MenuItem(models.Model):
    itemName = models.CharField(max_length=200)
    itemPrice = models.IntegerField()
    discription = models.CharField(max_length=200)
    category = models.CharField(max_length=200, default="")
    restaurant = models.ForeignKey(Restaurant,to_field="user",db_column="restaurant", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.itemName)+"("+str(self.restaurant)+")"


# class MealItem(models.Model):
#     itemName = models.CharField(max_length=200)
#     discription = models.CharField(max_length=200)
#     day = models.CharField(max_length=200)
#     restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
#
#     def __str__(self):
#         return self.itemName +"("+str(self.id)+")"


class OrderItem(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True)
    # meal_item = models.ForeignKey(MealItem, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.menu_item.itemName

    @property
    def amount(self):
        if MenuItem is not None:
            total = self.menu_item.itemPrice * self.quantity

        return total


PAYMENT_CHOICES = (
    ('cod', 'Cash on delivery'),
    ('card', 'credit/debit cards'),
)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(OrderItem)
    order_date = models.DateTimeField(auto_now_add=True, null=True)
    delivery_address = models.TextField(null=True)
    payment_mode = models.CharField(choices=PAYMENT_CHOICES, max_length=30, null=True)
    complete = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.customer.name

    @property
    def total_cart_amount(self):
        items = self.items.all()
        total = sum([item.amount for item in items])
        return total

    @property
    def total_cart_items(self):
        items = self.items.all()
        total = sum([item.quantity for item in items])
        return total


