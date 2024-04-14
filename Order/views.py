from django.shortcuts import render, get_object_or_404, redirect

# Authentications
from django.contrib.auth.decorators import login_required

# Model
from Order.models import Cart, Order
from Shop.models import Product,Coupon
# Messages
from django.contrib import messages


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)

    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            item.stock -= 1
            item.save()
            messages.info(request, f"{item.product_name} item quantity was updated.")
            return redirect("Shop:home")
        else:
            order.orderitems.add(order_item[0])
            item.stock -= 1
            item.save()
            messages.info(request, f"{item.product_name} item was added to your cart.")
            return redirect("Shop:home")
    else:
        order = Order(user=request.user)
        order.save()
        item.stock -= 1
        item.save()

        order.orderitems.add(order_item[0])
        messages.info(request, f"{item.product_name} item was added to your cart.")
        return redirect("Shop:home")
    
@login_required
def cart_view(request):
    carts = Cart.objects.filter(user =request.user,purchased = False)
    orders = Order.objects.filter(user =request.user,ordered= False)
    if carts.exists() and orders.exists():
        order = orders[0]
        if request.method =='POST':
            coupon_code = request.POST.get('coupon_code')
            pk = request.POST.get('product')
            product = Product.objects.get(id = pk)
            # print(coupon_code)
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                cart = Cart.objects.filter(item = product ,item__coupon_code=coupon)
                # print(coupon)
                # print(cart[0].coupon_applied)
                if cart:
                    if cart[0].coupon_applied == False:
                        for i in range(len(cart)):
                            cart[i].coupon_applied = True
                            cart[i].save()
                # print(order.item)
                # if coupon.cupon_user == request.user:
                #     # Apply discount to the order total
                #     order.total -= coupon.apply_discount(order.total)
                #     order.save()
                #     messages.success(request, "Coupon applied successfully!")
                # else:
                #     messages.error(request, "You are not authorized to use this coupon.")
            except Coupon.DoesNotExist:
                messages.error(request, "Invalid coupon code!")
        context = {
            'carts':carts,
            'order':order,
        }
        return render(request,'Order/cart.html',context=context)
    else:
        messages.warning(request, "You don't have any item in your cart!")
        return redirect("Shop:home")


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.orderitems.remove(order_item)
            item.stock += order_item.quantity
            item.save()
            order_item.delete()
            messages.warning(request, f"{item.product_name} item was removed form your cart")
            return redirect("Order:cart")
        else:
            messages.info(request, f"{item.product_name} item was not in your cart.")
            return redirect("Shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("Shop:home")
    
    
@login_required
def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                item.stock -= 1
                item.save()
                messages.info(request, f"{item.product_name} quantity has been updated")
                return redirect("Order:cart")
        else:
            messages.info(request, f"{item.product_name} is not in your cart")
            return redirect("Shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("Shop:home")


@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                item.stock += 1
                item.save()
                messages.info(request, f"{item.product_name} quantity has been updated")
                return redirect("Order:cart")
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.product_name} item has been removed from your cart")
                return redirect("Order:cart")
        else:
            messages.info(request, f"{item.product_name} is not in your cart")
            return redirect("Shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("Shop:home")
