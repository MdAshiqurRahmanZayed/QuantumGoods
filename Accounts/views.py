from django.shortcuts import render, HttpResponseRedirect,redirect

# Authetication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

# Forms and Models
from .models import Profile
from .forms import ProfileForm, SignUpForm

# Messages
from django.contrib import messages

# Create your views here.

def sign_up(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data  
            email = cleaned_data.get('email')
            username = email.split('@')[0] + '_' + email.split('@')[1].split('.')[0]
            form = form.save(commit=False)
            form.is_active = True
            form.username = username 
            form.save()
            messages.success(request, "Account Created Successfully!")
            return redirect('Accounts:login')
    return render(request, 'Accounts/sign_up.html', context={'form':form})


def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Shop:home')
    context={
         'form':form
         }
    return render(request, 'Accounts/login.html', context)


@login_required
def logout_user(request):
    logout(request)
    messages.warning(request, "You are logged out!!")
    return redirect('Shop:home')


@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Change Saved!!")
            form = ProfileForm(instance=profile)
    return render(request, 'Accounts/change_profile.html', context={'form':form})
