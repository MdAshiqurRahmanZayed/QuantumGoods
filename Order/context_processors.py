from Order.models import Order,Cart



def cart_count(request):
     if request.user.is_authenticated:
          order = Order.objects.filter(user=request.user, ordered=False)
          if order.exists():
               count =  order[0].orderitems.count()
          else:
               count =  0
     else:
          count = None
     return {'cart_count':count}
     