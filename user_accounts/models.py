from django.db import models
from django.contrib.auth.models import AbstractUser
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone

class User(AbstractUser):
    last_activity = models.DateTimeField(default=timezone.now)
    bio = CKEditor5Field(
        config_name='default',
        blank=True
    )

    def __str__(self):
        return f"{self.username}"