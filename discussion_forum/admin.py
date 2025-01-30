from django.contrib import admin
from .models import Category, Topic, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_description') 
    search_fields = ('name',)  
    ordering = ('name',)

    def short_description(self, obj):
        """Description alanının ilk 10 kelimesini döndür"""
        return ' '.join(obj.description.split()[:10]) + ('...' if len(obj.description.split()) > 10 else '')

    short_description.short_description = "Description (Fırst 10 Words)" 


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'created_at')
    list_filter = ('category', 'author')  
    search_fields = ('title', 'author__username', 'category__name') 
    ordering = ('-created_at',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'category', 'author', 'created_at')
    list_filter = ('topic', 'category', 'author')  
    search_fields = ('content', 'author__username', 'topic__title', 'category__name') 
    ordering = ('-created_at',)