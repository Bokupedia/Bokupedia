from django.urls import path
from . import views

app_name = 'post_interactions'

urlpatterns = [
    path('', views.profile_posts, name='profile_posts'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]