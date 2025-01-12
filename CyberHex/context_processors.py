from notifications.models import Notification
from private_messages.models import Message

def unread_notifications(request):
    unread_count = 0
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, read=False).count()
    return {'unread_count': unread_count}

def unread_messages(request):
    if request.user.is_authenticated:
        unread_count = Message.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()
        return {'unread_messages_count': unread_count}
    return {'unread_messages_count': 0}