from django.contrib import admin
from .models import *

class OrderAdmin(admin.ModelAdmin):
    '''Admin View for Order'''

    list_display = ('user','ordered',)


admin.site.register(Cart)
admin.site.register(Order,OrderAdmin)
