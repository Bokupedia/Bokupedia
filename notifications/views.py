from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Notification
from discussion_forum.models import Post
from post_interactions.models import Comment
from private_messages.models import Message

# ── Notification type icons ──────────────────────────────────────
TYPE_ICONS = {
    'haha':         '😆',
    'comment':      '💬',
    'dislike':      '👎',
    'angry':        '😡',
    'poop':         '💩',
    'nauseated':    '🤢',
    'message':      '📩',
    'comment_edit': '✏️',
}

# ── Helper functions ─────────────────────────────────────────────
def create_haha_notification(user, post):
    Notification.objects.create(
        user=user,
        message=f"«{post.title}» gönderinize 😆 reaksiyonu verildi!",
        notification_type='haha', post=post,
    )

def create_angry_notification(user, post):
    Notification.objects.create(
        user=user,
        message=f"«{post.title}» gönderinize 😡 reaksiyonu verildi.",
        notification_type='angry', post=post,
    )

def create_poop_notification(user, post):
    Notification.objects.create(
        user=user,
        message=f"«{post.title}» gönderinize 💩 reaksiyonu verildi.",
        notification_type='poop', post=post,
    )

def create_nauseated_notification(user, post):
    Notification.objects.create(
        user=user,
        message=f"«{post.title}» gönderinize 🤢 reaksiyonu verildi.",
        notification_type='nauseated', post=post,
    )

def create_dislike_notification(user, post):
    Notification.objects.create(
        user=user,
        message=f"«{post.title}» gönderiniz 👎 aldı.",
        notification_type='dislike', post=post,
    )

def create_comment_notification(user, post):
    Notification.objects.create(
        user=user,
        message=f"«{post.title}» gönderinize yeni bir yorum yapıldı.",
        notification_type='comment', post=post,
    )

def create_comment_edit_notification(user, post, comment):
    preview = comment.content[:40].strip() if comment.content else ''
    Notification.objects.create(
        user=user,
        message=f"«{post.title}» gönderinizdeki bir yorum düzenlendi: {preview}…",
        notification_type='comment_edit', post=post,
    )

def create_message_notification(user, sender):
    Notification.objects.create(
        user=user,
        message=f"{sender} sana yeni bir mesaj gönderdi.",
        notification_type='message',
    )


# ── Comment actions ──────────────────────────────────────────────
@login_required
def comment_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        create_comment_notification(post.author, post)
    except Post.DoesNotExist:
        pass
    return JsonResponse({'status': 'commented'})


@login_required
def edit_comment(request, comment_id):
    try:
        comment = Comment.objects.select_related('post').get(id=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)

    if request.method == 'POST':
        new_content = request.POST.get('content', '')
        if new_content != comment.content:
            comment.content = new_content
            comment.save()
            create_comment_edit_notification(comment.post.author, comment.post, comment)

    return JsonResponse({'status': 'comment_edited'})


@login_required
def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
    except Comment.DoesNotExist:
        pass
    return JsonResponse({'status': 'comment_deleted'})


# ── Notification list ────────────────────────────────────────────
@login_required
def notification_list(request):
    qs = (
        Notification.objects
        .filter(user=request.user)
        .select_related('post')
        .order_by('-created_at')
    )

    paginator = Paginator(qs, 20)
    page = request.GET.get('page', 1)
    try:
        notifications = paginator.page(page)
    except (EmptyPage, Exception):
        notifications = paginator.page(paginator.num_pages)

    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications,
        'type_icons': TYPE_ICONS,
    })


# ── Poll (live badge + toast) ────────────────────────────────────
@login_required
def poll_notifications(request):
    last_id = int(request.GET.get('last_id', 0))

    new_notifs = (
        Notification.objects
        .filter(user=request.user, id__gt=last_id)
        .order_by('-created_at')[:5]
    )

    unread_count = Notification.objects.filter(user=request.user, read=False).count()
    unread_messages = Message.objects.filter(receiver=request.user, is_read=False).count()
    latest_id = (
        Notification.objects
        .filter(user=request.user)
        .order_by('-id')
        .values_list('id', flat=True)
        .first() or 0
    )

    return JsonResponse({
        'unread_count': unread_count,
        'unread_messages_count': unread_messages,
        'latest_id': latest_id,
        'new_notifications': [
            {
                'id': n.id,
                'message': n.message,
                'type': n.notification_type,
                'icon': TYPE_ICONS.get(n.notification_type, '🔔'),
                'created_at': n.created_at.strftime('%d %b, %H:%M'),
            }
            for n in new_notifs
        ],
    })


# ── Mark read ────────────────────────────────────────────────────
@login_required
def mark_notification_read(request, notification_id):
    try:
        notif = Notification.objects.get(id=notification_id, user=request.user)
        notif.read = True
        notif.save()
        return JsonResponse({'status': 'marked'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'not_found'}, status=404)


@login_required
def mark_all_read(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)
    Notification.objects.filter(user=request.user, read=False).update(read=True)
    return JsonResponse({'status': 'marked'})


# ── Delete ───────────────────────────────────────────────────────
@login_required
def delete_notification(request, notification_id):
    try:
        Notification.objects.get(id=notification_id, user=request.user).delete()
        return JsonResponse({'status': 'deleted'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'not_found'}, status=404)


@login_required
def delete_all_notifications(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)
    Notification.objects.filter(user=request.user).delete()
    return JsonResponse({'status': 'deleted_all'})
