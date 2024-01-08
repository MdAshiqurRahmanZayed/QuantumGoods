from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Import views
from django.views.generic import ListView, DetailView

# Models
from .models import Product
from Order.models import Cart,Order
# Mixin
from django.contrib.auth.mixins import LoginRequiredMixin

class Home(ListView):
    model = Product
    context_object_name = 'products'
    template_name='Shop/home.html'
    
    
def home(request):
    products = Product.objects.filter(featured_product=True)
    context = {
        'products':products,
    }
    return render(request,'Shop/home.html',context=context)

def all_products(request):
    products = Product.objects.filter()
    paginator = Paginator(products, 2)  

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
        
    context = {
        'products':products,
    } 
    return render(request,'Shop/all-products.html',context=context)
    
class ProductDetail(LoginRequiredMixin,DetailView):
    model = Product
    context_object_name = 'product'
    slug_field = 'slug'
    template_name='Shop/product_detail.html'


@login_required
def product_detail(request,slug):
    product = Product.objects.get(slug=slug)
    
    if Cart.objects.filter( user= request.user,item = product,purchased = False).exists():
        cart = True
    else:
        cart = False
    context = {
        'product':product,
        'cart':cart
    }
    return render(request,'Shop/product_detail.html',context=context)