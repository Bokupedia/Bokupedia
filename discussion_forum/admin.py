from django.contrib import admin
from .models import Category, Topic, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)  
    ordering = ('name',) 

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'created_at')
    list_filter = ('category', 'author')  
    search_fields = ('title', 'author__username', 'category__name') 
    ordering = ('-created_at',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'author', 'created_at')
    list_filter = ('topic', 'author') 
    search_fields = ('content', 'author__username', 'topic__title')  
    ordering = ('-created_at',)
