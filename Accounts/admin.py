from dataclasses import fields
import django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account,Profile
from django.utils.html import format_html

# Register your models here.

class AccountAdmin(UserAdmin):
     list_display =('email','username','last_login','date_joined','is_active')
     
     list_display_links =('email',)
     readonly_fields = ('last_login','date_joined')
     ordering = ('-date_joined',)
      
     filter_horizontal =()
     list_filter = ()
     fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    # def thumbnail(self, object):
    #     return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;">'.format(object.profile_picture.url))
    # thumbnail.short_description = 'Profile Picture'
    list_display = ('user','first_name','last_name', 'user', 'city', 'zipcode', 'country')



admin.site.register(Account,AccountAdmin)
admin.site.register(Profile,UserProfileAdmin)
