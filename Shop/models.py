from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from Accounts.models import *
from django.urls import reverse
from django.db.models import Avg, Count


def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + get_random_string(length=5)
    return unique_slug


class Category(models.Model):
     category_name = models.CharField(max_length=50,unique=True)
     slug = models.SlugField(max_length=100,unique=True)
     description =models.TextField(max_length=300,blank=True)
     cat_image = models.ImageField(upload_to = 'images/categories',blank = True)

     class Meta:
          verbose_name = "Category"
          verbose_name_plural = "Categories"
          
     def get_url(self):
          return reverse('products_by_category',args=[self.slug])

     def __str__(self):
          return self.category_name    
      
     def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title))
        super().save(*args, **kwargs)     

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.IntegerField()
    max_usage = models.IntegerField()
    current_usage = models.IntegerField(default=0)

    def is_valid(self):
        return self.current_usage < self.max_usage

    def apply_discount(self, original_price):
        return original_price - (original_price * self.discount_percentage / 100)

class Product(models.Model):
     product_name = models.CharField(max_length = 200,unique = True)
     slug         = models.SlugField(max_length = 200,unique = True)
     description  = models.TextField(max_length = 500,blank=True)
     price        = models.IntegerField()
     images       = models.ImageField( upload_to='images/products')
     stock        = models.IntegerField()
     is_available = models.BooleanField()
     category     = models.ForeignKey(Category, on_delete=models.CASCADE)
     created_at   = models.DateTimeField( auto_now_add=True)
     modified_at  = models.DateTimeField( auto_now=True)
     featured_product = models.BooleanField(default = False)
     
     old_price = models.IntegerField(blank=True, null=True)
     coupon_code = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)

     
     def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
     
     def __str__(self):
         return self.product_name     
      
      
      
     def save(self, *args, **kwargs):  # new
        if self.slug:
            self.slug = slugify(self.product_name)
        return super().save(*args, **kwargs)
    
     def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

     def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
    
    #  def apply_discount(self):
    #     if self.coupon_code and self.coupon_code.is_valid():
    #         self.discount_price = self.coupon_code.apply_discount(self.price)
    #         self.coupon_code.current_usage += 1
    #         self.coupon_code.save()

    #  def save(self, *args, **kwargs):
    #     self.apply_discount()
    #     super().save(*args, **kwargs)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/products', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'