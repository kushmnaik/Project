from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.http import  HttpResponseRedirect
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
            return render(request, 'restaurant_home.html', {'form': form})
    else :
        print(request.user)
        restaurant = MenuItem(restaurant = restaurant_name)
        form = AddItem(instance=restaurant)
    items = MenuItem.objects.filter(restaurant=restaurant_name)
    return render(request, 'restaurant_home.html', {'form': form, 'items':items})

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
