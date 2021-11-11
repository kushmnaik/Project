from django.shortcuts import render

# Create your views here.
import datetime

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, ListView, DetailView
from restaurant.models import *

# Create your views here.
class Home(ListView):
    model = Restaurant
    template_name = "home.html"
    paginate_by = 10

class RestaurantDetail(DetailView):
    model = Restaurant
    template_name = "restaurantdetail.html"

class Cart(View):
    def get(self, request, **kwargs):
        try:
            order_id = request.session.get('order_id')
            order = Order.objects.get(id=order_id)
            context = {'order':order}
            return render(self.request, "cart.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order!")
            return redirect('customer:home')

def add_to_cart(request, pk):
    menu_item = get_object_or_404(MenuItem, id=pk)
    order_id = request.session.get('order_id', None)
    if order_id:
        order = Order.objects.get(id=order_id)
        if menu_item.restaurant == order.restaurant:
            if order.items.filter(menu_item__id=pk).exists():
                order_item = order.items.filter(menu_item__id=pk)[0]
                order_item.quantity += 1
                order_item.save()
            else:
                new_order_item = OrderItem.objects.create(menu_item=menu_item)
                order.items.add(new_order_item)
        else:
            if order.items.exists():
                order.items.all().delete()
            new_order_item = OrderItem.objects.create(menu_item=menu_item)
            order.items.add(new_order_item)
            order.restaurant = menu_item.restaurant
            order.save()
    else:
        customer = get_object_or_404(Customer, user=request.user)
        order = Order.objects.create(customer=customer, restaurant=menu_item.restaurant)
        request.session['order_id'] = order.id
        new_order_item = OrderItem.objects.create(menu_item=menu_item)
        order.items.add(new_order_item)
    return redirect('customer:restaurantdetail', pk=menu_item.restaurant.id)

def delete_from_cart(request, pk):
    order_item = get_object_or_404(OrderItem, id=pk)
    order_id = request.session.get('order_id')
    order = Order.objects.get(id=order_id)
    order.items.remove(order_item)
    order_item.delete()
    return redirect('customer:cart')

def increase_qty(request, pk):
    order_item = get_object_or_404(OrderItem, id=pk)
    if order_item.quantity < 10:
        order_item.quantity += 1
    order_item.save()
    return redirect('customer:cart')

def decrease_qty(request, pk):
    order_item = get_object_or_404(OrderItem, id=pk)
    if order_item.quantity > 1:
        order_item.quantity -= 1
    else:
        delete_from_cart(request, pk)
    order_item.save()
    return redirect('customer:cart')

def checkout(request):
    order_id = request.session.get('order_id')
    order = Order.objects.get(id=order_id)
    order.order_date = datetime.datetime.now()
    order.save()
    order.delete()
    del request.session['order_id']
    return redirect('customer:home')

class CustomerProfile(DetailView):
    model = Customer
    template_name = "customerprofile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect('customer:home')
        return super().dispatch(request, *args, **kwargs)

class CustomerOrderDetail(DetailView):
    model = Order
    template_name = "customerorderdetail.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.customer:
                return redirect('cutomer:customerprofile', request.user.customer.id)
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

class About(TemplateView):
    template_name = "about.html"

class Contact(TemplateView):
    template_name = "contactus.html"