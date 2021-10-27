from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.http import  HttpResponseRedirect
from authentication.forms import *
# Create your views here.
def index(request):
    return render(request,"home.html")

def add_item(request):
    restaurant_name = Restaurant.objects.get(user = request.user)
    
    if request.method == 'POST':
        form = AddItem(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home')
        else :
            messages.success(request, 'error while saving try again!!')
            return render(request, 'restaurant_home.html', {'form': form, 'restaurant':restaurant_name})
    else :
        print(request.user)
        restaurant = MenuItem(restaurant = restaurant_name)
        form = AddItem(instance=restaurant)
    items = MenuItem.objects.filter(restaurant=restaurant_name)
    return render(request, 'restaurant_home.html', {'form': form, 'items':items, 'restaurant':restaurant_name})

def delete_item(request,id):
    if request.method == "POST":
        item = MenuItem.objects.get(pk=id)
        item.delete()
        return redirect('add_item')

def edit_item(request,id):
    if request.method=='POST':
        item = MenuItem.objects.get(pk=id)
        item = AddItem(request.POST,instance=item)
        if item.is_valid():
            item.save()
            return redirect('add_item')
    else :
        item = MenuItem.objects.get(pk=id)
        item = AddItem(instance=item)
    return render(request, 'edit_item.html', {'form' : item})

def edit_profile(request):

    if request.method == 'POST':
        res_info = Restaurant.objects.get(user=request.user)
        res_info = RestaurantInfo(request.POST, request.FILES, instance=res_info)
        if res_info.is_valid():
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
            print(res_info.cleaned_data['image'])
            restaurant_info.save()
            return redirect('add_item')
    else:
        res_info = Restaurant.objects.get(user=request.user)
        res_info = RestaurantInfo( instance=res_info)

    return render(request, 'restaurant_info.html', context={"form": res_info})
    
