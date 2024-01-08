from django.urls import path
from .views import *

app_name = "Order"

urlpatterns = [
    path('add/<pk>/', add_to_cart, name="add"),
    path('cart/', cart_view, name="cart"),
    path('remove/<pk>/', remove_from_cart, name="remove_from_cart"),
    
    path('increase-item-quantity/<pk>/', increase_cart, name="increase_quantity"),
    path('decrease-item-quantity/<pk>/', decrease_cart, name="decrease_quantity"),

]
