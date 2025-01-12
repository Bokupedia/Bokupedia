from django.db import models
from user_accounts.models import User
from django_ckeditor_5.fields import CKEditor5Field
from discussion_forum.models import Post

class Notification(models.Model):
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    message = CKEditor5Field()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(
        max_length=50,
        choices=[
            ('haha', 'Haha'),
            ('angry', 'Angry'),
            ('poop', 'Poop'),
            ('nauseated', 'Nauseated'),
            ('comment', 'Comment'),
            ('dislike', 'Dislike'),
            ('message', 'Message')
        ],
        default='unknown'
    )
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    post = models.ForeignKey('discussion_forum.Post', on_delete=models.CASCADE, null=True, blank=True, related_name="notifications")

    def __str__(self):
        return f"Notification for {self.user.username} - {self.notification_type}"