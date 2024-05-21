from django.db import models
from django.conf import settings

# Model
from Shop.models import Product
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_product_name")
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    coupon_applied = models.BooleanField(default=False)  
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} X {self.item}'

    def get_total(self):
        if self.coupon_applied  == False:
            total = self.item.price * self.quantity
            float_total = format(total, '0.2f')
            return float_total
        else:
            # print(self.item.coupon_code.discount_percentage)
            # discount = (100 - int(self.item.coupon_code.discount_percentage)) / 100  
            # print(discount)
            total = (100- self.item.coupon_code.discount_percentage)/100 * self.item.price * self.quantity   
            # print((100- self.item.coupon_code.discount_percentage)/100 * self.item.price * self.quantity )
            float_total = format(total, '0.2f')
            return float_total

ORDER_STATUS_CHOICES = {
    'PENDING': 'Pending',
    'PROCESSING': 'Processing',
    'SHIPPED': 'Shipped',
    'DELIVERED': 'Delivered',
    'CANCELLED': 'Cancelled'
}
class Order(models.Model):
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=264, blank=True, null=True)
    orderId = models.CharField(max_length=200, blank=True, null=True)
    full_payment_data  = models.TextField( blank=True, null=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())
        return total
   
    def __str__(self):
        return f'{self.user}'
