from django.urls import path
from .views import *

app_name = "Shop"

urlpatterns = [
    # path('',Home.as_view(),name='home'),
    path('',home,name='home'),
    path('all-products/',all_products,name='all_products'),
    # path('product/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    
    
    # Product CRUD
    path('create-product/', createProduct, name='createProduct'),
    path('my-products/', product_list, name='product_list'),
    path('my-products/<int:pk>/update/', update_product, name='update_product'),
    path('my-products/<int:pk>/delete/', delete_product, name='delete_product'),
    
    # cupon
    path('coupon-create/', create_coupon, name='create_coupon'),
    path('coupon-list/', coupon_list, name='coupon_list'),
    path('coupon-update/<int:pk>/', update_coupon, name='update_coupon'),
    path('coupon-delete/<int:pk>/', delete_coupon, name='delete_coupon'),
    
    path('apply-coupon-products/<int:pk>/', apply_products_coupon, name='apply_products_coupon'),
    path('delete-applied-products/<int:pk>/', delete_products_coupon, name='delete_products_coupon'),
    
    #Category
    path('category-create/', create_category, name='create_category'),
    path('category-list/', all_category, name='all_category'),
    path('category-update/<int:pk>/', update_category, name='update_category'),
    path('category-delete/<int:pk>/', delete_category, name='delete_category'),
    
]
