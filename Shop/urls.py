from django.urls import path
from .views import *

app_name = "Shop"

urlpatterns = [
    # path('',Home.as_view(),name='home'),
    path('',home,name='home'),
    path('all-products/',all_products,name='all_products'),
    # path('product/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
]
