from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.utils.text import slugify
from django.core.exceptions import PermissionDenied
from django.contrib import messages

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
    query = request.GET.get('search')
    if query:
        products = Product.objects.filter(product_name__icontains=query).order_by('-id')
    else:
        products = Product.objects.all().order_by('-id')
    
    paginator = Paginator(products, 2)  
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
        
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'Shop/all-products.html', context=context)

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


@login_required
def createProduct(request):
    form = ProductForm(request.POST, request.FILES or None)
    if request.user.user_type == "seller":
    
        if request.method == 'POST':
            if form.is_valid():
                product = form.save(commit=False)
                # Automatically generate slug from product name
                product.slug = slugify(product.product_name)
                product.product_user = request.user
                product.save()
                return redirect('Shop:home')
        else:
            form = ProductForm()
    else:
        messages.info(request, f"You are not allowed")
        return redirect('Shop:home')
    context = {
        'form': form
    }
    return render(request, 'Shop/create-product.html', context=context)

@login_required
def product_list(request):
    if request.user.user_type == "seller":
        products = Product.objects.filter(product_user = request.user)
    else:
        messages.info(request, f"You are not allowed")
        return redirect('Shop:home')
    return render(request, 'Shop/product_list.html', {'products': products})

@login_required
def update_product(request, pk):
    if request.user.user_type == "seller":
        product = get_object_or_404(Product, pk=pk)
        if product.product_user == request.user:
            form = ProductForm(request.POST or None, request.FILES or None, instance=product)
            if form.is_valid():
                form.save()
                return redirect('Shop:product_list')
        else:
                return redirect('Shop:home')
        
    else:
        messages.info(request, f"You are not allowed")
        return redirect('Shop:home')

        
    return render(request, 'Shop/create-product.html', {'form': form})

@login_required
def delete_product(request, pk):
    if request.user.user_type == "seller":
        product = get_object_or_404(Product, pk=pk)
        if product.product_user == request.user:
        
            if request.method == 'POST':
                product.delete()
                return redirect('Shop:product_list')
        else:
                return redirect('Shop:home')
    else:
        messages.info(request, f"You are not allowed")
        return redirect('Shop:home')
    return render(request, 'Shop/product_confirm_delete.html', {'product': product})



# cupon
@login_required
def create_coupon(request):
    if request.user.user_type == "seller":
        
        if request.method == 'POST':
            form = CouponForm(request.POST)
            if form.is_valid():
                coupon = form.save(commit=False)
                coupon.cupon_user = request.user
                coupon.save()
                return redirect('Shop:coupon_list')
        else:
            form = CouponForm()
    else:
        messages.info(request, f"You are not allowed")
        return redirect('Shop:home')

    return render(request, 'coupon/create_coupon.html', {'form': form})

@login_required
def coupon_list(request):
    if request.user.user_type == "seller":
        coupons = Coupon.objects.filter(cupon_user=request.user)
    else:
        messages.info(request, f"You are not allowed")
        return redirect('Shop:home')
    return render(request, 'coupon/coupon_list.html', {'coupons': coupons})

@login_required
def update_coupon(request, pk):
    if request.user.user_type == "seller":
        
        coupon = get_object_or_404(Coupon, pk=pk)
        if coupon.cupon_user != request.user:
            raise PermissionDenied
        if request.method == 'POST':
            form = CouponForm(request.POST, instance=coupon)
            if form.is_valid():
                form.save()
                return redirect('Shop:coupon_list')
        else:
            form = CouponForm(instance=coupon)
    else:
        messages.info(request, f"You are not allowed")
        return redirect('Shop:home')

    return render(request, 'coupon/update_coupon.html', {'form': form})

@login_required
def delete_coupon(request, pk):
    if request.user.user_type == "seller":

        coupon = get_object_or_404(Coupon, pk=pk)
        if coupon.cupon_user != request.user:
            raise PermissionDenied
        if request.method == 'POST':
            coupon.delete()
            return redirect('Shop:coupon_list')

    else:
        messages.info(request, f"You are not allowed")
        return redirect('Shop:home')
    return render(request, 'coupon/delete_coupon.html', {'coupon': coupon})


@login_required
def apply_products_coupon(request, pk):
    if request.user.user_type == "seller":

        product = get_object_or_404(Product, id=pk)
        coupons = Coupon.objects.filter(cupon_user=request.user)
        if request.method == 'POST':
            coupon_code = request.POST.get('coupon_code')
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if coupon in coupons:
                    product.coupon_code = coupon
                    product.save()
                    messages.info(request, f"Coupon added for the products")
                    return redirect('Shop:product_list')
                else:
                    messages.error(request, f"Coupon was not added for the products")
                    return redirect('Shop:product_list')
                    # Coupon does not belong to the current user
            except Coupon.DoesNotExist:
                return redirect('Shop:product_list')

    else:
        messages.info(request, f"You are not allowed")
        return redirect('Shop:home')
    

    return render(request, 'coupon/apply_products_coupon.html', {'coupons': coupons, 'product': product})


@login_required
def delete_products_coupon(request,pk):
    
    if request.user.user_type == "seller":
        try:
            
            product = get_object_or_404(Product, id=pk)
            if product:
                product.coupon_code = None
                product.save()
                messages.info(request, f"Coupon deleted for the products")
                return redirect('Shop:product_list')
                
        except:
                messages.info(request, f"You are not allowed")
                return redirect('Shop:product_list')
    
    else:
        messages.info(request, f"You are not allowed")
        return redirect('Shop:home')
            
            
        
@login_required
def create_category(request):
    form = CategoryForm(request.POST or None)
    if request.user.user_type == "seller":

        if request.method =="POST":
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user 
                form.save()
                return redirect('Shop:all_category')
            
    else:
        messages.info(request, f"You are not allowed")
        return redirect('Shop:home')
        
        
    context = {
        'form':form
    }
    return render(request, 'Shop/category/form.html',context )
        
@login_required
def all_category(request):
    category = None
    if request.user.user_type == "seller":
        category = Category.objects.filter(user=request.user)            
    else:
        messages.info(request, f"You are not allowed")
        return redirect('Shop:home')
        
        
    context = {
        'category':category
    }
    return render(request, 'Shop/category/all-category.html',context )
        
@login_required
def update_category(request,pk):
    category = Category.objects.get(id = pk)
    form = CategoryForm(request.POST or None,instance = category)
    if request.user.user_type == "seller":

        if request.method =="POST":
            if form.is_valid():
                form = form.save(commit=False)
                form.save()
                return redirect('Shop:all_category')
            
            
    else:
        messages.info(request, f"You are not allowed")
        return redirect('Shop:home')
        
        
    context = {
        'form':form
    }
    return render(request, 'Shop/category/form.html',context )
        
@login_required
def delete_category(request,pk):
    category = Category.objects.get(id = pk)
    if request.user.user_type == "seller":

        if request.method =="POST":
            category.delete()
            return redirect('Shop:all_category')
    else:
        messages.info(request, f"You are not allowed")
        return redirect('Shop:home')
    context = {
        'category':category
    }
        
        
    return render(request, 'Shop/category/delete.html',context )
