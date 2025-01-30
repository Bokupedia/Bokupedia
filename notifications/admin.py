from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'message', 'post', 'read', 'created_at')
    list_filter = ('notification_type', 'read', 'created_at')  # Filtreleme için
    search_fields = ('user__username', 'message')  # Kullanıcı adı ve mesaj içinde arama yapmayı sağlar
    ordering = ('-created_at',)  # Yeni bildirimleri en üstte göstermek için

admin.site.register(Notification, NotificationAdmin)
