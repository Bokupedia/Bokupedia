from django.shortcuts import render
from discussion_forum.models import Post
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from .models import Comment
from notifications.models import Notification
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import base64
from django.core.exceptions import ValidationError

@login_required
def profile_posts(request):
    if not request.user.is_authenticated:
        return render(request, 'post_interactions/profile_posts.html', {'posts': []})
    
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    paginator = Paginator(user_posts, 5)
    page = request.GET.get('page', 1)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'post_interactions/profile_posts.html', {'posts': posts})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user != comment.author:
        return HttpResponseForbidden("Bu yorumu düzenleme yetkiniz yok.")
        
    if request.method == 'POST':
        content = request.POST.get('edited_content')
        
        # Yeni medya yüklendiyse
        if 'media' in request.FILES:
            file = request.FILES['media']
            if file.size > 5 * 1024 * 1024:
                raise ValidationError("Dosya boyutu 5MB'dan küçük olmalı")
            
            media_data = base64.b64encode(file.read()).decode('utf-8')
            media_type = file.content_type
            comment.media_data = media_data
            comment.media_type = media_type
            
        if content:
            comment.content = content
            comment.save()
            
            return redirect('discussion_forum:post_detail', post_id=comment.post.id)
            
    return HttpResponseForbidden("Geçersiz istek.")

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Sadece yorum sahibi silebilir
    if request.user != comment.author:
        return HttpResponseForbidden("Bu yorumu silme yetkiniz yok.")
        
    if request.method == 'POST':
        post_id = comment.post.id
        comment.delete()
        
        return redirect('discussion_forum:post_detail', post_id=post_id)
        
    return HttpResponseForbidden("Geçersiz istek.")