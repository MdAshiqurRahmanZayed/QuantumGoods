from django.contrib import admin
from .models import Product,Variation,ProductGallery,ReviewRating,Category,Coupon
import admin_thumbnails

class CategoryAdmin(admin.ModelAdmin):
     prepopulated_fields = {
          'slug':('category_name',)
          }


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
     list_display = ('product_name','price','stock','category','modified_at','is_available','featured_product')
     prepopulated_fields = {
          'slug':('product_name',)
          }
     inlines=[ProductGalleryInline]
     
class VariationsAdmin(admin.ModelAdmin):
     list_display = ('product', 'variation_category', 'variation_value', 'is_active')
     list_editable = ('is_active',)
     list_filter = ('product', 'variation_category', 'variation_value')
    


admin.site.register(Category,CategoryAdmin)
admin.site.register(Coupon)
admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationsAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)