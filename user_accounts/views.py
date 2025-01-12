from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from django.contrib.auth import login, logout, authenticate
from .forms import *

from django.contrib import messages

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user

    if user == request.user:
        if not user.first_name or not user.bio:
            messages.warning(request, "Profiliniz eksik. Lütfen tamamlayın.")
    
    return render(request, 'profile.html', {'user': user, 'profile': profile})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            return redirect('user_accounts:profile', username=user.username)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def accounts_index(request):
    return render(request, 'accounts_index.html')

def custom_logout(request):
    
    logout(request)
    return redirect('/')

def custom_login(request):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_accounts:profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})
