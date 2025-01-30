from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'short_content', 'timestamp')  
    list_filter = ('sender', 'receiver')  
    search_fields = ('sender', 'receiver', 'content')  

    def short_content(self, obj):
        return ' '.join(obj.content.split()[:10]) + ('...' if len(obj.content.split()) > 10 else '')

    short_content.short_description = "Content (Fırst 10 Words)"  

admin.site.register(Message, MessageAdmin)
