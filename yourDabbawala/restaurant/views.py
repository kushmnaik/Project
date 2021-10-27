from django.shortcuts import render
from .forms import *
from django.contrib import messages
from django.http import  HttpResponseRedirect
# Create your views here.
def index(request):
    return render(request,"home.html")

def add_item(request):
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
        restaurant_name = Restaurant.objects.get(user = request.user)
        restaurant = MenuItem(restaurant = restaurant_name)
        form = AddItem(instance=restaurant)

    return render(request, 'restaurant_home.html', {'form': form})