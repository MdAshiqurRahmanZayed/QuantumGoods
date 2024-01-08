
from django.contrib import admin
from django.urls import path,include

# For showing media file
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include('Accounts.urls')),
    path("", include('Shop.urls')),
    path("shop/", include('Order.urls')),
    path("payment/", include('Payment.urls')),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
