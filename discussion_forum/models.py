from django.db import models
from user_accounts.models import User
from django_ckeditor_5.fields import CKEditor5Field

class Category(models.Model):
   name = models.CharField(max_length=100)
   description = CKEditor5Field(blank=True)

   def __str__(self):
       return self.name

class Topic(models.Model):
   title = models.CharField(max_length=200) 
   content = CKEditor5Field()
   category = models.ForeignKey(Category, related_name="topics", on_delete=models.CASCADE, null=True, blank=True)
   author = models.ForeignKey(User, related_name="topics", on_delete=models.CASCADE)
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
       return self.title

class Post(models.Model):
    topic = models.ForeignKey(Topic, related_name="posts", on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, related_name="direct_posts", on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    content = CKEditor5Field()
    created_at = models.DateTimeField(auto_now_add=True)
    media_data = models.TextField(null=True, blank=True)
    media_type = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f"{self.author.username} - {self.created_at}"