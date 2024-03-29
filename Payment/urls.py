from django.urls import path
from .views import *

app_name = 'Payment'

urlpatterns = [
     path('checkout/', checkout, name="checkout"),
     path('pay/', payment, name="payment"),
    path('status/', complete, name="complete"),
    path('purchase/<val_id>/<tran_id>/<payment_data>/', purchase, name="purchase"),
    path('orders/', order_view, name="orders"),
]