from django.shortcuts import render
from django.http import JsonResponse
from .models import Notification
from discussion_forum.models import Post
from post_interactions.models import Comment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Bildirim fonksiyonları
def create_haha_notification(user, post):
    message = f"'{post.title}' başlıklı gönderiniz beğenildi!"
    Notification.objects.create(user=user, message=message, notification_type='haha', post=post)

def create_comment_notification(user, post):
    message = f"'{post.title}' başlıklı gönderinize yeni bir yorum yapıldı!"
    Notification.objects.create(user=user, message=message, notification_type='comment', post=post)

def create_dislike_notification(user, post):
    message = f"'{post.title}' başlıklı gönderiniz beğenilmedi."
    Notification.objects.create(user=user, message=message, notification_type='dislike', post=post)

def create_message_notification(user, sender):
    message = f"{sender} size yeni bir mesaj gönderdi."
    Notification.objects.create(user=user, message=message, notification_type='message')

def create_comment_edit_notification(user, post, comment):
    message = f"'{post.title}' başlıklı gönderinizdeki yorum düzenlendi: {comment.content[:30]}..."
    Notification.objects.create(user=user, message=message, notification_type='comment_edit', post=post)

# Yorumları İşleme
@login_required
def comment_post(request, post_id):
    post = Post.objects.get(id=post_id)
    create_comment_notification(post.user, post) 
    
    return JsonResponse({'status': 'commented'})

# Yorum düzenleme işlemi
@login_required
def edit_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    post = comment.post

    if request.method == 'POST':
        new_content = request.POST.get('content')
        old_content = comment.content
        
        # Yorum düzenlendiğinde bildirim gönder
        if new_content != old_content:
            comment.content = new_content
            comment.save()
            create_comment_edit_notification(post.user, post, comment)
    
    return JsonResponse({'status': 'comment_edited'})

# Yorum silme işlemi
@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
        
    return JsonResponse({'status': 'comment_deleted'})

# Bildirim Listeleme
@login_required
def notification_list(request):
    notification_list = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Add pagination
    paginator = Paginator(notification_list, 20) 
    page = request.GET.get('page', 1)

    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        notifications = paginator.page(1)
    except EmptyPage:
        notifications = paginator.page(paginator.num_pages)
    
    # Check post information for each notification
    for notification in notifications:
        if notification.related_object_id:
            try:
                post = Post.objects.get(id=notification.related_object_id)
                notification.post = post
            except Post.DoesNotExist:
                notification.post = None
        else:
            notification.post = None
                
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications
    })

# Bildirim Okundu Olarak İşaretleme
@login_required
def mark_notification_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.read = True
    notification.save()
    
    return JsonResponse({'status': 'marked'})

# Tüm Bildirimleri Okundu Olarak İşaretleme
@login_required
def mark_all_read(request):
    if request.method == "POST":
        try:
            Notification.objects.filter(user=request.user, read=False).update(read=True)
            return JsonResponse({'status': 'marked'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

# Bildirim Silme
@login_required
def delete_notification(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.delete()
        return JsonResponse({'status': 'deleted'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'not_found'}, status=404)

# Tum bildirimleri sil
@login_required
def delete_all_notifications(request):
    if request.method == "POST":
        try:
            Notification.objects.filter(user=request.user).delete()
            return JsonResponse({'status': 'deleted_all'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
