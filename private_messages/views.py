from django.shortcuts import render, redirect
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from user_accounts.models import User
from .models import Message
from notifications.models import Notification

@login_required(login_url='login')
def inbox(request):
    search_query = request.GET.get('search', '').lower()
    
    all_user_ids = set(User.objects.values_list('id', flat=True))
    
    contacts = User.objects.filter(id__in=all_user_ids).annotate(
        unread_count=Count(
            'sent_messages',
            filter=Q(sent_messages__receiver=request.user, sent_messages__is_read=False)
        )
    ).order_by('username')
    
    if search_query:
        contacts = contacts.filter(username__icontains=search_query)

    selected_user_id = request.GET.get('contact')
    if selected_user_id:
        selected_user = User.objects.get(id=selected_user_id)
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=selected_user)) |
            (Q(sender=selected_user) & Q(receiver=request.user))
        ).order_by('-timestamp')
        
        Message.objects.filter(
            sender=selected_user,
            receiver=request.user,
            is_read=False
        ).update(is_read=True)
    else:
        messages = Message.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        ).order_by('-timestamp')
        selected_user = None

    unread_messages_count = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()

    context = {
        'contacts': contacts,
        'messages': messages,
        'selected_user': selected_user,
        'user': request.user,
        'unread_messages_count': unread_messages_count
    }
    
    return render(request, 'private_messages/inbox.html', context)

@login_required(login_url='login')
def send_message(request):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        receiver_id = request.POST.get('receiver_id')
        
        try:
            receiver = User.objects.get(id=receiver_id)
            message = Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=message_content,
                is_read=False
            )
            
            Notification.objects.create(
                user=receiver,
                message=f"{request.user.username} tarafından yeni bir mesajın var!",
                notification_type='message',
                related_object_id=request.user.id
            )
            
            return JsonResponse({
                'status': 'success',
                'message': {
                    'content': message.content,
                    'timestamp': message.timestamp.strftime("%d %b %Y, %H:%M"),
                    'sender': message.sender.username
                }
            })
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Kullanıcı bulunamadı'})
    
    return JsonResponse({'status': 'error', 'message': 'Geçersiz istek'})