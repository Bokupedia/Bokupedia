from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.utils.html import strip_tags, escape
from datetime import timedelta
from user_accounts.models import User
from .models import Message
from notifications.models import Notification
import logging

logger = logging.getLogger(__name__)


@login_required(login_url='login')
def inbox(request):
    # One query: all messages involving this user, newest first
    all_my_messages = (
        Message.objects
        .filter(Q(sender=request.user) | Q(receiver=request.user))
        .select_related('sender', 'receiver')
        .order_by('-timestamp')
    )

    # Build last-message info per contact (only the most recent per pair)
    contact_info = {}
    for msg in all_my_messages:
        other = msg.receiver if msg.sender == request.user else msg.sender
        if other.id not in contact_info:
            contact_info[other.id] = {
                'last_msg_time': msg.timestamp,
                'last_msg_preview': strip_tags(msg.content)[:45],
                'last_msg_is_mine': msg.sender == request.user,
            }

    contacts_qs = User.objects.exclude(id=request.user.id).annotate(
        unread_count=Count(
            'sent_messages',
            filter=Q(sent_messages__receiver=request.user, sent_messages__is_read=False)
        )
    )

    contact_list = []
    for contact in contacts_qs:
        info = contact_info.get(contact.id, {})
        contact.last_msg_time = info.get('last_msg_time')
        contact.last_msg_preview = info.get('last_msg_preview', '')
        contact.last_msg_is_mine = info.get('last_msg_is_mine', False)
        contact_list.append(contact)

    # Sort: active conversations first (by recency), then alphabetically
    contact_list.sort(key=lambda c: (
        c.last_msg_time is None,
        -(c.last_msg_time.timestamp() if c.last_msg_time else 0),
    ))

    selected_user_id = request.GET.get('contact')
    messages = []
    selected_user = None

    if selected_user_id:
        try:
            selected_user = User.objects.get(id=selected_user_id)
            messages = Message.objects.filter(
                Q(sender=request.user, receiver=selected_user) |
                Q(sender=selected_user, receiver=request.user)
            ).order_by('timestamp')

            Message.objects.filter(
                sender=selected_user,
                receiver=request.user,
                is_read=False
            ).update(is_read=True)
        except User.DoesNotExist:
            pass

    unread_count = Message.objects.filter(receiver=request.user, is_read=False).count()

    return render(request, 'private_messages/inbox.html', {
        'contacts': contact_list,
        'messages': messages,
        'selected_user': selected_user,
        'user': request.user,
        'unread_messages_count': unread_count,
        'selected_user_id': selected_user_id,
    })


@login_required(login_url='login')
def send_message(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Geçersiz istek'})

    content = request.POST.get('message', '').strip()
    receiver_id = request.POST.get('receiver_id')

    if not content:
        return JsonResponse({'status': 'error', 'message': 'Mesaj boş olamaz'})

    try:
        receiver = User.objects.get(id=receiver_id)
        safe_content = escape(content)

        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=safe_content,
            is_read=False
        )

        # Notify only if no message notification in the last 10 minutes (anti-spam)
        recent = Notification.objects.filter(
            user=receiver,
            notification_type='message',
            related_object_id=request.user.id,
        ).order_by('-created_at').first()

        if not recent or (timezone.now() - recent.created_at) > timedelta(minutes=10):
            Notification.objects.create(
                user=receiver,
                message=f"{request.user.username} tarafından yeni bir mesajın var!",
                notification_type='message',
                related_object_id=request.user.id
            )

        return JsonResponse({
            'status': 'success',
            'message': {
                'id': message.id,
                'content': message.content,
                'timestamp': message.timestamp.strftime("%d %b %Y, %H:%M"),
                'sender': message.sender.username,
            }
        })
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Kullanıcı bulunamadı'})


@login_required(login_url='login')
def poll_messages(request):
    """Returns new messages since last_id for live updates."""
    contact_id = request.GET.get('contact')
    last_id = int(request.GET.get('last_id', 0))

    if not contact_id:
        return JsonResponse({'messages': [], 'unread_count': 0})

    try:
        contact = User.objects.get(id=contact_id)
        new_messages = Message.objects.filter(
            Q(sender=request.user, receiver=contact) |
            Q(sender=contact, receiver=request.user),
            id__gt=last_id
        ).order_by('timestamp')

        Message.objects.filter(
            sender=contact, receiver=request.user, is_read=False
        ).update(is_read=True)

        unread_count = Message.objects.filter(receiver=request.user, is_read=False).count()

        return JsonResponse({
            'messages': [
                {
                    'id': m.id,
                    'content': m.content,
                    'sender': m.sender.username,
                    'is_mine': m.sender == request.user,
                    'timestamp': m.timestamp.strftime("%d %b %Y, %H:%M"),
                }
                for m in new_messages
            ],
            'unread_count': unread_count,
        })
    except User.DoesNotExist:
        return JsonResponse({'messages': [], 'unread_count': 0})


@login_required(login_url='login')
def delete_message(request, message_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error'})

    try:
        message = Message.objects.get(id=message_id, sender=request.user)
        message.delete()
        return JsonResponse({'status': 'deleted'})
    except Message.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Mesaj bulunamadı veya yetkiniz yok'})
