from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('user_accounts.urls')),
    path('', include('discussion_forum.urls')),
    path('messages/', include('private_messages.urls')),
    path('interactions/', include('post_interactions.urls')),
    path('notifications/', include('notifications.urls')),
    path('mission', views.mission, name='mission'),
    path('staff', views.staff, name='staff'),
    path('contents', views.contents, name='contents'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'CyberHex.views.custom_403_view'
handler404 = 'CyberHex.views.custom_404_view'
handler500 = 'CyberHex.views.custom_500_view'
