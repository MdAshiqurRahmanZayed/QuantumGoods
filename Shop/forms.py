from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ('product_name','description','price','old_price','images','stock','category',)
        # fields = '__all__'
        
        
    def __init__(self, *args, **kwargs):
          super(ProductForm, self).__init__(*args, **kwargs)
          for field in self.fields:
               self.fields[field].widget.attrs['class'] = 'form-control'
               
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_percentage']
        
    def __init__(self, *args, **kwargs):
          super(CouponForm, self).__init__(*args, **kwargs)
          for field in self.fields:
               self.fields[field].widget.attrs['class'] = 'form-control'
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','description', ]
        
    def __init__(self, *args, **kwargs):
          super(CategoryForm, self).__init__(*args, **kwargs)
          for field in self.fields:
               self.fields[field].widget.attrs['class'] = 'form-control'