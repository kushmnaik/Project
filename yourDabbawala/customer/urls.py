from django.urls import path
from .views import *

app_name = "customer"
urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("about/", About.as_view(), name="about"),
    path("contact-us/", Contact.as_view(), name="contact"),
    path("restaurant-<int:pk>/", RestaurantDetail.as_view(), name="restaurantdetail"),
    path("add-to-cart-<int:pk>/", add_to_cart, name="addtocart"),
    path("cart/", Cart.as_view(), name="cart"),
    path("delete-from-cart-<int:pk>", delete_from_cart, name="deletefromcart"),
    path("increase-qty-<int:pk>", increase_qty, name="increaseqty"),
    path("decrease-qty-<int:pk>", decrease_qty, name="decreaseqty"),
    path("checkout/", checkout, name="checkout"),
    path("customer-profile-<int:pk>/", CustomerProfile.as_view(), name="customerprofile"),
    path("customer-order-detail-<int:pk>/", CustomerOrderDetail.as_view(), name="customerorderdetail"),
]