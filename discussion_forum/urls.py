from django.urls import path
from . import views

app_name = 'discussion_forum'

urlpatterns = [
    path('', views.forum_index, name='forum_index'),
    path('topic/<str:topic_title>/', views.topic_detail, name='topic_detail'),
    path('category/<int:category_id>/', views.category_topics, name='category_topics'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create-post/', views.create_post, name='create_post'),
    path('api/topics/<int:category_id>/', views.get_topics, name='get_topics'),
]