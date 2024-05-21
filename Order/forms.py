from django import forms
from .models import *


class OrderStatusForm(forms.ModelForm):
    order_status = forms.ChoiceField(
        choices=ORDER_STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Order
        fields = ('order_status',)