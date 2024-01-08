from django.forms import ModelForm
from .models import Account, Profile

from django.contrib.auth.forms import UserCreationForm


# forms

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

class SignUpForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('email', 'password1', 'password2',)
