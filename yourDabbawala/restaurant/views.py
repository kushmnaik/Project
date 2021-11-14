from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.http import  HttpResponseRedirect
from authentication.forms import *
from .decorators import *
from django.db.models import Q
from django.views.generic import View, TemplateView, ListView, DetailView

@is_authenticated
@allowed_users(['restaurant'])
def add_item(request):
    restaurant_name = Restaurant.objects.get(user = request.user)
    
    if request.method == 'POST':
        form = AddItem(request.POST, request.FILES)
        if form.is_valid():
            item = MenuItem()
            item.name = form.cleaned_data['name']
            item.price = form.cleaned_data['price']
            item.desc = form.cleaned_data['desc']
            item.image = form.cleaned_data['image']
            item.restaurant = restaurant_name
            item.save()
            return redirect('add_item')
        else :
            messages.success(request, 'error while saving try again!!')
            return render(request, 'restaurant_home.html', {'form': form, 'restaurant':restaurant_name})
    else :
        print(request.user)
        restaurant = MenuItem(restaurant = restaurant_name)
        form = AddItem(instance=restaurant)
    items = MenuItem.objects.filter(restaurant=restaurant_name)
   
    return render(request, 'restaurant_home.html', {'form': form, 'items':items, 'restaurant':restaurant_name})


@is_authenticated
@allowed_users(['restaurant'])
@is_owner
def delete_item(request,id):
    if request.method == "POST":
        item = MenuItem.objects.get(pk=id)
        item.delete()
        return redirect('add_item')


@is_authenticated
@allowed_users(['restaurant'])
@is_owner
def edit_item(request,id):
    restaurant_name = Restaurant.objects.get(user = request.user)
    if request.method=='POST':
        item = MenuItem.objects.get(pk=id)
        form = AddItem(request.POST,request.FILES,instance=item)
        if form.is_valid():
            item.name = form.cleaned_data['name']
            item.price = form.cleaned_data['price']
            item.desc = form.cleaned_data['desc']
            item.image = form.cleaned_data['image']
            item.restaurant = restaurant_name
            # item.restaurant = restaurant_name
            item.save()
            return redirect('add_item')
    else :
        item = MenuItem.objects.get(pk=id)
        form = AddItem(instance=item)
    return render(request, 'edit_item.html', {'form' : form, 'item':item})


@is_authenticated
@allowed_users(['restaurant'])
def edit_profile(request):
    if request.method == 'POST':
        res_info = Restaurant.objects.get(user=request.user)
        restaurant_info = RestaurantInfo(request.POST, request.FILES, instance=res_info)
        if restaurant_info.is_valid():
            # res_info = Restaurant()
            # res_info.user = request.user
            res_info.name = restaurant_info.cleaned_data['name']
            res_info.address = restaurant_info.cleaned_data['address']
            res_info.phone = restaurant_info.cleaned_data['phone']
            res_info.bio = restaurant_info.cleaned_data['bio']
            res_info.city = restaurant_info.cleaned_data['city']
            res_info.open_time = restaurant_info.cleaned_data['open_time']
            res_info.close_time = restaurant_info.cleaned_data['close_time']
            res_info.active = True
            res_info.meal_price = 100
            res_info.image = restaurant_info.cleaned_data['image']
            res_info.save()
            return redirect('add_item')
    else:
        res_info = Restaurant.objects.get(user=request.user)
        res_info = RestaurantInfo( instance=res_info)

    return render(request, 'restaurant_info.html', context={"form": res_info})
    
@is_authenticated
@allowed_users(['restaurant'])    
def Orders(request):
    orders =  Order.objects.filter(Q(restaurant=request.user.restaurant.id)).filter( Q(status='1')|Q(status='2')|Q(status='3')).order_by('order_date')

    return render(request,'orders.html', context={'orders':orders})


@is_authenticated
@allowed_users(['restaurant']) 
@is_order_owner
def orderDetail(request,id):
    if request.method=='POST':
        item = Order.objects.get(pk=id)
        form = OrderDetail(request.POST,instance=item)
        if form.is_valid():
            delivery = form.cleaned_data['delivery']
            if delivery.restaurant and delivery.restaurant.id == request.user.restaurant.id:
                item.status = form.cleaned_data['status']
                item.delivery = delivery
                item.save()
                return redirect('orders')
            else :
                messages.warning(request, "Please select delivery person that you have in given list !!")
                
    
    item = Order.objects.get(pk=id)
    form = OrderDetail(instance=item)
    delivery = Delivery.objects.filter(restaurant=request.user.restaurant.id)
    return render(request, 'order_detail.html', context={"form":form, 'order':item, 'delivery':delivery})


@is_authenticated
@allowed_users(['restaurant'])
def add_delivery_boy(request):
    if request.method == 'POST':
        form = AddDelivery(request.POST)
        if form.is_valid():
            user=form.cleaned_data['username']
            user = User.objects.get(username=user)
            user.delivery.restaurant = request.user.restaurant
            user.delivery.save()
            return redirect('add_delivery_boy')
    else :
        form = AddDelivery()
    boys = Delivery.objects.filter(restaurant=request.user.restaurant.id)

    return render(request,"add_delivery_boy.html",context={"form":form, "items":boys})

@is_authenticated
@allowed_users(['restaurant'])
@is_delivery_owner
def delete_delivery(request,id):
    if request.method == "POST":
        item = Delivery.objects.get(pk=id)
        item.restaurant = None
        item.save()
        return redirect('add_delivery_boy')



@is_authenticated
@allowed_users(['delivery']) 
def deliveryHome(request):
    orders = Order.objects.filter(delivery = request.user.delivery.id).filter(status="2")
    return render(request,'delivery_home.html', context={'orders':orders})

@is_authenticated
@allowed_users(['delivery']) 
@is_delivery_order_owner
def delivery_order_detail(request, id):
    if request.method=='POST':
        item = Order.objects.get(pk=id)
        form = deliveryOrderDetail(request.POST,instance=item)
        if form.is_valid():
            item.status = form.cleaned_data['status']
            item.save()
            return redirect('deliveryHome')
    else :
        item = Order.objects.get(pk=id)
        form = deliveryOrderDetail(instance=item)
    return render(request,"delivery_order_detail.html",context={"form":form, 'order':item})





def aboutUs(request):
    return render(request, 'about.html')

def contactUs(request):
    return render(request, 'contactus.html')
