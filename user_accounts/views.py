from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from django.contrib.auth import login, logout, authenticate
from .forms import *
from django.core.paginator import Paginator
from django.contrib import messages

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user
    post_count = user.posts.count()

    if user == request.user:
        if not user.first_name or not user.bio:
            messages.warning(request, "Profiliniz eksik. Lütfen tamamlayın.")
    
    return render(request, 'profile.html', {
        'user': user, 
        'profile': profile,
        'post_count': post_count
    })
@login_required
def profile_posts(request, username):
    user = get_object_or_404(User, username=username)
    
    posts = user.posts.all().order_by('-created_at')

    paginator = Paginator(posts, 10)  
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)

    return render(request, 'profile_posts.html', {'user': user, 'posts': posts_page})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            forbidden_usernames = ['admin', 'moderator', 'root', 'system', 'administrator']
            
            if username.lower() in forbidden_usernames:
                form.add_error('username', 'Bu kullanıcı adı kullanılamaz.')
                return render(request, 'registration/register.html', {'form': form})
            
            forbidden_words = ['admin', 'mod', 'allah', '4ll4h', 'atatürk', 'rte', 'akp', 'chp', 'mhp', 'terorist', 'terörist', 'ataturk', 'kuran', 'bokupedia', 'bokupediya', 'bokupedya', 'raptor', 'öyy', 'mordor']
            
            cleaned_username = ''.join(char.lower() if char.isalnum() else ' ' for char in username)
            username_parts = cleaned_username.split()
            
            if any(forbidden in part.lower() for part in username_parts for forbidden in forbidden_words):
                form.add_error('username', 'Kullanıcı adınız yasaklı kelimeler içeremez.')
                return render(request, 'registration/register.html', {'form': form})
            
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
