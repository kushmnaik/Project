from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',add_item , name='add_item'),
    path('delete/<int:id>/',delete_item, name='delete_item'),
    path('edit/<int:id>/',edit_item, name='edit_item'),

]