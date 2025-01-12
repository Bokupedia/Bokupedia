from django.db import models
from user_accounts.models import User
from discussion_forum.models import Post
from django_ckeditor_5.fields import CKEditor5Field

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    content = CKEditor5Field(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    media_data = models.TextField(null=True, blank=True)
    media_type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        topic_title = self.post.topic.title if self.post.topic else "No Topic"
        return f"{self.author.username} - {topic_title}"
    
class Haha(models.Model):
    user = models.ForeignKey(User, related_name="hahas", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="hahas", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

class Dislike(models.Model):
    user = models.ForeignKey(User, related_name="dislikes", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="dislikes", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

class Angry(models.Model):
    user = models.ForeignKey(User, related_name="angries", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="angries", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

class Poop(models.Model):
    user = models.ForeignKey(User, related_name="poops", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="poops", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

class Nauseated(models.Model):
    user = models.ForeignKey(User, related_name="nauseateds", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="nauseateds", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')
