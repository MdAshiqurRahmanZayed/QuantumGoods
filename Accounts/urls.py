from django.urls import path
from .views import *

app_name = "Accounts"

urlpatterns = [
    path('signup/', sign_up, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', user_profile, name='profile'),
]
