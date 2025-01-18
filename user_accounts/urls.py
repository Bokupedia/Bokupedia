from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'user_accounts'

urlpatterns = [
    path('', views.accounts_index, name='accounts_index'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('<str:username>/posts/', views.profile_posts, name='profile_posts'),

]
