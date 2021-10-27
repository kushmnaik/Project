from django.shortcuts import redirect,render, HttpResponse
from django.contrib import messages
from .models import *

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs ):
            group=None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else :
                return render(request,'Login_required.html')
        return wrapper_func
    return decorator



def is_authenticated(view_func):
    def wrapper_func(request, *args, **kwargs ):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else :
            return render(request,'Login_required.html')
    return wrapper_func



def is_owner(view_func):
    def wrapper_func(request,id, *args, **kwargs ):
        if request.user == MenuItem.objects.get(pk=id).restaurant.user:
            return view_func(request,id, *args, **kwargs)
        else :
            return render(request,'Login_required.html')
    return wrapper_func

